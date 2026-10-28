---
name: performance-report-writer
description: 흩어진 실적 자료(PDF·HWP·엑셀 등)로 경영평가·성과 실적보고서를 쓴다. 자료를 분석해 흐름과 구조를 설계하고, 양식·성과지표(편람)가 있으면 그에 맞춰 PDF·Word로 만든다.
---

> 단일 파일판입니다. 참고 문서는 부록 A, 스크립트와 데이터 틀은 부록 B에 있습니다.

# 실적보고서 작성 (performance-report-writer)

방대한 실적 자료를 읽고, **평가자가 한눈에 이해하는 흐름**으로 엮어 보고서 지면을 만든다. 핵심은 양식을 채우는 것이 아니라 **무엇을, 어떤 순서와 구조로 말할지 설계하는 것**이다. 어느 조직·부서·주제에도 쓴다.

## 도움말 모드

사용자가 작성 자료 없이 이 스킬을 부르거나 "사용법", "도움말", "어떻게 써?"라고 물으면, 작업하지 말고 아래 안내를 그대로 보여준다.

> **실적보고서 작성 도우미**
> 흩어진 실적 자료를 분석해, 평가자가 한눈에 이해하는 흐름의 보고서(PDF·Word)로 만들어 드립니다.
>
> | 구분 | 첨부할 것 | 하는 일 |
> |---|---|---|
> | **필수** | 작성 자료: 결과보고, 계획, 증빙, 회의자료, 과제 목록 엑셀 등 | 내용의 근거 |
> | 선택 | 양식: 따라 하고 싶은 보고서 샘플 | 구조·말투·지면을 그대로 따름 |
> | 선택 | 성과지표: 편람, 지표 정의서, 평가 기준 | 보고서 방향과 목차를 지표에 맞춤 |
> | 선택 | 가이드라인: 작성요령 | 쪽수·글자 크기 등 규정 준수 |
>
> 지원 형식: PDF, HWP, HWPX, DOCX, XLSX, PPTX, 이미지
>
> **요청 예시**
> - "첨부 자료로 경영평가 실적보고서 2쪽 써줘"
> - "이 양식대로, 첨부한 지표에 맞춰 3쪽으로 써줘"
> - "구성안(스토리라인)만 먼저 보여줘"
> - "○○ 사업을 대표 사례로 강조해줘"
>
> **받는 것:** PDF·Word 파일, 스토리라인 요약, 자료 사용 내역, 확인이 필요한 사항

## 작업 흐름

각 단계의 세부 방법은 이 파일 아래 **부록 A**에 있다. 해당 단계에 들어갈 때 그 부분을 읽는다.

| 단계 | 할 일 | 산출물 | 참고 |
|---|---|---|---|
| 1 | 첨부를 작성 자료 / 양식 / 성과지표 / 가이드라인으로 판별하고 모드(A~D)를 정한다 | 판별표 | 부록 A-01 |
| 2 | 자료를 **끝까지** 읽고 사실 카드로 뽑는다. 로직모델로 무게를 재고, 사업별 등급(A/B/C)을 매긴다 | `facts.md` | 부록 A-02 |
| 3 | 방향을 정한다: 지표가 있으면 지표를 해부하고, 없으면 자료에서 도출한다. 핵심 메시지 1문장과 축 2~4개 | `direction.md` | 부록 A-03 |
| 4 | **흐름·구조를 설계한다**: 섹션별 흐름 패턴, 주장형 제목, 문제-성과 짝, 지면 배분 | `storyline.md` | 부록 A-04 |
| 5 | 문체를 정한다: 양식이 있으면 문체 프로필을 뽑고, 없으면 기본 개조식 | `style.md` | 부록 A-05 |
| 6 | 블록을 골라 내용 데이터를 쓴다 | `content.json` | 부록 A-06 |
| 7 | PDF·Word를 만들고 지면을 맞춘다 | PDF, DOCX | 부록 A-07 |
| 8 | 사실·흐름·형식을 점검하고 정해진 형식으로 답한다 | 답변 | 부록 A-08 |

첫 답변에는 판별표와 정한 방향(모드, 핵심 메시지, 축)을 짧게 먼저 보여주고 바로 진행한다. 사용자가 "구성안만 먼저"라고 하면 4단계에서 멈춘다.

## 작업 모드

| 모드 | 첨부 | 방향(무엇을 말할지) | 구조·말투(어떻게 말할지) |
|---|---|---|---|
| A | 자료만 | 자료 분석으로 스스로 도출 | 기본 개조식 |
| B | 자료 + 양식 | 자료 분석으로 도출 | 양식을 그대로 따름 |
| C | 자료 + 성과지표 | 지표의 세부평가내용이 목차 뼈대 | 기본 개조식 |
| D | 자료 + 양식 + 성과지표 | 지표 | 양식 |

우선순위: 사용자 지시 > 가이드라인 > 성과지표(방향) / 양식(형식) > 기본값.

## 꼭 지킬 원칙

**흐름**
- 결론부터: 문서 → 핵심 메시지 → 축 → 근거. 섹션도 제목(주장)이 먼저 오고 근거가 뒤따른다.
- 제목은 주제가 아니라 주장: '수단 + 으로 + 결과', 가능하면 숫자를 넣는다.
- 제목만 이어 읽어도 핵심 메시지가 전달돼야 한다.
- 문제에서 꺼낸 숫자는 성과에서 같은 단위로 돌아온다. 모든 숫자에는 비교 기준(전·후, 전년, 목표)을 붙인다.
- 모든 대제목은 성과(3줄 이내)로 끝난다. 대표 사례가 앞에 오고, 지면을 더 많이 쓴다.

**사실**
- 원문에 없는 수치·사실은 쓰지 않는다. 모르면 `○○`로 비우고 보고한다.
- 계획은 '추진', 완료는 '달성'으로 구분한다. 목표·추정치에는 표시를 붙인다.
- 수치가 충돌하면 결과보고 > 평가 제출본 > 계획안 순, 같은 단계면 최신 자료를 쓴다.
- 양식은 형식만 빌린다. 양식에 있는 다른 조직의 내용은 절대 섞지 않는다.

**분량**
- 지정 쪽수를 정확히 지킨다. 빈칸은 자료의 근거로 채우고, 넘치면 등급이 낮은 내용부터 뺀다. 글자 크기로 맞추지 않는다.
- 박스·카드 하나에는 2~3항목만 둔다. 1항목은 1줄(최대 2줄)이다.

## 파일 안내

스크립트는 **부록 B**의 코드를 같은 이름의 파일로 저장해 쓴다. 코드를 실행할 수 없는 환경이면 1~6단계를 그대로 하고, 결과는 부록 A-07 3절의 Markdown 지면안으로 낸다.

최신판·설치 안내: https://github.com/BrightAsh/performance-report-writer

---

# 부록 A. 단계별 방법

## A-01. 입력 판별과 작업 모드

### 1. 입력의 네 가지 역할

