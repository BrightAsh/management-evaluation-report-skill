#!/usr/bin/env python3
"""Measure exact local size and optional Anthropic input-token counts.

Local mode reports bytes, Unicode characters and lines. ``--count-tokens``
uses Anthropic's model-specific Token Counting API and requires an
``ANTHROPIC_API_KEY`` environment variable. The key is never printed.

The API result is a preflight input estimate, not total agentic task usage.
Repeated history, thinking/output, tools and tool results must be measured in
an actual v2.2/v2.3 run.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import mimetypes
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


TEXT_EXTENSIONS = {
    ".md", ".txt", ".csv", ".json", ".html", ".xml", ".yaml", ".yml",
    ".py", ".js", ".ts", ".css",
}
IMAGE_MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif", ".webp": "image/webp",
}
SCENARIOS = {"A", "AB", "AC", "AD", "ABC", "ABD", "ACD", "ABCD"}


def count_visual_tokens(width: int, height: int) -> int:
    return math.ceil(width / 28) * math.ceil(height / 28)


def resized_image_size(width: int, height: int, max_edge: int = 2576, max_tokens: int = 4784) -> tuple[int, int]:
    """Apply Anthropic's documented Claude 4.7+ high-resolution limit."""

    def fits(w: int, h: int) -> bool:
        return max(w, h) <= max_edge and count_visual_tokens(w, h) <= max_tokens

    if fits(width, height):
        return width, height
    scale = min(max_edge / max(width, height), math.sqrt(max_tokens / count_visual_tokens(width, height)))
    lo, hi = 1, max(1, int(width * scale))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        h = max(1, round(mid * height / width))
        if fits(mid, h):
            lo = mid
        else:
            hi = mid - 1
    return lo, max(1, round(lo * height / width))


def image_stats(path: Path) -> dict[str, int | str]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required for local image measurements") from exc
    with Image.open(path) as image:
        width, height = image.size
    processed_w, processed_h = resized_image_size(width, height)
    return {
        "path": str(path), "width": width, "height": height,
        "processed_width": processed_w, "processed_height": processed_h,
        "visual_tokens": count_visual_tokens(processed_w, processed_h),
    }


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="strict")


def file_stats(path: Path) -> dict[str, int | str]:
    text = read_text(path)
    return {
        "path": str(path), "bytes": len(text.encode("utf-8")),
        "chars": len(text), "lines": text.count("\n") + 1,
    }


def validate_scenario(value: str) -> str:
    scenario = "".join(sorted(value.upper(), key="ABCD".index))
    if scenario not in SCENARIOS:
        raise ValueError("scenario must be A, AB, AC, AD, ABC, ABD, ACD, or ABCD")
    return scenario


def route_files(skill_dir: Path, scenario: str, task: str) -> list[Path]:
    """Return files explicitly routed by v2.2 or v2.3."""
    refs = skill_dir / "references"
    if (refs / "core.md").is_file():
        paths = [skill_dir / "SKILL.md"]
        if task == "help":
            return paths
        paths.append(refs / "core.md")
        if "C" in scenario:
            paths.append(refs / "indicators.md")
        if "B" in scenario:
            paths.append(refs / "template.md")
        if task == "report":
            if "B" not in scenario:
                paths.append(refs / "default_layout.md")
            paths.extend([refs / "visuals.md", refs / "layout_render.md"])
        return paths

    paths = [skill_dir / "SKILL.md"]
    if task == "help":
        return paths
    upper = 4 if task == "outline" else 8
    for number in range(1, upper + 1):
        matches = sorted(refs.glob(f"{number:02d}_*.md"))
        if len(matches) != 1:
            raise FileNotFoundError(f"expected one references/{number:02d}_*.md")
        paths.append(matches[0])
    if task == "report" and "B" not in scenario:
        matches = sorted(refs.glob("09_*.md"))
        if len(matches) != 1:
            raise FileNotFoundError("expected one references/09_*.md")
        paths.append(matches[0])
    return paths


def route_assets(skill_dir: Path, task: str) -> list[Path]:
    if task == "help":
        return []
    assets = skill_dir / "assets"
    if (skill_dir / "references" / "core.md").is_file():
        names = ["work_ledger.md"] + (["content_template.json"] if task == "report" else [])
    else:
        names = ["worksheets.md"] + (["content_template.json"] if task == "report" else [])
    return [assets / name for name in names if (assets / name).is_file()]


def text_block(text: str) -> dict:
    return {"type": "text", "text": text}


