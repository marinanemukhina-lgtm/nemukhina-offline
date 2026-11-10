# Changelog

## 0.3.0 — 2026-11-10

- General conversations without required documents; bounded multi-turn context.
- Persistent conversation history, renaming, recoverable archive, and Markdown exports.
- Local model configuration in the UI; cancellable inference with process cleanup.
- Atomic workspace backups v2 with v1 compatibility and conflict-preserving merge.
- A reference-led welcome screen, original paper illustration, dedicated conversation/result view, and responsive RU/EN/ZH layouts.
- Vendored Lora and Tabler assets with license notices; no remote UI assets.
- 33 local tests and two reproducible 12-task model reports under OS network denial. Reports include failures and hallucinations.

## 0.2.0 — 2026-11-10

- Local browser UI in Russian, English and Chinese; responsive layout and keyboard focus states.
- One-click synthetic examples; source inspection, citation copying, explicit text import.
- JSON backups and checksum-validated merge restores; existing documents preserved.
- Loopback-only server with per-session API token, Host/Origin checks and CSP.
- Optional model answers from retrieved sources; visible experimental status.
- Transaction locking for concurrent imports; integration and security-boundary tests.
- Cross-platform CI, contributor guide, security boundaries and reproducible model evidence.

## 0.1.0 — 2026-11-10

- Initial Python CLI, exact source search, SHA-256, synthetic multilingual examples.
- Experimental local llama.cpp adapter; no real model validation at initial publication.