| 역할 | 필수 여부 | 이 입력이 정하는 것 | 판별 단서 |
|---|---|---|---|
| **작성 자료** | 필수 | 쓸 **내용**(사실·수치·사례) | 우리 조직의 실적: 계획안, 결과보고, 증빙, 회의자료, 보도자료, 내부 메모, 과제 목록 엑셀 |
| **양식(템플릿)** | 선택 | **어떻게** 말할지: 구조·말투·지면 | 완성된 보고서 지면. 짧음(1~6쪽), 박스·도식·표 중심, 다른 조직이나 다른 연도 실적, '예시' 표기 |
| **성과지표** | 선택 | **무엇을** 말할지: 방향·목차 뼈대·강조점 | 지표명, 지표 정의, 세부평가내용, 평가방법, 가중치, 평가 기준, 전년도 지적사항 |
| **작성 가이드라인** | 선택 | 지켜야 할 **제약** | 작성요령·유의사항. 쪽수 상한, 글자 크기, 필수 항목, 금지 표현 등 규정 문장 |

사용자 메시지의 지시(쪽수, 강조할 사업, 부서명, 제출처 등)는 모든 첨부보다 우선한다.

### 2. 판별 절차

1. 모든 첨부의 앞 2~3쪽, 목차, 제목, 머리말·바닥글을 읽는다.
2. 양식 후보는 반드시 **이미지로 보고** 판단한다. 글자만으로는 지면 구조를 알 수 없다.
3. 한 파일에 역할이 섞여 있으면 쪽 범위별로 나눈다(예: 편람 1~3쪽은 성과지표, 4~6쪽은 가이드라인).
4. 판별 결과를 **판별표**로 남긴다: `파일 | 역할 | 근거 한 줄`.
5. 판단이 갈리고 결과가 크게 달라지는 파일만 짧게 묻는다. 물을 수 없으면 가장 그럴듯한 판단으로 진행하고 그렇게 했다고 밝힌다.

헷갈리는 경우:
- **다른 조직의 완성된 보고서** → 양식이다. 내용은 절대 가져오지 않는다.
- **우리 조직의 작년 보고서** → 양식이면서 작성 자료(전년 실적·비교 기준)이기도 하다. 두 역할을 모두 쓴다.
- **평가 결과 통보서·지적사항** → 성과지표 쪽에 넣는다. 지적사항은 반드시 대응한다.
- **과제 목록 엑셀** → 작성 자료다. 엑셀 안의 분류 체계는 그대로 따른다.

### 3. 작업 모드

| 모드 | 첨부 | 방향(무엇을) | 구조·말투(어떻게) | 지면 |
|---|---|---|---|---|
| A | 자료만 | 자료 분석으로 스스로 도출 (`03_direction.md` 2절) | 기본 문체 (`05_style.md` 3절) | 기본 지면 |
| B | 자료 + 양식 | 자료 분석으로 도출 | 양식의 구조·말투를 그대로 따름 | 양식 지면 |
| C | 자료 + 성과지표 | 지표에서 도출 (`03_direction.md` 1절) | 기본 문체 | 기본 지면 |
| D | 자료 + 양식 + 성과지표 | 지표에서 도출 | 양식을 따름 | 양식 지면 |

**역할 분리 원칙.** 성과지표는 '무엇을 말할지', 양식은 '어떻게 말할지'를 정한다. 둘이 부딪히면 이렇게 한다.
- 양식의 칸이 일반 칸(추진배경·추진내용·추진성과 등)이면 칸 구조는 양식대로 두고, 그 안을 지표 항목으로 채운다.
- 양식의 제목이 주제어(다른 조직의 사업명 등)면 지표 항목의 핵심어로 바꾼다.

**우선순위:** 사용자 지시 > 가이드라인 > 성과지표(방향) / 양식(형식) > 기본값.

### 4. 쪽수 결정

사용자 지정 > 가이드라인 상한 > 양식 샘플 쪽수 > 자료 분량에 맞춘 판단(기본 2쪽).
쪽수가 정해지면 끝까지 지킨다. 넘치면 약한 내용을 빼고, 모자라면 자료에서 근거를 더 찾는다. 글자 크기를 조절해 맞추지 않는다.

## A-02. 자료 분석: 방대한 자료에서 쓸 것을 고르는 법

좋은 보고서는 문장이 아니라 **고르기**에서 결정된다. 자료를 다 옮기는 것이 아니라, 평가자가 납득할 근거를 골라 하나의 이야기로 엮는다. 이 단계의 산출물은 `facts.md`(사실 카드)와 `inventory.md`(자료 목록)다. 이후 모든 문장은 사실 카드의 ID로 되짚을 수 있어야 한다.

### 1. 전부 읽기

- 모든 작성 자료를 **처음부터 끝까지** 읽는다. 앞부분만 읽고 쓰면 뒤쪽의 결과보고·최신 수치를 놓친다.
- `scripts/read_inputs.py`로 텍스트를 뽑은 뒤 구간을 나눠 읽는다. 표와 그림은 필요하면 이미지로 확인한다.
- 같은 사업이 여러 문서(계획안 → 중간보고 → 결과보고 → 평가 제출본)에 나오면 모두 찾아 묶는다.

### 2. 자료 목록 (inventory.md)

| 파일 | 성격 | 작성 시점 | 다루는 사업·주제 | 신뢰도 |
|---|---|---|---|---|
| A.pdf | 결과보고 | 2026.9 | ○○ 시스템 구축 | 높음(결재본) |
| B.xlsx | 과제 목록 | 2026.10 | 부서 과제 18건 | 중간(일부 '상세 미확보') |

성격 구분: 계획 / 중간 / 결과 / 평가 제출본 / 증빙(보도자료·결재) / 메모(미완 표기 '??' 포함 가능).

### 3. 사실 카드 (facts.md)

자료에서 쓸 수 있는 사실을 하나씩 카드로 뽑는다. 문장을 쓰기 전에 반드시 만든다.

| ID | 사업 | 무엇을 | 시점 | 주체 | 수치(기준 → 결과) | 상태 | 유형 | 인정 | 출처 |
|---|---|---|---|---|---|---|---|---|---|
| F01 | 민원 창구 통합 | 민원 접수·답변 창구를 하나로 통합 | '26.7 | 고객지원팀 | 처리기간 9일 → 4일 | 완료 | 성과 | - | B.xlsx 14행 |
| F02 | 설비 교체 | 노후 냉각설비 교체 공사 계약 | '26.9 | 시설팀+외부업체 | 계약 3.2억원 | 진행 | 활동 | 외부 공모 선정 | A.pdf p.3 |

필드 규칙:
- **수치**는 단위와 비교 기준을 함께 적는다(전년, 도입 전, 목표). 비교 기준이 없으면 '기준 없음'이라고 적는다.
- **상태**: 계획 / 진행 / 완료 / 목표·추정. 계획서에만 있는 일은 '계획'이다.
- **유형**은 로직모델로 분류한다(아래 4절).
- **인정**: 수상, 정부·외부기관 선정, 언론 보도, 학술 발표, 타 기관 확산.
- **출처**: 파일과 쪽(행). 검증 단계에서 되짚는다.

수치가 서로 다르면: **결과보고 > 평가 제출본 > 중간보고 > 계획안**, 같은 단계면 최신 자료를 쓴다. 채택하지 않은 값은 카드 비고에 남기고 최종 답변의 확인 사항에 적는다.

