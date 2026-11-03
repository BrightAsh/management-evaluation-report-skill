#!/usr/bin/env python3
"""Validate content.json before the renderers run."""

from __future__ import annotations

import json
from pathlib import Path
import sys


REQUIRED = {
    "title": ("text",), "ev": ("label", "text"), "key": ("text",),
    "bp": ("items",), "vision": ("k", "text"), "sec": ("no", "title"), "sub": ("title",),
    "grid": ("rows",), "flow": ("items",), "strip": ("items",),
    "boxes": ("items",), "kv": ("k",), "banner": ("text",),
    "chev": ("st",), "check": ("text",), "comb": ("cards", "res"),
    "line": ("k", "v"), "cmp": ("a", "b"), "bl": ("b",),
    "text": ("p",), "eff": ("k", "v", "rows"), "res": ("b",),
    "kpi": ("items",), "tbl": ("w", "head", "rows"),
    "cols": ("cols",), "img": (),
}


def fail(path: str, message: str) -> None:
    raise ValueError(f"{path}: {message}")


def validate_image(image: object, path: str) -> None:
    if not isinstance(image, dict):
        fail(path, "그림은 객체여야 합니다")
    if not image.get("src") and not image.get("label"):
        fail(path, "src 또는 label이 필요합니다")


def validate_blocks(blocks: object, path: str) -> int:
    if not isinstance(blocks, list):
        fail(path, "블록 배열이 필요합니다")
    count = 0
    for index, block in enumerate(blocks):
        current = f"{path}[{index}]"
        if not isinstance(block, dict):
            fail(current, "블록은 객체여야 합니다")
        kind = block.get("t")
        if kind not in REQUIRED:
            fail(current, f"알 수 없는 블록 타입 {kind!r}")
        missing = [key for key in REQUIRED[kind] if key not in block]
        if missing:
            fail(current, "필수 필드 누락: " + ", ".join(missing))
        count += 1

        if kind == "grid":
            for row_index, row in enumerate(block["rows"]):
                row_path = f"{current}.rows[{row_index}]"
                if not isinstance(row, dict) or "k" not in row:
                    fail(row_path, "k가 있는 행 객체가 필요합니다")
                if "cells" not in row and "span" not in row:
                    fail(row_path, "cells 또는 span이 필요합니다")
                for cell_index, cell in enumerate(row.get("cells", [])):
                    if isinstance(cell, dict) and "img" in cell:
                        images = cell["img"] if isinstance(cell["img"], list) else [cell["img"]]
                        for image_index, image in enumerate(images):
                            validate_image(image, f"{row_path}.cells[{cell_index}].img[{image_index}]")
        elif kind == "cols":
            for col_index, column in enumerate(block["cols"]):
                count += validate_blocks(column, f"{current}.cols[{col_index}]")
        elif kind == "kv":
            if not any(key in block for key in ("text", "b", "inner")):
                fail(current, "text, b 또는 inner가 필요합니다")
            if "img" in block:
                images = block["img"] if isinstance(block["img"], list) else [block["img"]]
                for image_index, image in enumerate(images):
                    validate_image(image, f"{current}.img[{image_index}]")
            if "inner" in block:
                count += validate_blocks(block["inner"], f"{current}.inner")
        elif kind == "strip":
            for item_index, image in enumerate(block["items"]):
                validate_image(image, f"{current}.items[{item_index}]")
        elif kind == "flow":
            for item_index, item in enumerate(block["items"]):
                if not isinstance(item, dict) or "h" not in item or "b" not in item:
                    fail(f"{current}.items[{item_index}]", "h와 b가 필요합니다")
        elif kind == "boxes":
            for item_index, item in enumerate(block["items"]):
                if not isinstance(item, dict) or "h" not in item or "b" not in item:
                    fail(f"{current}.items[{item_index}]", "h와 b가 필요합니다")
        elif kind == "chev":
            for item_index, item in enumerate(block["st"]):
                if not isinstance(item, dict) or "h" not in item or "t" not in item:
                    fail(f"{current}.st[{item_index}]", "h와 t가 필요합니다")
        elif kind == "comb":
            for item_index, item in enumerate(block["cards"]):
                if not isinstance(item, dict) or "h" not in item or "b" not in item:
                    fail(f"{current}.cards[{item_index}]", "h와 b가 필요합니다")
        elif kind == "cmp":
            for side in ("a", "b"):
                item = block[side]
                if not isinstance(item, dict) or any(key not in item for key in ("tag", "h", "b")):
                    fail(f"{current}.{side}", "tag, h, b가 필요합니다")
        elif kind == "kpi":
            for item_index, item in enumerate(block["items"]):
                if not isinstance(item, dict) or "v" not in item or "l" not in item:
                    fail(f"{current}.items[{item_index}]", "v와 l이 필요합니다")
        elif kind == "tbl":
            width = len(block["w"])
            if len(block["head"]) != width or any(len(row) != width for row in block["rows"]):
                fail(current, "w, head, 각 row의 열 수가 같아야 합니다")
        elif kind == "img":
            validate_image(block, current)
    return count


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_content.py content.json", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    data = json.loads(source.read_text(encoding="utf-8"))
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        fail("pages", "한 쪽 이상의 배열이 필요합니다")
    total = 0
    for index, page in enumerate(pages):
        if not isinstance(page, dict) or "blocks" not in page:
            fail(f"pages[{index}]", "blocks가 있는 쪽 객체가 필요합니다")
        total += validate_blocks(page["blocks"], f"pages[{index}].blocks")
    print(json.dumps({"pages": len(pages), "blocks": total}, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"content validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
