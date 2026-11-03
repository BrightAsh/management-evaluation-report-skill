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
  theme: { ink: '#222222', g1: '#F2F2F2', g2: '#DADADA', g3: '#A3A3A3', g4: '#5A5A5A' },
  fonts: { sans: 'Noto Sans CJK KR', serif: 'Noto Serif CJK KR' },
  labels: { result: '추진성과', key: '핵심성과', best: ['BEST', 'PRACTICE'] },
};
const cc = C.config || {};
const cfg = {
  theme: { ...DEF.theme, ...(cc.theme || {}) },
  fonts: { ...DEF.fonts, ...(cc.fonts || {}) },
  labels: { ...DEF.labels, ...(cc.labels || {}) },
  layout: cc.layout || null,   // 머리말·쪽번호·옆탭. 없으면 그리지 않는다
};
const css = fs.readFileSync(path.join(__dirname, 'base.css'), 'utf8');

// ---- 텍스트 마크업: **굵게** __밑줄굵게__ [[테두리 태그]] {{진한 태그}}
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const mk = s => esc(s)
  .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
  .replace(/__([^_]+)__/g, '<b><u>$1</u></b>')
  .replace(/\[\[([^\]]+)\]\]/g, '<span class="tag">$1</span>')
  .replace(/\{\{([^}]+)\}\}/g, '<span class="tag dk">$1</span>');
// 목록: "- " 하위, "* " 각주, "※ " 참고, "= " 기호 없음, 나머지는 "· "
const li = x => { const s = String(x);
  if (s.startsWith('- ')) return `<li class="d">${mk(s.slice(2))}</li>`;
  if (s.startsWith('* ')) return `<li class="n">${mk(s.slice(2))}</li>`;
  if (s.startsWith('※')) return `<li class="x">${mk(s.replace(/^※\s*/, ''))}</li>`;
  if (s.startsWith('= ')) return `<li class="p">${mk(s.slice(2))}</li>`;
  return `<li>${mk(s)}</li>`; };
const ul = (arr, cls = 'b serif') => `<ul class="${cls}">${(arr || []).map(li).join('')}</ul>`;
const imgData = p => {
  const f = path.resolve(baseDir, p);
  const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
  return `data:image/${ext};base64,${fs.readFileSync(f).toString('base64')}`;
};

// ---- 그림: src가 없으면(가린 견본) 빗금 자리표시로 그린다
const figure = i => {
  if (i.src && !fs.existsSync(path.resolve(baseDir, i.src))) { console.warn('그림 파일 없음(자리표시로 그림):', i.src); i = { ...i, src: null, label: i.label || '그림 없음' }; }
  const right = i.pos === 'right', w = i.w_mm || (right ? 30 : null);
  const st = [w ? `width:${w}mm` : '', i.h_mm ? `height:${i.h_mm}mm` : ''].filter(Boolean).join(';');
  const media = i.src ? `<img src="${imgData(i.src)}" style="${st}">`
    : `<div class="phimg" style="width:${w ? w + 'mm' : '100%'};height:${i.h_mm || 20}mm">${esc(i.label || '그림')}</div>`;
  return `<figure class="cimg"${right ? ` style="flex:none;width:${w}mm;margin-top:0"` : ''}>${media}${i.caption ? `<figcaption>${mk(i.caption)}</figcaption>` : ''}</figure>`;
};
// ---- 표 칸: 문자열=가운데 굵은 글, 배열=목록, 객체={h 칸머리, p 문장, b 목록, img 그림, c 가운데}
const normCell = x => typeof x === 'string' ? { p: [x], c: true } : Array.isArray(x) ? { b: x } : (x || {});
function cellInner(c) {
  const head = c.h ? `<div class="ch">${mk(c.h)}</div>` : '';
  const body = (c.p ? [].concat(c.p).map(x => `<div class="cp">${mk(x)}</div>`).join('') : '') + (c.b ? ul(c.b) : '');
  const imgs = [].concat(c.img || []), right = imgs.filter(i => i.pos === 'right'), below = imgs.filter(i => i.pos !== 'right');
  const mid = right.length ? `<div class="cw"><div class="cwt">${body}</div>${right.map(figure).join('')}</div>` : body;
  return head + mid + below.map(figure).join('');
}

