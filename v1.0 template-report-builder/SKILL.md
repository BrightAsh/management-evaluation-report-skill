---
name: "template-report-builder"
description: "양식(PDF·HWPX·이미지·작성 가이드라인)과 작성 자료를 함께 받으면 역할을 판별해 그 양식대로 보고서 지면(경영실적보고서 등)을 작성하고 PDF·Word로 만든다."
---

# 양식 기반 보고서 자동 작성

사용자가 **양식 파일**(PDF·HWPX·HWP·DOCX·이미지 샘플 지면, 또는 작성 가이드라인)과 **작성 자료**(실적 원문 PDF·HWP·HWPX·엑셀 등)를 한꺼번에 첨부한다. 각 파일의 역할을 판별하고, 그 양식대로 지정 쪽수의 보고서 지면을 만들어 **PDF(최종 지면) + Word(.docx, 편집용)**로 제공한다. 사용자가 원하면 Word를 한글에서 열어 HWPX로 저장하도록 안내한다(HWPX 직접 생성은 박스·표가 깨지기 쉬워 기본값으로 하지 않는다).

대표 용도: 한국석유공사 경영실적보고서 평가내용별 실적 페이지. 다른 보고서 양식에도 같은 절차를 쓴다.

---

## 1단계. 첨부 판별 (가장 먼저)

모든 첨부의 앞 2~3쪽, 목차, 제목, 머리말·바닥글을 읽는다. 양식 후보는 **반드시 이미지로 렌더해서 직접 본다**.

| 역할 | 판별 단서 |
|---|---|
| 양식 샘플 | 완성된 지면. 짧고(1~6쪽) 박스·흐름도·표 중심. 다른 기관·다른 연도 실적이거나 '예시' 표기 |
| 작성 가이드라인 | 작성요령·유의사항. 쪽수·글자 크기·여백·필수 항목·금지 사항 규정 문장 |
| 평가 편람 | 지표명·가중치·평가방법·세부평가내용 |
| 작성 자료 | 우리 기관 실적: 계획안, 결과보고, 증빙, 보도자료, 메모, 엑셀 과제 목록 |

- 한 파일에 역할이 섞여 있으면 쪽 범위별로 나눠 분류한다.
- 첫 답변에 **판별표(파일 | 역할 | 근거 한 줄)**를 보이고 바로 진행한다. 판단이 크게 갈리는 파일만 짧게 묻는다. 묻지 못하는 상황이면 가장 그럴듯한 판단으로 진행하고 그렇게 했다고 밝힌다.
- **우선순위: 사용자 메시지 지시 > 가이드라인 규정 > 양식 샘플 > 이 스킬의 기본 양식(부록 A).**
- 양식이 하나도 없으면 기본 양식(한국전력공사 경영실적보고서 스타일, 부록 A)을 쓴다.

## 2단계. 파일 읽기 (끝까지 전부)

- **PDF**: `pdftotext -layout f.pdf out.txt` → 연속 공백 압축, 빈 줄 제거 → 구간을 나눠 처음부터 끝까지 읽는다. `- 23 -` 같은 쪽 표시와 `□ ○ 실적①` 제목줄로 구조부터 파악한다. 양식이면 `pdftoppm -r 70 -png`로 렌더해 본다.
- **HWPX**: zip이다. `Contents/section*.xml`의 `<hp:t>` 텍스트를 순서대로 모으고, 표는 `<hp:tbl>`→`<hp:tr>`→`<hp:tc>` 구조로 읽는다. `Preview/PrvImage.png`(첫 쪽 미리보기)가 있으면 양식 모양 확인에 쓴다. 미리보기가 없으면 LibreOffice로 PDF 변환을 시도하고, 실패하면 XML 구조(표 칸 배치, 글꼴 크기 `charPr`, 테두리 `borderFill`)로 양식을 재구성한다.
- **HWP(5.0)**: `olefile`로 `BodyText/Section*` 스트림을 연다. FileHeader 압축 플래그가 있으면 `zlib.decompress(data, -15)`로 푼다. 레코드 태그 67(PARA_TEXT)을 UTF-16LE로 디코드한다. 깨진 글머리표는 무시한다.
- **DOCX**: `pandoc -t markdown`. **엑셀**: openpyxl `data_only=True`로 전 시트·전 행을 덤프한다. 비고란도 읽는다.
- **이미지**: 직접 본다.
- 다운로드·업로드 파일은 각자 새 폴더에 두고, 파이썬은 `-I`로 실행한다.

## 3단계. 양식·가이드라인 분석 → 양식 명세

1. **가이드라인 제약 목록**: 쪽수 상한, 최소 글자 크기, 여백, 용지, 필수 항목(예: 외부 지적사항 조치실적), 목차 순서, 금지 사항을 뽑는다. 작업 내내 지키고 납품 전에 항목별로 점검한다.
2. **양식 명세 md**를 만든다. 순서: 위계도 → 블록별 형식(원문 예시 포함) → 문체·표기 → 색·선·글꼴·크기 → 빈 템플릿 → 체크리스트. 샘플이 텍스트 PDF면 실제 문구·기호도 확인한다. 이 md는 결과물과 함께 준다(다음 작업에 재사용).
3. 양식 요소를 부록 B 렌더러의 블록에 매핑한다.
   - 매핑되는 요소는 그대로 쓰고, 색·선·글꼴·크기만 `base.css`와 `render_docx.js` 상단 상수(INK·G1~G4·SANS·SERIF·크기)를 양식에 맞게 고친다.
   - 매핑되지 않는 요소(2단 본문, 원형 지표, 사진 자리, 연도별 막대 등)는 **새 블록 타입을 render_html.js와 render_docx.js 양쪽에 함께 추가**한다. 그림이 꼭 필요하면 HTML 요소를 Playwright로 캡처(device_scale_factor 4)해 docx에 ImageRun으로 넣는다.
