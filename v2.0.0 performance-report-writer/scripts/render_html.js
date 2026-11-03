#!/usr/bin/env node
// 내용 데이터(content.json) → A4 HTML. PDF는 to_pdf.py로 만든다.
// 사용법: node render_html.js content.json report.html
const fs = require('fs');
const path = require('path');

const src = path.resolve(process.argv[2] || 'content.json');
const out = process.argv[3] || 'report.html';
const baseDir = path.dirname(src);
const C = src.endsWith('.json') ? JSON.parse(fs.readFileSync(src, 'utf8')) : require(src);

// ---- 설정 (content.json의 "config"로 덮어쓴다)
const DEF = {
  theme: { ink: '#1A1A1A', g1: '#F2F2F2', g2: '#E3E3E3', g3: '#BDBDBD', g4: '#7A7A7A' },
  fonts: { sans: 'Noto Sans CJK KR', serif: 'Noto Serif CJK KR' },
  labels: { result: '추진성과', best: ['BEST', 'PRACTICE'] },
};
const cfg = {
  theme: { ...DEF.theme, ...((C.config || {}).theme || {}) },
  fonts: { ...DEF.fonts, ...((C.config || {}).fonts || {}) },
  labels: { ...DEF.labels, ...((C.config || {}).labels || {}) },
};
const css = fs.readFileSync(path.join(__dirname, 'base.css'), 'utf8');

// ---- 텍스트 마크업: **굵게** __밑줄굵게__ [[연한태그]] {{진한태그}}
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const mk = s => esc(s)
  .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
  .replace(/__([^_]+)__/g, '<b><u>$1</u></b>')
  .replace(/\[\[([^\]]+)\]\]/g, '<span class="tag">$1</span>')
  .replace(/\{\{([^}]+)\}\}/g, '<span class="tag dk">$1</span>');
const ul = (arr, cls = 'b serif') => `<ul class="${cls}">${(arr || []).map(x => `<li>${mk(x)}</li>`).join('')}</ul>`;
const imgData = p => {
  const f = path.resolve(baseDir, p);
  const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
  return `data:image/${ext};base64,${fs.readFileSync(f).toString('base64')}`;
};

const R = {
  ev: b => `<div class="evhead"><div class="lab">${mk(b.label)}</div><div class="txt">${mk(b.text)}</div></div>`,
  bp: b => `<div class="bp"><div class="lab">${esc(b.label ? b.label[0] : cfg.labels.best[0])}<small>${esc(b.label ? b.label[1] || '' : cfg.labels.best[1])}</small></div><ul>${b.items.map(x => `<li>${mk(x)}</li>`).join('')}</ul></div>`,
  vision: b => `<div class="vision"><span>${mk(b.k)}</span>${mk(b.text)}</div>`,
  sec: (b, i) => `<div class="sec"${i === 0 ? ' style="margin-top:0"' : ''}><div class="no">${esc(b.no)}</div><div class="tt">${mk(b.title)}</div>${b.tag ? `<span class="tag dk">${esc(b.tag)}</span>` : ''}</div>`,
  sub: b => `<div class="sub"><span>${mk(b.title)}</span>${b.tag ? `<span class="tag">${mk(b.tag)}</span>` : ''}</div>`,
  boxes: b => `<div class="row">${b.items.map(x => `<div class="box"><div class="hd">${mk(x.h)}</div><div class="bd">${ul(x.b)}</div></div>`).join('')}</div>`,
  kv: b => `<div class="kv"><div class="k">${b.k.split('/').map(esc).join('<br>')}</div><div class="v${b.inner ? '' : ' serif'}">${
    b.text ? mk(b.text) : ''}${b.b ? ul(b.b) : ''}${b.ar ? `<div class="arrow serif">${mk(b.ar)}</div>` : ''}${b.inner ? b.inner.map(render).join('') : ''}</div></div>`,
  banner: b => `<div class="banner">${mk(b.text)}</div><div style="height:2.4mm"></div>`,
  chev: b => `<div class="chev serif">${b.st.map(s => `<div class="st${s.on ? ' on' : ''}"><div class="h">${mk(s.h)}</div><div class="t">${s.t.map(x => '· ' + mk(x)).join('<br>')}</div></div>`).join('')}</div>`,
  check: b => `<div class="check" style="margin-top:1.4mm">✓ ${mk(b.text)}</div>`,
  comb: b => `<div class="comb serif">${b.cards.map(c => `<div class="c"><div class="hd">${mk(c.h)}</div><div class="bd">${ul(c.b, 'b')}</div></div>`).join('<div class="plus">+</div>')}<div class="eq">=</div><div class="res">${mk(b.res[0])}<br>${mk(b.res[1] || '')}<small>${mk(b.res[2] || '')}</small></div></div>`,
  line: b => `<div class="line"><div class="k">${mk(b.k)}</div><div class="v serif">${mk(b.v)}</div></div>`,
  cmp: b => `<div class="cmp serif"><div class="c"><div class="h"><span class="tag">${esc(b.a.tag)}</span>${mk(b.a.h)}</div>${ul(b.a.b, 'b')}</div><div class="ar">➡</div><div class="c on"><div class="h"><span class="tag dk">${esc(b.b.tag)}</span>${mk(b.b.h)}</div>${ul(b.b.b, 'b')}</div></div>`,
  bl: b => ul(b.b),
  text: b => `<div class="txtblk serif">${(b.p || []).map(x => `<p>${mk(x)}</p>`).join('')}</div>`,
  eff: b => `<div class="eff"><div class="top"><div class="k">${mk(b.k)}</div><div class="v">${mk(b.v)}</div></div><ul class="serif">${b.rows.map(r => `<li><span>· ${mk(r[0])}</span><span>${mk(r[1])}</span></li>`).join('')}</ul></div>`,
  res: b => `<div class="res-box"><div class="k">${esc(b.label || cfg.labels.result)}</div><div class="v serif">${ul(b.b)}</div></div>`,
  kpi: b => `<div class="kpi">${b.items.map(x => `<div><b>${mk(x.v)}</b><span>${mk(x.l)}</span></div>`).join('')}</div>`,
  tbl: b => `<table class="tb serif"><colgroup>${b.w.map(w => `<col style="width:${w * 100}%">`).join('')}</colgroup><tr>${b.head.map(h => `<th>${mk(h)}</th>`).join('')}</tr>${b.rows.map(r => `<tr>${r.map((c, i) => `<td${i === 0 ? ' class="f"' : ''}>${mk(c)}</td>`).join('')}</tr>`).join('')}</table>`,
  cols: b => { const w = b.w || b.cols.map(() => 1 / b.cols.length);
    return `<div class="cols">${b.cols.map((col, i) => `<div style="flex:${w[i]}">${col.map(render).join('')}</div>`).join('')}</div>`; },
  img: b => `<figure class="img"><img src="${imgData(b.src)}" style="width:${b.w_mm}mm;height:${b.h_mm}mm">${b.caption ? `<figcaption>${mk(b.caption)}</figcaption>` : ''}</figure>`,
};
function render(b, i) {
  if (!R[b.t]) throw new Error(`알 수 없는 블록 타입: ${b.t}`);
  return R[b.t](b, i);
}

