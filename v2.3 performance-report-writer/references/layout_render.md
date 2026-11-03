# content.json과 결과물 만들기

PDF·Word 또는 `content.json`이 필요할 때만 읽는다.

## 1. 블록과 그림 필드

| 목적 | 블록 |
|---|---|
| 제목·평가내용·핵심성과 | `title`, `ev`, `key` |
| 대·중제목 | `sec`, `sub` |
| 라벨 칸 표 | `grid` |
| 단계·로드맵 | `flow`, `chev` |
| 배경·비교·대표 수치 | `boxes`, `cmp`, `kpi` |
| 여러 과제·요약 표 | `tbl` |
| 한 줄·일반 문장 | `kv`, `line`, `bl`, `text` |
| 좌우 배치 | `cols` |
| 그림·표시 상자 | 칸 안 `img`, `strip` |
| 섹션 마무리 | `res` |

`grid`는 `head`, `w`, `kw_mm`, `rows`를 쓴다. 행은 `k`, `cells` 또는 `span`, 필요하면 `res:true`를 가진다. 칸은 문자열·목록 또는 `{h,p,b,img,c}` 객체다.

- 실제 그림: `{src,h_mm,w_mm,pos,caption}`
- 표시 상자: `{label:"[이미지 삽입] 현장 적용 장면",h_mm:24,w_mm:34,pos:"right"}`
- `strip`: `{t:"strip",h_mm:22,items:[{src:"..."},{label:"[이미지 삽입] 현장 점검 장면"}]}`

텍스트 마크업은 `**굵게**`, `__밑줄+굵게__`, `[[테두리 상자]]`, `{{진한 상자}}`다. 목록의 `- `는 하위, `* `는 각주, `※ `는 참고다. 다른 구조는 `assets/content_template.json`과 렌더러가 이미 쓰는 블록을 확인한다.

## 2. 한 번에 렌더

```bash
python3 scripts/render_report.py content.json report --format both
```

필요한 형식만 요청받으면 `--format pdf` 또는 `--format docx`를 사용한다. Word 글자·간격 조정은 `--font-scale 1.17 --spacing-scale 1.65`를 시작값으로 한다. 스크립트는 요청한 PDF·Word와 가능한 Word 변환 점검을 한 번에 실행하고 짧은 JSON 요약만 출력한다.

오류가 없으면 개별 렌더러 소스를 읽지 않는다. 기존 블록으로 B를 표현할 수 없을 때만 `render_html.js`와 `render_docx.js` 양쪽에 같은 블록을 추가하고 둘 다 확인한다.

## 3. 지면·시각 점검

- 지정 쪽수를 정확히 맞춘다.
- PDF의 표·라벨·바닥글 잘림, Word 변환본의 겹침·줄바꿈을 페이지 이미지로 본다.
- PDF 쪽별 내용 하단은 약 960~1,055px(한계 1,065px), Word 변환본 채움은 0.80~0.91을 시작 범위로 삼는다.
- 글자 크기를 과도하게 줄이지 않는다. 넘치면 `visuals.md`의 제거 순서와 C등급·중복 내용을 따른다.
- 사용 가능한 원자료 그림이 이유 없이 빠지지 않았는지, `[이미지 삽입]`이 필요한 장면을 구체적으로 알리는지 확인한다.

코드를 실행할 수 없으면 같은 스토리라인을 Markdown 표 지면안으로 내고, 실제 그림은 `[그림: 원본 파일 p.쪽 — 내용·위치]`, 표시 상자는 `[이미지 삽입 필요: 필요한 장면 — 위치]`로 쓴다.
