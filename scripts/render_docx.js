#!/usr/bin/env node
// 내용 데이터(content.json) → Word(.docx). 표 기반으로 박스·흐름도를 그린다.
// 사용법: node render_docx.js content.json report.docx [글자배율=1.17] [간격배율=1.65]
//   지면이 넘치면 배율을 낮추고(1.13/1.5), 남으면 내용을 더 넣는다(배율로 메우지 않는다).
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, VerticalAlign, Header, Footer, TableLayoutType, ImageRun, HeightRule } = require('docx');

const src = path.resolve(process.argv[2] || 'content.json');
const OUT = process.argv[3] || 'report.docx';
const F = parseFloat(process.argv[4] || '1.17');
const SP = parseFloat(process.argv[5] || '1.65');
const baseDir = path.dirname(src);
const CT = src.endsWith('.json') ? JSON.parse(fs.readFileSync(src, 'utf8')) : require(src);

// ---- 설정
const cc = CT.config || {};
const hex = v => String(v).replace('#', '').toUpperCase();
const TH = { ink: '#222222', g1: '#F2F2F2', g2: '#DADADA', g3: '#A3A3A3', g4: '#5A5A5A', ...(cc.theme || {}) };
const INK = hex(TH.ink), G1 = hex(TH.g1), G2 = hex(TH.g2), G3 = hex(TH.g3), G4 = hex(TH.g4);
const FN = { docx_sans: '맑은 고딕', docx_serif: '바탕', ...(cc.fonts || {}) };
const LB = { result: '추진성과', key: '핵심성과', best: ['BEST', 'PRACTICE'], ...(cc.labels || {}) };
const LAY = cc.layout || null;
const font = n => ({ ascii: n, eastAsia: n, hAnsi: n });
const SANS = font(FN.docx_sans), SERIF = font(FN.docx_serif);

const mm = x => Math.round(x * 56.7);
const W = mm(172);
const SZ = 17;
const AL = AlignmentType;

function runs(text, o = {}) {
  const out = [], sz = Math.round((o.size || SZ) * F), tsz = Math.round(((o.size || SZ) - 3) * F);
  String(text ?? '').split(/(\*\*[^*]+\*\*|__[^_]+__|\[\[[^\]]+\]\]|\{\{[^}]+\}\})/g).filter(Boolean).forEach(t => {
    const base = { font: o.font || SERIF, size: sz, bold: o.bold, color: o.color };
    if (t.startsWith('**')) out.push(new TextRun({ ...base, text: t.slice(2, -2), bold: true }));
    else if (t.startsWith('__')) out.push(new TextRun({ ...base, text: t.slice(2, -2), bold: true, underline: {} }));
    else if (t.startsWith('[[')) out.push(new TextRun({ ...base, font: SANS, size: tsz, bold: true, color: INK, text: ` ${t.slice(2, -2)} `, border: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 0 } }), new TextRun({ ...base, text: ' ' }));
    else if (t.startsWith('{{')) out.push(new TextRun({ ...base, font: SANS, size: tsz, bold: true, color: 'FFFFFF', text: ` ${t.slice(2, -2)} `, shading: { type: ShadingType.CLEAR, fill: G4, color: 'auto' } }), new TextRun({ ...base, text: ' ' }));
    else out.push(new TextRun({ ...base, text: t }));
  });
  return out;
}
const P = (text, o = {}) => new Paragraph({ children: runs(text, o), alignment: o.align,
  spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 264 },
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
  indent: o.left !== undefined ? { left: o.left, hanging: o.hanging || 0 } : (o.hang ? { left: o.hang, hanging: o.hang } : (o.first ? { firstLine: o.first } : undefined)) });