const R = {
  title: b => `<div class="ttl">${mk(b.text)}</div>`,
  ev: b => `<div class="evhead"><div class="lab">${mk(b.label)}</div><div class="txt">${mk(b.text)}</div></div>`,
  key: b => `<div class="evhead key"><div class="lab">${mk(b.label || cfg.labels.key)}</div><div class="txt">☑&nbsp;${mk(b.text)}</div></div>`,
  bp: b => `<div class="bp"><div class="lab">${esc(b.label ? b.label[0] : cfg.labels.best[0])}<small>${esc(b.label ? b.label[1] || '' : cfg.labels.best[1])}</small></div><ul>${b.items.map(x => `<li>${mk(x)}</li>`).join('')}</ul></div>`,
  vision: b => `<div class="vision"><span>${mk(b.k)}</span>${mk(b.text)}</div>`,
  sec: (b, i) => `<div class="sec"${i === 0 ? ' style="margin-top:0"' : ''}><div class="no">${esc(b.no)}</div><div class="tt">${mk(b.title)}</div>${b.tag ? `<span class="tag dk">${esc(b.tag)}</span>` : ''}</div>`,
  sub: b => `<div class="sub"><span>${mk(b.title)}</span>${b.tag ? `<span class="tag dk">${mk(b.tag)}</span>` : ''}</div>`,
  grid: b => {
    const n = b.head ? b.head.length : Math.max(...b.rows.map(r => (r.cells || [0]).length));
    const w = b.w || Array(n).fill(1);
    let h = `<div class="grid" style="grid-template-columns:${b.kw_mm || 20}mm ${w.map(x => x + 'fr').join(' ')}">`;
    if (b.head) h += '<div></div>' + b.head.map(x => `<div class="gh">${mk(x)}</div>`).join('');
    b.rows.forEach(r => {
      const dk = r.res ? ' rk' : '', lt = r.res ? ' rc' : '';
      h += `<div class="gk${dk}">${String(r.k || '').split('/').map(mk).join('<br>')}</div>`;
      if (r.span !== undefined) { const c = normCell(r.span); h += `<div class="gc sp${lt}${c.c ? ' c' : ''}">${cellInner(c)}</div>`; }
      else r.cells.forEach(x => { const c = normCell(x); h += `<div class="gc${lt}${c.c ? ' c' : ''}">${cellInner(c)}</div>`; });
    });
    return h + '</div>';
  },
  flow: b => {
    const items = b.items.map(x => `<div class="fi"><div class="fh">${x.tag ? `<span class="tag dk">${esc(x.tag)}</span>` : ''}${mk(x.h)}</div>${x.b ? `<div class="fb">${ul(x.b)}</div>` : ''}</div>`)
      .join(`<div class="fs">${esc(b.sep || '+')}</div>`);
    const r = b.res ? [].concat(b.res) : null;
    return `<div class="flow">${items}</div>${r ? `<div class="fdown">▼</div><div class="fres">${mk(r[0])}${r[1] ? `<small>${mk(r[1])}</small>` : ''}</div>` : '<div style="height:2.4mm"></div>'}`;
  },
  strip: b => `<div class="strip">${b.items.map(i => `<figure>${i.src && fs.existsSync(path.resolve(baseDir, i.src)) ? `<img src="${imgData(i.src)}" style="height:${b.h_mm || 22}mm">`
    : `<div class="phimg" style="height:${b.h_mm || 22}mm">${esc(i.label || '사진')}</div>`}${i.caption ? `<figcaption>${mk(i.caption)}</figcaption>` : ''}</figure>`).join('')}</div>`,
  boxes: b => `<div class="row">${b.items.map(x => `<div class="box"><div class="hd">${mk(x.h)}</div><div class="bd">${ul(x.b)}</div></div>`).join('')}</div>`,
  kv: b => `<div class="kv"><div class="k">${String(b.k).split('/').map(esc).join('<br>')}</div><div class="v${b.inner ? '' : ' serif'}">${
    b.text ? mk(b.text) : ''}${b.b ? ul(b.b) : ''}${b.ar ? `<div class="arrow serif">${mk(b.ar)}</div>` : ''}${[].concat(b.img || []).map(figure).join('')}${b.inner ? b.inner.map(render).join('') : ''}</div></div>`,
  banner: b => `<div class="banner">${mk(b.text)}</div><div style="height:2.4mm"></div>`,
  chev: b => `<div class="chev serif">${b.st.map(s => `<div class="st${s.on ? ' on' : ''}"><div class="h">${mk(s.h)}</div><div class="t">${s.t.map(x => '· ' + mk(x)).join('<br>')}</div></div>`).join('')}</div>`,
  check: b => `<div class="check" style="margin-top:1.4mm">✓ ${mk(b.text)}</div>`,
  comb: b => `<div class="comb serif">${b.cards.map(c => `<div class="c"><div class="hd">${mk(c.h)}</div><div class="bd">${ul(c.b, 'b')}</div></div>`).join('<div class="plus">+</div>')}<div class="eq">=</div><div class="res">${mk(b.res[0])}<br>${mk(b.res[1] || '')}<small>${mk(b.res[2] || '')}</small></div></div>`,
  line: b => `<div class="line"><div class="k">${mk(b.k)}</div><div class="v serif">${mk(b.v)}</div></div>`,
  cmp: b => `<div class="cmp serif"><div class="c"><div class="h"><span class="tag">${esc(b.a.tag)}</span>${mk(b.a.h)}</div>${ul(b.a.b, 'b')}</div><div class="ar">➡</div><div class="c on"><div class="h"><span class="tag dk">${esc(b.b.tag)}</span>${mk(b.b.h)}</div>${ul(b.b.b, 'b')}</div></div>`,
  bl: b => ul(b.b),
  text: b => `<div class="txtblk serif">${(b.p || []).map(x => `<p>${mk(x)}</p>`).join('')}</div>`,
  eff: b => `<div class="eff"><div class="top"><div class="k">${mk(b.k)}</div><div class="v">${mk(b.v)}</div></div><ul class="serif">${b.rows.map(r => `<li><span>· ${mk(r[0])}</span><span>${mk(r[1])}</span></li>`).join('')}</ul></div>`,
  res: b => `<div class="res-box"><div class="k">${String(b.label || cfg.labels.result).split('/').map(esc).join('<br>')}</div><div class="v serif">${ul(b.b)}</div></div>`,
  kpi: b => `<div class="kpi">${b.items.map(x => `<div><b>${mk(x.v)}</b><span>${mk(x.l)}</span></div>`).join('')}</div>`,
  tbl: b => `<table class="tb serif"><colgroup>${b.w.map(w => `<col style="width:${w * 100}%">`).join('')}</colgroup><tr>${b.head.map(h => `<th>${mk(h)}</th>`).join('')}</tr>${b.rows.map(r => `<tr>${r.map((c, i) => `<td${i === 0 ? ' class="f"' : ''}>${mk(c)}</td>`).join('')}</tr>`).join('')}</table>`,
  cols: b => { const w = b.w || b.cols.map(() => 1 / b.cols.length);
    return `<div class="cols">${b.cols.map((col, i) => `<div style="flex:${w[i]}">${col.map(render).join('')}</div>`).join('')}</div>`; },
  img: b => `<div class="img">${figure({ ...b, pos: 'below' })}</div>`,
};
function render(b, i) {
  if (!R[b.t]) throw new Error(`알 수 없는 블록 타입: ${b.t}`);
  return R[b.t](b, i);
}

