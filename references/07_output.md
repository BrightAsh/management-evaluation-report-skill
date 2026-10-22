# 07. 결과물 만들기: PDF·Word(·HWPX)

## 1. 환경별 결과물

| 환경 | 결과물 |
|---|---|
| 코드를 실행할 수 있음(Claude, Codex, 코드 실행이 켜진 ChatGPT 등) | content.json → **PDF + Word(.docx)** |
| 코드를 실행할 수 없음 | **Markdown 지면안**(3절)과 content.json. 사용자가 다른 환경에서 렌더링하거나 그대로 옮겨 쓴다 |
| HWPX가 필요함 | PDF→HWPX 변환 도구가 있으면 사용한다. 없으면 Word를 한글에서 열어 'HWPX로 저장'하도록 안내한다 |

## 2. 렌더링 명령

`scripts/` 폴더 안의 파일을 작업 폴더에 둔 채로 실행한다. `render_html.js`는 같은 폴더의 `base.css`를 읽는다.

```bash
# 0) 준비 (처음 한 번)
npm ls docx >/dev/null 2>&1 || npm install docx
pip install olefile openpyxl pillow playwright 2>/dev/null   # 필요한 것만

# 1) 첨부 읽기 (텍스트 + 그림 추출, 그림 미리보기 모음)
python3 -I scripts/read_inputs.py work/inputs 첨부1.pdf 첨부2.hwpx 첨부3.xlsx
#    → work/inputs/_images.md, images/_sheet_N.png, pages/ (PDF 쪽 모음)

# 1-1) PDF 속 벡터 그래프·표를 그림으로 자르기 (필요할 때만)
python3 scripts/crop_pdf.py 첨부1.pdf 5 --grid work/inputs      # 눈금 이미지로 위치 확인
python3 scripts/crop_pdf.py 첨부1.pdf 5 0.20 0.50 0.71 0.59 work/inputs/images/C01.png

# 1-2) 비교 값 계산 (전년·도입 전후·목표 대비)
python3 scripts/compare.py 140 462 명 --years 24 25
python3 scripts/compare.py --csv work/compare.csv

# 2) PDF
node scripts/render_html.js content.json report.html
python3 scripts/to_pdf.py report.html            # report.pdf + 쪽별 내용 하단(px)

# 3) Word
node scripts/render_docx.js content.json report.docx 1.17 1.65   # 글자배율, 간격배율

# 4) Word 지면 점검 (LibreOffice가 있으면)
cp report.docx check.docx && soffice --headless --convert-to pdf check.docx
python3 scripts/fill_check.py check.pdf
```

- Playwright가 없으면 Word를 LibreOffice로 PDF 변환한 결과를 PDF로 낸다.
- 파일 이름에 한글이 있으면 LibreOffice 변환이 실패할 수 있다. 점검용은 영문 이름으로 복사해서 변환한다.

## 3. 코드 없이 쓸 때: Markdown 지면안

렌더링을 못 하는 환경에서는 지면을 Markdown 표로 표현한다. 사람이 그대로 한글·Word에 옮겨 쓸 수 있게 한다.

```markdown
# Ⅰ. 20XX년 평가내용별 추진실적 및 성과

| 평가내용 1 | (평가 항목 원문) |
|---|---|
| **핵심성과** | ☑ **(핵심 메시지 1문장)** |

## 1  (주장형 대제목)

### 가. (주장형 중제목)  `B.P`

| | (열1) | (열2) | (열3) |
|---|---|---|---|
| **현황 및 문제점** | · … | · … | · … |
| **추진내용** | **(실행 단위·시점)**<br>· …<br>  – … | · … | · … |
| **추진성과** | · … (230%↑, '24년 140명 → '25년 462명) | · … | · … |

[그림: 결과보고.pdf p.5 — 예측 결과 그래프, 추진내용 (열1) 칸 아래]

| **기대효과** | · …<br>· … |
|---|---|
```
그림은 넣을 자리에 `[그림: 원본 파일 쪽 — 무엇, 위치]`로 표시한다.

## 4. 새 블록 추가 방법

양식에 기존 블록으로 표현할 수 없는 요소가 있을 때만 추가한다.
1. `render_html.js`의 `R` 객체에 `새이름: b => '<div class="새이름">…</div>'`를 추가하고 `extra` CSS에 스타일을 넣는다.
2. `render_docx.js`의 `R` 객체에 같은 이름으로 `(b, w) => T([[C(...)]], [w])` 형태를 추가한다. `w`는 쓸 수 있는 폭(DXA)이다.
3. 두 결과물을 모두 렌더해서 모양이 같은지 이미지로 확인한다.
4. 블록 함수가 배열을 돌려주면 펼쳐서 넣는다(중첩 배열은 Word XML 오류를 낸다). 렌더러의 `push()`가 이를 처리한다.

## 5. 지면 맞춤

- 쪽수는 정확히 지킨다(`pdfinfo`로 확인).
- **PDF**: 쪽별 내용 하단이 약 960~1,055px면 알맞다(한계 1,065px, 넘으면 잘리고 바닥글과 겹친다).
- **Word**: 쪽별 채움 0.80~0.91이 알맞다. 사용자 PC의 실제 글꼴이 점검 환경의 대체 글꼴보다 넓을 수 있어 5~10% 여유를 둔다. 글자배율 1.13~1.24, 간격배율 1.5~2.0 사이에서 조정한다.
- **빈칸이 남으면** 글자를 키우지 말고 자료에서 근거를 더 넣는다(전후 비교, KPI, 기대효과, 과제 표). **넘치면** 등급이 낮은 내용부터 뺀다.
- 렌더한 쪽을 **이미지로 직접 보고** 확인한다: 태그 잘림, 라벨 줄바꿈, 표·흐름도 칸 넘침, 바닥글 겹침, 그림이 너무 크거나 흐린지.
- 그림이 지면을 많이 차지하면 높이(`h_mm`)를 줄이거나 그림을 뺀다. 근거 문장보다 그림을 먼저 뺀다.

## 6. 납품 파일
- `보고서명.pdf`, `보고서명.docx`
- 작업 기록(사용자가 원하면 함께 준다): `facts.md`, `storyline.md`, `content.json`, 새 양식이면 `style.md`(양식 명세)