const extra = `
:root{--ink:${cfg.theme.ink};--g1:${cfg.theme.g1};--g2:${cfg.theme.g2};--g3:${cfg.theme.g3};--g4:${cfg.theme.g4};
--sans:"${cfg.fonts.sans}","Malgun Gothic",sans-serif;--serif:"${cfg.fonts.serif}","Batang",serif}
.vision{background:var(--ink);color:#fff;font-weight:900;font-size:10.6pt;text-align:center;padding:1.5mm;margin-bottom:2mm}
.vision span{border:1px solid #fff;font-size:8.4pt;padding:0 1.6mm;margin-right:3mm;vertical-align:1px}
.kpi{display:flex;gap:2mm;margin-bottom:2.4mm}
.kpi>div{flex:1;border:1px solid var(--g3);border-top:2.4px solid var(--ink);text-align:center;padding:1.4mm 1mm}
.kpi b{display:block;font-size:15pt;font-weight:900;line-height:1.15}
.kpi span{font-size:8.4pt;color:#444}
.tb{width:100%;border-collapse:collapse;margin-bottom:2.4mm;font-size:9.3pt;table-layout:fixed}
.tb th{background:var(--g2);font-family:var(--sans);font-weight:700;border:1px solid var(--g3);padding:1mm;font-size:9.4pt}
.tb td{border:1px solid var(--g3);padding:1mm 1.8mm;vertical-align:middle}
.tb td.f{font-family:var(--sans);font-weight:700;background:var(--g1);font-size:9.2pt}
.kv .v .tb,.kv .v .kpi{margin-bottom:1.2mm}
.txtblk{margin-bottom:2.4mm;font-size:10pt}.txtblk p{margin-bottom:1.2mm;text-indent:2mm}
.cols{display:flex;gap:2.7mm;align-items:flex-start}.cols>div{min-width:0}
.img{margin:1mm 0 2.4mm;text-align:center}.img figcaption{font-size:8.4pt;color:var(--g4);margin-top:.8mm}
`;
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${esc(C.title || 'report')}</title><style>${css}${extra}</style></head><body>
${C.pages.map(p => `<section class="page">${p.blocks.map(render).join('\n')}${p.footer ? `<div class="footer ${p.align === 'left' ? 'l' : 'r'}">${esc(p.footer)}</div>` : ''}</section>`).join('\n')}
</body></html>`;
fs.writeFileSync(out, html);
console.log('ok:', out);
