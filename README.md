# 一级市场访前助手

第一次发布或安装请先阅读 [`START-HERE.md`](START-HERE.md)。API Key 与费用归属见 [`AUTHENTICATION.md`](AUTHENTICATION.md)。

`prepare-investment-visit` 是一个面向一级市场投资人的 Codex Plugin。它可以根据公司名称、简介、Teaser 或 BP，生成证据可追溯的公司交流前置 Note，并把公开事实、公司口径、推断和待核验事项分开。

当前版本：`0.1.0`。核心 Skill 已通过原子跳动 standard 案例和碳生万物 quick 案例回归；飞书适配器仍需在部署组织的真实应用中完成联调。

## 主要能力

- 公司、产品、技术与商业模式梳理
- 行业、市场、竞争和替代方案研究
- 创始人、团队、近期公开发言和关键人风险
- 客户、合同、经营数据、财务与单位经济性核验框架
- 融资历史、股东、关联主体和治理问题
- 决策优先的交流问题与会后资料清单
- 可选音频脚本、播客和视频分镜
- 快速、标准、深度三档研究预算

## 安装

```text
codex plugin marketplace add mengyao007/prepare-investment-visit
codex plugin add prepare-investment-visit@prepare-investment-visit
```

重启 Codex 或开启新线程，然后通过 `$prepare-investment-visit` 显式调用。Codex 也可以根据任务描述自动触发该 Skill。

## 谁支付模型费用

安装包不包含作者的 API Key，也不会把使用者的任务转发到作者账户。

- **在个人 Codex 中使用：**使用者登录自己的 Codex/ChatGPT 账户，或在自己的环境配置自己的 OpenAI API Key；用量计入使用者自己的账户。
- **部署飞书机器人：**机器人由部署方统一承担模型用量。应使用公司专用 OpenAI API Project 或公司管理账户，不能使用作者个人 Key。
- **不要把 Key 发给 Skill 作者或飞书机器人：**密钥只应保存在使用者本机或部署方的 Secret 管理器中。

完整说明见 [`AUTHENTICATION.md`](AUTHENTICATION.md)。

## 最小用法

```text
使用 $prepare-investment-visit 调研“示例科技”，交流对象是创始人张三，
生成标准版中文访前 Note。附件是公司 BP。
```

只提供公司名称也可以。若公司身份存在歧义，Skill 会先询问官网、所在地、法律主体或创始人等识别信息。

## 研究档位

| 档位 | 适用场景 | 公开来源目标 | 默认时间上限 |
|---|---|---:|---:|
| quick | 临时拜访、路上速读 | 4-8 | 5 分钟 |
| standard | 常规创始人交流 | 10-18 | 12 分钟 |
| deep | 重点项目、投前准备 | 20-35 | 30 分钟 |

默认交付为 Markdown Note。音频和视频只有在对应工具可用且用户明确请求时才渲染；否则提供可直接制作的播客脚本或视频分镜。

## 飞书机器人

`integrations/feishu-bot` 提供可选的企业自建应用适配器，支持单聊/群聊、BP 文件、任务确认、Codex 调用和 Note/证据台账回传。飞书凭证、Codex 凭证和聊天白名单由部署方自行配置，不包含在 Plugin 中。

## 数据与保密

- BP、Teaser 和生成结果默认只保存在任务工作目录。
- 公司材料中的数据一律先视为公司口径，除非获得独立来源验证。
- 部署机器人时应配置数据保留期限、磁盘加密、访问白名单和日志脱敏。
- 不要把真实 BP、客户合同、财务数据或生成的保密 Note 提交到公开仓库。

## 发布状态

发布者、MIT 许可证、GitHub 仓库与安全报告渠道已写入发行包。飞书适配器的生产部署仍需组织自有凭据和实机联调。见 `PUBLISHING-CHECKLIST.md`。
