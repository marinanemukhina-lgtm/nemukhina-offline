"""Offline task samples with raw answers; not a general quality benchmark."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import socket
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import conversations
import offline

parser = argparse.ArgumentParser()
parser.add_argument("--engine", required=True)
parser.add_argument("--model", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
cases = [
    (
        "ru-plan",
        "ru",
        "Предложи три конкретных шага, чтобы начать изучать английский самостоятельно по 20 минут в день. Ответь кратко.",
        None,
    ),
    (
        "ru-writing",
        "ru",
        "Перепиши вежливо, сохрани смысл: «Пришли мне черновик завтра, я проверю». Одно предложение.",
        None,
    ),
    (
        "ru-ideas",
        "ru",
        "Придумай три разные идеи для короткого фантастического рассказа. По одному предложению на идею.",
        None,
    ),
    (
        "en-code",
        "en",
        "Write a Python function mean(numbers) that returns the arithmetic mean and raises ValueError for an empty list. Return only code.",
        None,
    ),
    (
        "en-reason",
        "en",
        "A box contains 3 red balls and 2 blue balls. One ball is drawn uniformly. What is the probability it is blue? Explain in one sentence.",
        None,
    ),
    (
        "en-writing",
        "en",
        "Rewrite this to be clear and polite: Send the notes today. One sentence.",
        None,
    ),
    (
        "zh-translate",
        "zh",
        "请把这句英文翻译成中文：The meeting starts at ten tomorrow morning. 只输出译文。",
        None,
    ),
    ("zh-plan", "zh", "给出三个整理学习笔记的具体步骤，每个步骤一句话。", None),
    (
        "ru-translate",
        "ru",
        "Переведи на русский: The meeting starts at ten tomorrow morning. Только перевод.",
        None,
    ),
]
source = {
    "id": hashlib.sha256("synthetic".encode()).hexdigest(),
    "name": "synthetic-schedule.md",
    "line": 1,
    "quote": "Команда Альфа встречается по четвергам в 15:00 в аудитории 7.",
}
cases.extend(
    [
        (
            "ru-source",
            "ru",
            "В какое время встречается команда Альфа? Укажи ссылку [1].",
            [source],
        ),
        (
            "ru-source-unknown",
            "ru",
            "В каком городе находится аудитория 7? Если источник не сообщает город, так и скажи.",
            [source],
        ),
    ]
)
report = {
    "kind": "task samples, not an accuracy benchmark",
    "platform": platform.platform(),
    "python": platform.python_version(),
    "model_file": Path(args.model).name,
    "cases": [],
}
sha = hashlib.sha256()
with open(args.model, "rb") as f:
    for block in iter(lambda: f.read(1024 * 1024), b""):
        sha.update(block)
report["model_sha256"] = sha.hexdigest()
probe = socket.socket()
probe.settimeout(1)
try:
    probe.connect(("1.1.1.1", 443))
    report["network_negative_control"] = "not blocked"
except PermissionError:
    report["network_negative_control"] = "PermissionError: OS denied outbound connect"
except OSError as e:
    report["network_negative_control"] = "inconclusive: " + type(e).__name__
finally:
    probe.close()
for name, lang, question, sources in cases:
    prompt, omitted = conversations.prompt(question, [], lang, sources)
    start = time.monotonic()
    answer = offline.generate(args.engine, args.model, prompt)
    report["cases"].append(
        {
            "name": name,
            "lang": lang,
            "question": question,
            "sources": sources,
            "answer": answer,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "citation_warning": (
                offline.citation_warning(answer, len(sources)) if sources else None
            ),
        }
    )
    print(name, report["cases"][-1]["elapsed_seconds"], flush=True)
# A second turn must recover a user-supplied detail from the previous conversation.
question = "Мой учебный проект называется «Орион». Ответь только: понял."
prompt, _ = conversations.prompt(question, [], "ru")
first = offline.generate(args.engine, args.model, prompt)
follow = "Как называется мой учебный проект? Ответь одним словом."
prompt, _ = conversations.prompt(
    follow, [{"question": question, "answer": first}], "ru"
)
start = time.monotonic()
answer = offline.generate(args.engine, args.model, prompt)
report["cases"].append(
    {
        "name": "ru-followup",
        "lang": "ru",
        "question": follow,
        "previous_question": question,
        "previous_answer": first,
        "answer": answer,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "contains_supplied_name": "орион" in answer.casefold(),
    }
)
Path(args.output).write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Saved", args.output, flush=True)