// 목록: "- " 하위, "* " 각주, "※ " 참고, "= " 기호 없음
const B = (t, o = {}) => { const s = String(t);
  if (s.startsWith('- ')) return P('– ' + s.slice(2), { left: 300, hanging: 150, ...o });
  if (s.startsWith('* ')) return P('* ' + s.slice(2), { left: 260, hanging: 110, ...o, size: (o.size || SZ) - 3, color: '444444' });
  if (s.startsWith('※')) return P('※ ' + s.replace(/^※\s*/, ''), { left: 200, hanging: 200, ...o, size: (o.size || SZ) - 2 });
  if (s.startsWith('= ')) return P(s.slice(2), o);
  return P('· ' + s, { hang: 150, ...o }); };
const Bs = (a, o) => (a || []).map(t => B(t, o));
const H = (t, o = {}) => P(t, { font: SANS, bold: true, size: 17, align: AL.CENTER, ...o });

const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const ln = (c = G3, s = 4) => ({ style: BorderStyle.SINGLE, size: s, color: c });
const bAll = b => ({ top: b, bottom: b, left: b, right: b });
const NOB = bAll(NONE);
function C(children, w, o = {}) {
  return new TableCell({ children: Array.isArray(children) ? (children.length ? children : [P('')]) : [children], width: { size: w, type: WidthType.DXA },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    borders: o.borders || bAll(ln()), verticalAlign: o.v || VerticalAlign.CENTER, columnSpan: o.span, rowSpan: o.rowSpan,
    margins: { top: Math.round((o.mt ?? 45) * SP), bottom: Math.round((o.mb ?? 45) * SP), left: o.ml ?? 90, right: o.mr ?? 90 } });
}
function T(rows, widths, heights) {
  return new Table({ rows: rows.map((r, i) => new TableRow({ children: r, cantSplit: true,
      height: heights && heights[i] ? { value: heights[i], rule: HeightRule.EXACT } : undefined })), columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, layout: TableLayoutType.FIXED,
    borders: { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE } });
}
const gap = (h = 70) => new Paragraph({ spacing: { before: 0, after: 0, line: Math.max(20, Math.round(h * SP)), lineRule: 'exact' }, children: [new TextRun({ text: '', size: 2 })] });
const split = (total, ws, gapW, n) => { const s = ws.reduce((a, b) => a + b, 0), avail = total - gapW * (n - 1);
  const cw = ws.map(x => Math.round(avail * x / s)); cw[n - 1] = avail - cw.slice(0, -1).reduce((a, b) => a + b, 0); return cw; };
const KW = mm(20);
const push = (arr, r) => (Array.isArray(r) ? arr.push(...r) : arr.push(r));
const blocks = (list, w) => { const kids = []; list.forEach((x, i) => { if (i) kids.push(gap(40)); push(kids, R[x.t](x, w)); }); return kids; };

// ---- 그림 크기(px)와 자리표시
function imgSize(buf) {
  if (buf[0] === 0x89 && buf[1] === 0x50) return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
  if (buf[0] === 0x47 && buf[1] === 0x49) return [buf.readUInt16LE(6), buf.readUInt16LE(8)];
  if (buf[0] === 0xFF && buf[1] === 0xD8) { let i = 2;
    while (i < buf.length) { if (buf[i] !== 0xFF) { i++; continue; } const m = buf[i + 1], L = buf.readUInt16BE(i + 2);
      if (m >= 0xC0 && m <= 0xCF && ![0xC4, 0xC8, 0xCC].includes(m)) return [buf.readUInt16BE(i + 7), buf.readUInt16BE(i + 5)];
      i += 2 + L; } }
  return [4, 3];
}
const px = v => Math.round(v * 96 / 25.4);           // mm → px(96dpi)
const dxa2mm = d => d / 56.7;
function picture(i, maxW) {   // maxW: DXA
  const maxMm = dxa2mm(maxW) - 1.5;
  if (i.src && !fs.existsSync(path.resolve(baseDir, i.src))) { console.warn('그림 파일 없음(자리표시로 그림):', i.src); i = { ...i, src: null, label: i.label || '그림 없음' }; }
  if (!i.src) {   // 가린 견본: 빗금 대신 회색 칸
    const wmm = Math.min(i.w_mm || maxMm, maxMm), hmm = i.h_mm || 20;
    return T([[C(P(i.label || '그림', { font: SANS, bold: true, size: 14, color: G4, align: AL.CENTER }), mm(wmm), { fill: G2, borders: NOB })]], [mm(wmm)], [mm(hmm)]);
  }
  const f = path.resolve(baseDir, i.src), buf = fs.readFileSync(f), [iw, ih] = imgSize(buf);
  let wmm = i.w_mm, hmm = i.h_mm;
  if (wmm && !hmm) hmm = wmm * ih / iw; else if (hmm && !wmm) wmm = hmm * iw / ih; else if (!wmm && !hmm) { wmm = Math.min(maxMm, 40); hmm = wmm * ih / iw; }
  if (wmm > maxMm) { hmm = hmm * maxMm / wmm; wmm = maxMm; }
  let ext = path.extname(f).slice(1).toLowerCase(); if (ext === 'jpeg') ext = 'jpg';
  return new Paragraph({ alignment: AL.CENTER, spacing: { before: 30, after: 10 },
    children: [new ImageRun({ type: ext, data: buf, transformation: { width: px(wmm), height: px(hmm) } })] });
}
const figure = (i, maxW) => { const out = [picture(i, maxW)];
  if (i.caption) out.push(P(i.caption, { font: SANS, size: 13, color: G4, align: AL.CENTER })); return out; };

