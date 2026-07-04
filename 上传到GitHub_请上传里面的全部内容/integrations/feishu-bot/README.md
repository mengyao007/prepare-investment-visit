# 飞书机器人适配器

该服务通过飞书长连接接收消息和 BP/Teaser 文件，在隔离任务目录中调用 `codex exec` 与 `$prepare-investment-visit`，再把 Note 和可选媒体文件发回原会话。

## 认证与费用归属

飞书机器人是集中式服务：所有飞书用户的任务都由部署机器上的 Codex 身份执行。因此生产环境必须使用公司拥有的 OpenAI API Project 或公司管理的 Codex 账户，不要使用 Skill 作者或员工个人的 API Key。

- 飞书用户不需要、也不应该向机器人发送自己的 API Key。
- `CODEX_API_KEY` 留空时，CLI 使用部署机器上已有的 Codex 登录状态。
- 设置 `CODEX_API_KEY` 时，必须通过部署平台的 Secret 管理器注入；不要写入代码、`.env.example`、日志或 Git 仓库。
- 当前版本不提供“每个飞书用户自带 Key（BYOK）”。如需按个人结算，应让用户在自己的 Codex 中安装 Plugin，而不是共用飞书机器人。
- 上线前应在公司 API Project 中设置成员权限、预算告警和使用上限，并结合 `ALLOWED_CHAT_IDS`、并发数和运行超时控制成本。

## 飞书侧配置

1. 创建企业自建应用并启用机器人能力。
2. 在“事件与回调”中选择长连接，订阅 `im.message.receive_v1`。
3. 申请最小权限：接收机器人单聊或群聊 @ 消息、发送消息、获取消息资源、上传文件。
4. 发布应用版本，并把机器人加入允许使用的群聊或用户范围。

官方依据：[长连接接收事件](https://open.feishu.cn/document/server-docs/event-subscription-guide/event-subscription-configure-/request-url-configuration-case)、[消息概述](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/introduction)、[发送消息](https://open.feishu.cn/document/server-docs/im-v1/message/create)、[获取消息资源](https://open.feishu.cn/s/61BYfgpwQ01)。

## 本地启动

1. 安装 Node.js 20+ 和 Codex CLI，并确保 `codex` 已完成认证。
2. 复制 `.env.example` 为 `.env`，通过部署平台的 Secret 管理填写凭证；不要提交 `.env`。
3. 安装依赖后运行 `npm start`。

服务不会自动读取 `.env` 文件；本地开发可由 PowerShell、容器或进程管理器注入环境变量。生产环境建议使用密钥管理服务，并为机器人设置允许的 chat ID。

## 使用方式

向机器人发送公司名称、简介或 BP，并可补充：

```text
公司：示例科技
交流对象：张三，创始人
时间：2026-07-10
深度：标准
交付：Note
```

机器人汇总后，回复“确认开始”。发送“重置”可清空当前会话草稿。

## 生产约束

- 每个任务使用独立目录；附件只保存为数据文件，不执行。
- 每次调研先执行只读/写入预检；预检失败时不启动公开检索。
- 默认附件上限 30 MB，且只接受 PDF、PPT/PPTX、DOC/DOCX、XLS/XLSX、TXT、MD、CSV。
- 默认运行上限：快速版 5 分钟、标准版 12 分钟、深度版 30 分钟；超时后终止任务并保留已落盘检查点。
- `CODEX_API_KEY` 只注入 Codex 子进程，不会写入任务目录或回传飞书。
- 配置 chat allowlist、任务并发、日志脱敏、磁盘加密和自动清理策略后再上线。
- 公司名称会用于公开网络检索；BP 原文不应被发送给无授权的第三方服务。
