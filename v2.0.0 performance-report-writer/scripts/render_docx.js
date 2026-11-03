#!/usr/bin/env node
// 내용 데이터(content.json) → Word(.docx). 표 기반으로 박스·흐름도를 그린다.
// 사용법: node render_docx.js content.json report.docx [글자배율=1.17] [간격배율=1.65]
//   지면이 넘치면 배율을 낮추고(1.13/1.5), 남으면 내용을 더 넣는다(배율로 메우지 않는다).
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, VerticalAlign, Footer, TableLayoutType, ImageRun } = require('docx');

const src = path.resolve(process.argv[2] || 'content.json');
const OUT = process.argv[3] || 'report.docx';
const F = parseFloat(process.argv[4] || '1.17');
const SP = parseFloat(process.argv[5] || '1.65');
const baseDir = path.dirname(src);
const CT = src.endsWith('.json') ? JSON.parse(fs.readFileSync(src, 'utf8')) : require(src);

// ---- 설정
const cc = CT.config || {};
const hex = v => String(v).replace('#', '').toUpperCase();
const TH = { ink: '#1A1A1A', g1: '#F2F2F2', g2: '#E3E3E3', g3: '#BDBDBD', g4: '#7A7A7A', ...(cc.theme || {}) };
const INK = hex(TH.ink), G1 = hex(TH.g1), G2 = hex(TH.g2), G3 = hex(TH.g3), G4 = hex(TH.g4);
const FN = { docx_sans: '맑은 고딕', docx_serif: '바탕', ...(cc.fonts || {}) };
const LB = { result: '추진성과', best: ['BEST', 'PRACTICE'], ...(cc.labels || {}) };
const font = n => ({ ascii: n, eastAsia: n, hAnsi: n });
const SANS = font(FN.docx_sans), SERIF = font(FN.docx_serif);

const mm = x => Math.round(x * 56.7);
const W = mm(186);
const SZ = 17;
const AL = AlignmentType;

function runs(text, o = {}) {
  const out = [], sz = Math.round((o.size || SZ) * F), tsz = Math.round(((o.size || SZ) - 3) * F);
  String(text).split(/(\*\*[^*]+\*\*|__[^_]+__|\[\[[^\]]+\]\]|\{\{[^}]+\}\})/g).filter(Boolean).forEach(t => {
    const base = { font: o.font || SERIF, size: sz, bold: o.bold, color: o.color };
    if (t.startsWith('**')) out.push(new TextRun({ ...base, text: t.slice(2, -2), bold: true }));
    else if (t.startsWith('__')) out.push(new TextRun({ ...base, text: t.slice(2, -2), bold: true, underline: {} }));
    else if (t.startsWith('[[')) out.push(new TextRun({ ...base, font: SANS, size: tsz, bold: true, color: INK, text: ` ${t.slice(2, -2)} `, shading: { type: ShadingType.CLEAR, fill: G2, color: 'auto' } }), new TextRun({ ...base, text: ' ' }));
    else if (t.startsWith('{{')) out.push(new TextRun({ ...base, font: SANS, size: tsz, bold: true, color: 'FFFFFF', text: ` ${t.slice(2, -2)} `, shading: { type: ShadingType.CLEAR, fill: INK, color: 'auto' } }), new TextRun({ ...base, text: ' ' }));
    else out.push(new TextRun({ ...base, text: t }));
  });
  return out;
}
const P = (text, o = {}) => new Paragraph({ children: runs(text, o), alignment: o.align,
  spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 264 },
  indent: o.hang ? { left: o.hang, hanging: o.hang } : (o.first ? { firstLine: o.first } : undefined) });
const B = (t, o = {}) => P('· ' + t, { hang: 150, ...o });
const Bs = (a, o) => (a || []).map(t => B(t, o));
const H = (t, o = {}) => P(t, { font: SANS, bold: true, size: 17, align: AL.CENTER, ...o });