// ---- 표 칸
const normCell = x => typeof x === 'string' ? { p: [x], c: true } : Array.isArray(x) ? { b: x } : (x || {});
function cellKids(c, w) {
  const kids = [];
  if (c.h) kids.push(P(c.h, { font: SANS, bold: true, size: 16, align: AL.CENTER, fill: G1, after: 40 }));
  const body = [];
  [].concat(c.p || []).forEach(x => body.push(c.c ? P(x, { font: SANS, bold: true, size: 17, align: AL.CENTER }) : P(x, { size: 16 })));
  body.push(...Bs(c.b, { size: 16 }));
  const imgs = [].concat(c.img || []), right = imgs.filter(i => i.pos === 'right'), below = imgs.filter(i => i.pos !== 'right');
  if (right.length) {
    const iw = mm(right[0].w_mm || 30) + 120, tw = w - iw - 180;
    kids.push(T([[C(body, tw, { borders: NOB, v: VerticalAlign.TOP, ml: 0, mr: 60, mt: 0, mb: 0 }),
      C(right.flatMap(i => figure(i, iw)), iw, { borders: NOB, v: VerticalAlign.TOP, ml: 0, mr: 0, mt: 0, mb: 0 })]], [tw, iw]));
  } else kids.push(...body);
  below.forEach(i => kids.push(...figure(i, w - 180)));
  return kids;
}

