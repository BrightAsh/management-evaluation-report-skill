#!/usr/bin/env python3
"""Build the Claude upload ZIP from runtime files only."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parent.parent
NAME = "performance-report-writer-v2-3"
OUT = ROOT / "dist" / f"{NAME}.zip"
ROOT_FILES = ("SKILL.md", "LICENSE", "package.json", "requirements.txt")
RUNTIME_DIRS = ("references", "scripts", "assets")
SKIP_SUFFIXES = {".pyc", ".zip"}


def runtime_files():
    for name in ROOT_FILES:
        path = ROOT / name
        if path.is_file():
            yield path
    for directory in RUNTIME_DIRS:
        for path in sorted((ROOT / directory).rglob("*")):
            if path.is_file() and path.suffix not in SKIP_SUFFIXES and "__pycache__" not in path.parts:
                yield path


OUT.parent.mkdir(parents=True, exist_ok=True)
files = list(runtime_files())
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, Path(NAME) / path.relative_to(ROOT))
print(f"{OUT.relative_to(ROOT)}: {len(files)} files, {OUT.stat().st_size:,} bytes")