// ---- 쪽 머리말·쪽번호·옆탭 (config.layout). 짝수 쪽=왼쪽 면, 홀수 쪽=오른쪽 면
function chrome(p, i) {
  if (p.footer) return `<div class="footer ${p.align === 'left' ? 'l' : 'r'}">${esc(p.footer)}</div>`;
  const L = cfg.layout; if (!L) return '';
  const n = (L.page_start || 1) + i, even = n % 2 === 0;
  let s = '';
  if (p.header !== false) {
    if (even && L.chapter) s += `<div class="ph even">${L.chapter.no ? `<span class="no">${esc(L.chapter.no)}</span>` : ''}<span class="tt">${esc(L.chapter.text || '')}</span></div>`;
    if (!even && L.running) s += `<div class="ph odd"><span class="tt">${esc(L.running)}</span></div>`;
  }
  if (L.page_numbers !== false) s += even
    ? `<div class="pf even"><span class="pn">${n}</span>${L.org ? `<span class="sep"></span><span class="org">${esc(L.org)}</span>` : ''}</div>`
    : `<div class="pf odd">${L.slogan ? `<span class="slogan">${esc(L.slogan)}</span><span class="sep"></span>` : ''}<span class="pn">${n}</span></div>`;
  if (!even && L.sidetab) s += `<div class="stab"><div class="t">${esc(L.sidetab)}</div><div class="k"></div></div>`;
  return s;
}

