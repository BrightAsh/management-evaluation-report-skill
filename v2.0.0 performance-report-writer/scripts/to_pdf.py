#!/usr/bin/env python3
# 사용법: python3 to_pdf.py 보고서.html  → 같은 이름 .pdf 생성 + 쪽별 내용 하단 위치(px) 출력
import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123})
    pg.goto(src.as_uri()); pg.wait_for_timeout(500)
    fill = pg.evaluate("""[...document.querySelectorAll('.page')].map(p=>{const r=p.getBoundingClientRect();let m=0;
      p.querySelectorAll('*').forEach(e=>{if(e.classList.contains('footer'))return;const v=e.getBoundingClientRect().bottom-r.top;if(v>m)m=v});return Math.round(m)})""")
    print('쪽별 내용 하단(px):', fill, '/ 한계 약 1075px (넘으면 바닥글 침범)')
    pg.pdf(path=str(src.with_suffix('.pdf')), format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
