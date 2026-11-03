#!/usr/bin/env python3
"""첨부 파일을 한 번에 텍스트로 뽑고, 그림을 따로 모으고, 역할 판별을 돕는 목록을 만든다.

사용법:  python3 -I read_inputs.py <출력폴더> <파일1> [파일2 ...] [--no-images]
지원:    PDF, HWP(5.0), HWPX, DOCX, PPTX, XLSX/XLSM, CSV, TXT, MD, 이미지(PNG/JPG)
결과:    <출력폴더>/<파일명>.txt   — 본문 텍스트(PDF는 쪽 구분 '=== p.N ===')
         <출력폴더>/preview/       — PDF 앞 2쪽 이미지, HWPX 미리보기 이미지(양식 판별용)
         <출력폴더>/images/        — 원자료 속 그림(사진·그래프·화면). 아이콘·선 조각·중복은 거른다
         <출력폴더>/images/_sheet_N.png — 그림 미리보기 모음(번호 붙음). 이것부터 보고 고른다
         <출력폴더>/pages/         — PDF 쪽 미리보기 모음(벡터 그래프·표를 찾아 crop_pdf.py로 자를 때)
         <출력폴더>/_images.md     — 그림 목록(번호·원본·쪽·크기·경로)
         <출력폴더>/_inventory.md  — 파일별 분량·첫 줄·역할 추정 점수
필요 시:  pip install olefile openpyxl pillow   (HWP, XLSX, 그림 처리를 할 때만)
"""
import sys, os, re, zipfile, shutil, subprocess, zlib, struct, hashlib, tempfile
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


# ---------- 그림 추출 ----------
MIN_SIDE = 150      # px. 이보다 작으면 아이콘·글머리표·선 조각으로 보고 버린다
MAX_ASPECT = 6.0    # 가로세로 비가 이보다 크면 띠·밑줄 조각으로 보고 버린다
MEDIA_DIRS = ('word/media/', 'ppt/media/', 'xl/media/', 'bindata/')


def sniff(b):
    if b[:4] == b'\x89PNG': return 'png'
    if b[:2] == b'\xff\xd8': return 'jpg'
    if b[:4] == b'GIF8': return 'gif'
    if b[:2] == b'BM': return 'bmp'
    if b[40:44] == b' EMF': return 'emf'
    if b[:4] in (b'\xd7\xcd\xc6\x9a', b'\x01\x00\x09\x00'): return 'wmf'
    return None