4. 쪽수: 사용자 지정 > 가이드라인 상한 > 양식 샘플 쪽수 > 2쪽.
5. 양식 샘플이 여러 개면 공통 요소는 따르고, 서로 다르면 최신·우리 기관 것 > 사용자가 언급한 것 순으로 고른다.

## 4단계. 작성 자료 통합

1. **자료 목록표**: 파일 | 성격(계획/결과보고/증빙/엑셀) | 작성 시점 | 다루는 실적.
2. **커버리지 표**: 편람 세부 항목(또는 평가 축) × 근거 자료. 비는 항목은 '자료 부족'으로 보고하고 지어내지 않는다.
3. **수치 충돌**: 결과보고 > 평가 제출본 > 계획안 순으로, 같은 단계면 작성일이 최신인 값을 쓴다. 채택하지 않은 값은 확인 사항에 적는다.
4. 실적기간(예: '25.11~'26.9) 밖은 제외한다. 같은 사실은 한 번만, 가장 구체적인 수치로 쓴다.
5. 자료 안에 분류가 있으면(예: 엑셀 '생산성 14·안전 7·대국민 1') 그대로 따른다.
6. 소재 우선순위: 편람 직결 > 정량 성과(단축률·절감액·건수·이용자) > 외부 인정(수상·정부 선정·보도) > 협업·확산. 약한 소재는 빼고, 뺀 것은 보고한다.

## 5단계. 쪽 구성 (기본 양식 기준. 첨부 양식이 다르면 그 위계를 따른다)

- 헤더는 편람 문구를 원문 그대로 쓴다. 편람의 세부 축을 대제목(1, 2, 3…)의 뼈대로 삼는다.
- 지정 사업(예: 혁신프로젝트)은 BEST PRACTICE ①②로 올리고 대제목 태그 `B.P①` `B.P②`를 붙인다.
- 쪽당 대제목 1~2개. 첫 쪽만 헤더 + BEST PRACTICE.
- 대제목마다 **왜**(배경 3단: 국정과제/대외환경/기관전략 + 문제점 ➡ 결론) → **무엇을**(추진내용) → **그래서**(추진성과) 순으로 쓴다.
- 작은 대제목은 추진방향 → 추진내용 → 추진성과의 3블록. 큰 대제목은 가·나·다 중제목으로 나눈다.
- **모든 대제목은 추진성과 박스(3줄 이내: 외부 인정 → 확정된 활용 → 확산)로 끝난다.**
- 예시 배치: 2쪽 = [헤더·BP·대제목1(풀 블록)] / [대제목2(3블록) + 대제목3(가·나)]. 5쪽 = 추진기반 / 생산성 / 안전(B.P①) / 대국민(B.P②) / 역량·종합성과·향후계획.

## 6단계. 내용 데이터 작성 (content.js 하나)

내용은 **하나의 데이터 파일**에만 쓴다. PDF와 Word는 둘 다 이 파일에서 만든다. 수정 요청이 오면 이 파일만 고쳐 두 파일을 다시 만든다. 블록 종류와 필드는 부록 B의 예시 데이터를 보고 쓴다.

- 마크업: `**굵게**`, `__밑줄+굵게__`(추진성과 최고 수치만), `[[연한 태그]]`, `{{진한 태그}}`
- 문체: 개조식 명사형 종결(~구축, ~확대, ~달성). '~다' 금지. 제목은 '수단 + 으로 + 결과'. 1불릿 1줄(최대 2줄). 박스당 2~3줄로 글을 최소화한다.
- 표기: '26.9 / (전년대비 70종↑) / 79%↓ / 20분→26.8초 / 64개社 / 多 / 全. 결론은 ➡, 흐름·변화는 →.
- 흐름도는 올해 단계만 on:true. 추진경과는 → 로 이은 한 줄.
- 바닥글: 짝수쪽 왼쪽 `n │ 기관명`, 홀수쪽 오른쪽 `○○년도 경영실적보고서 │ n`(양식에 따라 바꾼다).

## 7단계. 렌더링

부록 B의 파일들을 작업 폴더에 그대로 저장한 뒤 실행한다.

```bash
npm ls docx >/dev/null 2>&1 || npm install docx
node render_html.js content.js 보고서.html
python3 to_pdf.py 보고서.html                         # → 보고서.pdf + 쪽별 내용 하단(px)
node render_docx.js content.js 보고서.docx 1.17 1.65   # 글자배율 1.13~1.24, 간격배율 1.5~2.0
cp 보고서.docx t.docx && soffice --headless --convert-to pdf t.docx   # Word 점검용(파일명은 영문으로)
python3 fill_check.py t.pdf
```

- Playwright가 없으면 Word를 PDF로 변환한 결과를 PDF로 낸다.
- docx 스킬이 있으면 그 validate.py로 검증한다.

## 8단계. 지면 맞춤·검증 (필수)

- 쪽수가 지정 쪽수와 정확히 같아야 한다(`pdfinfo`).
- PDF는 쪽별 내용 하단이 약 900~1,040px여야 한다(한계 1,075px). Word는 쪽별 채움 0.80~0.91로 맞춘다. 사용자 PC의 맑은 고딕·바탕이 대체 글꼴보다 넓을 수 있으므로 5~10% 여유를 둔다.
- 빈칸이 남으면 글자를 키우지 말고 원문 소재(전후 비교, KPI 타일, 기대효과, 과제표)를 더 넣는다. 넘치면 근거가 약한 블록을 뺀다.
- 렌더한 쪽을 이미지로 직접 보고 확인한다: 태그 잘림, '추진성과' 라벨 줄바꿈, 흐름도·표 칸 넘침, 바닥글 겹침.
- 블록 함수가 배열을 반환하면 펼쳐서 넣는다(중첩 배열은 XML `<0/>` 오류를 낸다).
- **모든 수치·날짜를 원문 텍스트에서 grep으로 대조한다.** 다른 대화·자료에서 가져온 수치는 출처를 밝힌다.
- 가이드라인 규정을 항목별로 점검한다.