### 4. 로직모델로 무게 재기

평가자는 '얼마나 바빴나'보다 '무엇이 달라졌나'를 본다. 사실을 다섯 층으로 나눈다.

| 유형 | 뜻 | 예 | 보고서에서의 무게 |
|---|---|---|---|
| 투입 | 넣은 자원 | 예산 3.2억원, 인력 3명 | 낮음 (맥락용) |
| 활동 | 한 일 | 교육 실시, 협약 체결, 시스템 발주 | 중간 (과정 설명) |
| 산출 | 직접 결과물 | 시스템 구축, 데이터 7종 개방, 교육 480명 | 중간 |
| 성과 | 달라진 상태 | 처리시간 90% 단축, 오류율 75%→98% | **높음** |
| 파급 | 밖으로 번진 효과 | 타 기관 도입, 국민 이용 3,200명, 정책 반영 | **높음** |

한 사업에 활동만 있고 성과가 없으면, 자료에서 성과 수치를 더 찾는다. 끝내 없으면 '성과 측정 예정'으로 정직하게 쓰고 비중을 낮춘다.

### 5. 묶기: 사업 단위 → 테마

1. 사실 카드를 **사업 단위**로 묶는다(같은 사업의 계획·활동·성과를 한 줄로).
2. 사업들을 **테마**로 묶는다. 테마는 성과지표 항목이 있으면 그 항목, 없으면 자료에서 반복되는 목적(예: 효율, 안전, 고객, 비용, 협력, 역량)이다.
3. 자료 안에 이미 분류가 있으면(엑셀 '분야' 열 등) 그것을 따른다.

### 6. 선별 점수

사업마다 점수를 매겨 무엇을 대표 사례로 올리고 무엇을 뺄지 정한다.

| 기준 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 지표 적합성 | 무관 | 간접 | 관련 | 지표 문구와 직접 일치 |
| 성과 수준 | 계획만 | 활동 | 산출 | 정량 성과·파급 |
| 차별성 | 흔함 | 개선 | 전사·최대 규모 | 최초·유일·외부 인정 |
| 인과 명확성 | 연결 불명 | 추정 | 자료로 일부 입증 | 전후 비교로 입증 |
| 지속·확산 | 일회성 | 계획 있음 | 제도화 | 타 부서·기관 확산 |

- **A등급(12점 이상)**: 대표 사례. BEST PRACTICE, 독립 대제목, 가장 많은 지면.
- **B등급(7~11점)**: 본문 사례. 표·카드 한 칸 또는 중제목.
- **C등급(6점 이하)**: 한 줄 언급 또는 제외. 제외한 것은 최종 답변에 목록으로 알린다.

점수는 판단 보조 도구다. 성과지표가 특정 사업을 요구하면(예: '혁신프로젝트 반영') 점수와 관계없이 넣는다.

### 7. 공백·약점 진단

글을 쓰기 전에 약한 곳을 먼저 찾는다.
- **지표 공백**: 성과지표 항목 중 근거 사업이 없는 곳 → '자료 부족'으로 보고한다. 지어내지 않는다.
- **성과 공백**: 활동만 있고 결과 수치가 없는 사업.
- **인과 공백**: 성과는 있는데 우리 노력과의 연결이 약한 것(외부 요인 가능성).
- **시점 문제**: 실적기간 밖의 실적, 계획 단계인데 완료처럼 보이는 것.
- **미완 표기**: '??', '상세 미확보', 빈칸 → 넣지 않고 보고한다.

### 8. 이 단계의 점검

- [ ] 모든 작성 자료를 끝까지 읽었다
- [ ] inventory.md와 facts.md를 만들었다
- [ ] 모든 수치에 비교 기준과 출처가 있다
- [ ] 수치 충돌을 정리했다
- [ ] 사업별 선별 점수와 A/B/C 등급을 정했다
- [ ] 공백·약점 목록을 만들었다

## A-03. 방향 설정: 무엇을 말할 것인가

방향은 '이 보고서를 읽은 평가자가 기억해야 할 한 가지'다. 방향이 없으면 실적 나열이 되고, 방향이 틀리면 좋은 실적도 점수로 이어지지 않는다.

### 1. 성과지표가 있을 때 (모드 C·D)

#### 1-1. 지표 해부
지표 문서에서 다음을 뽑아 `direction.md`에 적는다.

| 항목 | 뽑을 것 | 쓰임 |
|---|---|---|
| 지표명·정의·목적 | 지표가 왜 존재하는가 | 핵심 메시지의 방향 |
| 세부평가내용 | 번호 매긴 평가 항목 원문 | **대제목의 뼈대와 순서** |
| 평가방법 | 정성(노력+성과) / 정량(목표 대비) / 등급 | 서술 비중 |
| 가중치·배점 | 항목별 무게 | 지면 배분 |
| 평가 기준·착안사항 | '적정성', '체계성', '차별성', '확산' 등 키워드 | 각 섹션의 강조점 |
| 전년도 지적사항 | 평가위원 지적 원문 | 반드시 대응 (지적 → 조치 → 결과) |
| 지정 과제 | '○○ 프로젝트 반영' 같은 요구 | 대표 사례로 필수 배치 |

#### 1-2. 지표를 목차로 바꾸기
- **세부평가내용 1개 = 대제목 1개.** 순서는 지표 문서 순서를 따른다. 평가자는 지표 문서를 옆에 두고 읽으며, 항목마다 해당 부분을 찾는다.
- 대제목 문구에는 해당 항목의 **핵심어를 그대로** 넣는다. 평가자가 찾기 쉬워야 한다.
- 항목이 '노력과 성과'를 함께 묻으면, 섹션 안에 노력(체계·과정·차별점)과 성과(정량·전후 비교)를 모두 둔다. 성과 없이 노력만 쓰면 감점 요인이다.
- 지면은 배점에 비례해 나눈다. 배점이 없으면 근거의 양과 질에 비례한다.
- 근거가 없는 항목은 빈 섹션을 꾸미지 말고 '자료 부족'으로 보고한다.

#### 1-3. 지표 키워드를 강조점으로
평가 기준의 키워드마다, 그것을 보여주는 장치를 정해 둔다.

| 평가 키워드 | 보여주는 장치 |
|---|---|
| 적정성·정합성 | 상위 정책·기관 전략과 연결한 배경 박스 |
| 체계성 | 단계 흐름도, 추진체계도, 역할 분담 |
| 적극성·노력 | 추진 경과 타임라인, 주도·협업 구분 |
| 차별성·혁신성 | 기존 → 개선 비교, '최초·유일' 근거 |
| 성과·효과 | 전후 수치, 목표 대비 실적, KPI 타일 |
| 확산·지속성 | 제도화, 타 부서·기관 확산, 향후계획 |
| 환류 | 문제 → 개선 → 재점검 순환, 지적사항 반영 |

### 2. 성과지표가 없을 때 (모드 A·B)

