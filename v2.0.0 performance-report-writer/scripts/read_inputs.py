#!/usr/bin/env python3
"""첨부 파일을 한 번에 텍스트로 뽑고, 역할 판별을 돕는 목록(_inventory.md)을 만든다.

사용법:  python3 -I read_inputs.py <출력폴더> <파일1> [파일2 ...]
지원:    PDF, HWP(5.0), HWPX, DOCX, PPTX, XLSX/XLSM, CSV, TXT, MD, 이미지(PNG/JPG)
결과:    <출력폴더>/<파일명>.txt  — 본문 텍스트(PDF는 쪽 구분 '=== p.N ===')
         <출력폴더>/preview/      — PDF 앞 2쪽 이미지, HWPX 미리보기 이미지(양식 판별용)
         <출력폴더>/_inventory.md — 파일별 분량·첫 줄·역할 추정 점수
필요 시:  pip install olefile openpyxl   (HWP, XLSX를 읽을 때만)
"""
import sys, os, re, zipfile, shutil, subprocess, zlib, struct
import xml.etree.ElementTree as ET

ROLE_HINTS = {
    '성과지표': ['세부평가내용', '평가방법', '가중치', '배점', '평가지표', '지표정의', '평가기준', '착안사항', '등급 평가', '지적사항'],
    '가이드라인': ['작성요령', '작성 요령', '유의사항', '작성지침', '작성 지침', '분량', '글자 크기', '쪽 이내', '페이지 이내', '제출 기한'],
    '양식': ['예시', '샘플', '작성 예', '(예)', 'BEST PRACTICE', '추진배경', '추진성과'],
    '작성 자료': ['결과보고', '계획(안)', '추진계획', '실적', '보도자료', '결재', '회의', '현황', '성과'],
}


def squeeze(text):
    lines = [re.sub(r'[ \t　]+', ' ', l).strip() for l in text.splitlines()]
    return '\n'.join(l for l in lines if l)


def local(tag):
    return tag.rsplit('}', 1)[-1]


# ---------- 형식별 추출 ----------
def read_pdf(path):
    raw = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, check=True).stdout
    pages = raw.split('\f')
    if pages and not pages[-1].strip():   # pdftotext는 마지막 쪽 뒤에도 \f를 붙인다
        pages = pages[:-1]
    out = [f'=== p.{i + 1} ===\n' + squeeze(p) for i, p in enumerate(pages) if p.strip()]
    return '\n'.join(out), f'{len(pages)}쪽'


def xml_blocks(root, para='p', table='tbl', row='tr', cell='tc', text='t'):
    """문단·표 순서를 지키며 텍스트를 뽑는다(HWPX·DOCX 공통).
    HWPX는 표가 문단 안(run 안)에 들어 있고, DOCX는 문단과 나란히 있다. 둘 다 처리한다."""
    parent = {c: p for p in root.iter() for c in p}
    in_tbl = set()
    for el in root.iter():
        if local(el.tag) == table:
            in_tbl.update(d for d in el.iter() if d is not el)

    def paragraph_text(p):
        return ''.join(t.text or '' for t in p.iter() if local(t.tag) == text and t not in in_tbl).strip()

    def table_rows(tbl):
        rows = []
        for tr in tbl:
            if local(tr.tag) != row:
                continue
            cells = []
            for tc in tr:
                if local(tc.tag) != cell:
                    continue
                parts = [''.join(t.text or '' for t in p.iter() if local(t.tag) == text).strip()
                         for p in tc.iter() if local(p.tag) == para]
                cells.append(' '.join(x for x in parts if x))
            if any(cells):
                rows.append('| ' + ' | '.join(cells) + ' |')
        return rows

    def top_tables(p):  # 이 문단 안에서 다른 표에 속하지 않은 표
        out = []
        for d in p.iter():
            if d is p or local(d.tag) != table:
                continue
            q, nested = parent.get(d), False
            while q is not None and q is not p:
                if local(q.tag) == table:
                    nested = True
                    break
                q = parent.get(q)
            if not nested:
                out.append(d)
        return out

    lines = []

    def walk(el):
        name = local(el.tag)
        if name == table:
            lines.extend(table_rows(el))
            return
        if name == para:
            t = paragraph_text(el)
            if t:
                lines.append(t)
            for tb in top_tables(el):
                lines.extend(table_rows(tb))
            return
        for ch in el:
            walk(ch)

    walk(root)
    return lines


def read_hwpx(path, prev_dir):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        secs = sorted([n for n in names if re.match(r'Contents/section\d+\.xml', n)],
                      key=lambda n: int(re.findall(r'\d+', n)[-1]))
        lines = []
        for s in secs:
            lines += xml_blocks(ET.fromstring(z.read(s)))
        for n in names:
            if n.lower().startswith('preview/') and n.lower().endswith(('.png', '.jpg', '.jpeg')):
                os.makedirs(prev_dir, exist_ok=True)
                dst = os.path.join(prev_dir, os.path.basename(path) + '_' + os.path.basename(n))
                with open(dst, 'wb') as f:
                    f.write(z.read(n))
    return '\n'.join(lines), f'{len(secs)}개 구역'


