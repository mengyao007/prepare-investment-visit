# 发布检查清单

## 必须确认

- [x] 最终 Plugin 名称和中文展示名
- [x] 发布者：`mengyao007`
- [x] 开源许可证：MIT
- [x] GitHub 仓库：`mengyao007/prepare-investment-visit`
- [x] 安全问题通过 GitHub Issues 报告且禁止粘贴密钥
- [x] 明确个人 Codex 与集中式飞书机器人的认证/费用边界
- [x] 发行包不包含作者 API Key，且示例配置中的密钥值为空

## 发布前验证

- [x] Skill frontmatter 和目录结构校验
- [x] Plugin manifest 校验
- [x] Markdown Note 结构校验器测试
- [x] 原子跳动真实案例标准版回归
- [x] 飞书适配器语法、SDK 加载和本地逻辑自检
- [x] 第二个不同行业真实案例回归（碳生万物，quick 模式）
- [x] 使用隔离 `CODEX_HOME` 从本地 Marketplace 安装并启用 `0.1.0`
- [x] 最终 ZIP 包含 Marketplace、License 和认证说明
- [ ] 在沙箱正常的 Codex CLI 主机完成端到端文件生成
- [ ] 使用真实飞书自建应用完成消息和附件收发
- [x] 确认公开发行包不含 BP、Note、凭证、日志或任务数据
- [ ] 推送 GitHub `main` 并从远程 Marketplace 重新安装验证

## 发布命令

仓库推送完成后：

```text
codex plugin marketplace add mengyao007/prepare-investment-visit
codex plugin add prepare-investment-visit@prepare-investment-visit
```

安装后开启新线程，使用：

```text
$prepare-investment-visit
```
