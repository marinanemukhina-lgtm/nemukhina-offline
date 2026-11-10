# Nemukhina Offline — Offline AI Assistant

**For your tasks. On your computer.**

[Русский](../README.md) · [中文](README.zh.md) · [Test evidence](VALIDATION.md)

Ask questions, develop ideas, write, translate, work through code and plan your next steps. A private local workspace with conversations on the left and useful results on the right. Documents are optional. Russian, English and Chinese interfaces; no account, cloud API or telemetry.

![Running application](images/assistant.jpg)

## What works

- General multi-turn conversations with a local GGUF model.
- Persistent conversations, renaming and recoverable archive.
- Copy answers, save Markdown or export a whole conversation.
- Import TXT/Markdown; exact source quotes, line numbers and SHA-256.
- Separate source-based mode with visible citation warnings.
- Local model setup, cancellation, JSON backup and non-destructive restore.

## Start

Python 3.10+. No Python dependencies, Node.js or build step.

```sh
git clone https://github.com/marinanemukhina-lgtm/nemukhina-offline.git
cd nemukhina-offline
python3 server.py
```

On Windows use `py -3 server.py`. Open **http://127.0.0.1:8765** and choose English. Stop with `Ctrl+C`.

Choose **Connect a model**, enter absolute paths to the official `llama-completion` executable and a compatible instruction-tuned `.gguf` model, then click **Connect and check**. Alternatively, place the extracted engine in `runtime` and the model in `models` beside `server.py`, then choose **Find prepared files**. The startup check shows the model name, actual answer and elapsed time; it does not assess overall answer quality. Initial downloads require internet. The app downloads nothing automatically. Search and backups work without a model. See [model setup](MODELS.md).

```sh
python3 server.py --engine /path/to/llama-completion --model /path/to/model.gguf
```

The app helps generate answers; it does not execute suggested code or act on your computer. Model quality is not guaranteed. Our small-model tests include repeated ideas, changed deadlines, mixed languages and a fabricated source detail. Read the [raw evidence and limits](VALIDATION.md), not just screenshots.

## Data and limits

SQLite at `data/library.sqlite3` stores conversations, materials and model paths. JSON v2 backups merge without replacing existing records and accept v1 document backups. Data is plaintext. Keep backups outside the repository.

- Documents: UTF-8 TXT/MD, 1 MiB each, 200 files / 50 MiB total.
- History: 500 conversations, 100 answers per conversation, 20 MiB.
- Recent complete exchanges fit a 10,000-byte prompt budget; omitted older exchanges are reported.
- Generation: 4096-token context, 512 new tokens, 180-second timeout, one request at a time. Long answers may stop at the token limit.
- Quote search is lexical: every query word must occur on the same line. No semantic RAG, PDF, OCR or web search.
- Citation checks only check reference numbers. Even a cited answer may be unsupported.

All application assets are local. The server binds to loopback and checks Host, Origin and a session token. Do not expose it publicly. The chosen executable is trusted and is not automatically sandboxed. [Security](../SECURITY.md).

## Contribute

```sh
python3 -m unittest discover -s tests -v
```

[CI](https://github.com/marinanemukhina-lgtm/nemukhina-offline/actions/workflows/test.yml) covers Python 3.10/3.14 on Linux/macOS/Windows; real model and browser checks were on macOS ARM64. Bring synthetic reproductions, translations, accessibility improvements or model evaluations. [Contributing](../CONTRIBUTING.md) · [Roadmap](ROADMAP.md).

Code: MIT. Tabler icons: MIT. Lora font: SIL OFL. Bundled notices are in `web/assets`. Models and personal documents are not redistributed. [Comparison and provenance](COMPARISON.md).
