#!/usr/bin/env python3
"""SKILL.md + references + scripts를 한 파일로 합쳐 dist/SKILL_single_file.md를 만든다.

파일을 하나만 받는 환경(계정 스킬 저장, 코드 실행 AI에 붙여넣기)에서 쓴다.
사용법: python3 tools/build_single_file.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
front, body = re.match(r'(---\n.*?\n---\n)(.*)', skill, re.S).groups()

# 본문의 참고 경로를 부록 안내로 바꾼다
body = body.replace('각 단계의 세부 방법은 `references/`에 있다. 해당 단계에 들어갈 때 그 문서를 읽는다.',
                    '각 단계의 세부 방법은 이 파일 아래 **부록 A**에 있다. 해당 단계에 들어갈 때 그 부분을 읽는다.')
body = re.sub(r'`(0\d)_\w+\.md`', lambda m: f'부록 A-{m.group(1)}', body)
body = body.replace('코드를 실행할 수 없는 환경이면', '스크립트는 **부록 B**의 코드를 같은 이름의 파일로 저장해 쓴다. 코드를 실행할 수 없는 환경이면')
body = re.sub(r'## 폴더 안내\n\n```.*?```\n\n', '## 파일 안내\n\n', body, flags=re.S)   # 단일 파일판에는 폴더가 없다

out = [front, '\n> 단일 파일판입니다. 참고 문서는 부록 A, 스크립트와 데이터 틀은 부록 B에 있습니다.\n', body,
       '\n---\n\n# 부록 A. 단계별 방법\n']
for f in sorted((ROOT / 'references').glob('0*.md')):
    text = f.read_text(encoding='utf-8')
    lines, in_code = [], False
    for line in text.split('\n'):          # 코드 블록 밖의 제목만 한 단계 아래로
        if line.startswith('```'):
            in_code = not in_code
        elif not in_code and re.match(r'#{1,5} ', line):
            line = '#' + line
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'^## (0\d)\.', r'## A-\1.', text, count=1, flags=re.M)
    out.append('\n' + text.strip() + '\n')

out.append('\n---\n\n# 부록 B. 스크립트와 데이터 틀\n\n아래 파일을 **이름 그대로** 한 폴더에 저장해 쓴다(`render_html.js`는 같은 폴더의 `base.css`를 읽는다). Word 출력에는 `npm install docx`, PDF 출력에는 Playwright가 필요하다.\n')
lang = {'.py': 'python', '.js': 'js', '.css': 'css', '.json': 'json'}
for name in ['read_inputs.py', 'crop_pdf.py', 'compare.py', 'render_html.js', 'base.css', 'to_pdf.py', 'render_docx.js', 'fill_check.py']:
    p = ROOT / 'scripts' / name
    out.append(f'\n### 파일: {name}\n\n```{lang[p.suffix]}\n{p.read_text(encoding="utf-8").rstrip()}\n```\n')
p = ROOT / 'assets' / 'content_template.json'
out.append(f'\n### 파일: content.json (빈 틀)\n\n```json\n{p.read_text(encoding="utf-8").rstrip()}\n```\n')

dist = ROOT / 'dist'
dist.mkdir(exist_ok=True)
(dist / 'SKILL_single_file.md').write_text(''.join(out), encoding='utf-8')
print('dist/SKILL_single_file.md', len(''.join(out)), 'chars')
