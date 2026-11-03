#!/usr/bin/env python3
"""Build requested report formats and return one compact JSON summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def executable(value: str) -> str:
    found = shutil.which(value)
    if found:
        return found
    path = Path(value)
    if path.is_file():
        return str(path.resolve())
    raise FileNotFoundError(f"executable not found: {value}")


def run_step(name: str, command: list[str], timeout: int = 300) -> list[str]:
    result = subprocess.run(
        command, capture_output=True, text=True, errors="replace",
        timeout=timeout, check=False,
    )
    output = (result.stdout + "\n" + result.stderr).strip().splitlines()
    if result.returncode:
        raise RuntimeError(f"{name} failed ({result.returncode})\n" + "\n".join(output[-12:]))
    return output[-4:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("content", type=Path, help="content.json")
    parser.add_argument("output_stem", type=Path, help="output path without extension")
    parser.add_argument("--format", choices=("pdf", "docx", "both"), default="both")
    parser.add_argument("--font-scale", default="1.17")
    parser.add_argument("--spacing-scale", default="1.65")
    parser.add_argument("--node", default="node")
    parser.add_argument("--soffice", default="soffice")
    parser.add_argument("--skip-word-check", action="store_true")
    args = parser.parse_args()

    content = args.content.resolve()
    if not content.is_file():
        raise FileNotFoundError(content)
    stem = args.output_stem.resolve()
    stem.parent.mkdir(parents=True, exist_ok=True)
    scripts = Path(__file__).resolve().parent
    node = executable(args.node)
    summary: dict[str, object] = {"content": str(content), "format": args.format, "files": [], "steps": {}}

    if args.format in {"pdf", "both"}:
        html, pdf = stem.with_suffix(".html"), stem.with_suffix(".pdf")
        summary["steps"]["html"] = run_step("render_html", [node, str(scripts / "render_html.js"), str(content), str(html)])
        summary["steps"]["pdf"] = run_step("to_pdf", [sys.executable, str(scripts / "to_pdf.py"), str(html)])
        for path in (html, pdf):
            if not path.is_file():
                raise RuntimeError(f"expected output missing: {path}")
            summary["files"].append(str(path))

    if args.format in {"docx", "both"}:
        docx = stem.with_suffix(".docx")
        summary["steps"]["docx"] = run_step(
            "render_docx", [node, str(scripts / "render_docx.js"), str(content), str(docx), args.font_scale, args.spacing_scale]
        )
        if not docx.is_file():
            raise RuntimeError(f"expected output missing: {docx}")
        summary["files"].append(str(docx))

        soffice = shutil.which(args.soffice)
        if args.skip_word_check:
            summary["steps"]["word_check"] = "skipped by option"
        elif not soffice:
            summary["steps"]["word_check"] = "skipped: soffice not found"
        else:
            with tempfile.TemporaryDirectory(prefix="report-word-check-") as temp_dir:
                summary["steps"]["word_to_pdf"] = run_step(
                    "word_to_pdf", [soffice, "--headless", "--convert-to", "pdf", "--outdir", temp_dir, str(docx)], timeout=180
                )
                check_pdf = Path(temp_dir) / f"{docx.stem}.pdf"
                if not check_pdf.is_file():
                    raise RuntimeError("Word check PDF was not created")
                summary["steps"]["word_check"] = run_step(
                    "fill_check", [sys.executable, str(scripts / "fill_check.py"), str(check_pdf)], timeout=180
                )

    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"render_report: {exc}", file=sys.stderr)
        raise SystemExit(1)
