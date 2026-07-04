# 从这里开始

## A. 作者发布（只做一次）

### 第 1 步：创建空的 GitHub 公共仓库（已完成）

1. 登录 GitHub。
2. 点击右上角 `+` → `New repository`。
3. Repository name 填：`prepare-investment-visit`。
4. Visibility 选择 `Public`。
5. 不要勾选自动创建 README、`.gitignore` 或 License；这些文件已经在发行包中。
6. 点击 `Create repository`。
7. 本项目仓库：`https://github.com/mengyao007/prepare-investment-visit.git`。

发布者为 `mengyao007`，许可证为 MIT。维护者将完成 Git 初始化、提交、推送、版本标签和安装验证。

### 第 2 步：发布后自己做一次安装验收

```text
codex plugin marketplace add mengyao007/prepare-investment-visit
codex plugin add prepare-investment-visit@prepare-investment-visit
```

也可以在 Codex 的 Plugins 页面选择新加入的 marketplace，再点击安装。重启 Codex 或开启新线程后输入：

```text
使用 $prepare-investment-visit 调研某家公司，生成 quick 版访前 Note。
```

## B. 普通使用者安装

1. 使用者先在自己的 Codex 登录自己的 ChatGPT/Codex 账户。
2. 添加上述 marketplace 并安装 Plugin。
3. 输入 `$prepare-investment-visit` 调用。

使用者不需要向作者申请 API Key，也不应把自己的 API Key 填进 Skill。模型用量归使用者自己的 Codex 账户。

## C. 飞书机器人（发布后再做）

飞书机器人不是每个领导单独运行 Codex，而是由公司服务器统一执行。因此：

1. 公司创建专用 OpenAI API Project 或公司管理的 Codex 账户。
2. 管理员把公司凭据放入部署平台的 Secret 管理器。
3. 管理员配置飞书 App ID/Secret 和允许使用机器人的群聊白名单。
4. 普通飞书用户只上传 BP、确认公司与交流对象，不接触任何 API Key。

不要使用作者个人 Key 部署公共或公司机器人。详见 [`AUTHENTICATION.md`](AUTHENTICATION.md)。
