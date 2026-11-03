# content.json과 결과물 만들기

PDF·Word 또는 `content.json`이 필요할 때만 읽는다.

## 1. `content.json` 규격

최상위는 `{title,config?,pages:[{header?,footer?,align?,blocks:[]}]}`다. `config`는 선택이다.

- `layout`: `{page_start,chapter:{no,text},running,org,slogan,sidetab,page_numbers?}`
- `theme`: `{ink,g1,g2,g3,g4}`, `fonts`: `{sans,serif,docx_sans,docx_serif}`, `labels`: `{result,key,best:[2개]}`
- 쪽별 `header:false`는 머리말을 끄고, `footer`와 `align:"left|right"`는 별도 바닥글을 쓴다.

내용 성격으로 블록을 고르고 아래 필드만 사용한다. `?`는 선택이다.

| `t` | 필드 |
|---|---|
| `title` | `text` |
| `ev` | `label,text` |
| `key` | `text,label?` |
| `bp` | `items:[2개],label?:[2개]` — B에 실제 상자가 있을 때만 |
| `vision` | `k,text` — B에 실제 띠가 있을 때만 |
| `sec` | `no,title,tag?` |
| `sub` | `title,tag?` |
| `grid` | `rows:[{k,cells 또는 span,res?}],head?,w?,kw_mm?` |
| `flow` | `items:[{tag,h,b:[]}]` 2~4개, `sep?,res?:[제목,보조]` |
| `chev` | `st:[{h,t:[],on?}]` 3~4단 |
| `kv` | `k`, `text` 또는 `b:[]`, `ar?,img?,inner?` |
| `boxes` | `items:[{h,b:[]}]` 2~3개 |
| `banner`,`check` | `text` |
| `comb` | `cards:[{h,b:[]}],res:[]` |
| `cmp` | `a:{tag,h,b:[]},b:{tag,h,b:[]}` |
| `line` | `k,v` |
| `kpi` | `items:[{v,l}]` 3~4개 |
| `tbl` | `w:[],head:[],rows:[[]]` |
| `eff` | `k,v,rows:[[내용,결과]]` |
| `bl` | `b:[]` |
| `text` | `p:[]` |
| `cols` | `cols:[[블록],[블록]],w?` |
| `strip` | `items:[그림],h_mm?` |
| `img` | 아래 그림 필드 |
| `res` | `b:[]` 3줄 이내, `label?` |

`grid` 칸은 문자열(가운데 굵은 글), 배열(목록), 또는 `{h,p,b:[],img,c?}`다. `inner`와 `cols` 안에는 같은 블록 객체를 넣는다.

- 실제 그림: `{src,h_mm,w_mm,pos,caption}`
- 표시 상자: `{label:"[이미지 삽입] 현장 적용 장면",h_mm:24,w_mm:34,pos:"right"}`
- 사진 띠: `{t:"strip",h_mm:22,items:[{src:"..."},{label:"[이미지 삽입] 현장 점검 장면"}]}`

텍스트 마크업은 `**굵게**`, `__밑줄+굵게__`, `[[테두리 상자]]`, `{{진한 상자}}`다. 목록의 `- `는 하위, `* `는 각주, `※ `는 참고다. 기존 블록을 쓸 때 렌더러 소스를 읽지 않는다.

## 2. 한 번에 렌더

```bash
python3 scripts/render_report.py content.json report --format both
```

필요한 형식만 요청받으면 `--format pdf` 또는 `--format docx`를 사용한다. Word 글자·간격 조정은 `--font-scale 1.17 --spacing-scale 1.65`를 시작값으로 한다. 스크립트는 JSON 구조를 먼저 검증하고 요청한 PDF·Word와 가능한 Word 변환 점검을 한 번에 실행한 뒤 짧은 JSON 요약만 출력한다.

오류가 없으면 개별 렌더러 소스를 읽지 않는다. 기존 블록으로 B를 표현할 수 없을 때만 `render_html.js`와 `render_docx.js` 양쪽에 같은 블록을 추가하고 둘 다 확인한다.

## 3. 지면·시각 점검

- 지정 쪽수를 정확히 맞춘다.
- PDF의 표·라벨·바닥글 잘림, Word 변환본의 겹침·줄바꿈을 페이지 이미지로 본다.
- PDF 쪽별 내용 하단은 약 960~1,055px(한계 1,065px), Word 변환본 채움은 0.80~0.91을 시작 범위로 삼는다.
- 글자 크기를 과도하게 줄이지 않는다. 넘치면 `visuals.md`의 제거 순서와 C등급·중복 내용을 따른다.
- 사용 가능한 원자료 그림이 이유 없이 빠지지 않았는지, `[이미지 삽입]`이 필요한 장면을 구체적으로 알리는지 확인한다.

코드를 실행할 수 없으면 같은 스토리라인을 Markdown 표 지면안으로 내고, 실제 그림은 `[그림: 원본 파일 p.쪽 — 내용·위치]`, 표시 상자는 `[이미지 삽입 필요: 필요한 장면 — 위치]`로 쓴다.
