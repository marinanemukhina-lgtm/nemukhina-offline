"""Validate selected files; discover only the application's runtime and models folders."""

import os
from pathlib import Path

ENGINE_NAMES = ("llama-completion", "llama-completion.exe")


def validate(engine, model):
    if not all(isinstance(p, str) and 0 < len(p) <= 4096 for p in (engine, model)):
        raise ValueError("invalid_request")
    engine, model = Path(engine).expanduser().resolve(), Path(model).expanduser().resolve()
    if engine.name not in ENGINE_NAMES or not engine.is_file() or not os.access(engine, os.X_OK):
        raise ValueError("engine_path")
    if not model.is_file() or model.suffix.lower() != ".gguf":
        raise ValueError("model_path")
    with model.open("rb") as stream:
        if stream.read(4) != b"GGUF":
            raise ValueError("model_path")
    return str(engine), str(model)


def fingerprint(engine, model):
    """Invalidate session checks after file changes; this is not a trust checksum."""
    try:
        return tuple(
            (str(p), p.stat().st_size, p.stat().st_mtime_ns)
            for p in (Path(engine), Path(model))
        )
    except (OSError, TypeError):
        return None


def discover(root):
    """Bounded and read-only. Never search home, Downloads, or symlinked folders."""
    root = Path(root).resolve()
    found = {"engines": [], "models": []}
    for folder, key in (("runtime", "engines"), ("models", "models")):
        base = root / folder
        if base.is_symlink() or not base.is_dir():
            continue
        visited = 0
        for directory, dirs, names in os.walk(base, followlinks=False):
            depth = len(Path(directory).relative_to(base).parts)
            dirs[:] = (
                sorted(d for d in dirs if not (Path(directory) / d).is_symlink())[:32]
                if depth < 2 else []
            )
            for name in sorted(names):
                visited += 1
                if visited > 512:
                    break
                path = Path(directory) / name
                try:
                    if path.is_symlink() or not path.is_file():
                        continue
                    match = (
                        name in ENGINE_NAMES and os.access(path, os.X_OK)
                        if key == "engines" else path.suffix.lower() == ".gguf"
                    )
                    if match and len(found[key]) < 32:
                        found[key].append({
                            "path": str(path),
                            "name": str(path.relative_to(base)),
                            "bytes": path.stat().st_size,
                        })
                except OSError:
                    continue
            if visited > 512:
                break
    return found
