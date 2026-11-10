"""Validated interchange for the local library; no network or implicit file access."""

import hashlib
import json
from pathlib import PurePosixPath

from offline import MAX_FILE, MAX_TOTAL

FORMAT = "nemukhina-offline"


def validate_document(item):
    if not isinstance(item, dict):
        raise ValueError("document_format")
    name, text = item.get("name"), item.get("text")
    if (
        not isinstance(name, str)
        or not name.strip()
        or len(name) > 255
        or "/" in name
        or "\\" in name
        or any(ord(c) < 32 for c in name)
        or PurePosixPath(name).suffix.lower() not in (".txt", ".md")
    ):
        raise ValueError("file_name")
    if not isinstance(text, str) or "\x00" in text:
        raise ValueError("file_encoding")
    try:
        raw = text.encode("utf-8")
    except UnicodeError:
        raise ValueError("file_encoding") from None
    if len(raw) > MAX_FILE:
        raise ValueError("file_size")
    digest = hashlib.sha256(raw).hexdigest()
    if "id" in item and item["id"] != digest:
        raise ValueError("checksum")
    return digest, name, text, len(raw)


def add_documents(db, items):
    if not isinstance(items, list) or len(items) > 200:
        raise ValueError("document_count")
    rows = [validate_document(item) for item in items]
    # Lock before reading counts so concurrent imports cannot lose updates.
    with db:
        db.execute("BEGIN IMMEDIATE")
        before = db.execute("SELECT count(*) FROM documents").fetchone()[0]
        db.executemany("INSERT OR IGNORE INTO documents VALUES (?,?,?,?)", rows)
        count, size = db.execute(
            "SELECT count(*),coalesce(sum(size),0) FROM documents"
        ).fetchone()
        if count > 200 or size > MAX_TOTAL:
            raise ValueError("library_limit")
    return count - before


def snapshot(db):
    rows = db.execute("SELECT id,name,text FROM documents ORDER BY name,id").fetchall()
    return {
        "format": FORMAT,
        "version": 1,
        "documents": [dict(zip(("id", "name", "text"), row)) for row in rows],
    }


def restore(db, data):
    if (
        not isinstance(data, dict)
        or data.get("format") != FORMAT
        or type(data.get("version")) is not int
        or data["version"] != 1
        or not isinstance(data.get("documents"), list)
    ):
        raise ValueError("backup_format")
    if any(not isinstance(d, dict) or "id" not in d for d in data["documents"]):
        raise ValueError("checksum")
    # Merge, never replace: a restore cannot erase the user's existing library.
    return add_documents(db, data["documents"])