const R = {
  title: (b) => P(b.text, { font: SANS, bold: true, size: 29, align: AL.CENTER, after: 60 }),
  ev: (b, w) => T([[C(P(b.label, { font: SANS, bold: true, size: 20, align: AL.CENTER }), mm(28), { fill: G2, borders: bAll(ln(G3, 6)) }),
    C(P(b.text, { font: SANS, size: 18 }), w - mm(28), { borders: bAll(ln(G3, 6)), ml: 140 })]], [mm(28), w - mm(28)]),
  key: (b, w) => T([[C(P(b.label || LB.key, { font: SANS, bold: true, size: 19, color: 'FFFFFF', align: AL.CENTER }), mm(28), { fill: G4, borders: bAll(ln(G3, 6)) }),
    C(P('☑ ' + b.text, { font: SANS, bold: true, size: 18 }), w - mm(28), { borders: bAll(ln(G3, 6)), ml: 140 })]], [mm(28), w - mm(28)]),
  bp: (b, w) => { const lb = b.label || LB.best;
    return T([[C([P(lb[0], { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER, line: 220 }),
      P(lb[1] || '', { font: SANS, size: 11, color: 'FFFFFF', align: AL.CENTER, line: 200 })], mm(20), { fill: G4 }),
      C(b.items.map(t => P(t, { font: SANS, size: 18 })), w - mm(20), { ml: 140 })]], [mm(20), w - mm(20)]); },
  vision: (b, w) => T([[C(P(`[[${b.k}]] ${b.text}`, { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER }), w, { fill: G4, borders: NOB })]], [w]),
  sec: (b, w) => { const ws = [mm(9), w - mm(9) - (b.tag ? mm(20) : 0)]; if (b.tag) ws.push(mm(20));
    const tb = { top: NONE, bottom: ln(G3, 6), left: NONE, right: NONE };
    const r = [C(P(b.no, { font: SANS, bold: true, size: 23, color: 'FFFFFF', align: AL.CENTER }), ws[0], { fill: G4, borders: tb, ml: 0, mr: 0 }),
      C(P(b.title, { font: SANS, bold: true, size: 26 }), ws[1], { borders: tb, ml: 140 })];
    if (b.tag) r.push(C(P(`{{${b.tag}}}`, { size: 19, align: AL.RIGHT }), ws[2], { borders: tb }));
    return T([r], ws); },
  sub: (b, w) => P(b.title + (b.tag ? `  {{${b.tag}}}` : ''), { font: SANS, bold: true, size: 21 }),
  grid: (b, w) => {
    const n = b.head ? b.head.length : Math.max(...b.rows.map(r => (r.cells || [0]).length));
    const kw = mm(b.kw_mm || 20), cw = split(w - kw, b.w || Array(n).fill(1), 0, n), ws = [kw, ...cw], rows = [];
    if (b.head) rows.push([C(P(''), kw, { borders: NOB }), ...b.head.map((x, i) => C(H(x, { size: 17 }), cw[i], { fill: G2, borders: bAll(ln(G3, 4)) }))]);
    b.rows.forEach(r => {
      const lab = C(String(r.k || '').split('/').map(x => P(x, { font: SANS, bold: true, size: 17, align: AL.CENTER, color: r.res ? 'FFFFFF' : INK })), kw,
        { fill: r.res ? G4 : G2, borders: bAll(ln(G3, 4)) });
      const fill = r.res ? G1 : undefined;
      if (r.span !== undefined) { const c = normCell(r.span); rows.push([lab, C(cellKids(c, w - kw), w - kw, { span: n, fill, v: c.c ? VerticalAlign.CENTER : VerticalAlign.TOP })]); }
      else rows.push([lab, ...r.cells.map((x, i) => { const c = normCell(x); return C(cellKids(c, cw[i]), cw[i], { fill, v: c.c ? VerticalAlign.CENTER : VerticalAlign.TOP }); })]);
    });
    return T(rows, ws); },
  flow: (b, w) => { const n = b.items.length, sw = mm(6), cw = split(w, b.items.map(() => 1), sw, n), ws = [], r = [];
    b.items.forEach((x, i) => { ws.push(cw[i]);
      r.push(C([P((x.tag ? `{{${x.tag}}}` : '') + x.h, { font: SANS, bold: true, size: 17, align: AL.CENTER, fill: G1, after: 30 }), ...Bs(x.b, { size: 16 })], cw[i], { v: VerticalAlign.TOP, mt: 0 }));
      if (i < n - 1) { ws.push(sw); r.push(C(P(b.sep || '+', { font: SANS, bold: true, size: 26, color: G4, align: AL.CENTER }), sw, { borders: NOB, ml: 0, mr: 0 })); } });
    const out = [T([r], ws)];
    if (b.res) { const rs = [].concat(b.res);
      out.push(P('▼', { font: SANS, size: 16, color: G4, align: AL.CENTER, before: 20 }),
        T([[C([P(rs[0], { font: SANS, bold: true, size: 18, color: 'FFFFFF', align: AL.CENTER }), ...(rs[1] ? [P(rs[1], { font: SANS, size: 15, color: 'EEEEEE', align: AL.CENTER })] : [])], w, { fill: G4, borders: NOB })]], [w])); }
    return out; },
  strip: (b, w) => { const n = b.items.length, g = mm(1.6), cw = split(w, b.items.map(() => 1), g, n), ws = [], r = [];
    b.items.forEach((x, i) => { ws.push(cw[i]);
      r.push(C(figure({ ...x, h_mm: b.h_mm || 22 }, cw[i]), cw[i], { borders: NOB, ml: 0, mr: 0, mt: 0, mb: 0 }));
      if (i < n - 1) { ws.push(g); r.push(C(P(''), g, { borders: NOB })); } });
    return T([r], ws); },
  boxes: (b, w) => { const n = b.items.length, g = mm(1.6), cw = split(w, b.items.map(() => 1), g, n), ws = [], r1 = [], r2 = [];
    b.items.forEach((x, i) => { ws.push(cw[i]); r1.push(C(H(x.h), cw[i], { fill: G2 })); r2.push(C(Bs(x.b), cw[i], { v: VerticalAlign.TOP }));
      if (i < n - 1) { ws.push(g); r1.push(C(P(''), g, { borders: NOB })); r2.push(C(P(''), g, { borders: NOB })); } });
    return T([r1, r2], ws); },
  kv: (b, w) => { const iw = w - KW - 240; const kids = [];
    if (b.text) kids.push(P(b.text)); if (b.b) kids.push(...Bs(b.b)); if (b.ar) kids.push(P(`**${b.ar}**`));
    [].concat(b.img || []).forEach(i => kids.push(...figure(i, iw)));
    if (b.inner) { kids.push(...blocks(b.inner, iw)); kids.push(gap(20)); }
    return T([[C(String(b.k).split('/').map(x => P(x, { font: SANS, bold: true, size: 17, align: AL.CENTER })), KW, { fill: G2 }),
      C(kids, w - KW, { ml: 120, v: b.inner ? VerticalAlign.TOP : VerticalAlign.CENTER, mt: b.inner ? 70 : 45 })]], [KW, w - KW]); },
  banner: (b, w) => T([[C(P(`▼  ${b.text}  ▼`, { font: SANS, bold: true, size: 19, align: AL.CENTER }), w, { fill: G1, mt: 50, mb: 50 })]], [w]),
  chev: (b, w) => { const aw = mm(4), n = b.st.length, sw = Math.floor((w - aw * (n - 1)) / n), ws = [], r1 = [], r2 = [];
    b.st.forEach((s, i) => { ws.push(sw);
      r1.push(C(H(s.h, { color: s.on ? 'FFFFFF' : INK, size: 16 }), sw, { fill: s.on ? G4 : G2, borders: NOB, ml: 40, mr: 40 }));
      r2.push(C(Bs(s.t, { size: 16 }), sw, { borders: NOB, v: VerticalAlign.TOP, ml: 60, mr: 40 }));
      if (i < n - 1) { ws.push(aw); r1.push(C(P('▶', { font: SANS, size: 15, color: G4, align: AL.CENTER }), aw, { borders: NOB, ml: 0, mr: 0 }));
        r2.push(C(P(''), aw, { borders: NOB, ml: 0, mr: 0 })); } });
    ws[ws.length - 1] += w - ws.reduce((a, c) => a + c, 0); return T([r1, r2], ws); },
  check: (b) => P('✓ ' + b.text, { font: SANS, bold: true, size: 18, before: 30, after: 10 }),
  comb: (b, w) => { const n = b.cards.length, pw = mm(5), rw = mm(28), cw = Math.floor((w - pw * n - rw) / n);
    const card = h => C(H(h, { size: 17 }), cw, { borders: { top: ln(), left: ln(), right: ln(), bottom: { style: BorderStyle.DASHED, size: 4, color: G3 } } });
    const sym = s => C(P(s, { font: SANS, bold: true, size: 26, color: G4, align: AL.CENTER }), pw, { borders: NOB, rowSpan: 2, ml: 0, mr: 0 });
    const body = a => C(Bs(a, { size: 16 }), cw, { borders: { top: NONE, left: ln(), right: ln(), bottom: ln() }, v: VerticalAlign.TOP });
    const ws = [], r1 = [], r2 = [];
    b.cards.forEach((c, i) => { ws.push(cw, pw); r1.push(card(c.h), sym(i < n - 1 ? '+' : '=')); r2.push(body(c.b)); });
    const last = w - ws.reduce((a, x) => a + x, 0); ws.push(last);
    r1.push(C([P(b.res[0], { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }), P(b.res[1] || '', { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }),
      P(b.res[2] || '', { font: SANS, size: 14, color: 'DDDDDD', align: AL.CENTER })], last, { fill: G4, borders: NOB, rowSpan: 2 }));
    return T([r1, r2], ws); },
  line: (b, w) => T([[C(P(b.k, { font: SANS, bold: true, size: 16, align: AL.CENTER }), mm(18), { fill: G2, mt: 25, mb: 25, ml: 40, mr: 40 }),
    C(P(b.v, { size: 16 }), w - mm(18), { mt: 25, mb: 25 })]], [mm(18), w - mm(18)]),
  cmp: (b, w) => { const aw = mm(9), cw = Math.floor((w - aw) / 2);
    const side = (x, dark) => [P(`${dark ? '{{' : '[['}${x.tag}${dark ? '}}' : ']]'}**${x.h}**`, { size: 17 }), ...Bs(x.b, { size: 16 })];
    return T([[C(side(b.a), cw, { v: VerticalAlign.TOP }), C(P('➡', { font: SANS, bold: true, size: 28, color: G4, align: AL.CENTER }), aw, { borders: NOB, ml: 0, mr: 0 }),
      C(side(b.b, true), w - cw - aw, { v: VerticalAlign.TOP, borders: bAll(ln(G4, 12)) })]], [cw, aw, w - cw - aw]); },
  bl: (b) => Bs(b.b),
  text: (b) => (b.p || []).map(x => P(x, { first: 120, after: 40 })),
  eff: (b, w) => { const a = mm(26), c = mm(54), m = w - a - c, o = ln();
    const row = (t, r, last) => [C(B(t), a + m, { span: 2, borders: { top: NONE, left: o, right: NONE, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, ml: 140 }),
      C(P(r, { bold: true, align: AL.RIGHT }), c, { borders: { top: NONE, left: NONE, right: o, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, mr: 140 })];
    return T([[C(P(b.k, { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }), a, { fill: G4 }),
      C(P(b.v, { font: SANS, bold: true, size: 17 }), m + c, { span: 2, ml: 140 })],
      ...b.rows.map((r, i) => row(r[0], r[1], i === b.rows.length - 1))], [a, m, c]); },
  res: (b, w) => T([[C(String(b.label || LB.result).split('/').map(x => P(x, { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER })), KW, { fill: G4, borders: bAll(ln(G3, 4)) }),
    C(Bs(b.b), w - KW, { fill: G1, borders: bAll(ln(G3, 4)), ml: 130, mt: 55, mb: 55 })]], [KW, w - KW]),
  kpi: (b, w) => { const n = b.items.length, g = mm(1.6), cw = split(w, b.items.map(() => 1), g, n), ws = [], r = [];
    b.items.forEach((x, i) => { ws.push(cw[i]);
      r.push(C([P(x.v, { font: SANS, bold: true, size: 26, align: AL.CENTER, line: 300 }), P(x.l, { font: SANS, size: 14, color: '444444', align: AL.CENTER })], cw[i],
        { borders: { top: ln(G4, 18), left: ln(), right: ln(), bottom: ln() } }));
      if (i < n - 1) { ws.push(g); r.push(C(P(''), g, { borders: NOB })); } });
    return T([r], ws); },
  tbl: (b, w) => { const ws = split(w, b.w, 0, b.w.length);
    return T([b.head.map((h, i) => C(H(h, { size: 16 }), ws[i], { fill: G2 })),
      ...b.rows.map(r => r.map((c, i) => i === 0 ? C(P(c, { font: SANS, bold: true, size: 16 }), ws[i], { fill: G1 }) : C(P(c, { size: 16 }), ws[i], { ml: 110 })))], ws); },
  cols: (b, w) => { const n = b.cols.length, g = mm(2.4), cw = split(w, b.w || b.cols.map(() => 1), g, n), ws = [], r = [];
    b.cols.forEach((col, i) => { ws.push(cw[i]); r.push(C(blocks(col, cw[i] - 20), cw[i], { borders: NOB, v: VerticalAlign.TOP, ml: 0, mr: 0, mt: 0, mb: 0 }));
      if (i < n - 1) { ws.push(g); r.push(C(P(''), g, { borders: NOB })); } });
    return T([r], ws); },
  img: (b, w) => figure(b, w),
};

// ---- 머리말·바닥글 (config.layout). 짝수 쪽=왼쪽 면, 홀수 쪽=오른쪽 면. 옆탭은 PDF에서만 그린다
const rule = { bottom: { style: BorderStyle.SINGLE, size: 6, color: G3, space: 2 } };
function chrome(p, i) {
  if (p.footer) return { footers: { default: new Footer({ children: [P(p.footer, { font: SANS, bold: true, size: 16, color: G4, align: p.align === 'left' ? AL.LEFT : AL.RIGHT })] }) } };
  if (!LAY) return {};
  const n = (LAY.page_start || 1) + i, even = n % 2 === 0, o = {};
  const t = (text, x = {}) => new TextRun({ text, font: SANS, size: Math.round((x.size || 18) * F), bold: x.bold, color: x.color || INK, shading: x.fill ? { type: ShadingType.CLEAR, fill: x.fill, color: 'auto' } : undefined });
  if (p.header !== false) {
    if (even && LAY.chapter) o.headers = { default: new Header({ children: [new Paragraph({ border: rule, children: [
      ...(LAY.chapter.no ? [t(` ${LAY.chapter.no} `, { bold: true, color: 'FFFFFF', fill: G4, size: 20 }), t('  ')] : []), t(LAY.chapter.text || '', { bold: true, size: 20 })] })] }) };
    if (!even && LAY.running) o.headers = { default: new Header({ children: [new Paragraph({ alignment: AL.RIGHT, border: rule, children: [t(`  ${LAY.running}  `, { size: 16, fill: G1 })] })] }) };
  }
  if (LAY.page_numbers !== false) o.footers = { default: new Footer({ children: [new Paragraph({ alignment: even ? AL.LEFT : AL.RIGHT, children: even
    ? [t(String(n), { bold: true, size: 16 }), ...(LAY.org ? [t('  |  ', { color: G3, size: 16 }), t(LAY.org, { bold: true, color: G4, size: 16 })] : [])]
    : [...(LAY.slogan ? [t(LAY.slogan, { color: G3, size: 16 }), t('  |  ', { color: G3, size: 16 })] : []), t(String(n), { bold: true, size: 16 })] })] }) };
  return o;
}

const before = { sec: 150, sub: 110, ev: 0, title: 0, key: 50 };
function pageChildren(list) {
  const out = [];
  list.forEach((b, i) => {
    if (!R[b.t]) throw new Error(`알 수 없는 블록 타입: ${b.t}`);
    if (i) out.push(gap(before[b.t] ?? 80));
    push(out, R[b.t](b, W));
  });
  return out;
}
const pageProps = { page: { size: { width: 11906, height: 16838 }, margin: { top: mm(18), bottom: mm(15), left: mm(19), right: mm(19), header: mm(8.5), footer: mm(7) } } };
const doc = new Document({ styles: { default: { document: { run: { font: SERIF, size: SZ } } } },
  sections: CT.pages.map((p, i) => ({ properties: pageProps, ...chrome(p, i), children: pageChildren(p.blocks) })) });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('ok:', OUT); });
