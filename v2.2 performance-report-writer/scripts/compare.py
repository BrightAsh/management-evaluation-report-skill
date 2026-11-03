#!/usr/bin/env python3
"""비교 값(전년 대비·도입 전후·목표 대비)을 계산하고 보고서 표기로 만들어 준다. 암산하지 말고 이것으로 계산한다.

하나:  python3 compare.py 140 462 명                 → 140명 → 462명 (230%↑, 3.3배)
       python3 compare.py 18 71 %                    → 18% → 71% (53%p↑)
       python3 compare.py 140 462 명 --years 24 25   → '24년 140명 → '25년 462명 (230%↑, 3.3배)
여럿:  python3 compare.py --csv 비교후보.csv
       CSV 열: 항목,이전값,이후값,단위[,이전시점,이후시점[,출처]]  (첫 줄은 머리글)

경고(⚠)가 붙은 비교는 그대로 쓰지 말고 표현을 바꾸거나 뺀다.
"""
import sys, csv


def num(s):
    return float(str(s).replace(',', '').strip())


def fmt(v):
    if abs(v - round(v)) < 1e-9:
        return f'{int(round(v)):,}'
    return f'{v:,.1f}' if abs(v) >= 10 else f'{v:,.2f}'.rstrip('0').rstrip('.')


def rate_txt(r):
    return f'{round(r):,}' if abs(r) >= 10 else f'{r:.1f}'.rstrip('0').rstrip('.')


def compare(a, b, unit='', ya=None, yb=None):
    pa = f"'{ya}년 " if ya else ''
    pb = f"'{yb}년 " if yb else ''
    left, right = f'{pa}{fmt(a)}{unit}', f'{pb}{fmt(b)}{unit}'
    warns, parts = [], []
    arrow = lambda d: '↑' if d > 0 else '↓' if d < 0 else ''
    if unit in ('%', '%p'):            # 비율끼리는 %p(차이)로 쓴다
        d = b - a
        parts.append(f'{rate_txt(abs(d))}%p{arrow(d)}')
        if abs(d) < 1:
            warns.append('변화 폭이 1%p 미만 → 강조용으로 쓰지 않는다')
    elif unit == '점':                 # 점수는 점 차이로 쓴다
        d = b - a
        parts.append(f'{rate_txt(abs(d))}점{arrow(d)}')
        if abs(d) < 1:
            warns.append('변화 폭이 1점 미만 → 강조용으로 쓰지 않는다')
    elif a == 0:
        warns.append('기준값 0 → 증감률 계산 불가. "신규 N" 또는 실수치로 쓴다')
    else:
        r = (b - a) / abs(a) * 100
        parts.append(f"{rate_txt(abs(r))}%{'↑' if r > 0 else '↓' if r < 0 else ''}")
        if a > 0 and b > 0 and b / a >= 2:
            parts.append(f'{b / a:.1f}배'.replace('.0배', '배'))
        if abs(a) < 10 and abs(r) >= 200:
            warns.append('기준값이 작아 증감률이 과장돼 보임 → 실수치(전→후)나 배수로 쓴다')
        if abs(r) < 3:
            warns.append('변화 폭이 작다(3% 미만) → 강조용으로 쓰지 않는다')
    text =f"{left} → {right}" + (f" ({', '.join(parts)})" if parts else '')
    return text, warns


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == '--csv':
        rows = list(csv.reader(open(a[1], encoding='utf-8-sig')))[1:]
        print('| 항목 | 비교 표기 | 경고 | 출처 |\n|---|---|---|---|')
        for r in rows:
            if not r or not r[0].strip():
                continue
            r += [''] * (7 - len(r))
            try:
                t, w = compare(num(r[1]), num(r[2]), r[3].strip(), r[4].strip() or None, r[5].strip() or None)
            except ValueError:
                t, w = '(숫자가 아님)', ['값 확인 필요']
            print(f"| {r[0]} | {t} | {'⚠ ' + ' / '.join(w) if w else ''} | {r[6]} |")
        return
    ya = yb = None
    if '--years' in a:
        i = a.index('--years'); ya, yb = a[i + 1], a[i + 2]; del a[i:i + 3]
    t, w = compare(num(a[0]), num(a[1]), a[2] if len(a) > 2 else '', ya, yb)
    print(t)
    for x in w:
        print('⚠', x)


if __name__ == '__main__':
    main()