## 9단계. 사실성 규칙 (최우선)

1. 원문에 없는 수치·사실은 만들지 않는다. 모르는 값(국정과제 번호, 쪽번호 등)은 ○○으로 비우고 보고한다.
2. 계획서에 있는 일은 '착수·추진'으로 쓰고 '완료'라고 쓰지 않는다. 목표·추정치에는 (목표)·(추정)·'예상'을 붙인다.
3. 원문이 미완('??', '상세 미확보')이면 넣지 않고 보고한다.
4. 성격 태그(지적반영 등)는 근거가 있을 때만 쓴다. 근거가 없으면 중립 태그(수요 기반, 현업 발굴)를 쓰고 보고한다.
5. 연도·쪽번호를 추정했으면 밝힌다.

## 10단계. 답변 형식

PDF·docx와 양식 명세 md(새 양식일 때)를 첨부한다. 본문은 다음만 쓴다.
1. 한 줄 요약(쪽수, 기준 양식)
2. 쪽별 구성표(쪽 | 내용 | 핵심 수치)
3. 자료 사용 내역(쓴 것, 뺀 것과 이유)
4. 가이드라인 준수 점검(가이드라인이 첨부된 경우)
5. 확인 필요 사항: 계획/완료 불확실, 수치 충돌, 추정치, 임의로 정한 태그·쪽번호·연도, ○○, 자료 부족

후속 요청:
- 추가 자료가 오면 전부 읽고 기존 분류에 넣는다. 정량 성과가 큰 순으로 반영하고, 쪽수를 유지하며 종합성과까지 갱신한다.
- 문구 수정은 content.js만 고쳐 다시 생성한다.

---

## 부록 A. 기본 양식 요약 (양식이 첨부되지 않았을 때)