def input_blocks(paths: list[Path], label: str) -> list[dict]:
    blocks: list[dict] = [text_block(f"\n--- {label} ---\n")]
    for path in paths:
        ext = path.suffix.lower()
        if ext in TEXT_EXTENSIONS:
            blocks.append(text_block(f"\n--- FILE: {path.name} ---\n{read_text(path)}"))
        elif ext == ".pdf":
            blocks.append({"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": base64.standard_b64encode(path.read_bytes()).decode("ascii")}})
        elif ext in IMAGE_MEDIA_TYPES:
            blocks.append({"type": "image", "source": {"type": "base64", "media_type": IMAGE_MEDIA_TYPES[ext], "data": base64.standard_b64encode(path.read_bytes()).decode("ascii")}})
        else:
            guessed = mimetypes.guess_type(path.name)[0] or "unknown"
            raise ValueError(
                f"{path}: {guessed} cannot be counted directly. Run scripts/read_inputs.py "
                "and pass the extracted .txt plus images Claude will inspect."
            )
    return blocks


def count_tokens(blocks: list[dict], model: str) -> int:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set; set it locally and never commit it")
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": blocks}]}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages/count_tokens", data=payload, method="POST",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return int(json.load(response)["input_tokens"])
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic token counting failed ({exc.code}): {detail}") from exc


def parse_paths(values: list[str] | None) -> list[Path]:
    paths = [Path(value).resolve() for value in (values or [])]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing files: " + ", ".join(missing))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--task", choices=("help", "outline", "report"), default="report")
    parser.add_argument("--A", nargs="*", default=[])
    parser.add_argument("--B", nargs="*", default=[])
    parser.add_argument("--C", nargs="*", default=[])
    parser.add_argument("--D", nargs="*", default=[])
    parser.add_argument("--model", default="claude-opus-5-5")
    parser.add_argument("--exclude-assets", action="store_true")
    parser.add_argument("--count-tokens", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    scenario = validate_scenario(args.scenario)
    skill_paths = route_files(skill_dir, scenario, args.task)
    asset_paths = [] if args.exclude_assets else route_assets(skill_dir, args.task)
    groups = {
        "skill": skill_paths + asset_paths,
        "A": parse_paths(args.A), "B": parse_paths(args.B),
        "C": parse_paths(args.C), "D": parse_paths(args.D),
    }
    for letter in "BCD":
        if letter not in scenario and groups[letter]:
            raise ValueError(f"{letter} files supplied but {letter} is absent from scenario")

    text_measurements = {
        name: [file_stats(path) for path in paths if path.suffix.lower() in TEXT_EXTENSIONS]
        for name, paths in groups.items()
    }
    image_measurements = {
        name: [image_stats(path) for path in paths if path.suffix.lower() in IMAGE_MEDIA_TYPES]
        for name, paths in groups.items()
    }
    totals = {
        name: {
            "files": len(paths), "bytes": sum(path.stat().st_size for path in paths),
            "text_chars": sum(int(item["chars"]) for item in text_measurements[name]),
            "visual_tokens": sum(int(item["visual_tokens"]) for item in image_measurements[name]),
        }
        for name, paths in groups.items()
    }
    result: dict = {
        "model": args.model, "scenario": scenario, "task": args.task,
        "scope": "preflight routed input only; not total agentic task usage",
        "route_files": [str(path.relative_to(skill_dir)) for path in skill_paths],
        "route_assets": [str(path.relative_to(skill_dir)) for path in asset_paths],
        "groups": totals, "images": image_measurements,
    }

    if args.count_tokens:
        per_group: dict[str, int] = {}
        combined: list[dict] = []
        for name in ("skill", "A", "B", "C", "D"):
            if not groups[name]:
                continue
            blocks = input_blocks(groups[name], name)
            per_group[name] = count_tokens(blocks, args.model)
            combined.extend(blocks)
        result["input_tokens_by_group"] = per_group
        result["input_tokens_combined"] = count_tokens(combined, args.model)
        result["token_count_note"] = "Anthropic documents count_tokens as an estimate; an actual request may differ slightly."

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"model: {args.model}\nscenario: {scenario}\ntask: {args.task}\nscope: {result['scope']}")
        for name, item in totals.items():
            if item["files"]:
                print(f"{name}: {item['files']} files, {item['bytes']:,} bytes, {item['text_chars']:,} text chars")
                if item["visual_tokens"]:
                    print(f"{name}_visual_tokens: {item['visual_tokens']:,}")
        if args.count_tokens:
            for name, value in result["input_tokens_by_group"].items():
                print(f"{name}_input_tokens: {value:,}")
            print(f"combined_input_tokens: {result['input_tokens_combined']:,}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
