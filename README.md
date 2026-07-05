# 一级市场访前助手

prepare-investment-visit 是面向一级市场投资人的 Codex Plugin。它在研究前先确认交流对象、补充材料和播客需求，再结合用户提供的 BP/Teaser/简介与当前公开信息，生成证据可追溯的专业 PDF 访前研究。

当前版本：0.3.0。

## 主要能力

- 公司、产品、技术、商业模式与经营验证
- 行业价值链、市场测算、竞争与替代方案
- 交流对象及核心团队的可核验履历、公开观点与针对性问题
- 客户、合同、交付、财务、单位经济性、融资、股权与治理
- 近期时间线、矛盾日志、红旗风险和牛/基/熊情景
- 决策优先的会谈计划与会后资料清单
- 默认交付排版专业、引用可点击的 PDF
- 可选 5-10 分钟单主持人专业投研播客

## 安装

    codex plugin marketplace add mengyao007/prepare-investment-visit
    codex plugin add prepare-investment-visit@prepare-investment-visit

安装后开启新线程，通过 $prepare-investment-visit 调用。

## 使用流程

只需先提供公司名称。Skill 会在检索前一次性询问：

1. 与这家公司的谁交流（姓名和职务；不知道可回复“待定”）；
2. 是否有 BP、Teaser、一段话简介、官网或其他补充材料；
3. 是否需要把最终 PDF 改编成 5-10 分钟播客音频。

回答后才开始研究。若用户提供材料，Note 会同时使用材料和公开信息，并明确区分公司口径、已验证事实、第三方报道、推断和未知项。

## 输出

- 必选：company-visit-note.pdf
- 可选：company-visit-podcast.mp3（官方 Speech）或 company-visit-podcast.wav（无 Key 本机兜底）
- 内部中间稿和证据台账默认不交付，除非用户要求

PDF 的前两页给出会议目标、当前建议、投资主线、关键正负信号、证据置信度和最高价值问题；正文覆盖人物、公司、产品、市场、竞争、经营、团队、财务、融资、治理、近期动态、风险、会谈计划和资料清单。

## 播客与 API Key

主体研究与 PDF 生成不需要额外 API Key，使用用户自己的 Codex 订阅环境。

高质量音频优先调用 OpenAI 官方 curated speech Skill。该路径需要用户在本机配置自己的 OPENAI_API_KEY，API 与 ChatGPT/Codex 订阅分开计费。不要把密钥粘贴到聊天、Skill 或仓库中。

没有 API Key 时，Windows 用户可使用内置离线中文语音兜底生成 WAV。音色可能不如官方 Speech 自然，但内容仍是重新编写的专业播客摘要，不会逐字朗读 Note。

安装官方 speech Skill 可在 Codex 中调用：

    $skill-installer speech

重启 Codex 后生效。

## 研究档位

| 档位 | 公开来源目标 | 检索上限 | 典型 PDF |
|---|---:|---:|---:|
| quick | 4-8 | 8 | 3-5 页 |
| standard | 10-18 | 20 | 8-15 页 |
| deep | 20-35 | 40 | 15-30 页 |

默认使用 standard。

## 数据与保密

- BP、Teaser、合同、财务数据和生成结果只留在用户授权的任务目录。
- 公司材料中的数据先视为公司口径，除非获得独立来源验证。
- 不要把真实保密材料或生成的保密 Note 提交到公开仓库。
- 输出是访前研究辅助材料，不构成正式法律、财务、税务、监管、医疗或技术尽调。

安装与验收见 START-HERE.md；认证边界见 AUTHENTICATION.md。
