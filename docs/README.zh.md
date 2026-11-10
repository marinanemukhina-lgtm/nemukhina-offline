# Nemukhina Offline — 离线 AI 助手

**为您的任务而来。在您的电脑上运行。**

[Русский](../README.md) · [English](README.en.md) · [测试记录](VALIDATION.md)

提问、理解问题、构思想法、写作、翻译、分析代码、规划下一步。左侧对话，右侧查看和保存结果。文档不是普通对话的前提。支持俄语、英语和中文界面，无需账号，没有云端 API 或遥测。

![应用实际运行界面](images/assistant.jpg)

## 已实现

- 使用本地 GGUF 模型进行多轮对话。
- 本地保存历史，重命名、归档及取消归档。
- 复制回答、保存 Markdown、导出整个对话。
- 导入 TXT/Markdown，查看精确引用、行号和 SHA-256。
- 单独的来源模式，显示引用警告。
- 配置本地模型、停止生成、JSON 备份及合并恢复。

## 启动

需要 Python 3.10 或更新版本。无需额外 Python 依赖、Node.js 或构建步骤。

```sh
git clone https://github.com/marinanemukhina-lgtm/nemukhina-offline.git
cd nemukhina-offline
python3 server.py
```

Windows 使用 `py -3 server.py`。打开 **http://127.0.0.1:8765**，选择中文。按 `Ctrl+C` 停止服务器。

点击“连接模型”，填写官方 `llama-completion` 可执行文件及兼容的 GGUF 指令模型的完整路径。首次下载需要网络；应用不会自动下载。准备完毕后可以离线生成回答。没有模型也能搜索资料和备份。参见[模型设置](MODELS.md)。

```sh
python3 server.py --engine /path/to/llama-completion --model /path/to/model.gguf
```

本应用生成回答，不会执行模型提供的代码，也不会自行操作电脑。小模型的实测出现了重复创意、修改截止日期、混用语言和编造来源细节等错误。请阅读[原始回答及限制](VALIDATION.md)，不要将运行成功等同于回答准确。

## 数据与限制

SQLite 数据库 `data/library.sqlite3` 保存对话、资料和模型路径。JSON v2 备份包含文档及对话，也能导入旧版 v1 文档备份。恢复时添加缺少的记录，保留已有记录。数据未加密，请妥善保管备份。

- 文档：UTF-8 TXT/MD，每个不超过 1 MiB，共 200 个或 50 MiB。
- 历史：最多 500 个对话，每个 100 次回答，总计 20 MiB。
- 上下文：保留最近的完整问答，提示词最多 10,000 字节；省略旧内容时会提示。
- 生成：4096 token 上下文，最多 512 个新 token，180 秒超时，一次一个请求；长回答可能在上限处中断。
- 引用搜索是词面匹配：所有关键词须在同一行。没有语义 RAG、PDF、OCR 或网页搜索。
- 引用检查只能检查编号，不能证明结论正确。

界面资源均保存在本地。服务器只绑定回环地址，并检查 Host、Origin 和会话令牌。不要公开此端口。用户选择的运行程序是受信任代码，应用不会自动将其隔离。[安全说明](../SECURITY.md)。

## 参与

```sh
python3 -m unittest discover -s tests -v
```

CI 覆盖 Linux/macOS/Windows 的 Python 3.10/3.14；真实模型和浏览器测试在 macOS ARM64 上完成。欢迎提交合成示例、翻译改进、无障碍检查和模型测试。[贡献指南](../CONTRIBUTING.md) · [路线图](ROADMAP.md)。

代码采用 MIT；Tabler 图标采用 MIT；Lora 字体采用 SIL OFL。许可证位于 `web/assets`。不分发模型权重或个人文档。[比较与来源](COMPARISON.md)。
