# Contributing / Участие

Help make offline AI useful for everyday tasks. Good first contributions: improve RU/EN/ZH translations, reproduce a bug with synthetic text, test keyboard navigation, simplify first-time setup, or document a model's actual limitations. Sources are an optional workflow; preserve the general-purpose conversation experience.

## Development

Python 3.9+; standard library only. No build step or package installation.

```sh
python3 -m unittest discover -s tests -v
python3 server.py --db /tmp/nemukhina-dev.sqlite3
```

Use Python 3.10+ for ongoing development (3.9 is a legacy compatibility target). On Windows use a local temporary path and `py -3` where appropriate. CI covers Python 3.10/3.14 on Linux/macOS/Windows. POSIX-only process fixture is explicitly skipped on Windows.

Keep changes focused. Explain the user-visible problem and validation. Tests should cover behavior and failure cases, not mirror implementation. Preserve UTF-8, exact source quotes, atomic workspace writes, recoverable archives, bounded history, loopback binding and the no-cloud default. Never add telemetry, remote assets, a model download or a new dependency without discussing its need. UI work should follow [the design rationale](docs/DESIGN.md), then be checked in a browser.

All text from documents and models is untrusted. Render it as text, not HTML. Do not enable shell execution, URL tools or filesystem tools for models.

## Before a pull request

- Run the tests; show what you actually checked.
- Exercise empty state, errors, keyboard and narrow screens for UI changes.
- Add only synthetic fixtures. Never commit databases, weights, credentials or personal files.
- Update documentation if behavior or limits change.
- Include relevant upstream license/attribution when borrowing code or material.

Contributions are under the project's MIT license. Be specific and respectful in reviews. No star exchanges, purchased stars or promotional spam.