- A4. 여백 상 11mm, 좌우 12mm. 흑백 계열(잉크 #1A1A1A, 회색 #F2F2F2·#E3E3E3·#BDBDBD·#7A7A7A).
- 글꼴: 제목·라벨은 고딕(맑은 고딕), 본문은 명조(바탕).
- 위계: 평가내용 헤더(라벨 + 편람 문구) → BEST PRACTICE(①② 2줄) → 대제목 바(검정 번호칸 + 연회색 바 + 오른쪽 B.P 태그) → 중제목(가·나 + 오른쪽 성격 태그) → 블록들 → 추진성과(검정 라벨 + 굵은 테두리).
- 블록: 배경 3단 박스, 좌측 라벨 박스(문제점·추진방향·목적·추진내용·향후계획), 전환 배너(▼), 단계 흐름도(올해 반전), 결합 카드(A + B + C = 결과), 기존→확대 비교, ✓ 헤드라인, 한 줄 라벨(추진경과·공사주도·참여기관), KPI 숫자 타일, 표(AS-IS/TO-BE·과제표·종합성과), 기대효과(대표 수치 + ➡ 결과 3줄), 추진성과.

## 부록 B. 렌더러와 예시 데이터

아래 파일을 **이름 그대로** 작업 폴더에 저장해 쓴다. 새 양식이면 사본을 만들어 고친다.


### 파일: base.css

```css

@page{size:A4;margin:0}
:root{--ink:#1a1a1a;--navy:#1f3a5f;--g1:#f2f2f2;--g2:#e3e3e3;--g3:#bdbdbd;--g4:#7a7a7a;--acc:#c0392b}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Sans CJK KR",sans-serif;color:var(--ink);font-size:10.0pt;line-height:1.42;background:#fff}
.page{width:210mm;height:297mm;padding:11mm 12mm 9mm;position:relative;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.serif{font-family:"Noto Serif CJK KR",serif}
b,strong{font-weight:700}
u{text-decoration:underline;text-underline-offset:2px}
/* header */
.evhead{display:flex;border:1.2px solid var(--ink);margin-bottom:2.97mm}
.evhead .lab{background:var(--g2);font-weight:900;font-size:12.2pt;padding:2.70mm 4.73mm;display:flex;align-items:center;white-space:nowrap;border-right:1.2px solid var(--ink)}
.evhead .txt{padding:2.16mm 4.05mm;font-size:11.1pt;font-weight:500;display:flex;align-items:center}
.bp{display:flex;align-items:stretch;border:1px solid var(--g3);margin-bottom:3.51mm}
.bp .lab{background:var(--g4);color:#fff;font-weight:900;font-size:11.6pt;line-height:1.05;padding:2.03mm 4.05mm;display:flex;flex-direction:column;justify-content:center;text-align:center}
.bp .lab small{font-size:7.2pt;font-weight:500;letter-spacing:.5px}
.bp ul{list-style:none;padding:1.89mm 4.05mm;font-size:10.2pt;font-weight:500}
.bp b{font-weight:900}
/* section title */
.sec{display:flex;align-items:center;background:var(--g1);border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);margin:3.24mm 0 2.70mm}
.sec .no{background:var(--ink);color:#fff;font-weight:900;font-size:15.1pt;width:9mm;text-align:center;padding:1.08mm 0}
.sec .tt{flex:1;font-weight:900;font-size:13.9pt;padding:0 4.05mm;letter-spacing:-.3px}
.tag{display:inline-block;text-indent:0;border:1px solid var(--ink);background:#fff;font-size:8.1pt;font-weight:700;padding:0 1.89mm;border-radius:1mm;margin-right:2mm;white-space:nowrap}
.tag.dk{background:var(--ink);color:#fff}
.sub{font-weight:900;font-size:11.8pt;margin:2.97mm 0 1.89mm;display:flex;justify-content:space-between;align-items:center;letter-spacing:-.3px}
/* generic boxes */
.row{display:flex;gap:2.70mm;margin-bottom:2.43mm}
.box{border:1px solid var(--g3);flex:1}
.box .hd{background:var(--g2);text-align:center;font-weight:700;font-size:10.0pt;padding:0.94mm 0;border-bottom:1px solid var(--g3)}
.box .bd{padding:1.62mm 2.70mm}
.kv{display:flex;border:1px solid var(--g3);margin-bottom:2.43mm}
.kv .k{background:var(--g2);font-weight:700;width:17mm;display:flex;align-items:center;justify-content:center;text-align:center;border-right:1px solid var(--g3);font-size:9.7pt;padding:1.35mm}
.kv .v{flex:1;padding:1.62mm 3.24mm}
ul.b{list-style:none}
ul.b>li{padding-left:2.6mm;text-indent:-2.6mm}
ul.b>li:before{content:"· "}
ul.d{list-style:none;padding-left:2.6mm}
ul.d>li{padding-left:2.4mm;text-indent:-2.4mm;font-size:9.5pt}
ul.d>li:before{content:"- "}
.arrow{font-weight:700}
.banner{text-align:center;background:linear-gradient(90deg,#fff,var(--g2) 15%,var(--g2) 85%,#fff);font-weight:900;font-size:10.9pt;padding:1.35mm 0;margin:0 0 2.43mm;position:relative}
.banner:after{content:"";position:absolute;left:50%;bottom:-2mm;transform:translateX(-50%);border:2mm solid transparent;border-top-color:var(--g2);border-bottom:0}
.tag-ttl{font-weight:700;font-size:9.3pt;display:inline-block;background:var(--ink);color:#fff;padding:0.27mm 2.16mm;margin-right:1.5mm}
/* chevrons */
.chev{display:flex;gap:0;margin-bottom:1.62mm}
.chev .st{flex:1;position:relative}
.chev .st .h{background:var(--g2);font-weight:700;text-align:center;padding:1.22mm 5.40mm 1.22mm 6.75mm;font-size:9.6pt;clip-path:polygon(0 0,calc(100% - 3mm) 0,100% 50%,calc(100% - 3mm) 100%,0 100%,3mm 50%)}
.chev .st:first-child .h{clip-path:polygon(0 0,calc(100% - 3mm) 0,100% 50%,calc(100% - 3mm) 100%,0 100%)}
.chev .st.on .h{background:var(--ink);color:#fff}
.chev .st .t{padding:1.35mm 2.16mm 0 2.70mm;font-size:9.3pt}
/* combine cards */
.comb{display:flex;align-items:stretch;gap:1.35mm;margin:1.62mm 0 1.89mm}
.comb .c{flex:1;border:1px solid var(--g3)}
.comb .c .hd{background:#fff;border-bottom:1px dashed var(--g3);text-align:center;font-weight:900;font-size:10.0pt;padding:0.81mm 0}
.comb .c .bd{padding:1.35mm 2.43mm;font-size:9.3pt}
.comb .plus{display:flex;align-items:center;font-weight:900;font-size:15.1pt;color:var(--g4)}
.comb .eq{display:flex;align-items:center;font-weight:900;font-size:13.9pt;color:var(--g4)}
.comb .res{flex:.9;background:var(--ink);color:#fff;display:flex;flex-direction:column;justify-content:center;text-align:center;font-weight:700;font-size:9.7pt;padding:1.35mm}
.comb .res small{font-weight:400;font-size:8.4pt;opacity:.85}
.line{display:flex;border:1px solid var(--g3);font-size:9.5pt;margin-bottom:1.08mm}
.line .k{background:var(--g2);font-weight:700;padding:0.81mm 2.70mm;white-space:nowrap;border-right:1px solid var(--g3)}
.line .v{padding:0.81mm 2.97mm}
.res-box{border:1.6px solid var(--ink);display:flex;margin-top:2.16mm}
.res-box .k{background:var(--ink);color:#fff;font-weight:900;width:17mm;display:flex;align-items:center;justify-content:center;text-align:center;font-size:10.4pt}
.res-box .v{flex:1;padding:1.76mm 3.51mm;font-weight:500}
.eff{border:1px solid var(--g3);margin-top:2.16mm}
.eff .top{display:flex;align-items:center;border-bottom:1px solid var(--g3)}
.eff .top .k{background:var(--g4);color:#fff;font-weight:900;padding:1.08mm 3.38mm;font-size:10.0pt}
.eff .top .v{padding:0.81mm 3.38mm;font-weight:700;font-size:10.2pt}
.eff ul{padding:1.35mm 3.38mm}
.eff li{display:flex;justify-content:space-between}
.eff li span:last-child{font-weight:700;white-space:nowrap;padding-left:2mm}
/* compare */
.cmp{display:flex;align-items:stretch;gap:2.03mm;margin:1.35mm 0 1.62mm}
.cmp .c{flex:1;border:1px solid var(--g3);padding:1.62mm 2.70mm}
.cmp .c.on{border:1.6px solid var(--ink)}
.cmp .c .h{font-weight:900;font-size:10.0pt;margin-bottom:0.81mm}
.cmp .ar{display:flex;align-items:center;font-size:16.2pt;font-weight:900;color:var(--g4)}
.check{font-weight:900;font-size:10.4pt;margin:0.54mm 0 0.54mm}
/* hub diagram */
.hub{display:grid;grid-template-columns:1fr 1.1fr 1fr;grid-template-rows:auto auto;gap:1.35mm 2.03mm;align-items:center;margin-top:1.62mm;font-size:8.8pt;text-align:center}
.hub .n{border:1px solid var(--g3);padding:1.08mm 0.68mm;border-radius:1mm;background:#fff}
.hub .n b{display:block;font-size:9.3pt}
.hub .c{grid-row:1/3;grid-column:2;background:var(--ink);color:#fff;border-radius:50%;aspect-ratio:1;display:flex;flex-direction:column;justify-content:center;font-weight:900;font-size:10.4pt;max-width:24mm;margin:auto;width:100%}
.hub .c small{font-weight:400;font-size:7.7pt}
.bars{display:flex;align-items:flex-end;gap:5.40mm;height:17mm;margin:1.35mm 0 0 2.70mm}
.bars .bar{width:9mm;background:var(--g3);position:relative;text-align:center;font-size:8.6pt}
.bars .bar.on{background:var(--ink)}
.bars .bar span{position:absolute;top:-3.6mm;left:0;right:0;font-weight:700}
.bars .bar em{position:absolute;bottom:-3.6mm;left:-2mm;right:-2mm;font-style:normal;font-size:8.1pt}
.footer{position:absolute;bottom:6mm;font-size:9.3pt;color:var(--g4);font-weight:700}
.footer.l{left:12mm}.footer.r{right:12mm}
.note{font-size:8.1pt;color:var(--g4)}

.bars{height:15mm;margin-bottom:4mm}.hub .c{max-width:27mm}
```

### 파일: render_html.js

```js
const fs = require('fs');
const C = require(require('path').resolve(process.argv[2] || './content.js'));
const css = fs.readFileSync(__dirname + '/base.css', 'utf8');

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const mk = s => esc(s)
  .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
  .replace(/__([^_]+)__/g, '<b><u>$1</u></b>')
  .replace(/\[\[([^\]]+)\]\]/g, '<span class="tag">$1</span>')
  .replace(/\{\{([^}]+)\}\}/g, '<span class="tag dk">$1</span>');
const ul = (arr, cls = 'b serif') => `<ul class="${cls}">${arr.map(x => `<li>${mk(x)}</li>`).join('')}</ul>`;

const R = {
  vision: b => `<div class="vision"><span>${mk(b.k)}</span>${mk(b.text)}</div>`,
  ev: b => `<div class="evhead"><div class="lab">${mk(b.label)}</div><div class="txt">${mk(b.text)}</div></div>`,
  bp: b => `<div class="bp"><div class="lab">BEST<small>PRACTICE</small></div><ul>${b.items.map(x => `<li>${mk(x)}</li>`).join('')}</ul></div>`,
  sec: (b, i) => `<div class="sec"${i === 0 ? ' style="margin-top:0"' : ''}><div class="no">${b.no}</div><div class="tt">${mk(b.title)}</div>${b.tag ? `<span class="tag dk">${b.tag}</span>` : ''}</div>`,
  sub: b => `<div class="sub"><span>${mk(b.title)}</span><span class="tag">${mk(b.tag)}</span></div>`,
  boxes: b => `<div class="row">${b.items.map(x => `<div class="box"><div class="hd">${mk(x.h)}</div><div class="bd">${ul(x.b)}</div></div>`).join('')}</div>`,
  kv: b => `<div class="kv"><div class="k">${b.k.split('/').join('<br>')}</div><div class="v${b.inner ? '' : ' serif'}">${
    b.text ? mk(b.text) : ''}${b.b ? ul(b.b) : ''}${b.ar ? `<div class="arrow serif">${mk(b.ar)}</div>` : ''}${b.inner ? b.inner.map(render).join('') : ''}</div></div>`,
  banner: b => `<div class="banner">${mk(b.text)}</div><div style="height:2.4mm"></div>`,
  chev: b => `<div class="chev serif">${b.st.map(s => `<div class="st${s.on ? ' on' : ''}"><div class="h">${mk(s.h)}</div><div class="t">${s.t.map(x => '· ' + mk(x)).join('<br>')}</div></div>`).join('')}</div>`,
  check: b => `<div class="check" style="margin-top:1.4mm">✓ ${mk(b.text)}</div>`,
  comb: b => `<div class="comb serif">${b.cards.map(c => `<div class="c"><div class="hd">${mk(c.h)}</div><div class="bd">${ul(c.b, 'b')}</div></div>`).join('<div class="plus">+</div>')}<div class="eq">=</div><div class="res">${mk(b.res[0])}<br>${mk(b.res[1])}<small>${mk(b.res[2])}</small></div></div>`,
  line: b => `<div class="line"><div class="k">${mk(b.k)}</div><div class="v serif">${mk(b.v)}</div></div>`,
  cmp: b => `<div class="cmp serif"><div class="c"><div class="h"><span class="tag">${b.a.tag}</span>${mk(b.a.h)}</div>${ul(b.a.b, 'b')}</div><div class="ar">➡</div><div class="c on"><div class="h"><span class="tag dk">${b.b.tag}</span>${mk(b.b.h)}</div>${ul(b.b.b, 'b')}</div></div>`,
  bl: b => ul(b.b),
  eff: b => `<div class="eff"><div class="top"><div class="k">${mk(b.k)}</div><div class="v">${mk(b.v)}</div></div><ul class="serif">${b.rows.map(r => `<li><span>· ${mk(r[0])}</span><span>${mk(r[1])}</span></li>`).join('')}</ul></div>`,
  res: b => `<div class="res-box"><div class="k">추진성과</div><div class="v serif">${ul(b.b)}</div></div>`,
  kpi: b => `<div class="kpi">${b.items.map(x => `<div><b>${mk(x.v)}</b><span>${mk(x.l)}</span></div>`).join('')}</div>`,
  tbl: b => `<table class="tb serif"><colgroup>${b.w.map(w => `<col style="width:${w * 100}%">`).join('')}</colgroup><tr>${b.head.map(h => `<th>${mk(h)}</th>`).join('')}</tr>${b.rows.map(r => `<tr>${r.map((c, i) => `<td${i === 0 ? ' class="f"' : ''}>${mk(c)}</td>`).join('')}</tr>`).join('')}</table>`,
};
function render(b, i) { return R[b.t](b, i); }

const extra = `
.vision{background:var(--ink);color:#fff;font-weight:900;font-size:10.6pt;text-align:center;padding:1.5mm;margin-bottom:2mm}.vision span{border:1px solid #fff;font-size:8.4pt;padding:0 1.6mm;margin-right:3mm;vertical-align:1px}
.kpi{display:flex;gap:2mm;margin-bottom:2.4mm}
.kpi>div{flex:1;border:1px solid var(--g3);border-top:2.4px solid var(--ink);text-align:center;padding:1.4mm 1mm}
.kpi b{display:block;font-size:15pt;font-weight:900;line-height:1.15}
.kpi span{font-size:8.4pt;color:#444}
.tb{width:100%;border-collapse:collapse;margin-bottom:2.4mm;font-size:9.3pt;table-layout:fixed}
.tb th{background:var(--g2);font-family:"Noto Sans CJK KR",sans-serif;font-weight:700;border:1px solid var(--g3);padding:1mm;font-size:9.4pt}
.tb td{border:1px solid var(--g3);padding:1mm 1.8mm;vertical-align:middle}
.tb td.f{font-family:"Noto Sans CJK KR",sans-serif;font-weight:700;background:var(--g1);font-size:9.2pt}
.kv .v .tb,.kv .v .kpi{margin-bottom:1.2mm}
`;
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${C.title}</title><style>${css}${extra}</style></head><body>
${C.pages.map(p => `<section class="page">${p.blocks.map(render).join('\n')}<div class="footer ${p.align === 'left' ? 'l' : 'r'}">${esc(p.footer)}</div></section>`).join('\n')}
</body></html>`;
fs.writeFileSync(process.argv[3] || 'out.html', html);
```

### 파일: render_docx.js

```js
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, VerticalAlign, Footer, TableLayoutType } = require('docx');
const CT = require(require('path').resolve(process.argv[2]));
const OUT = process.argv[3];
const F = parseFloat(process.argv[4] || '1.13');   // font scale
const SP = parseFloat(process.argv[5] || '1.5');   // spacing scale

const mm = x => Math.round(x * 56.7);
const W = mm(186);
const SANS = { ascii: 'Malgun Gothic', eastAsia: '맑은 고딕', hAnsi: 'Malgun Gothic' };
const SERIF = { ascii: 'Batang', eastAsia: '바탕', hAnsi: 'Batang' };
const INK = '1A1A1A', G1 = 'F2F2F2', G2 = 'E3E3E3', G3 = 'BDBDBD', G4 = '7A7A7A';
const SZ = 17;
const AL = AlignmentType;

function runs(text, o = {}) {
  const out = [], sz = Math.round((o.size || SZ) * F), tsz = Math.round(((o.size || SZ) - 3) * F);
  text.split(/(\*\*[^*]+\*\*|__[^_]+__|\[\[[^\]]+\]\]|\{\{[^}]+\}\})/g).filter(Boolean).forEach(t => {
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
  indent: o.hang ? { left: o.hang, hanging: o.hang } : undefined });
const B = (t, o = {}) => P('· ' + t, { hang: 150, ...o });
const Bs = (a, o) => a.map(t => B(t, o));
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

const R = {
  ev: (b, w) => T([[C(P(b.label, { font: SANS, bold: true, size: 20, align: AL.CENTER }), mm(26), { fill: G2, borders: bAll(ln(INK, 10)) }),
    C(P(b.text, { font: SANS, size: 19 }), w - mm(26), { borders: bAll(ln(INK, 10)), ml: 140 })]], [mm(26), w - mm(26)]),
  bp: (b, w) => T([[C([P('BEST', { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER, line: 220 }),
    P('PRACTICE', { font: SANS, size: 11, color: 'FFFFFF', align: AL.CENTER, line: 200 })], mm(20), { fill: G4 }),
    C(b.items.map(t => P(t, { font: SANS, size: 18 })), w - mm(20), { ml: 140 })]], [mm(20), w - mm(20)]),
  vision: (b, w) => T([[C(P(`[[${b.k}]] ${b.text}`, { font: SANS, bold: true, size: 20, color: 'FFFFFF', align: AL.CENTER }), w, { fill: INK, borders: NOB })]], [w]),
  sec: (b, w) => { const ws = [mm(10), w - mm(10) - (b.tag ? mm(20) : 0)]; if (b.tag) ws.push(mm(20));
    const tb = { top: ln(INK, 16), bottom: ln(INK, 6), left: NONE, right: NONE };
    const r = [C(P(b.no, { font: SANS, bold: true, size: 26, color: 'FFFFFF', align: AL.CENTER }), ws[0], { fill: INK, borders: tb }),
      C(P(b.title, { font: SANS, bold: true, size: 24 }), ws[1], { fill: G1, borders: tb, ml: 140 })];
    if (b.tag) r.push(C(P(`{{${b.tag}}}`, { size: 19, align: AL.RIGHT }), ws[2], { fill: G1, borders: tb }));
    return T([r], ws); },
  sub: (b, w) => T([[C(P(b.title, { font: SANS, bold: true, size: 20 }), w - mm(32), { borders: NOB, ml: 0 }),
    C(P(`[[${b.tag}]]`, { size: 19, align: AL.RIGHT }), mm(32), { borders: NOB, mr: 0 })]], [w - mm(32), mm(32)]),
  boxes: (b, w) => { const n = b.items.length, g = mm(2), cw = split(w, b.items.map(() => 1), g, n), ws = [], r1 = [], r2 = [];
    b.items.forEach((x, i) => { ws.push(cw[i]); r1.push(C(H(x.h), cw[i], { fill: G2 })); r2.push(C(Bs(x.b), cw[i], { v: VerticalAlign.TOP }));
      if (i < n - 1) { ws.push(g); r1.push(C(P(''), g, { borders: NOB })); r2.push(C(P(''), g, { borders: NOB })); } });
    return T([r1, r2], ws); },
  kv: (b, w) => { const iw = w - KW - 240; const kids = [];
    if (b.text) kids.push(P(b.text)); if (b.b) kids.push(...Bs(b.b)); if (b.ar) kids.push(P(`**${b.ar}**`));
    if (b.inner) b.inner.forEach((x, i) => { if (i) kids.push(gap(40)); const r = R[x.t](x, iw); Array.isArray(r) ? kids.push(...r) : kids.push(r); });
    if (b.inner) kids.push(gap(20));
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
  comb: (b, w) => { const pw = mm(5), rw = mm(28), cw = Math.floor((w - pw * 3 - rw) / 3), ws = [cw, pw, cw, pw, cw, pw, w - cw * 3 - pw * 3];
    const card = h => C(H(h, { size: 17 }), cw, { borders: { top: ln(), left: ln(), right: ln(), bottom: { style: BorderStyle.DASHED, size: 4, color: G3 } } });
    const sym = s => C(P(s, { font: SANS, bold: true, size: 26, color: G4, align: AL.CENTER }), pw, { borders: NOB, rowSpan: 2, ml: 0, mr: 0 });
    const body = a => C(Bs(a, { size: 16 }), cw, { borders: { top: NONE, left: ln(), right: ln(), bottom: ln() }, v: VerticalAlign.TOP });
    const res = C([P(b.res[0], { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }), P(b.res[1], { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }),
      P(b.res[2], { font: SANS, size: 14, color: 'DDDDDD', align: AL.CENTER })], ws[6], { fill: INK, borders: NOB, rowSpan: 2 });
    const c = b.cards;
    return T([[card(c[0].h), sym('+'), card(c[1].h), sym('+'), card(c[2].h), sym('='), res], [body(c[0].b), body(c[1].b), body(c[2].b)]], ws); },
  line: (b, w) => T([[C(P(b.k, { font: SANS, bold: true, size: 16, align: AL.CENTER }), mm(18), { fill: G2, mt: 25, mb: 25, ml: 40, mr: 40 }),
    C(P(b.v, { size: 16 }), w - mm(18), { mt: 25, mb: 25 })]], [mm(18), w - mm(18)]),
  cmp: (b, w) => { const aw = mm(9), cw = Math.floor((w - aw) / 2);
    const side = (x, dark) => [P(`${dark ? '{{' : '[['}${x.tag}${dark ? '}}' : ']]'}**${x.h}**`, { size: 17 }), ...Bs(x.b, { size: 16 })];
    return T([[C(side(b.a), cw, { v: VerticalAlign.TOP }), C(P('➡', { font: SANS, bold: true, size: 28, color: G4, align: AL.CENTER }), aw, { borders: NOB, ml: 0, mr: 0 }),
      C(side(b.b, true), w - cw - aw, { v: VerticalAlign.TOP, borders: bAll(ln(INK, 12)) })]], [cw, aw, w - cw - aw]); },
  bl: (b) => Bs(b.b),
  eff: (b, w) => { const a = mm(26), c = mm(54), m = w - a - c, o = ln();
    const row = (t, r, last) => [C(B(t), a + m, { span: 2, borders: { top: NONE, left: o, right: NONE, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, ml: 140 }),
      C(P(r, { bold: true, align: AL.RIGHT }), c, { borders: { top: NONE, left: NONE, right: o, bottom: last ? o : NONE }, mt: 15, mb: last ? 50 : 15, mr: 140 })];
    return T([[C(P(b.k, { font: SANS, bold: true, size: 17, color: 'FFFFFF', align: AL.CENTER }), a, { fill: G4 }),
      C(P(b.v, { font: SANS, bold: true, size: 17 }), m + c, { span: 2, ml: 140 })],
      ...b.rows.map((r, i) => row(r[0], r[1], i === b.rows.length - 1))], [a, m, c]); },
  res: (b, w) => T([[C(P('추진성과', { font: SANS, bold: true, size: 15, color: 'FFFFFF', align: AL.CENTER }), KW, { fill: INK, borders: bAll(ln(INK, 14)) }),
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
};

const before = { sec: 150, sub: 120, ev: 0 };
function pageChildren(blocks) {
  const out = [];
  blocks.forEach((b, i) => { if (i) out.push(gap(before[b.t] ?? 85)); const r = R[b.t](b, W); Array.isArray(r) ? out.push(...r) : out.push(r); });
  return out;
}
const pageProps = { page: { size: { width: 11906, height: 16838 }, margin: { top: mm(11), bottom: mm(13), left: mm(12), right: mm(12), footer: mm(6) } } };
const doc = new Document({ styles: { default: { document: { run: { font: SERIF, size: SZ } } } },
  sections: CT.pages.map(p => ({ properties: pageProps,
    footers: { default: new Footer({ children: [P(p.footer, { font: SANS, bold: true, size: 16, color: G4, align: p.align === 'left' ? AL.LEFT : AL.RIGHT })] }) },
    children: pageChildren(p.blocks) })) });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('ok'); });
```

### 파일: to_pdf.py

```python
# 사용법: python3 to_pdf.py 보고서.html  → 같은 이름 .pdf 생성 + 쪽별 내용 하단 위치(px) 출력
import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123})
    pg.goto(src.as_uri()); pg.wait_for_timeout(500)
    fill = pg.evaluate("""[...document.querySelectorAll('.page')].map(p=>{const r=p.getBoundingClientRect();let m=0;
      p.querySelectorAll('*').forEach(e=>{if(e.classList.contains('footer'))return;const v=e.getBoundingClientRect().bottom-r.top;if(v>m)m=v});return Math.round(m)})""")
    print('쪽별 내용 하단(px):', fill, '/ 한계 약 1075px (넘으면 바닥글 침범)')
    pg.pdf(path=str(src.with_suffix('.pdf')), format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
```

### 파일: fill_check.py

```python
# 사용법: python3 fill_check.py 변환된.pdf  → 쪽별 내용 하단 비율 (0.95 넘으면 위험, 0.80~0.90 권장)
import sys, subprocess, glob, os, tempfile
import numpy as np
from PIL import Image
d = tempfile.mkdtemp(); subprocess.run(['pdftoppm', '-r', '60', '-png', sys.argv[1], d + '/p'], check=True)
for f in sorted(glob.glob(d + '/p-*.png')):
    a = np.array(Image.open(f).convert('L')); h = a.shape[0]
    rows = np.where((a[:int(h * 0.94)] < 200).sum(1) > 3)[0]
    print(os.path.basename(f), round(rows.max() / h, 3) if len(rows) else 0)
```

### 파일: content.js (예시)

```js
// 예시 데이터: 모든 블록 사용법 (2쪽). 새 보고서는 이 구조를 복사해 내용만 바꾼다.
module.exports = {
  title: '평가내용 예시',
  pages: [
  { footer: '2026년도 경영실적보고서 │ 1', align: 'right', blocks: [
    { t: 'ev', label: '평가내용❷', text: '민간수요 맞춤형 개방체계 구축, 협업데이터 공동생산 협력체계 구축 등을 위한 노력과 성과' },
    { t: 'bp', items: ["① **[민간수요 기반 'AI 친화 유가 데이터']** 개방으로 민간 AI 서비스 창출 기여", "② 산학 공동연구로 **'AI 생성 탐사자료'** 65공 공동생산"] },
    { t: 'vision', k: 'AI 비전', text: '사람, 데이터, AI 연결로 에너지 산업의 미래 가치 창출' },
    { t: 'sec', no: '1', title: '민간 수요를 AI 데이터로 연결하여 민간 AI 서비스 창출 기여', tag: 'B.P①' },
    { t: 'boxes', items: [
      { h: '국정과제', b: ['[[과제 ○○]]AI 기반 공공데이터 개방·활용 확대'] },
      { h: '대외 환경', b: ['고유가 지속, 국민·기업 유가정보 관심 급증'] },
      { h: '기관 전략', b: ['[[비전]]사람, 데이터, AI 연결'] } ] },
    { t: 'kv', k: '문 제 점', b: ['기존 API는 실시간 시세 위주 제공'], ar: '➡ 장기 시계열 부족으로 AI 학습 활용 곤란' },
    { t: 'banner', text: '민간 수요 기반 4단계 절차로 AI 친화 데이터 발굴·개방' },
    { t: 'kv', k: '추 진/내 용', inner: [
      { t: 'chev', st: [ { h: '① 수요조사', t: ["국민·기업('26.6)"] }, { h: '② 현황조사', t: ['후보 5종'] }, { h: '③ 전문가 평가', t: ['3인 평가'] }, { h: '④ 개방', t: ['포털 개방'], on: true } ] },
      { t: 'check', text: '「일별 주유소 가격」을 AI가 바로 학습하는 형태로 개방' },
      { t: 'comb', cards: [ { h: '10년 시계열', b: ['(규모) 66,170건'] }, { h: '표준코드', b: ['(코드) 법정동 10자리'] }, { h: 'AI-Ready 문서', b: ['(설명서) md'] } ], res: ['AI 학습용', '고가치 데이터', "('26.9.18 개방)"] },
      { t: 'line', k: '추진경과', v: "수요조사('26.6) → 전문가 평가('26.9) → 개방('26.9.18)" },
      { t: 'cmp', a: { tag: '기존', h: '실시간 API', b: ['현재가만 제공'] }, b: { tag: '확대', h: 'AI 친화 데이터', b: ['10년 시계열 + 데이터 사전'] } } ] },
    { t: 'kpi', items: [ { v: '4,500명', l: '누적 이용자' }, { v: '86%', l: '재이용률' }, { v: '9종', l: 'AI 데이터 개방' }, { v: '0건', l: '결측치' } ] },
    { t: 'eff', k: '민간활용 사례', v: 'AI 주유소 추천앱 출시 2개월 만에 누적 4,500명', rows: [ ['월간 활성 이용자 3,869명', '➡ 이용 확대'], ['최근 30일 재이용 86%', '➡ 일상 정착'] ] },
    { t: 'res', b: ['AI 친화 데이터 __9종 개방__', '민간 수요 → 개방 → 서비스 창출의 **선순환 기반 마련**'] },
  ] },
  { footer: '2 │ 한국석유공사', align: 'left', blocks: [
    { t: 'sec', no: '2', title: '산학 협업으로 AI 탐사자료를 공동생산하여 의사결정 지원', tag: 'B.P②' },
    { t: 'sub', title: '가. 머신러닝 기반 탐사자료 생성', tag: '현장 적용' },
    { t: 'kv', k: '추진방향', text: '일반검층 기반 ML로 고가 탐사자료 생성, 산학 공동연구로 공동생산' },
    { t: 'tbl', w: [0.3, 0.35, 0.35], head: ['과제', '기존(AS-IS)', '개선(TO-BE)'], rows: [ ['탐사자료 확보', '특수검층 5공뿐', 'ML로 **65공** 생성'] ] },
    { t: 'bl', b: ['**공사주도** : 모델 개발', '**참여기관** : 공주대(산학 공동연구)'] },
    { t: 'res', b: ['취득비용 __약 325만불 대체__(추정)'] },
  ] },
  ],
};
```