const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const ln = (c = G3, s = 4) => ({ style: BorderStyle.SINGLE, size: s, color: c });
const bAll = b => ({ top: b, bottom: b, left: b, right: b });
const NOB = bAll(NONE);
function C(children, w, o = {}) {
  return new TableCell({ children: Array.isArray(children) ? children : [children], width: { size: w, type: WidthType.DXA },
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    borders: o.borders || bAll(ln()), verticalAlign: o.v || VerticalAlign.CENTER, columnSpan: o.span, rowSpan: o.rowSpan,
    margins: { top: Math.round((o.mt ?? 45) * SP), bottom: Math.round((o.mb ?? 45) * SP), left: o.ml ?? 90, right: o.mr ?? 90 } });
}
function T(rows, widths) {
  return new Table({ rows: rows.map(r => new TableRow({ children: r, cantSplit: true })), columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, layout: TableLayoutType.FIXED,
    borders: { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE } });
}
const gap = (h = 70) => new Paragraph({ spacing: { before: 0, after: 0, line: Math.max(20, Math.round(h * SP)), lineRule: 'exact' }, children: [new TextRun({ text: '', size: 2 })] });
const split = (total, ws, gapW, n) => { const s = ws.reduce((a, b) => a + b, 0), avail = total - gapW * (n - 1);
  const cw = ws.map(x => Math.round(avail * x / s)); cw[n - 1] = avail - cw.slice(0, -1).reduce((a, b) => a + b, 0); return cw; };
const KW = mm(17);
const push = (arr, r) => (Array.isArray(r) ? arr.push(...r) : arr.push(r));
const blocks = (list, w) => { const kids = []; list.forEach((x, i) => { if (i) kids.push(gap(40)); push(kids, R[x.t](x, w)); }); return kids; };

