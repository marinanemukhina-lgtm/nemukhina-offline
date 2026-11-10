"""Reproducible smoke evidence, not an accuracy benchmark. No model download."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import offline

parser = argparse.ArgumentParser()
parser.add_argument("--engine", required=True)
parser.add_argument("--model", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
cases = [
    ("ru", "дробь", "Чему равна 1/2? Ответь одним предложением со ссылкой [1]."),
    (
        "en",
        "fraction",
        "What does 1/2 equal? Answer in one sentence with citation [1].",
    ),
    ("zh", "分数", "1/2 等于多少？请用一句话回答，并引用 [1]。"),
]
report = {
    "kind": "smoke, not accuracy benchmark",
    "platform": platform.platform(),
    "python": platform.python_version(),
    "cases": [],
}
hash_model = hashlib.sha256()
with open(args.model, "rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        hash_model.update(chunk)
report["model_sha256"] = hash_model.hexdigest()
with tempfile.TemporaryDirectory() as tmp:
    db = offline.connect(Path(tmp) / "eval.db")
    offline.import_files(db, sorted((root / "examples").glob("*.md")))
    for lang, query, question in cases:
        sources = offline.search(db, query)
        start = time.monotonic()
        answer = offline.generate(
            args.engine,
            args.model,
            offline.prompt_for(question, sources, lang, "general"),
        )
        report["cases"].append(
            {
                "language": lang,
                "question": question,
                "sources": sources,
                "answer": answer,
                "elapsed_seconds": round(time.monotonic() - start, 3),
                "contains_expected_number": bool(re.search(r"0[.,]5", answer)),
                "contains_reference_1": "[1]" in answer,
            }
        )
    db.close()
Path(args.output).write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(
    json.dumps(
        [
            {k: v for k, v in c.items() if k not in ("sources", "question")}
            for c in report["cases"]
        ],
        ensure_ascii=False,
        indent=2,
    )
)
