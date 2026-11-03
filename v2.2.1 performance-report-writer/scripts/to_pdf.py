#!/usr/bin/env python3
# 사용법: python3 to_pdf.py 보고서.html  → 같은 이름 .pdf 생성 + 쪽별 내용 하단 위치(px) 출력
import os, pathlib, shutil, sys
from playwright.sync_api import sync_playwright


def launch_chromium(playwright):
    """Use Playwright Chromium, then a system browser if its bundle is absent."""
    try:
        return playwright.chromium.launch()
    except Exception as first_error:
        candidates = [
            os.environ.get('CHROMIUM_PATH'),
            shutil.which('chromium'), shutil.which('chromium-browser'),
            shutil.which('google-chrome'), shutil.which('msedge'),
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        ]
        for executable in candidates:
            if executable and pathlib.Path(executable).is_file():
                return playwright.chromium.launch(executable_path=executable)
        raise first_error


src = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = launch_chromium(p); pg = b.new_page(viewport={'width': 794, 'height': 1123})
    pg.goto(src.as_uri()); pg.wait_for_timeout(500)
    fill = pg.evaluate("""[...document.querySelectorAll('.page')].map(p=>{const r=p.getBoundingClientRect();let m=0;
      p.querySelectorAll('*').forEach(e=>{if(e.closest('.footer,.pf,.ph,.stab'))return;const v=e.getBoundingClientRect().bottom-r.top;if(v>m)m=v});return Math.round(m)})""")
    print('쪽별 내용 하단(px):', fill, '/ 알맞음 약 960~1,055 · 한계 1,065px (넘으면 잘림·바닥글 침범)')
    pg.pdf(path=str(src.with_suffix('.pdf')), format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