#### 2-1. 맥락 추정
자료에서 단서를 모아 무엇을 위한 보고서인지 먼저 정한다.
- 보고서 종류: 경영평가 실적, 내부 성과보고, 공모·수상 신청, 사업 결과보고 등. 문서 제목·표지·제출처로 판단한다.
- 기간: 실적기간이 명시돼 있으면 그 범위만 쓴다.
- 상위 방향: 자료에 인용된 정부 정책·국정과제·기관 비전·중장기 전략.
- 부서 성격: 아래 2-3의 표로 판단한다.

#### 2-2. 기본 평가틀
지표가 없으면 다음 다섯 질문으로 구성한다. 대부분의 성과 평가가 결국 이 다섯 가지를 묻는다.

1. **왜** 했나: 정책·환경 변화, 기존 방식의 문제(정량 근거)
2. **어떻게** 계획했나: 목표, 전략, 추진체계
3. **무엇을** 했나: 추진 내용, 차별화된 방식, 협업
4. **무엇이 달라졌나**: 정량 성과, 전년·도입 전 대비, 외부 인정
5. **어떻게 이어가나**: 제도화, 확산, 환류, 향후계획

#### 2-3. 부서 성격별 성과 언어
분야에 따라 평가자가 기대하는 성과의 '말'이 다르다. 핵심 메시지와 KPI를 이 언어로 쓴다.

| 분야 | 평가자가 듣고 싶은 성과 | 대표 지표 예 |
|---|---|---|
| 사업·생산 | 매출·생산량·수익 증가, 사업 성공 | 생산량 ○%↑, 수익 ○억원 |
| 안전·환경 | 사고·위험 감소, 예방 체계 | 재해율, 위험 발굴 건수, 점검 시간 |
| 재무·회계 | 비용 절감, 재무 건전성, 정확성 | 절감액, 부채비율, 오류 건수 |
| 경영지원·행정 | 업무 효율, 처리 시간, 만족도 | 처리시간 ○%↓, 만족도 ○점 |
| 대국민·고객 | 이용자 편익, 접근성, 민원 해소 | 이용자 수, 처리 기간, 만족도 |
| 기술·연구·디지털 | 신기술 적용, 문제 해결, 비용 대체 | 정확도, 자동화율, 대체 비용 |
| 인사·조직·문화 | 역량 향상, 참여, 제도 개선 | 교육 이수, 참여율, 자격 취득 |
| 상생·사회가치 | 지역·중소기업·사회 기여 | 지원 금액, 수혜 기업 수, 일자리 |

한 보고서가 여러 분야에 걸치면, 지표(또는 자료의 분류)를 기준으로 축마다 다른 언어를 쓴다.

### 3. 핵심 메시지와 축 (모든 모드 공통)

#### 3-1. 핵심 메시지 1문장
'**[누가] [무엇으로] [무엇을 바꿨다]**' 형태로 한 문장을 만든다.
- 좋은 예: "점검 방식을 데이터 기반으로 바꿔 설비 돌발 고장을 79% 줄이고, 그 방식을 전사 지침으로 굳혔다"
- 나쁜 예: "다양한 안전관리 노력을 추진하였다" (무엇이 바뀌었는지 없음)

#### 3-2. 축 2~4개
핵심 메시지를 받치는 기둥이다.
- 지표가 있으면 세부평가내용이 곧 축이다.
- 없으면 A등급 사업들이 모이는 테마가 축이다.
- 축은 서로 겹치지 않고(MECE), 합치면 핵심 메시지가 된다.
- 축 이름은 '**수단 + 으로 + 결과**' 형태로 쓴다(예: "현장 데이터 연결로 설비 고장 사전 차단").

#### 3-3. 방향 공개
도출한 방향(핵심 메시지, 축, 근거로 삼은 단서)을 첫 답변에 짧게 밝힌다. 지표가 없을 때는 특히 '이렇게 해석했다'를 보여 사용자가 바로잡을 수 있게 한다.

### 4. 이 단계의 점검
- [ ] 핵심 메시지가 '무엇이 바뀌었나'를 말한다
- [ ] 축이 2~4개이고 겹치지 않는다
- [ ] 지표가 있으면 모든 세부평가내용이 축(대제목)에 대응한다
- [ ] 전년도 지적사항과 지정 과제를 빠뜨리지 않았다
- [ ] 부서 성격에 맞는 성과 언어를 골랐다

## A-04. 흐름·구조 설계: 어떻게 엮어서 말할 것인가

이 단계가 보고서의 품질을 결정한다. 같은 사실로도 흐름에 따라 '열심히 했다'로 읽히기도 하고 '확실히 바꿨다'로 읽히기도 한다. 문장을 쓰기 전에 **스토리라인 표**(`storyline.md`)를 먼저 완성한다.

### 1. 일곱 가지 원칙

#### ① 결론부터 (피라미드)
문서 전체 → 핵심 메시지 1문장 → 축 2~4개 → 축별 근거. 각 섹션도 같다. 첫 줄(제목)에 주장을 두고 아래에 근거를 둔다. 평가자는 시간이 없다. 첫 줄에서 판단하고, 아래는 확인용으로 읽는다.

#### ② 제목은 주제가 아니라 주장
| 주제형 (✗) | 주장형 (✓) |
|---|---|
| AI 활용 현황 | 현업이 만든 AI 도구 18건으로 반복업무 시간 최대 90% 단축 |
| 안전관리 추진 실적 | 설비 위험 신호를 미리 잡는 예측 점검으로 고장 정지 0건 달성 |
| 고객만족 제고 노력 | 민원 접수부터 답변까지 한 창구로 묶어 처리기간 절반 단축 |

형식은 '**수단 + 으로 + 결과**'. 결과에는 가능하면 숫자를 넣는다.

#### ③ 제목 이어 읽기 테스트
대제목과 중제목만 순서대로 읽어도 핵심 메시지가 전달돼야 한다. 전달되지 않으면 제목을 고치거나 순서를 바꾼다. 스토리라인 표를 만든 뒤 반드시 해 본다.

#### ④ 문제와 성과의 짝
문제에서 꺼낸 숫자는 성과에서 **같은 단위로** 다시 나와야 한다.
- 문제: "보고 완료율 18%에 그침" → 성과: "보고 완료율 18% → 71%"
- 문제에서 '시간'을 말했는데 성과에서 '만족도'만 말하면 흐름이 끊긴다.
짝이 맞는 숫자가 자료에 없으면, 문제 서술을 성과가 있는 쪽으로 맞춘다(없는 숫자를 만들지 않는다).

#### ⑤ 숫자는 항상 비교와 함께
단독 숫자는 크기를 알 수 없다. 기준을 붙인다: 도입 전 → 후, 전년 → 올해, 목표 → 실적, 우리 → 평균. 기준이 정말 없으면 규모(전체 중 몇 %)라도 붙인다.

#### ⑥ 주장 → 사례 → 숫자의 사다리
모든 주장 아래에는 최소 하나의 구체 사례나 숫자가 있어야 한다. "체계를 구축하였다"에는 체계도가, "확산하였다"에는 몇 곳으로 확산됐는지가 따라온다.

#### ⑦ 한 번만, 겹치지 않게
같은 사실은 가장 잘 어울리는 섹션에 한 번만 쓴다. 축끼리 겹치면(MECE 위반) 둘 중 하나로 합치거나 경계를 다시 긋는다. 단, 종합성과 표처럼 요약하는 곳은 예외다.

