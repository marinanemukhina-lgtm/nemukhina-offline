# Nemukhina Offline

**Your texts. Verifiable quotes. On your computer.**

A small local workspace for learning and working with sources. Useful without an AI model: import UTF-8 TXT/Markdown, search exact lines, open the original, copy a citation, and back up your library.

## Start

Install Python 3.10+, download/unzip the repository, and run from its folder:

```sh
python3 server.py
```

Windows: `py -3 server.py`. Open **http://127.0.0.1:8765**, switch to **English**, then click **Make sense of fractions**. The synthetic example is added automatically. There is no pip install, frontend build, login or cloud API. Initial software downloads require internet; the local UI uses no remote assets.

## Optional local model

```sh
python3 server.py --engine /path/to/llama-completion --model /path/to/model.gguf
```

Obtain llama.cpp and a compatible licensed GGUF model beforehand. Tested with llama.cpp build 12110; uses the model's chat template. School, university and everyday modes change the instructions, not the model's capabilities. Generation is experimental. A real network-denied RU/EN/ZH smoke test succeeded, but the tiny test model omitted citations in all three answers. The app flags missing/invalid citation numbers; it does not prove claims. [Evidence](VALIDATION.md).

## Boundaries

All query terms must appear in one line: this is lexical search, not semantic retrieval or translation. Up to 20 results. Files: 1 MiB each, 200 documents / 50 MiB total. Browser imports: 8 MiB JSON per batch. Backups: up to 320 MiB JSON, checksum-validated merge restores.

Data lives in `data/library.sqlite3`, relative to the working directory; select another location with `--db`. It is plaintext. Download backups and keep them outside Git. The server is loopback-only and intended for one local user; do not expose its port or proxy it. No PDF/OCR, voice, bundled encyclopedia or signed installer yet.

[Русский](../README.md) · [中文](README.zh.md) · [Contribute](../CONTRIBUTING.md) · [Security](../SECURITY.md) · [Roadmap](ROADMAP.md)
