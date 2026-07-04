import * as Lark from '@larksuiteoapi/node-sdk';
import { spawn } from 'node:child_process';
import { cp, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { randomUUID } from 'node:crypto';
import assert from 'node:assert/strict';

const SELF_TEST = process.argv.includes('--self-test');
const REQUIRED_ENV = ['FEISHU_APP_ID', 'FEISHU_APP_SECRET'];
if (!SELF_TEST) {
  for (const key of REQUIRED_ENV) {
    if (!process.env[key]) throw new Error(`Missing environment variable: ${key}`);
  }
}

const APP_ID = process.env.FEISHU_APP_ID;
const APP_SECRET = process.env.FEISHU_APP_SECRET;
const CODEX_BIN = process.env.CODEX_BIN || 'codex';
const DATA_DIR = path.resolve(process.env.BOT_DATA_DIR || './data');
const SKILL_SOURCE = path.resolve(
  process.env.SKILL_SOURCE || '../../plugins/prepare-investment-visit/skills/prepare-investment-visit',
);
const RESULT_SCHEMA = path.resolve('./bot-result.schema.json');
const MAX_ATTACHMENT_BYTES = Number(process.env.MAX_ATTACHMENT_MB || 30) * 1024 * 1024;
const MAX_CONCURRENT_JOBS = Math.max(1, Number(process.env.MAX_CONCURRENT_JOBS || 2));
const PREFLIGHT_TIMEOUT_MS = Number(process.env.PREFLIGHT_TIMEOUT_SECONDS || 90) * 1000;
const JOB_TIMEOUT_MS = {
  quick: Number(process.env.QUICK_TIMEOUT_MINUTES || 5) * 60 * 1000,
  standard: Number(process.env.STANDARD_TIMEOUT_MINUTES || 12) * 60 * 1000,
  deep: Number(process.env.DEEP_TIMEOUT_MINUTES || 30) * 60 * 1000,
};
const ALLOWED_CHAT_IDS = new Set(
  (process.env.ALLOWED_CHAT_IDS || '').split(',').map((x) => x.trim()).filter(Boolean),
);
const ALLOWED_EXTENSIONS = new Set([
  '.pdf', '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.md', '.csv',
]);

const drafts = new Map();
const seenMessages = new Set();
const runningChats = new Set();
let activeJobs = 0;
const jobWaiters = [];
let tokenCache = { token: '', expiresAt: 0 };

if (!SELF_TEST) await mkdir(path.join(DATA_DIR, 'jobs'), { recursive: true });

function log(event, fields = {}) {
  console.log(JSON.stringify({ at: new Date().toISOString(), event, ...fields }));
}

function newDraft(chatId) {
  return {
    chatId,
    companyBrief: '',
    meetingPerson: '',
    meetingDate: '',
    depth: 'standard',
    deliverable: 'note',
    attachments: [],
    notes: [],
  };
}

function getDraft(chatId) {
  if (!drafts.has(chatId)) drafts.set(chatId, newDraft(chatId));
  return drafts.get(chatId);
}

function stripMentions(text) {
  return text.replace(/@_user_\d+/g, '').trim();
}

function parseTextIntoDraft(draft, rawText) {
  const text = stripMentions(rawText);
  if (!text) return;
  const fields = [
    ['companyBrief', /(?:公司|项目|企业)\s*[：:]\s*(.+)/i],
    ['meetingPerson', /(?:交流对象|拜访对象|联系人)\s*[：:]\s*(.+)/i],
    ['meetingDate', /(?:时间|日期|交流时间)\s*[：:]\s*(.+)/i],
  ];
  for (const [key, regex] of fields) {
    const match = text.match(regex);
    if (match) draft[key] = match[1].trim();
  }
  if (/深度\s*[：:]?\s*(快速|quick)/i.test(text)) draft.depth = 'quick';
  if (/深度\s*[：:]?\s*(深度|deep)/i.test(text)) draft.depth = 'deep';
  if (/深度\s*[：:]?\s*(标准|standard)/i.test(text)) draft.depth = 'standard';
  if (/视频|video/i.test(text)) draft.deliverable = 'note+audio+video';
  else if (/音频|播客|audio|podcast/i.test(text)) draft.deliverable = 'note+audio';
  else if (/交付\s*[：:]?\s*(note|文字|文档)/i.test(text)) draft.deliverable = 'note';

  const isControl = /^(确认开始|开始|确认|重置|取消)$/i.test(text);
  const hasLabeledField = fields.some(([, regex]) => regex.test(text));
  if (!isControl && !hasLabeledField) {
    if (!draft.companyBrief) draft.companyBrief = text;
    else draft.notes.push(text);
  }
}

function renderDraft(draft) {
  const files = draft.attachments.length
    ? draft.attachments.map((x) => x.fileName).join('、')
    : '无';
  return [
    '已记录当前访前任务：',
    `公司/简介：${draft.companyBrief || '待补充'}`,
    `交流对象：${draft.meetingPerson || '未提供（可选）'}`,
    `时间：${draft.meetingDate || '未提供（可选）'}`,
    `深度：${draft.depth}`,
    `交付：${draft.deliverable}`,
    `附件：${files}`,
    '',
    draft.companyBrief ? '如无误，请回复“确认开始”。' : '请补充公司名称或一段公司简介。',
  ].join('\n');
}

async function getTenantToken() {
  if (tokenCache.token && Date.now() < tokenCache.expiresAt) return tokenCache.token;
  const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const payload = await response.json();
  if (!response.ok || payload.code !== 0) {
    throw new Error(`Feishu token failed: ${response.status} ${payload.msg || ''}`);
  }
  tokenCache = {
    token: payload.tenant_access_token,
    expiresAt: Date.now() + Math.max(60, Number(payload.expire || 7200) - 120) * 1000,
  };
  return tokenCache.token;
}

async function feishuApi(url, options = {}) {
  const token = await getTenantToken();
  const response = await fetch(`https://open.feishu.cn${url}`, {
    ...options,
    headers: { authorization: `Bearer ${token}`, ...(options.headers || {}) },
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Feishu API failed: ${response.status} ${body.slice(0, 500)}`);
  }
  return response;
}

async function sendMessage(chatId, msgType, content) {
  const response = await feishuApi('/open-apis/im/v1/messages?receive_id_type=chat_id', {
    method: 'POST',
    headers: { 'content-type': 'application/json; charset=utf-8' },
    body: JSON.stringify({ receive_id: chatId, msg_type: msgType, content: JSON.stringify(content) }),
  });
  const payload = await response.json();
  if (payload.code !== 0) throw new Error(`Feishu send failed: ${payload.msg}`);
  return payload.data;
}

async function sendText(chatId, text) {
  return sendMessage(chatId, 'text', { text: text.slice(0, 120000) });
}

function safeFileName(name) {
  const base = path.basename(name || 'attachment.bin');
  return base.replace(/[<>:"/\\|?*\x00-\x1F]/g, '_').slice(0, 180);
}

async function downloadAttachment({ messageId, fileKey, fileName, jobDir }) {
  const cleanName = safeFileName(fileName);
  const ext = path.extname(cleanName).toLowerCase();
  if (!ALLOWED_EXTENSIONS.has(ext)) throw new Error(`不支持的附件格式：${ext || '未知'}`);
  const response = await feishuApi(
    `/open-apis/im/v1/messages/${encodeURIComponent(messageId)}/resources/${encodeURIComponent(fileKey)}?type=file`,
  );
  const contentLength = Number(response.headers.get('content-length') || 0);
  if (contentLength > MAX_ATTACHMENT_BYTES) throw new Error('附件超过机器人配置的大小上限');
  const bytes = new Uint8Array(await response.arrayBuffer());
  if (bytes.byteLength > MAX_ATTACHMENT_BYTES) throw new Error('附件超过机器人配置的大小上限');
  let target = path.join(jobDir, 'inputs', cleanName);
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, bytes, { flag: 'wx' }).catch(async (error) => {
    if (error.code !== 'EEXIST') throw error;
    target = path.join(jobDir, 'inputs', `${randomUUID()}-${cleanName}`);
    await writeFile(target, bytes, { flag: 'wx' });
  });
  return target;
}

async function uploadFile(filePath) {
  const info = await stat(filePath);
  if (info.size > MAX_ATTACHMENT_BYTES) throw new Error('输出文件超过机器人配置的大小上限');
  const form = new FormData();
  form.set('file_type', 'stream');
  form.set('file_name', path.basename(filePath));
  form.set('file', new Blob([await readFile(filePath)]), path.basename(filePath));
  const response = await feishuApi('/open-apis/im/v1/files', { method: 'POST', body: form });
  const payload = await response.json();
  if (payload.code !== 0) throw new Error(`Feishu upload failed: ${payload.msg}`);
  return payload.data.file_key;
}

async function sendOutputFile(chatId, filePath) {
  const fileKey = await uploadFile(filePath);
  await sendMessage(chatId, 'file', { file_key: fileKey });
}

async function acquireJobSlot() {
  if (activeJobs < MAX_CONCURRENT_JOBS) {
    activeJobs += 1;
    return;
  }
  await new Promise((resolve) => jobWaiters.push(resolve));
  activeJobs += 1;
}

function releaseJobSlot() {
  activeJobs -= 1;
  const next = jobWaiters.shift();
  if (next) next();
}

function runProcess(command, args, options, timeoutMs = 0) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { ...options, windowsHide: true, shell: false });
    let stdout = '';
    let stderr = '';
    let settled = false;
    const timer = timeoutMs > 0 ? setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill();
      reject(new Error(`Process timed out after ${Math.round(timeoutMs / 1000)} seconds`));
    }, timeoutMs) : null;
    child.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    child.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    child.on('error', (error) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      reject(error);
    });
    child.on('close', (code) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      if (code === 0) resolve({ stdout, stderr });
      else reject(new Error(`Codex exited ${code}: ${stderr.slice(-2000)}`));
    });
  });
}

async function prepareJob(draft) {
  const jobId = `${new Date().toISOString().replace(/[:.]/g, '-')}-${randomUUID()}`;
  const jobDir = path.join(DATA_DIR, 'jobs', jobId);
  await mkdir(path.join(jobDir, '.agents', 'skills'), { recursive: true });
  await mkdir(path.join(jobDir, 'outputs'), { recursive: true });
  await cp(SKILL_SOURCE, path.join(jobDir, '.agents', 'skills', 'prepare-investment-visit'), {
    recursive: true,
    force: false,
  });
  return { jobId, jobDir };
}

function buildPrompt(draft, jobDir) {
  const attachmentList = draft.attachments.map((x) => `- ${x.localPath}`).join('\n') || '- 无';
  return [
    'Use $prepare-investment-visit.',
    `Research depth: ${draft.depth}.`,
    `Deliverable: ${draft.deliverable}.`,
    `Company or supplied brief: ${draft.companyBrief}`,
    `Meeting person: ${draft.meetingPerson || 'not provided'}`,
    `Meeting date: ${draft.meetingDate || 'not provided'}`,
    `Additional notes: ${draft.notes.join(' | ') || 'none'}`,
    'Supplied files:',
    attachmentList,
    '',
    `Work only inside ${jobDir}. Save the final Markdown note to outputs/note.md.`,
    'Follow the selected depth budget and stop with labeled evidence gaps when its query or wall-time ceiling is reached.',
    'Write research/material-claims.md before public research and research/evidence-ledger.md before drafting.',
    'If an essential identity ambiguity prevents research, do not guess. Return needs_clarification with concise questions.',
    'Return the structured final result required by the provided output schema. Use paths relative to the job directory.',
    'On complete runs, include research/material-claims.md and research/evidence-ledger.md in supporting_paths.',
  ].join('\n');
}

async function runCodexPreflight(jobDir, draft) {
  const probePath = path.join(jobDir, 'outputs', '.codex-preflight');
  const finalPath = path.join(jobDir, 'outputs', '.codex-preflight-final.txt');
  const declaredInputs = draft.attachments.map((x) => x.localPath).filter(Boolean);
  const prompt = [
    'This is a local preflight only. Do not browse the web and do not research the company.',
    'Read .agents/skills/prepare-investment-visit/SKILL.md.',
    ...declaredInputs.map((file) => `Confirm this input is readable: ${file}`),
    'Create outputs/.codex-preflight containing exactly OK, read it back, and return exactly OK.',
    'If any read or write fails, return PRECHECK_FAILED and the exact error.',
  ].join('\n');
  const args = [
    '--sandbox', 'workspace-write',
    'exec',
    '--skip-git-repo-check',
    '--output-last-message', finalPath,
    prompt,
  ];
  const env = { ...process.env };
  const result = await runProcess(CODEX_BIN, args, { cwd: jobDir, env }, PREFLIGHT_TIMEOUT_MS);
  const finalMessage = await readFile(finalPath, 'utf8').catch(() => '');
  const probe = await readFile(probePath, 'utf8').catch(() => '');
  if (finalMessage.trim() !== 'OK' || probe.trim() !== 'OK') {
    throw new Error(`Codex preflight failed: ${(finalMessage || result.stderr).slice(-1200)}`);
  }
}

function extractUsage(jsonl) {
  let usage = null;
  for (const line of jsonl.split(/\r?\n/)) {
    try {
      const event = JSON.parse(line);
      if (event.type === 'turn.completed' && event.usage) usage = event.usage;
    } catch { /* ignore non-JSON diagnostics */ }
  }
  return usage;
}

async function runResearch(chatId, draft) {
  if (runningChats.has(chatId)) {
    await sendText(chatId, '当前会话已有任务运行中，请等待完成后再启动。');
    return;
  }
  runningChats.add(chatId);
  await acquireJobSlot();
  try {
    const { jobId, jobDir } = await prepareJob(draft);
    for (const attachment of draft.attachments) {
      attachment.localPath = await downloadAttachment({ ...attachment, jobDir });
    }
    await sendText(chatId, '文件与运行环境预检中；预检通过后才会开始公开检索。');
    await runCodexPreflight(jobDir, draft);
    const resultPath = path.join(jobDir, 'result.json');
    const args = [
      '--search',
      '--sandbox', 'workspace-write',
      'exec',
      '--skip-git-repo-check',
      '--json',
      '--output-schema', RESULT_SCHEMA,
      '--output-last-message', resultPath,
      buildPrompt(draft, jobDir),
    ];
    const env = { ...process.env };
    if (!process.env.CODEX_API_KEY) delete env.CODEX_API_KEY;
    log('job_started', { chatId, jobId });
    await sendText(chatId, `已开始调研：${draft.companyBrief}\n完成后会回传 Note。`);
    const execution = await runProcess(
      CODEX_BIN,
      args,
      { cwd: jobDir, env },
      JOB_TIMEOUT_MS[draft.depth] || JOB_TIMEOUT_MS.standard,
    );
    const usage = extractUsage(execution.stdout);
    const result = JSON.parse(await readFile(resultPath, 'utf8'));

    if (result.status === 'needs_clarification') {
      await sendText(chatId, [result.message, ...result.clarification_questions.map((q, i) => `${i + 1}. ${q}`)].join('\n'));
      return;
    }
    if (result.status !== 'complete') throw new Error(result.message || 'Codex reported failure');

    const outputPaths = [
      result.note_path,
      result.audio_path,
      result.video_path,
      ...(Array.isArray(result.supporting_paths) ? result.supporting_paths : []),
    ]
      .filter(Boolean)
      .map((relative) => path.resolve(jobDir, relative))
      .filter((resolved) => resolved.startsWith(path.resolve(jobDir) + path.sep));
    await sendText(chatId, result.message || '调研完成。');
    for (const outputPath of outputPaths) await sendOutputFile(chatId, outputPath);
    drafts.set(chatId, newDraft(chatId));
    log('job_completed', { chatId, jobId, usage, outputs: outputPaths.map(path.basename) });
  } catch (error) {
    log('job_failed', { chatId, error: String(error) });
    const message = String(error.message || error);
    const prefix = message.includes('preflight') || message.includes('orchestrator_helper_launch_failed')
      ? '运行环境预检失败，未开始公开调研'
      : '任务失败';
    await sendText(chatId, `${prefix}：${message.slice(0, 800)}`);
  } finally {
    releaseJobSlot();
    runningChats.delete(chatId);
  }
}

async function onMessage(data) {
  const message = data?.message;
  if (!message?.message_id || !message?.chat_id) return;
  if (seenMessages.has(message.message_id)) return;
  seenMessages.add(message.message_id);
  if (seenMessages.size > 10000) seenMessages.delete(seenMessages.values().next().value);

  const chatId = message.chat_id;
  if (ALLOWED_CHAT_IDS.size && !ALLOWED_CHAT_IDS.has(chatId)) return;
  const draft = getDraft(chatId);
  let content = {};
  try { content = JSON.parse(message.content || '{}'); } catch { /* ignore malformed content */ }

  if (message.message_type === 'text') {
    const text = stripMentions(content.text || '');
    if (/^(重置|取消)$/i.test(text)) {
      drafts.set(chatId, newDraft(chatId));
      await sendText(chatId, '当前访前任务已重置。');
      return;
    }
    parseTextIntoDraft(draft, text);
    if (/^(确认开始|开始|确认)$/i.test(text)) {
      if (!draft.companyBrief) {
        await sendText(chatId, '请先提供公司名称或一段公司简介，再回复“确认开始”。');
        return;
      }
      void runResearch(chatId, structuredClone(draft));
      return;
    }
    await sendText(chatId, renderDraft(draft));
    return;
  }

  if (message.message_type === 'file') {
    const fileName = safeFileName(content.file_name || 'attachment.bin');
    const ext = path.extname(fileName).toLowerCase();
    if (!ALLOWED_EXTENSIONS.has(ext)) {
      await sendText(chatId, `暂不支持 ${ext || '该'} 格式，请发送 PDF、PPTX、DOCX、XLSX、TXT、MD 或 CSV。`);
      return;
    }
    draft.attachments.push({
      messageId: message.message_id,
      fileKey: content.file_key,
      fileName,
      localPath: '',
    });
    await sendText(chatId, renderDraft(draft));
    return;
  }

  await sendText(chatId, '当前支持文本以及 PDF、PPTX、DOCX、XLSX、TXT、MD、CSV 文件。');
}

if (SELF_TEST) {
  const draft = newDraft('test-chat');
  parseTextIntoDraft(draft, '@_user_1 公司：示例科技\n交流对象：张三\n深度：深度\n交付：播客');
  assert.equal(draft.companyBrief, '示例科技');
  assert.equal(draft.meetingPerson, '张三');
  assert.equal(draft.depth, 'deep');
  assert.equal(draft.deliverable, 'note+audio');
  assert.match(renderDraft(draft), /示例科技/);
  assert.equal(safeFileName('../a?.pdf'), 'a_.pdf');
  assert.deepEqual(
    extractUsage('{"type":"turn.completed","usage":{"input_tokens":12,"output_tokens":3}}'),
    { input_tokens: 12, output_tokens: 3 },
  );
  let timeoutObserved = false;
  try {
    await runProcess(process.execPath, ['-e', 'setTimeout(() => {}, 2000)'], { cwd: process.cwd() }, 100);
  } catch (error) {
    timeoutObserved = /timed out/.test(String(error));
  }
  assert.equal(timeoutObserved, true);
  console.log('Feishu bot self-test passed');
} else {
  const eventDispatcher = new Lark.EventDispatcher({}).register({
    'im.message.receive_v1': async (data) => {
      try {
        await onMessage(data);
      } catch (error) {
        log('message_handler_failed', { error: String(error) });
      }
    },
  });

  const wsClient = new Lark.WSClient({
    appId: APP_ID,
    appSecret: APP_SECRET,
    loggerLevel: Lark.LoggerLevel.info,
  });

  log('bot_starting', { dataDir: DATA_DIR, skillSource: SKILL_SOURCE });
  await wsClient.start({ eventDispatcher });
}
