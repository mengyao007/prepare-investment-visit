# 认证、API Key 与费用归属

## 结论

这个 Plugin 发布的是工作流、参考资料和本地适配代码，不提供模型额度，也不包含作者凭据。安装者使用自己的 Codex 身份；集中部署飞书机器人时，部署组织使用自己的企业凭据。

## 场景一：用户在自己的 Codex 中安装

用户只需要：

1. 安装该 Plugin。
2. 在自己的 Codex 客户端登录自己的 ChatGPT/Codex 账户；或者由用户自己在本机配置 OpenAI API Key。
3. 调用 `$prepare-investment-visit`。

Plugin 不读取作者账户，不要求用户把 API Key 填到 Skill 文件中，也不会把 Key 发给发布者。用量和权限由用户自己的 Codex 环境决定。

## 场景二：组织部署飞书机器人

飞书群里的所有任务在一台受控服务器上运行，因此费用由该服务器配置的 Codex 身份承担。推荐做法：

1. 由公司创建专用 OpenAI API Project 或公司管理的 Codex 执行账户。
2. 只授予机器人必要权限，并设置预算、告警和使用上限。
3. 通过云平台 Secret Manager、容器 Secret 或操作系统安全凭据注入 `CODEX_API_KEY`。
4. 配置 `ALLOWED_CHAT_IDS`、最大并发和 quick/standard/deep 超时。
5. 不允许用户在聊天消息、BP 文件或机器人命令中提交 API Key。

## 不支持的模式

当前版本不支持飞书用户逐人 BYOK。原因是聊天内收集密钥会扩大泄露面，还需要安全的密钥库、身份绑定、撤销、轮换和审计机制。若希望每个人自行承担用量，推荐每个人在自己的 Codex 中安装 Plugin。

## 仓库安全规则

- 不提交 `.env`、API Key、Codex 登录缓存、飞书 Secret、BP、生成 Note 或运行日志。
- `.env.example` 只能保留空值和说明。
- 发现密钥误提交时，应立即撤销并轮换；仅删除 Git 当前版本并不足够。