def hwp_para_text(buf):
    """HWP PARA_TEXT: 제어문자 0,10,13,24~31은 1칸, 그 밖의 제어문자(1~31)는 8칸(16바이트)을 차지한다."""
    units = struct.unpack('<%dH' % (len(buf) // 2), buf[:len(buf) // 2 * 2])
    out, i = [], 0
    while i < len(units):
        c = units[i]
        if c < 32:
            if c in (10, 13):
                out.append('\n')
            i += 1 if c in (0, 10, 13) or c >= 24 else 8
            continue
        out.append(chr(c))
        i += 1
    return ''.join(out)


def read_hwp(path):
    try:
        import olefile
    except ImportError:
        return '[HWP를 읽으려면 pip install olefile 이 필요합니다]', '-'
    f = olefile.OleFileIO(path)
    compressed = f.openstream('FileHeader').read()[36] & 1
    secs = sorted([s for s in f.listdir() if s[0] == 'BodyText'], key=lambda x: int(x[1][7:]))
    out = []
    for s in secs:
        d = f.openstream(s).read()
        if compressed:
            d = zlib.decompress(d, -15)
        i = 0
        while i < len(d):
            h = struct.unpack('<I', d[i:i + 4])[0]
            tag, size = h & 0x3ff, (h >> 20) & 0xfff
            i += 4
            if size == 0xfff:
                size = struct.unpack('<I', d[i:i + 4])[0]
                i += 4
            if tag == 67:  # PARA_TEXT
                t = hwp_para_text(d[i:i + size])
                if t.strip():
                    out.append(t.strip())
            i += size
    return '\n'.join(out), f'{len(secs)}개 구역'


def read_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    return '\n'.join(xml_blocks(root)), '-'


def read_pptx(path):
    with zipfile.ZipFile(path) as z:
        slides = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml', n)],
                        key=lambda n: int(re.findall(r'\d+', n)[-1]))
        out = []
        for i, s in enumerate(slides, 1):
            root = ET.fromstring(z.read(s))
            paras = [''.join(t.text or '' for t in p.iter() if local(t.tag) == 't') for p in root.iter() if local(p.tag) == 'p']
            out.append(f'=== slide {i} ===\n' + '\n'.join(p for p in paras if p.strip()))
    return '\n'.join(out), f'{len(slides)}장'


def read_xlsx(path):
    try:
        import openpyxl
    except ImportError:
        return '[엑셀을 읽으려면 pip install openpyxl 이 필요합니다]', '-'
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f'=== sheet: {ws.title} ===')
        for row in ws.iter_rows(values_only=True):
            if any(c is not None for c in row):
                out.append(' | '.join('' if c is None else str(c).replace('\n', ' / ') for c in row))
    return '\n'.join(out), f'{len(wb.worksheets)}개 시트'


def pdf_preview(path, prev_dir):
    if shutil.which('pdftoppm'):
        os.makedirs(prev_dir, exist_ok=True)
        stem = os.path.join(prev_dir, os.path.basename(path))
        subprocess.run(['pdftoppm', '-r', '60', '-f', '1', '-l', '2', '-png', path, stem], capture_output=True)


def role_scores(text):
    return {r: sum(text.count(k) for k in kws) for r, kws in ROLE_HINTS.items()}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    out_dir, files = sys.argv[1], sys.argv[2:]
    os.makedirs(out_dir, exist_ok=True)
    prev_dir = os.path.join(out_dir, 'preview')
    rows = []
    for p in files:
        ext = os.path.splitext(p)[1].lower()
        name = os.path.basename(p)
        try:
            if ext == '.pdf':
                text, size = read_pdf(p)
                pdf_preview(p, prev_dir)
            elif ext == '.hwpx':
                text, size = read_hwpx(p, prev_dir)
            elif ext == '.hwp':
                text, size = read_hwp(p)
            elif ext == '.docx':
                text, size = read_docx(p)
            elif ext == '.pptx':
                text, size = read_pptx(p)
            elif ext in ('.xlsx', '.xlsm'):
                text, size = read_xlsx(p)
            elif ext in ('.csv', '.txt', '.md'):
                text, size = open(p, encoding='utf-8', errors='ignore').read(), '-'
            elif ext in ('.png', '.jpg', '.jpeg', '.gif', '.webp'):
                text, size = '[이미지 파일 — 직접 보고 판단할 것]', '이미지'
            else:
                text, size = f'[지원하지 않는 형식: {ext}]', '-'
        except Exception as e:  # 한 파일이 실패해도 나머지는 계속
            text, size = f'[읽기 실패: {e}]', '-'
        with open(os.path.join(out_dir, name + '.txt'), 'w', encoding='utf-8') as f:
            f.write(text)
        first = [l for l in text.splitlines() if l.strip() and not l.startswith('===')][:3]
        sc = role_scores(text)
        guess = max(sc, key=sc.get) if max(sc.values()) else '판별 필요'
        rows.append((name, ext[1:].upper(), size, len(text), ' / '.join(first)[:120], guess, sc))
        print(f'[ok] {name}: {size}, {len(text):,}자 → {name}.txt')

    with open(os.path.join(out_dir, '_inventory.md'), 'w', encoding='utf-8') as f:
        f.write('# 첨부 목록 (자동 추출)\n\n역할 추정은 키워드 빈도일 뿐이다. 반드시 내용과 미리보기 이미지를 보고 최종 판별한다.\n\n')
        f.write('| 파일 | 형식 | 분량 | 글자 수 | 첫 줄 | 역할 추정 | 키워드 점수 |\n|---|---|---|---|---|---|---|\n')
        for n, e, s, c, fl, g, sc in rows:
            scs = ', '.join(f'{k} {v}' for k, v in sc.items() if v)
            f.write(f'| {n} | {e} | {s} | {c:,} | {fl.replace("|", "/")} | {g} | {scs} |\n')
    print('목록:', os.path.join(out_dir, '_inventory.md'))


if __name__ == '__main__':
    main()
