#!/usr/bin/env python3
"""Claude 스킬 업로드용 zip을 만든다: dist/performance-report-writer.zip
zip을 열면 맨 위에 performance-report-writer/ 폴더가 있고, 그 안에 SKILL.md가 있다.
개발용 파일(node_modules, .git, 이전 zip 등)은 넣지 않는다."""
import os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'performance-report-writer'
OUT = os.path.join(ROOT, 'dist', NAME + '.zip')
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', 'work', '.github'}
SKIP_EXT = {'.pyc', '.zip'}
SKIP_FILES = {'.DS_Store', 'package-lock.json'}

n = 0
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            if f in SKIP_FILES or os.path.splitext(f)[1] in SKIP_EXT:
                continue
            if f.endswith('.html') and os.path.basename(d) == 'demo':
                continue  # 데모 중간 산출물(.gitignore와 같게)
            full = os.path.join(d, f)
            rel = os.path.relpath(full, ROOT)
            z.write(full, os.path.join(NAME, rel))
            n += 1
print(f'{os.path.relpath(OUT, ROOT)}: 파일 {n}개, {os.path.getsize(OUT):,} bytes')
