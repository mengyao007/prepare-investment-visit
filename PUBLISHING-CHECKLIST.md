# 发布检查清单

## 结构与内容

- [ ] 仓库根目录没有重复嵌套的上传目录
- [ ] 仓库不包含任何已删除集成的代码、依赖或文档
- [ ] Skill frontmatter、agents/openai.yaml 和 Plugin manifest 一致
- [ ] 版本号、README、CHANGELOG 和示例一致
- [ ] 没有 BP、Note、音频、密钥、日志或临时研究数据

## 功能验收

- [ ] 仅输入公司名时先询问交流对象、补充材料和是否播客
- [ ] 未回答 intake 前不开始公开检索
- [ ] 材料型案例能保留文件页码/幻灯片引用并与公开信息核验
- [ ] quick 和 standard 工作稿通过 validate_note.py
- [ ] 中文示例成功渲染 PDF 并通过 validate_pdf.py
- [ ] 所有 PDF 页面已转为 PNG 并逐页目视检查
- [ ] 无 Key Windows 路径能生成非空 WAV
- [ ] 官方 speech 路径的调用说明、Key 边界和失败降级清晰
- [ ] Skill quick_validate 和 Plugin validate_plugin 通过

## 发布

- [ ] 从远端 main 最新提交创建发布提交，不改写公开历史
- [ ] 推送 main
- [ ] 创建并推送 v0.3.0 标签
- [ ] 从远端 Marketplace 重新安装 Plugin
- [ ] 新线程中完成一次 intake 与 PDF 生成验收
