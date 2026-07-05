# 从这里开始

## 安装

    codex plugin marketplace add mengyao007/prepare-investment-visit
    codex plugin add prepare-investment-visit@prepare-investment-visit

安装后开启一个新线程。

## 最小验收

输入：

    使用 $prepare-investment-visit 调研示例科技。

正确行为是先询问交流对象、补充材料和是否需要播客，不应立即开始公开检索。

回答示例：

    与创始人张三交流；有一份BP稍后上传；需要播客；使用standard档。

随后 Skill 应先读取 BP，再结合公开信息生成 PDF。若选择播客，应在 PDF 验证完成后生成单主持人音频。

## 无 API Key 用户

公司研究与 PDF 不需要额外 API Key。高质量官方 Speech 音频需要单独的 OpenAI API Key；没有 Key 的 Windows 用户会使用本机离线 WAV 兜底。

## 发布者验收

发布前执行 PUBLISHING-CHECKLIST.md 中的检查。必须确认仓库没有密钥、用户材料、生成 Note 或临时研究数据。