const extra = `
:root{--ink:${cfg.theme.ink};--g1:${cfg.theme.g1};--g2:${cfg.theme.g2};--g3:${cfg.theme.g3};--g4:${cfg.theme.g4};
--sans:"${cfg.fonts.sans}","Malgun Gothic",sans-serif;--serif:"${cfg.fonts.serif}","Batang",serif}
.vision{background:var(--g4);color:#fff;font-weight:900;font-size:10.6pt;text-align:center;padding:1.5mm;border-radius:1.4mm;margin-bottom:2mm}
.vision span{border:1px solid #fff;font-size:8.4pt;padding:0 1.6mm;margin-right:3mm;vertical-align:1px}
.kpi{display:flex;gap:1.6mm;margin-bottom:2.4mm}
.kpi>div{flex:1;border:.8px solid var(--g3);border-top:2.4px solid var(--g4);border-radius:1mm;text-align:center;padding:1.3mm 1mm}
.kpi b{display:block;font-size:15pt;font-weight:900;line-height:1.15}
.kpi span{font-size:8.4pt;color:#444}
.tb{width:100%;border-collapse:collapse;margin-bottom:2.4mm;font-size:9.3pt;table-layout:fixed}
.tb th{background:var(--g2);font-family:var(--sans);font-weight:700;border:.8px solid var(--g3);padding:1mm;font-size:9.4pt}
.tb td{border:.8px solid var(--g3);padding:1mm 1.8mm;vertical-align:middle}
.tb td.f{font-family:var(--sans);font-weight:700;background:var(--g1);font-size:9.2pt}
.kv .v .tb,.kv .v .kpi,.kv .v .grid{margin-bottom:1.2mm}
.txtblk{margin-bottom:2.4mm;font-size:10pt}.txtblk p{margin-bottom:1.2mm;text-indent:2mm}
.cols{display:flex;gap:2.4mm;align-items:flex-start}.cols>div{min-width:0}
.img{margin:1mm 0 2.4mm}
`;
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${esc(C.title || 'report')}</title><style>${css}${extra}</style></head><body>
${C.pages.map((p, i) => `<section class="page">${p.blocks.map(render).join('\n')}${chrome(p, i)}</section>`).join('\n')}
</body></html>`;
fs.writeFileSync(out, html);
console.log('ok:', out);