### 2. 섹션 흐름 패턴 (스파인)

대제목 하나 안의 흐름이다. 사업 성격에 맞는 패턴을 고른다.

| 패턴 | 흐름 | 맞는 경우 |
|---|---|---|
| **문제 해결형** (기본) | 배경 → 문제(정량) ➡ 해결 방향 → 추진 내용 → 성과(전후) → 확산 | 대부분의 대표 사례 |
| **체계 구축형** | 필요성 → 추진체계(조직·제도·절차) → 운영 실적 → 성과 → 정착·확산 | 거버넌스, 제도, 플랫폼 |
| **단계 확장형** | 1단계(과거) → 2단계(올해, 강조) → 3단계(계획) → 누적 성과 | 다년도 사업, 로드맵 |
| **지적 대응형** | 지적사항 원문 → 원인 분석 → 조치 → 결과 → 재발 방지 | 전년도 지적 반영 |
| **과제 묶음형** | 추진 방향 → 과제 표(과제·기존·개선) → 종합 효과 | 여러 소과제(경진대회 과제 등) |
| **협업 확산형** | 협업 구조(누구와) → 공동 추진 → 각자 얻은 것 → 외부 확산 | 산학연·기관 간 협력, 상생 |
| **3블록 약식** | 추진방향 → 추진내용 → 추진성과 | B등급 사례, 지면이 좁을 때 |

모든 섹션은 **성과로 끝난다**(성과 박스, 3줄 이내). 순서는 '외부 인정 → 확정된 활용·정량 성과 → 확산·다음 단계'.

### 3. 섹션 사이의 흐름

- **순서**: 지표가 있으면 지표 순서. 없으면 기반(체계·조직) → 핵심 성과(대표 사례) → 확산·역량 → 종합. 대표 사례(A등급)는 앞쪽에 둔다.
- **전환 문장**: 문제에서 해결로 넘어갈 때 한 줄로 방향을 말한다(배너). 예: "▼ 흩어진 점검 기록을 하나로 모아 위험을 먼저 찾는 체계로 전환 ▼"
- **처음과 끝**: 첫 쪽 상단에 대표 사례 요약(BEST PRACTICE 등)을 두고, 마지막에 종합성과·향후계획으로 닫는다. 처음에 약속한 것이 끝에서 숫자로 확인되게 한다.

### 4. 지면 배분

- 대표 사례(A등급)는 다른 섹션의 1~1.5배 지면을 쓴다.
- 지표 배점이 있으면 배점 비율을 따른다.
- 한 쪽에 대제목은 1~2개. 첫 쪽만 헤더와 대표 사례 요약을 둔다.
- 쪽수가 정해지면 스토리라인 단계에서 쪽별로 배치하고, 넘치거나 남을 것을 미리 조정한다.

### 5. 스토리라인 표 (storyline.md)

글을 쓰기 전에 이 표를 완성하고, 최종 답변에도 요약해 보여준다.

```
핵심 메시지: (1문장)
축: ① ... ② ... ③ ...

| 쪽 | 섹션 | 제목(주장형) | 대응 지표 항목 | 흐름 패턴 | 근거 사실 ID | 대표 숫자(전→후) | 지면 블록 |
|---|---|---|---|---|---|---|---|
| 1 | 헤더·대표 요약 | ... | - | - | F03, F11 | - | 헤더, 대표사례 박스 |
| 1 | 1 | ...으로 ... 달성 | 세부평가① | 문제 해결형 | F03,F04,F07 | 18%→71% | 배경 3단, 문제, 흐름도, 성과 |
| 2 | 2 | ... | 세부평가② | 과제 묶음형 | F11~F18 | 최대 90%↓ | 방향, 과제 표, 성과 |
```

### 6. 설계 점검 질문

스토리라인 표를 놓고 스스로 묻는다.
1. 제목만 이어 읽으면 핵심 메시지가 전달되는가?
2. 평가자가 각 쪽을 30초 보고 기억할 숫자 하나가 있는가?
3. 문제에서 꺼낸 숫자가 성과에서 같은 단위로 돌아오는가?
4. 지표 항목마다 대응하는 섹션이 있는가? 비는 곳은 보고했는가?
5. '우리가 한 일 때문에 달라졌다'는 인과가 보이는가?
6. 같은 사실을 두 번 쓰지 않았는가?
7. 계획 단계의 일을 완료처럼 쓰지 않았는가?

### 7. 작은 예 (가상 기관)

자료: 시설관리부서의 점검일지 3년치, 설비 고장 보고서, 신규 점검 앱 도입 결과보고.

- 핵심 메시지: "종이 점검을 데이터 점검으로 바꿔 고장을 미리 잡는 시설관리로 전환"
- 축: ① 점검 데이터 디지털화 ② 위험 예측 점검 ③ 현장 정착·확산
- 1번 섹션(문제 해결형):
  - 배경: 설비 노후화(평균 사용연수 21년)
  - 문제: 종이 일지라 이상 징후 추세를 볼 수 없음 ➡ 연 14건 돌발 고장
  - 전환: "▼ 점검 기록을 데이터로 모아 이상 징후를 미리 찾는 체계로 ▼"
  - 내용: 점검 앱 도입 → 3년치 기록 입력 → 이상치 알림 기준 설정
  - 성과: 돌발 고장 14건 → 3건, 점검 기록 누락 0건
  - 확산: 2개 지사 추가 적용, 점검 지침 개정
- 제목 이어 읽기: "점검 기록 디지털화로 이상 징후 추세 파악 체계 마련" → "위험 예측 점검으로 돌발 고장 79% 감소" → "현장 지침 개정으로 전 지사 확산 기반 확보" ✓

(위 숫자는 설명을 위한 가상 수치다.)

## A-05. 문체: 어떤 말투로 쓸 것인가

### 1. 원칙
- 양식이 있으면 **양식의 말투를 그대로** 따른다. 평가자는 그 말투에 익숙하다.
- 양식이 없으면 3절의 기본 문체를 쓴다.
- 어느 경우든 **양식의 내용(다른 조직의 사업·수치)은 절대 가져오지 않는다.** 패턴만 따른다.

### 2. 양식에서 문체 프로필 뽑기

양식 샘플을 읽고 아래 표를 채워 `style.md`에 둔다. 이 표가 이후 모든 문장의 기준이다.

| 항목 | 확인할 것 | 예 |
|---|---|---|
| 문장 종결 | 명사형('~구축'), '~함/~임', 서술형('~했다') | 명사형 종결 |
| 기호 체계 | 단계별 글머리표 | □ → ○ → - → · |
| 제목 문법 | 주장형/주제형, 길이 | '수단+으로+결과', 25자 안팎 |
| 문장 길이 | 한 줄 글자 수, 줄바꿈 | 1항목 1줄(최대 2줄) |
| 숫자 표기 | 연도·증감·단위 | '26.9 / 12종↑ / 79%↓ / 20분→3분 |
| 강조 방식 | 굵게, 밑줄, 색, 상자 | 핵심 수치 굵게, 최고 성과만 밑줄 |
| 괄호 사용 | 키워드 괄호, 주석 | (사용량) …, ※ 주석 |
| 주체 표기 | 주관·협업 구분 | 기관주도 : … / 참여기관 : … |
| 자주 쓰는 표현 | 반복되는 서술 어휘 | 기반 마련, 체계 구축, 성과 창출 |
| 고유 라벨 | 양식이 쓰는 칸 이름 | 추진배경 / 추진내용 / 추진성과 / BEST PRACTICE |
| 도식 빈도 | 표·흐름도·카드 비율 | 쪽당 도식 3~5개 |

