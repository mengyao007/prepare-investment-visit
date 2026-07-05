# 认证、API Key 与费用

## 主体功能

公司研究和 PDF 生成运行在安装者自己的 Codex 环境中。Plugin 不包含作者凭据，不读取作者账户，也不会把用户任务转发给作者。

仅使用 Codex 订阅即可完成研究和 PDF；不要把任何 API Key 写入 Skill 文件、聊天消息或公开仓库。

## 可选官方 Speech 音频

OpenAI 官方 speech Skill 通过 Audio API 生成音频，因此需要安装者自己的 OPENAI_API_KEY。ChatGPT/Codex 订阅与 API 平台分开计费，订阅本身不等于可供脚本使用的 API Key 或 API 额度。

正确做法：

1. 用户在自己的 OpenAI API 账户中创建并管理 Key；
2. 在本机安全地设置 OPENAI_API_KEY 环境变量；
3. 不在聊天中粘贴完整 Key；
4. 由用户自己的 API 账户承担音频调用费用。

## 无 Key 兜底

Windows 用户可以使用 Skill 内置的 System.Speech 离线渲染器生成 WAV，不需要 API Key。该模式音色自然度较低，但不会影响 PDF，也不会把数据发送到额外的语音 API。

## 仓库安全

- 不提交 .env、API Key、登录缓存、BP、合同、财务数据、生成 Note、播客稿或运行日志。
- 如果密钥误提交，应立即撤销并轮换；只删除当前文件不足以消除历史泄露。
