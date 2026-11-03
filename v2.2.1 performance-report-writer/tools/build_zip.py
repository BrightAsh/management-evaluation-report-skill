#!/usr/bin/env python3
"""Build the Claude upload ZIP from runtime files only."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parent.parent
NAME = "performance-report-writer-v2-2-1"
OUT = ROOT / "dist" / f"{NAME}.zip"
ROOT_FILES = ("SKILL.md", "LICENSE", "package.json", "requirements.txt")
RUNTIME_DIRS = ("references", "scripts", "assets")
SKIP_SUFFIXES = {".pyc", ".zip"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".py", ".js", ".css", ".yaml", ".yml"}
TEXT_NAMES = {"LICENSE"}


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
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in files:
        arcname = (Path(NAME) / path.relative_to(ROOT)).as_posix()
        data = path.read_bytes()
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
            data = text.encode("utf-8")
        info = zipfile.ZipInfo(arcname, date_time=(2020, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
print(f"{OUT.relative_to(ROOT)}: {len(files)} files, {OUT.stat().st_size:,} bytes")
