# Validation / Проверки — 10 ноября 2026

## Local application

macOS ARM64 / Python 3.9.6. Test command:

```sh
python3 -m unittest discover -s tests -v
```

Coverage includes multilingual exact search, hashes, duplicates, invalid UTF-8, atomic import and limits, concurrent imports, backup round-trip and merge, tampered backups, path validation, API Host/Origin/token checks, inaccessible arbitrary files, API content types/limits, no-model/no-evidence paths, citation syntax, and no-outbound-connect control for source search.

Browser acceptance: actual app opened in the in-app browser; one-click example, source inspection with line numbers, RU/EN/ZH UI and search exercised. A 390px viewport had no horizontal document overflow (clientWidth = scrollWidth = 390). The in-app browser's narrow screenshot scaling was unusual; this is not full physical-mobile acceptance. Desktop screenshot in `images/workspace.jpg` is the running app, not a mockup. Upload/download/restore paths have HTTP integration tests; manual cross-browser file-picker acceptance remains outstanding.

CI matrix: Python 3.10 / 3.14 on Ubuntu, macOS, Windows. See the live [Actions results](https://github.com/marinanemukhina-lgtm/nemukhina-offline/actions/workflows/test.yml), rather than assuming a configured job passed. One POSIX executable fixture is explicitly skipped on Windows.

## Actual local model, with OS network denied

- Engine: official llama.cpp **b12110**, version `0.9.0-dev`, commit `cd959bae9`, macOS ARM64.
- Engine archive SHA-256: `4f5b8de12e0b9516658ca6a5764c6ffb3d7c659c3dd538556b1413c7b4050662`, matched GitHub's release digest.
- Model: [Qwen/Qwen2.5-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF), revision `9217f5db79a29953eb74d5343926648285ec7e67`, `qwen2.5-0.5b-instruct-q4_k_m.gguf`.
- Model SHA-256: `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`. Model card labels Apache-2.0; no weights are redistributed here.
- All source texts and questions in the test are synthetic. Raw output: [model-smoke.json](model-smoke.json).

| Language | Answer | Wall time | Requested citation present |
|---|---|---|---|
| Russian | Дробь 1/2 равна 0,5. | 0.614 s | No |
| English | 1/2 equals 0.5. | 0.429 s | No |
| Chinese | 分数 1/2 等于 0.5。 | 0.470 s | No |

These are three trivial arithmetic smoke cases, **not an accuracy, safety, educational-quality or performance benchmark**. Warm-cache effects apply; peak memory was not measured. No claim of reliable citation following is made. The UI/CLI now warn when the model omits citation numbers or cites nonexistent numbers. Even syntactically valid citations do not prove support.

The first run with a plain completion prompt repeated instructions and generated irrelevant text. The adapter was corrected to use the model's built-in chat template (`--jinja --single-turn`), temperature 0 and seed 42. The table records the corrected adapter.

### Reproduce on macOS

After downloading the engine and model from their official sources:

```sh
sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  python3 scripts/evaluate_model.py \
  --engine /path/to/llama-completion \
  --model /path/to/qwen2.5-0.5b-instruct-q4_k_m.gguf \
  --output /tmp/model-smoke.json
```

A separate negative control attempted a socket connection to a running local server within the same sandbox profile; it failed with `PermissionError: Operation not permitted`. This confirms network denial was active. This verification applies to this macOS engine/model run, not every possible user-selected executable.

The earlier 0.1 session could not nest `sandbox-exec` inside its execution sandbox. In this iteration, running the test through the authorized execution path allowed the inner network-denial profile. No system security setting was disabled.

## Still unverified

Broad model grounding, prompt-injection resilience, large libraries, accessibility with real assistive devices, full browser file flows on Windows/Linux, supported-device RAM and latency, and signed installers. See [release gates](ROADMAP.md).