텍스트가 뽑히는 양식이면 실제 문장을 10개 이상 모아 패턴을 확인한다. 이미지 양식이면 확대해서 읽는다.

### 3. 기본 문체 (양식이 없을 때)

한국어 공공·기업 실적보고서에서 가장 널리 쓰이는 개조식이다.

**문장**
- 개조식, 명사형 종결: ~구축, ~추진, ~확대, ~달성, ~마련. '~다', '~습니다'로 끝내지 않는다.
- 1항목 1줄, 길어도 2줄. 한 항목에는 한 가지 사실만 쓴다.
- 박스·카드 하나에는 2~3항목만 둔다. 글이 많으면 읽히지 않는다.
- 주어를 생략하되, 주체가 중요하면 앞에 둔다: "(협업) ○○대학과 공동 분석".
- 키워드를 괄호로 앞에 둔다: "(대상) 전 직원 480명", "(방식) 현장 실습".

**글머리표 위계**
| 단계 | 기호 | 용도 |
|---|---|---|
| 1 | □ 또는 · | 일반 항목 |
| 2 | ○ 또는 - | 세부 항목 |
| 결론 | ➡ | 문제의 결론, 효과 |
| 흐름 | → | 시간 순서, 전후 변화 |
| 핵심 | ✓ | 블록의 요지 한 줄 |
| 주석 | ※ | 출처, 산식, 단서 |