class Images:
    """그림을 모아 번호를 붙인다. 중복(같은 내용)·작은 조각은 거른다."""
    def __init__(self, out_dir):
        self.dir = os.path.join(out_dir, 'images'); self.items = []; self.seen = set(); self.skipped = 0
        os.makedirs(self.dir, exist_ok=True)

    def add(self, data, src, where):
        ext = sniff(data)
        if not ext:
            return
        h = hashlib.md5(data).hexdigest()
        if h in self.seen:
            return
        self.seen.add(h)
        if ext in ('emf', 'wmf'):   # 벡터 그림: LibreOffice가 있으면 PNG로 바꾼다
            data, ext = self._vector_to_png(data, ext)
            if data is None:
                return
        try:
            from PIL import Image
            import io
            im = Image.open(io.BytesIO(data)); w, hgt = im.size
        except Exception:
            return
        if min(w, hgt) < MIN_SIDE or max(w, hgt) / max(1, min(w, hgt)) > MAX_ASPECT:
            self.skipped += 1
            return
        try:   # 단색 바탕·빗금 무늬(명암 차이가 거의 없는 그림)는 버린다
            from PIL import ImageStat
            small = im.convert('L').resize((64, 64))
            if ImageStat.Stat(small).stddev[0] < 8 or len(set(small.point(lambda v: v // 16).tobytes())) <= 3:
                self.skipped += 1
                return
        except Exception:
            pass
        if ext == 'bmp' or ext == 'gif':
            im = im.convert('RGB'); buf = io.BytesIO(); im.save(buf, 'PNG'); data, ext = buf.getvalue(), 'png'
        n = len(self.items) + 1
        path = os.path.join(self.dir, f'I{n:02d}.{ext}')
        with open(path, 'wb') as f:
            f.write(data)
        self.items.append({'id': f'I{n:02d}', 'src': src, 'where': where, 'w': w, 'h': hgt, 'path': path})

    def _vector_to_png(self, data, ext):
        if not shutil.which('soffice'):
            return None, None
        d = tempfile.mkdtemp(); f = os.path.join(d, 'v.' + ext)
        open(f, 'wb').write(data)
        subprocess.run(['soffice', '--headless', '--convert-to', 'png', '--outdir', d, f], capture_output=True, timeout=90)
        g = os.path.join(d, 'v.png')
        return (open(g, 'rb').read(), 'png') if os.path.exists(g) else (None, None)

    def from_zip(self, path):
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if n.lower().startswith(MEDIA_DIRS):
                    self.add(z.read(n), os.path.basename(path), n.split('/')[-1])

    def from_hwp(self, path):
        import olefile
        f = olefile.OleFileIO(path)
        for s in f.listdir():
            if s[0] == 'BinData':
                d = f.openstream(s).read()
                for cand in (d, None):
                    if cand is None:
                        try: cand = zlib.decompress(d, -15)
                        except Exception: break
                    if sniff(cand):
                        self.add(cand, os.path.basename(path), s[-1]); break

    def from_pdf(self, path):
        if not shutil.which('pdfimages'):
            return
        lst = subprocess.run(['pdfimages', '-list', path], capture_output=True, text=True).stdout.splitlines()[2:]
        kind = {}
        for l in lst:
            c = l.split()
            if len(c) > 3: kind[int(c[1])] = (int(c[0]), c[2])   # num → (page, type)
        d = tempfile.mkdtemp()
        subprocess.run(['pdfimages', '-png', path, os.path.join(d, 'x')], capture_output=True)
        for fn in sorted(os.listdir(d)):
            m = re.match(r'x-(\d+)\.png$', fn)
            if not m: continue
            num = int(m.group(1)); page, typ = kind.get(num, (0, 'image'))
            if typ != 'image': continue                     # smask·stencil(투명도 마스크) 제외
            self.add(open(os.path.join(d, fn), 'rb').read(), os.path.basename(path), f'p.{page}')

    def from_file(self, path):
        self.add(open(path, 'rb').read(), os.path.basename(path), '파일 자체')

    def sheets(self):
        """번호 붙인 미리보기 모음(한 장에 20개)."""
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            return []
        out, tw, th, cols = [], 260, 200, 4
        for k in range(0, len(self.items), 20):
            chunk = self.items[k:k + 20]; rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new('RGB', (cols * tw, rows * (th + 22)), 'white'); dr = ImageDraw.Draw(sheet)
            for j, it in enumerate(chunk):
                x, y = (j % cols) * tw, (j // cols) * (th + 22)
                try:
                    im = Image.open(it['path']).convert('RGB'); im.thumbnail((tw - 10, th - 10))
                    sheet.paste(im, (x + (tw - im.width) // 2, y + 22 + (th - im.height) // 2))
                except Exception:
                    pass
                dr.rectangle([x, y, x + tw - 1, y + th + 21], outline=(180, 180, 180))
                dr.text((x + 6, y + 5), f"{it['id']}  {it['w']}x{it['h']}", fill=(0, 0, 0))
            p = os.path.join(self.dir, f'_sheet_{k // 20 + 1}.png'); sheet.save(p); out.append(p)
        return out


def pdf_page_sheets(path, out_dir):
    """PDF 전 쪽 미리보기 모음(한 장에 12쪽). 벡터로 그린 그래프·표를 찾을 때 본다."""
    if not shutil.which('pdftoppm'):
        return []
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return []
    d = tempfile.mkdtemp(); subprocess.run(['pdftoppm', '-r', '30', '-png', path, os.path.join(d, 'p')], capture_output=True)
    files = sorted(os.listdir(d), key=lambda f: int(re.findall(r'\d+', f)[-1]))
    pdir = os.path.join(out_dir, 'pages'); os.makedirs(pdir, exist_ok=True); out = []
    stem = re.sub(r'[^\w가-힣]+', '_', os.path.splitext(os.path.basename(path))[0])[:40]
    for k in range(0, len(files), 12):
        chunk = files[k:k + 12]; ims = [Image.open(os.path.join(d, f)).convert('RGB') for f in chunk]
        tw, th = max(i.width for i in ims), max(i.height for i in ims)
        sheet = Image.new('RGB', (4 * tw, ((len(ims) + 3) // 4) * (th + 16)), 'white'); dr = ImageDraw.Draw(sheet)
        for j, im in enumerate(ims):
            x, y = (j % 4) * tw, (j // 4) * (th + 16)
            sheet.paste(im, (x, y + 16)); dr.text((x + 4, y + 2), f'p.{k + j + 1}', fill=(0, 0, 0))
        p = os.path.join(pdir, f'{stem}_{k // 12 + 1}.png'); sheet.save(p); out.append(p)
    return out


def role_scores(text):
    return {r: sum(text.count(k) for k in kws) for r, kws in ROLE_HINTS.items()}


def main():
    args = [a for a in sys.argv[1:] if a != '--no-images']
    want_img = '--no-images' not in sys.argv
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    out_dir, files = args[0], args[1:]
    os.makedirs(out_dir, exist_ok=True)
    prev_dir = os.path.join(out_dir, 'preview')
    imgs = Images(out_dir) if want_img else None
    page_sheets = []
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
        if imgs is not None:
            try:
                before = len(imgs.items)
                if ext == '.pdf':
                    imgs.from_pdf(p); page_sheets += pdf_page_sheets(p, out_dir)
                elif ext in ('.docx', '.pptx', '.xlsx', '.xlsm', '.hwpx'):
                    imgs.from_zip(p)
                elif ext == '.hwp':
                    imgs.from_hwp(p)
                elif ext in ('.png', '.jpg', '.jpeg', '.gif'):
                    imgs.from_file(p)
                size = f'{size}, 그림 {len(imgs.items) - before}개'
            except Exception as e:
                size = f'{size}, 그림 추출 실패({e})'
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

    if imgs is not None:
        sheets = imgs.sheets()
        with open(os.path.join(out_dir, '_images.md'), 'w', encoding='utf-8') as f:
            f.write('# 원자료 그림 목록 (자동 추출)\n\n')
            f.write(f'작은 조각·띠·중복 {imgs.skipped}개는 걸렀다. 미리보기 모음을 먼저 보고, 보고서에 쓸 후보만 원본 크기로 확인한다.\n')
            f.write('PDF 안의 그래프·표가 벡터로 그려진 경우 이 목록에 없다 → pages/ 미리보기에서 찾아 crop_pdf.py로 자른다.\n\n')
            f.write('미리보기 모음: ' + (', '.join(os.path.relpath(x, out_dir) for x in sheets) or '없음') + '\n')
            f.write('PDF 쪽 모음: ' + (', '.join(os.path.relpath(x, out_dir) for x in page_sheets) or '없음') + '\n\n')
            f.write('| 번호 | 원본 파일 | 위치 | 크기(px) | 파일 |\n|---|---|---|---|---|\n')
            for it in imgs.items:
                f.write(f"| {it['id']} | {it['src']} | {it['where']} | {it['w']}x{it['h']} | {os.path.relpath(it['path'], out_dir)} |\n")
        print(f'그림: {len(imgs.items)}개 (걸러낸 조각 {imgs.skipped}개) → _images.md')


if __name__ == '__main__':
    main()
