#!/usr/bin/env python3
"""PDF 쪽에서 그래프·표·사진 영역을 잘라 그림 파일로 만든다 (벡터로 그려져 그림 추출이 안 될 때).

1) 위치 찾기:  python3 crop_pdf.py 자료.pdf 3 --grid [출력폴더]
   → 3쪽 위에 10% 눈금을 그린 이미지(page3_grid.png). 눈금을 보고 영역의 비율 좌표를 정한다.
2) 자르기:     python3 crop_pdf.py 자료.pdf 3 0.12 0.40 0.58 0.71 [출력.png] [--dpi 200]
   → 왼쪽 위(x0,y0)~오른쪽 아래(x1,y1)를 쪽 크기 대비 비율(0~1)로 준다.
   잘린 결과를 반드시 열어 보고, 글자가 잘리거나 다른 내용이 섞이면 좌표를 고쳐 다시 자른다.
"""
import sys, os, subprocess, tempfile, glob
from PIL import Image, ImageDraw


def render(pdf, page, dpi):
    d = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page), '-l', str(page), '-png', pdf, os.path.join(d, 'p')], check=True)
    return Image.open(glob.glob(os.path.join(d, 'p*.png'))[0]).convert('RGB')


def main():
    a = sys.argv[1:]
    dpi = 200
    if '--dpi' in a:
        i = a.index('--dpi'); dpi = int(a[i + 1]); del a[i:i + 2]
    if len(a) < 3:
        print(__doc__); sys.exit(1)
    pdf, page = a[0], int(a[1])
    if a[2] == '--grid':
        out_dir = a[3] if len(a) > 3 else '.'
        im = render(pdf, page, 100); dr = ImageDraw.Draw(im); w, h = im.size
        for k in range(1, 10):
            x, y = w * k // 10, h * k // 10
            dr.line([(x, 0), (x, h)], fill=(230, 60, 60), width=1); dr.line([(0, y), (w, y)], fill=(230, 60, 60), width=1)
            dr.text((x + 2, 2), f'.{k}', fill=(230, 60, 60)); dr.text((2, y + 2), f'.{k}', fill=(230, 60, 60))
        out = os.path.join(out_dir, f'page{page}_grid.png'); im.save(out); print('눈금 이미지:', out)
        return
    x0, y0, x1, y1 = map(float, a[2:6])
    out = a[6] if len(a) > 6 else f'crop_p{page}.png'
    im = render(pdf, page, dpi); w, h = im.size
    im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))).save(out)
    print('잘라낸 그림:', out, f'({int((x1 - x0) * w)}x{int((y1 - y0) * h)}px)')


if __name__ == '__main__':
    main()