**표기**
| 항목 | 표기 |
|---|---|
| 연도·월 | '26년, '26.9, ('26.9.18) |
| 증감 | 12종↑, 79%↓, (전년대비 12%p↑) |
| 전후 | 20분→3분, 18%→71% |
| 기관 수 | 3社, 45개社 (조직 관행에 따라 '3개사') |
| 많음·전체 | 多, 全 (쓰지 않는 조직이면 풀어 씀) |
| 추정·목표 | (추정), (목표), 예상 |

**강조**
- 핵심 수치는 굵게, 섹션의 최고 성과 하나만 밑줄. 강조는 블록당 1~2곳.
- '획기적', '혁신적', '최고 수준' 같은 꾸밈말은 근거 숫자 없이 쓰지 않는다.

### 4. 문장 다듬기 점검
- [ ] 제목이 주장형이다
- [ ] 모든 항목이 1~2줄이다
- [ ] 숫자마다 비교 기준이 있다
- [ ] 계획인 일에 '완료', '달성'을 쓰지 않았다
- [ ] 근거 없는 최상급·꾸밈말이 없다
- [ ] 양식의 문체 프로필과 어긋나는 문장이 없다

## A-06. 지면 구성: 내용을 어떤 블록에 담을 것인가

### 1. 원칙
- 블록은 **내용의 성격**으로 고른다. 모양이 예뻐서 고르지 않는다.
- 쪽당 도식(표·흐름도·카드)은 3~5개. 글만 있는 쪽도, 도식만 있는 쪽도 피한다.
- 양식이 있으면 양식의 블록 구성을 그대로 따르고, 아래 카탈로그에 없는 요소는 렌더러에 새로 추가한다(`07_output.md` 4절).

### 2. 내용 성격 → 블록

| 내용 성격 | 블록(t) | 쓰는 자리 |
|---|---|---|
| 평가 항목 원문 | `ev` | 첫 쪽 맨 위 |
| 대표 사례 요약 2줄 | `bp` | 첫 쪽 헤더 아래 |
| 비전·슬로건 한 줄 | `vision` | 체계도 위 |
| 대제목(주장형) | `sec` | 섹션 시작 |
| 중제목 + 성격 태그 | `sub` | 큰 섹션을 가·나로 나눌 때 |
| 배경 2~3요소(정책·환경·전략) | `boxes` | 섹션 첫머리 |
| 문제 → 결론 | `kv` + `ar` | 배경 다음 |
| 문제에서 해결로 넘어가는 한 줄 | `banner` | 문제 다음 |
| 라벨 + 내용(추진방향·목적·향후계획) | `kv` | 어디든 |
| 추진내용 묶음(여러 블록을 한 칸에) | `kv` + `inner` | 섹션 본문 |
| 단계·과정·연도별 진행 | `chev` (올해 단계만 `on`) | 추진내용 |
| 요소 결합 → 결과물 | `comb` | 시스템·플랫폼·협업 구조 |
| 기존 → 개선 | `cmp` | 차별성 강조 |
| 요지 한 줄 | `check` | 블록 묶음의 요약 |
| 한 줄 라벨(추진경과·협업·주도) | `line` | 추진내용 끝 |
| 대표 숫자 3~4개 | `kpi` | 성과 직전 |
| 여러 과제·사례 비교 | `tbl` | 과제 묶음형 섹션, 종합성과 |
| 효과 나열(➡ 결과) | `eff` | 성과 앞뒤 |
| 일반 불릿 | `bl` | 주도·참여 구분 등 |
| 서술 문단 | `text` | 서술형 양식, 짧은 설명 |
| 좌우 나란히 | `cols` | 체계도 + 실적, 두 사례 병렬 |
| 그림·도식 이미지 | `img` | 원문 도표, 사진 |
| 섹션 결론 | `res` | **모든 대제목의 끝** |

### 3. content.json 형식

```json
{
  "title": "문서 제목",
  "config": {
    "theme":  { "ink": "#1A1A1A", "g1": "#F2F2F2", "g2": "#E3E3E3", "g3": "#BDBDBD", "g4": "#7A7A7A" },
    "fonts":  { "sans": "Noto Sans CJK KR", "serif": "Noto Serif CJK KR", "docx_sans": "맑은 고딕", "docx_serif": "바탕" },
    "labels": { "result": "추진성과", "best": ["BEST", "PRACTICE"] }
  },
  "pages": [
    { "footer": "2026년도 실적보고서 │ 1", "align": "right", "blocks": [ ... ] }
  ]
}
```
- `config`는 모두 선택이다. 빼면 기본값(흑백, 노토 글꼴/맑은 고딕·바탕, '추진성과')을 쓴다.
- 바닥글은 보통 홀수쪽 오른쪽, 짝수쪽 왼쪽(`align`). 양식에 맞춘다.
- 텍스트 마크업: `**굵게**`, `__밑줄+굵게__`, `[[연한 태그]]`, `{{진한 태그}}`.

#### 블록 필드

| t | 필드 |
|---|---|
| `ev` | `label`, `text` |
| `bp` | `items`[2], 선택 `label`[2] |
| `vision` | `k`, `text` |
| `sec` | `no`, `title`, 선택 `tag` |
| `sub` | `title`, 선택 `tag` |
| `boxes` | `items`[{`h`, `b`[]}] (2~3개) |
| `kv` | `k`(`/`로 줄바꿈), 그리고 `text` 또는 `b`[], 선택 `ar`, 선택 `inner`[블록] |
| `banner` | `text` |
| `chev` | `st`[{`h`, `t`[], 선택 `on`}] (3~4단) |
| `check` | `text` |
| `comb` | `cards`[{`h`, `b`[]}] (2~3개), `res`[3줄] |
| `cmp` | `a`{`tag`,`h`,`b`[]}, `b`{`tag`,`h`,`b`[]} |
| `line` | `k`, `v` |
| `kpi` | `items`[{`v`, `l`}] (3~4개) |
| `tbl` | `w`[비율], `head`[], `rows`[][] |
| `eff` | `k`, `v`, `rows`[[내용, '➡ 결과']] |
| `bl` | `b`[] |
| `text` | `p`[문단] |
| `cols` | `cols`[[블록], [블록]], 선택 `w`[비율] |
| `img` | `src`(content.json 기준 경로), `w_mm`, `h_mm`, 선택 `caption` |
| `res` | `b`[] (3줄 이내), 선택 `label` |

완성 예: `examples/demo/content.json`, `assets/content_template.json`.

### 4. 양식을 블록에 대응시키기

1. 양식 각 쪽을 이미지로 보며 요소마다 이름을 붙인다(예: '좌측 회색 라벨 + 오른쪽 본문' → `kv`).
2. 대응하는 블록이 있으면 그대로 쓰고, 색·선·글꼴·라벨은 `config`로 맞춘다.
3. 대응이 안 되는 요소는 다음 순서로 해결한다.
   - 기존 블록 조합으로 표현(예: 2단 배치 → `cols`, 서술형 → `text`)
   - 원문 도표·사진이면 `img`
   - 그래도 안 되면 새 블록을 `render_html.js`와 `render_docx.js` **양쪽에** 추가한다. 한쪽에만 추가하면 PDF와 Word가 달라진다.
4. 양식의 칸 이름(추진배경, 추진성과 등)은 그대로 쓴다. 다른 이름을 쓰는 양식이면 `labels`와 블록의 `k`·`label`을 바꾼다.

### 5. 블록 선택 점검
- [ ] 모든 대제목이 `res`로 끝난다
- [ ] 쪽마다 기억할 숫자 하나가 큰 글씨(`kpi`나 `res` 밑줄)로 보인다
- [ ] 흐름도에서 올해 단계만 강조했다
- [ ] 같은 블록이 한 쪽에 세 번 이상 연달아 나오지 않는다

## A-07. 결과물 만들기: PDF·Word(·HWPX)

### 1. 환경별 결과물

| 환경 | 결과물 |
|---|---|
| 코드를 실행할 수 있음(Claude, Codex, 코드 실행이 켜진 ChatGPT 등) | content.json → **PDF + Word(.docx)** |
| 코드를 실행할 수 없음 | **Markdown 지면안**(3절)과 content.json. 사용자가 다른 환경에서 렌더링하거나 그대로 옮겨 쓴다 |
| HWPX가 필요함 | PDF→HWPX 변환 도구가 있으면 사용한다. 없으면 Word를 한글에서 열어 'HWPX로 저장'하도록 안내한다 |

### 2. 렌더링 명령

`scripts/` 폴더 안의 파일을 작업 폴더에 둔 채로 실행한다. `render_html.js`는 같은 폴더의 `base.css`를 읽는다.

```bash
# 0) 준비 (처음 한 번)
npm ls docx >/dev/null 2>&1 || npm install docx
pip install olefile openpyxl playwright 2>/dev/null   # 필요한 것만

# 1) 첨부 읽기
python3 -I scripts/read_inputs.py work/inputs 첨부1.pdf 첨부2.hwpx 첨부3.xlsx

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

### 3. 코드 없이 쓸 때: Markdown 지면안

렌더링을 못 하는 환경에서는 지면을 Markdown 표로 표현한다. 사람이 그대로 한글·Word에 옮겨 쓸 수 있게 한다.

```markdown
| 평가내용① | (평가 항목 원문) |
|---|---|

> **BEST PRACTICE**
> ① …
> ② …

## 1  (주장형 대제목)  `B.P①`

| 정부 정책 | 대외 환경 | 기관 전략 |
|---|---|---|
| · … | · … | · … |

| 문제점 | · …<br>**➡ …** |
|---|---|

> ▼ **(전환 문장)** ▼

| 추진내용 | ① … ▶ **② …(올해)** ▶ ③ … |
|---|---|

| 추진성과 | · …<br>· … |
|---|---|
```

### 4. 새 블록 추가 방법

양식에 기존 블록으로 표현할 수 없는 요소가 있을 때만 추가한다.
1. `render_html.js`의 `R` 객체에 `새이름: b => '<div class="새이름">…</div>'`를 추가하고 `extra` CSS에 스타일을 넣는다.
2. `render_docx.js`의 `R` 객체에 같은 이름으로 `(b, w) => T([[C(...)]], [w])` 형태를 추가한다. `w`는 쓸 수 있는 폭(DXA)이다.
3. 두 결과물을 모두 렌더해서 모양이 같은지 이미지로 확인한다.
4. 블록 함수가 배열을 돌려주면 펼쳐서 넣는다(중첩 배열은 Word XML 오류를 낸다). 렌더러의 `push()`가 이를 처리한다.

### 5. 지면 맞춤

- 쪽수는 정확히 지킨다(`pdfinfo`로 확인).
- **PDF**: 쪽별 내용 하단이 약 900~1,040px면 알맞다(한계 1,075px, 넘으면 바닥글과 겹친다).
- **Word**: 쪽별 채움 0.80~0.91이 알맞다. 사용자 PC의 실제 글꼴이 점검 환경의 대체 글꼴보다 넓을 수 있어 5~10% 여유를 둔다. 글자배율 1.13~1.24, 간격배율 1.5~2.0 사이에서 조정한다.
- **빈칸이 남으면** 글자를 키우지 말고 자료에서 근거를 더 넣는다(전후 비교, KPI, 기대효과, 과제 표). **넘치면** 등급이 낮은 내용부터 뺀다.
- 렌더한 쪽을 **이미지로 직접 보고** 확인한다: 태그 잘림, 라벨 줄바꿈, 표·흐름도 칸 넘침, 바닥글 겹침.

### 6. 납품 파일
- `보고서명.pdf`, `보고서명.docx`
- 작업 기록(사용자가 원하면 함께 준다): `facts.md`, `storyline.md`, `content.json`, 새 양식이면 `style.md`(양식 명세)

## A-08. 품질 점검과 답변 형식

### 1. 사실성 규칙 (가장 중요)

1. **원문에 없는 수치·사실은 쓰지 않는다.** 모르는 값(정책 번호, 쪽번호 등)은 `○○`로 비우고 보고한다.
2. **계획과 완료를 구분한다.** 계획서에만 있는 일은 '착수·추진'으로 쓰고 '완료·달성'으로 쓰지 않는다.
3. **목표·추정치는 표시한다:** (목표), (추정), 예상.
4. **미완 자료는 넣지 않는다.** '??', '상세 미확보', 빈칸은 제외하고 보고한다.
5. **근거 없는 성격 태그를 붙이지 않는다.** '지적반영', '최초', '유일'은 자료에 근거가 있을 때만 쓴다.
6. **추정한 것은 밝힌다.** 연도, 쪽번호, 보고서 종류, 실적기간 등.
7. **양식의 내용은 가져오지 않는다.** 다른 조직의 사업·수치가 섞이지 않았는지 확인한다.

### 2. 납품 전 점검표

**사실**
- [ ] 보고서의 모든 수치·날짜가 facts.md의 카드와 연결되고, 원문 텍스트에서 다시 찾아진다(검색으로 대조)
- [ ] 수치 충돌을 정리했고, 채택하지 않은 값을 기록했다
- [ ] 계획/완료, 목표/추정 표시가 맞다

**방향**
- [ ] 성과지표가 있으면 모든 세부평가내용에 대응하는 섹션이 있다(없으면 '자료 부족'으로 보고)
- [ ] 전년도 지적사항, 지정 과제를 반영했다
- [ ] 핵심 메시지가 문서 처음(대표 사례 요약)과 끝(종합성과)에서 일치한다

**흐름**
- [ ] 제목만 이어 읽어도 핵심 메시지가 전달된다
- [ ] 문제의 숫자가 성과에서 같은 단위로 돌아온다
- [ ] 모든 숫자에 비교 기준이 있다
- [ ] 같은 사실을 두 번 쓰지 않았다
- [ ] 모든 대제목이 성과로 끝난다

**형식**
- [ ] 양식이 있으면 문체 프로필(style.md)과 어긋나는 문장이 없다
- [ ] 가이드라인 규정(쪽수, 글자 크기, 필수 항목, 금지 표현)을 하나씩 지켰다
- [ ] 지정 쪽수와 정확히 같다
- [ ] 렌더한 쪽을 이미지로 보고 잘림·겹침이 없음을 확인했다

### 3. 답변 형식

결과물(PDF·Word)을 첨부하고, 본문은 아래 순서로 짧게 쓴다.

1. **한 줄 요약**: 몇 쪽, 어떤 모드(자료만/양식/지표), 핵심 메시지
2. **첨부 판별표**: 파일 | 역할 | 근거 (첫 답변에서만)
3. **스토리라인 요약**: 쪽 | 섹션 제목 | 대표 숫자
4. **자료 사용 내역**: 대표 사례로 올린 것, 뺀 것과 이유(지표 무관, 기간 외, 중복, 근거 부족)
5. **지표·가이드라인 점검**: 항목별 대응 여부 (해당 시)
6. **확인 필요 사항**: 계획/완료 불확실, 수치 충돌, 추정치, 임의로 정한 값, `○○`, 자료 부족

글은 짧게 쓴다. 판별표·구성표·확인 사항은 표나 번호 목록으로 쓴다.

### 4. 후속 요청 처리

| 요청 | 처리 |
|---|---|
| 문구·수치 수정 | content.json만 고쳐 PDF·Word를 다시 만든다 |
| 추가 자료 첨부 | 전부 읽고 facts.md에 추가 → 등급 재평가 → 스토리라인 갱신(쪽수 유지, 약한 내용과 교체) → 종합성과까지 갱신 |
| 방향 변경("○○을 더 강조") | 03 단계부터 다시: 핵심 메시지·축 수정 → 스토리라인 → 렌더링 |
| 양식 변경 | 05·06 단계만 다시: 문체 프로필·블록 대응 → 같은 내용으로 렌더링 |
| 쪽수 변경 | 스토리라인의 지면 배분만 다시 하고, 등급 순으로 넣거나 뺀다 |
| "구성안만 먼저" | 스토리라인 표까지만 만들어 보여주고 멈춘다 |

---

# 부록 B. 스크립트와 데이터 틀

아래 파일을 **이름 그대로** 한 폴더에 저장해 쓴다(`render_html.js`는 같은 폴더의 `base.css`를 읽는다). Word 출력에는 `npm install docx`, PDF 출력에는 Playwright가 필요하다.

### 파일: read_inputs.py

```python
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
```

### 파일: render_html.js

```js
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
```

### 파일: base.css

```css
/* 기본 지면 스타일. 색·글꼴은 content.json의 config로 덮어쓴다. */
@page{size:A4;margin:0}
:root{--ink:#1a1a1a;--g1:#f2f2f2;--g2:#e3e3e3;--g3:#bdbdbd;--g4:#7a7a7a;--sans:"Noto Sans CJK KR","Malgun Gothic",sans-serif;--serif:"Noto Serif CJK KR","Batang",serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--ink);font-size:10.0pt;line-height:1.42;background:#fff}
.page{width:210mm;height:297mm;padding:11mm 12mm 9mm;position:relative;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.serif{font-family:var(--serif)}
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
.footer{position:absolute;bottom:6mm;font-size:9.3pt;color:var(--g4);font-weight:700}
.footer.l{left:12mm}.footer.r{right:12mm}
.note{font-size:8.1pt;color:var(--g4)}
```

### 파일: to_pdf.py

```python
#!/usr/bin/env python3
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

### 파일: render_docx.js

```js
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
```

### 파일: fill_check.py

```python
#!/usr/bin/env python3
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

### 파일: content.json (빈 틀)

```json
{
  "title": "보고서 제목",
  "config": {
    "labels": { "result": "추진성과", "best": ["BEST", "PRACTICE"] }
  },
  "pages": [
    {
      "footer": "○○년도 실적보고서 │ 1",
      "align": "right",
      "blocks": [
        { "t": "ev", "label": "평가내용①", "text": "(성과지표의 평가 항목 원문, 없으면 보고서 주제)" },
        { "t": "bp", "items": ["① **[대표 사례 1]** (수단)으로 (결과·숫자)", "② **[대표 사례 2]** (수단)으로 (결과·숫자)"] },
        { "t": "sec", "no": "1", "title": "(수단)으로 (결과) — 주장형 제목", "tag": "B.P①" },
        { "t": "boxes", "items": [
          { "h": "정부 정책", "b": ["(상위 정책과의 연결)"] },
          { "h": "대외 환경", "b": ["(환경 변화 + 숫자 1개)"] },
          { "h": "기관 전략", "b": ["(기관 전략과의 연결)"] }
        ] },
        { "t": "kv", "k": "문 제 점", "b": ["(기존 방식의 한계)"], "ar": "➡ (핵심 문제, 숫자)" },
        { "t": "banner", "text": "(해결 방향 한 줄)" },
        { "t": "kv", "k": "추 진/내 용", "inner": [
          { "t": "chev", "st": [
            { "h": "(1단계)", "t": ["(내용)"] },
            { "h": "(2단계·올해)", "t": ["(내용)"], "on": true },
            { "h": "(3단계)", "t": ["(내용)"] }
          ] },
          { "t": "line", "k": "추진경과", "v": "(단계)('YY.M) → (단계) → (단계)" }
        ] },
        { "t": "res", "b": ["(외부 인정)", "(정량 성과: 기준 → 결과)", "(확산·다음 단계)"] }
      ]
    }
  ]
}
```