const R = {
  ev: (b, w) => T([[C(P(b.label, { font: SANS, bold: true, size: 20, align: AL.CENTER }), mm(26), { fill: G2, borders: bAll(ln(INK, 10)) }),
    C(P(b.text, { font: SANS, size: 19 }), w - mm(26), { borders: bAll(ln(INK, 10)), ml: 140 })]], [mm(26), w - mm(26)]),
  bp: (b, w) => { const lb = b.label || LB.best;
    return T([[C([P(lb[0], { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER, line: 220 }),
      P(lb[1] || '', { font: SANS, size: 11, color: 'FFFFFF', align: AL.CENTER, line: 200 })], mm(20), { fill: G4 }),
      C(b.items.map(t => P(t, { font: SANS, size: 18 })), w - mm(20), { ml: 140 })]], [mm(20), w - mm(20)]); },
  vision: (b, w) => T([[C(P(`[[${b.k}]] ${b.text}`, { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER }), w, { fill: INK, borders: NOB })]], [w]),
  sec: (b, w) => { const ws = [mm(10), w - mm(10) - (b.tag ? mm(20) : 0)]; if (b.tag) ws.push(mm(20));
    const tb = { top: ln(INK, 16), bottom: ln(INK, 6), left: NONE, right: NONE };
    const r = [C(P(b.no, { font: SANS, bold: true, size: 26, color: 'FFFFFF', align: AL.CENTER }), ws[0], { fill: INK, borders: tb }),
      C(P(b.title, { font: SANS, bold: true, size: 24 }), ws[1], { fill: G1, borders: tb, ml: 140 })];
    if (b.tag) r.push(C(P(`{{${b.tag}}}`, { size: 19, align: AL.RIGHT }), ws[2], { fill: G1, borders: tb }));
    return T([r], ws); },
  sub: (b, w) => { const tw = b.tag ? mm(32) : 0;
    const r = [C(P(b.title, { font: SANS, bold: true, size: 20 }), w - tw, { borders: NOB, ml: 0 })];
    if (b.tag) r.push(C(P(`[[${b.tag}]]`, { size: 19, align: AL.RIGHT }), tw, { borders: NOB, mr: 0 }));
    return T([r], b.tag ? [w - tw, tw] : [w]); },
  boxes: (b, w) => { const n = b.items.length, g = mm(2), cw = split(w, b.items.map(() => 1), g, n), ws = [], r1 = [], r2 = [];
    b.items.forEach((x, i) => { ws.push(cw[i]); r1.push(C(H(x.h), cw[i], { fill: G2 })); r2.push(C(Bs(x.b), cw[i], { v: VerticalAlign.TOP }));
      if (i < n - 1) { ws.push(g); r1.push(C(P(''), g, { borders: NOB })); r2.push(C(P(''), g, { borders: NOB })); } });
    return T([r1, r2], ws); },
  kv: (b, w) => { const iw = w - KW - 240; const kids = [];
    if (b.text) kids.push(P(b.text)); if (b.b) kids.push(...Bs(b.b)); if (b.ar) kids.push(P(`**${b.ar}**`));
    if (b.inner) { kids.push(...blocks(b.inner, iw)); kids.push(gap(20)); }
    return T([[C(b.k.split('/').map(x => P(x, { font: SANS, bold: true, size: 17, align: AL.CENTER })), KW, { fill: G2 }),
      C(kids, w - KW, { ml: 120, v: b.inner ? VerticalAlign.TOP : VerticalAlign.CENTER, mt: b.inner ? 70 : 45 })]], [KW, w - KW]); },
  banner: (b, w) => T([[C(P(`▼  ${b.text}  ▼`, { font: SANS, bold: true, size: 19, align: AL.CENTER }), w, { fill: G2, borders: NOB, mt: 50, mb: 50 })]], [w]),
  chev: (b, w) => { const aw = mm(4), n = b.st.length, sw = Math.floor((w - aw * (n - 1)) / n), ws = [], r1 = [], r2 = [];
    b.st.forEach((s, i) => { ws.push(sw);
      r1.push(C(H(s.h, { color: s.on ? 'FFFFFF' : INK, size: 16 }), sw, { fill: s.on ? INK : G2, borders: NOB, ml: 40, mr: 40 }));
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
      P(b.res[2] || '', { font: SANS, size: 14, color: 'DDDDDD', align: AL.CENTER })], last, { fill: INK, borders: NOB, rowSpan: 2 }));
    return T([r1, r2], ws); },
  line: (b, w) => T([[C(P(b.k, { font: SANS, bold: true, size: 16, align: AL.CENTER }), mm(18), { fill: G2, mt: 25, mb: 25, ml: 40, mr: 40 }),
    C(P(b.v, { size: 16 }), w - mm(18), { mt: 25, mb: 25 })]], [mm(18), w - mm(18)]),
  cmp: (b, w) => { const aw = mm(9), cw = Math.floor((w - aw) / 2);
    const side = (x, dark) => [P(`${dark ? '{{' : '[['}${x.tag}${dark ? '}}' : ']]'}**${x.h}**`, { size: 17 }), ...Bs(x.b, { size: 16 })];
    return T([[C(side(b.a), cw, { v: VerticalAlign.TOP }), C(P('➡', { font: SANS, bold: true, size: 28, color: G4, align: AL.CENTER }), aw, { borders: NOB, ml: 0, mr: 0 }),
      C(side(b.b, true), w - cw - aw, { v: VerticalAlign.TOP, borders: bAll(ln(INK, 12)) })]], [cw, aw, w - cw - aw]); },
  bl: (b) => Bs(b.b),
  text: (b) => (b.p || []).map(x => P(x, { first: 120, after: 40 })),
  eff: (b, w) => { const a = mm(26), c = mm(54), m = w - a - c, o = ln();
    const row = (t, r, last) => [C(B(t), a + m, { span: 2, borders: { top: NONE, left: o, right: NONE, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, ml: 140 }),
      C(P(r, { bold: true, align: AL.RIGHT }), c, { borders: { top: NONE, left: NONE, right: o, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, mr: 140 })];
    return T([[C(P(b.k, { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }), a, { fill: G4 }),
      C(P(b.v, { font: SANS, bold: true, size: 17 }), m + c, { span: 2, ml: 140 })],
      ...b.rows.map((r, i) => row(r[0], r[1], i === b.rows.length - 1))], [a, m, c]); },
  res: (b, w) => T([[C(P(b.label || LB.result, { font: SANS, bold: true, size: 15, color: 'FFFFFF', align: AL.CENTER }), KW, { fill: INK, borders: bAll(ln(INK, 14)) }),
    C(Bs(b.b), w - KW, { borders: bAll(ln(INK, 14)), ml: 130, mt: 60, mb: 60 })]], [KW, w - KW]),
  kpi: (b, w) => { const n = b.items.length, g = mm(2), cw = split(w, b.items.map(() => 1), g, n), ws = [], r = [];
    b.items.forEach((x, i) => { ws.push(cw[i]);
      r.push(C([P(x.v, { font: SANS, bold: true, size: 26, align: AL.CENTER, line: 300 }), P(x.l, { font: SANS, size: 14, color: '444444', align: AL.CENTER })], cw[i],
        { borders: { top: ln(INK, 18), left: ln(), right: ln(), bottom: ln() } }));
      if (i < n - 1) { ws.push(g); r.push(C(P(''), g, { borders: NOB })); } });
    return T([r], ws); },
  tbl: (b, w) => { const ws = split(w, b.w, 0, b.w.length);
    return T([b.head.map((h, i) => C(H(h, { size: 16 }), ws[i], { fill: G2 })),
      ...b.rows.map(r => r.map((c, i) => i === 0 ? C(P(c, { font: SANS, bold: true, size: 16 }), ws[i], { fill: G1 }) : C(P(c, { size: 16 }), ws[i], { ml: 110 })))], ws); },
  cols: (b, w) => { const n = b.cols.length, g = mm(2.7), cw = split(w, b.w || b.cols.map(() => 1), g, n), ws = [], r = [];
    b.cols.forEach((col, i) => { ws.push(cw[i]); r.push(C(blocks(col, cw[i] - 20), cw[i], { borders: NOB, v: VerticalAlign.TOP, ml: 0, mr: 0, mt: 0, mb: 0 }));
      if (i < n - 1) { ws.push(g); r.push(C(P(''), g, { borders: NOB })); } });
    return T([r], ws); },
  img: (b) => { const f = path.resolve(baseDir, b.src), ext = path.extname(f).slice(1).toLowerCase();
    const px = v => Math.round(v * 96 / 25.4);
    const out = [new Paragraph({ alignment: AL.CENTER, spacing: { before: 40, after: 20 },
      children: [new ImageRun({ type: ext === 'jpeg' ? 'jpg' : ext, data: fs.readFileSync(f), transformation: { width: px(b.w_mm), height: px(b.h_mm) } })] })];
    if (b.caption) out.push(P(b.caption, { font: SANS, size: 14, color: G4, align: AL.CENTER }));
    return out; },
};

const before = { sec: 150, sub: 120, ev: 0 };
function pageChildren(list) {
  const out = [];
  list.forEach((b, i) => {
    if (!R[b.t]) throw new Error(`알 수 없는 블록 타입: ${b.t}`);
    if (i) out.push(gap(before[b.t] ?? 85));
    push(out, R[b.t](b, W));
  });
  return out;
}
const pageProps = { page: { size: { width: 11906, height: 16838 }, margin: { top: mm(11), bottom: mm(13), left: mm(12), right: mm(12), footer: mm(6) } } };
const doc = new Document({ styles: { default: { document: { run: { font: SERIF, size: SZ } } } },
  sections: CT.pages.map(p => ({ properties: pageProps,
    footers: p.footer ? { default: new Footer({ children: [P(p.footer, { font: SANS, bold: true, size: 16, color: G4, align: p.align === 'left' ? AL.LEFT : AL.RIGHT })] }) } : undefined,
    children: pageChildren(p.blocks) })) });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('ok:', OUT); });
