# v2.3 토큰 경량화 연구 기록

기준일: 2026-11-03

기준 버전: 저장소의 현재 v2.2

상태: 구조 경량화·정적 계측·로컬 검증 진행. Opus 5.5 동일 자료 전후 실행은 미실시.

## 1. 결론부터

1. v2.2의 주요 정적 병목은 ZIP 크기나 `SKILL.md` 하나가 아니라, 완성 보고서마다 `references/01~08`을 사실상 모두 읽고 양식이 없으면 09까지 읽은 뒤 `SKILL.md`의 보정표가 그 일부를 다시 덮어쓰는 구조다.
2. v2.3은 v2.2의 최종 품질 규칙을 조건부 참고문서 6개로 재배치했다. 보고서 경로의 지침·작업 서식은 41,263~45,098자에서 12,682~15,060자로 줄었다. 정확한 문자 감소율은 66.6~69.3%다.
3. 이 감소율은 **Claude 토큰 감소율이나 전체 작업량 감소율이 아니다.** 한국어 Opus 5.5 토큰은 공식 Token Counting API로 세고, 전체 사용량·시간은 실제 동일 조건 실행으로 확인해야 한다.
4. 사용자가 관찰한 `Opus 5.5 Extra, 30분, 5시간 한도의 약 50%`는 중요한 기준선이지만, 공개된 고정 환산식이 없어 토큰으로 역산할 수 없다.
5. 현재 환경에는 `ANTHROPIC_API_KEY`가 없다. 따라서 정확한 토큰 숫자를 추정치로 꾸미지 않고 공식 API를 호출하는 `token_audit.py`와 실제 전후 실험 절차를 제공한다.

## 2. 무엇을 측정할 수 있나

| 항목 | 상태 | 방법 |
|---|---|---|
| 파일 바이트·문자·줄 | 정확히 측정 가능 | 로컬 파일 계측 |
| 특정 요청의 모델 입력 토큰 | 공식 사전 추정 가능 | Anthropic `/v1/messages/count_tokens` |
| API 실행 입력·캐시·출력 토큰 | 실행 후 측정 가능 | Messages API 응답 `usage` |
| 이미지 시각 토큰 | 공식 산식으로 내용 부분 계산 가능 | `ceil(width/28) × ceil(height/28)`; 자동 리사이즈 반영 |
| PDF 사전 입력 토큰 | 공식 추정 가능 | PDF를 Token Counting API에 전송 |
| Claude Code/API 전체 턴·시간 | 실행 후 측정 가능 | 동일 새 세션의 JSON/usage 기록 |
| claude.ai 개별 작업의 정확한 토큰 | 공개 UI만으로 알 수 없음 | 사용률·벽시계 시간만 기록 가능 |
| 5시간 사용률 50%의 토큰 환산 | 알 수 없음 | 계정별 고정 토큰 총량·환산식 비공개 |

Token Counting API도 실제 요청과 조금 다를 수 있는 **사전 추정치**다. 모델별 토크나이저가 다르므로 글자 수나 다른 회사 토크나이저를 Claude 토큰이라고 표시하지 않는다. Anthropic은 Claude 4.7 계열부터 이전 모델보다 토큰이 약 30% 더 많이 산출될 수 있으므로 대상 모델로 직접 세라고 안내한다.

## 3. 공식 Claude 근거

### 3.1 스킬은 점진적으로 읽힌다

Anthropic의 [Agent Skills 개요](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)는 다음 구조를 설명한다.

- 스킬 메타데이터는 항상 로드된다.
- `SKILL.md` 본문은 스킬이 실행될 때 로드된다.
- 참고문서와 코드는 필요할 때만 읽는다.
- 스크립트를 실행하면 정상 경로에서는 스크립트 전문이 아니라 출력만 문맥에 들어간다.

[스킬 작성 모범 사례](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)는 `SKILL.md`를 개요·목차로 쓰고 상세 내용을 필요할 때 참고문서로 읽는 점진적 공개를 권장하며, 본문은 500줄 이하를 권한다. 따라서 v2.3은 의미가 다른 규칙을 억지로 한 문장으로 압축하지 않고, 입력 조건과 산출물에 따라 문서를 분기했다.

### 3.2 긴 에이전트 작업은 이전 문맥이 누적된다

[비용·지능 최적화 문서](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)는 에이전트가 매 턴 늘어난 대화 이력을 다시 보내므로 긴 작업의 비용이 빠르게 커질 수 있다고 설명한다. [도구 문맥 관리](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)는 도구 정의와 누적 `tool_result`도 문맥을 차지하며, 여러 왕복을 한 프로그램 실행으로 합치고 출력 범위를 줄이는 방법을 제시한다.

프롬프트 캐싱은 가격·지연을 낮출 수 있지만 [컨텍스트 창 문서](https://platform.claude.com/docs/en/build-with-claude/context-windows)가 설명하듯 문맥에서 토큰 자체를 없애지는 않는다. 따라서 v2.3은 `render_report.py`로 렌더 왕복을 합치고, 요구하지 않은 중간 분석 출력과 PDF 전체 페이지 연락판을 줄였다.

### 3.3 문서와 이미지는 별도 비용이 든다

[PDF 지원 문서](https://platform.claude.com/docs/en/build-with-claude/pdf-support)에 따르면 PDF 페이지마다 텍스트를 추출하고 페이지를 이미지로 변환해 둘 다 분석한다. 공개 대략치는 페이지당 텍스트 1,500~3,000토큰에 이미지 토큰이 더해지는 수준이다. 실제 문서는 Token Counting API로 세어야 한다.

[Vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)는 시각 토큰 산식을 `ceil(width/28) × ceil(height/28)`로 공개한다. Claude 4.7+ 고해상도 처리에서는 긴 변 최대 2,576px, 시각 토큰 최대 4,784로 자동 축소될 수 있다. 불필요하게 같은 이미지를 여러 번 열면 그만큼 문맥이 커진다.

[파일 업로드 안내](https://support.claude.com/en/articles/8241126-upload-files-to-claude)에 따르면 비PDF 문서는 주로 텍스트를 추출하며 내장 이미지는 자동 해석하지 않는다. 반면 100쪽 이하 PDF는 텍스트와 시각요소를 함께 분석하고, 101~1,000쪽 PDF는 텍스트 위주다. 따라서 DOCX·XLSX·PPTX 등의 그림 추출 기능은 유지하되, 저해상도 연락판을 먼저 보고 선택 원본만 여는 구조가 필요하다. PDF 전체 쪽 연락판은 기본 생성하지 않는다.

### 3.4 노력 수준은 별도 변수다

[Claude 노력·사고 설정 안내](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)는 높은 노력 수준이 더 많은 토큰·시간을 쓸 수 있다고 설명하며 Opus 5.5는 모든 노력 수준에서 thinking이 켜져 있다고 안내한다. v2.3 구조와 노력 수준 효과를 섞지 않기 위해 전후 시험에서는 모델과 effort를 고정해야 한다.

## 4. v2.2 구조 실측

v2.2의 완성 보고서 작업표는 1~8단계에서 `01_inputs.md`부터 `08_quality.md`까지를 각각 읽게 한다. B가 없으면 `09_default_template.md`도 읽는다. 동시에 `SKILL.md`는 09와 여러 참조의 개정 전 규칙을 별도 표로 다시 보정한다.

정적 계측 범위는 다음과 같다.

```text
SKILL.md
+ 작업 흐름이 명시적으로 읽게 하는 references
+ assets/worksheets.md 또는 work_ledger.md
+ 보고서 경로의 assets/content_template.json
```

스크립트 소스, README·예시·연구자료, A/B/C/D 원자료, 이미지, 제품 시스템 프롬프트·도구 정의는 이 표에 포함하지 않았다.

### 지침·서식 파일별 원측정

UTF-8 바이트는 디스크 전송량, 문자는 UTF-8 디코딩 뒤 Unicode 코드포인트 수다. 둘 다 토큰이 아니다.

| 버전 | 파일 | 바이트 | 문자 | 줄 |
|---|---|---:|---:|---:|
| v2.2 | `SKILL.md` | 20,299 | 11,025 | 233 |
| v2.2 | `references/01_inputs.md` | 4,083 | 2,030 | 49 |
| v2.2 | `references/02_analysis.md` | 9,560 | 4,988 | 145 |
| v2.2 | `references/03_direction.md` | 6,339 | 3,056 | 97 |
| v2.2 | `references/04_storyline.md` | 7,729 | 3,791 | 110 |
| v2.2 | `references/05_style.md` | 4,182 | 2,265 | 75 |
| v2.2 | `references/06_layout.md` | 8,517 | 5,249 | 126 |
| v2.2 | `references/07_output.md` | 5,088 | 3,245 | 95 |
| v2.2 | `references/08_quality.md` | 4,292 | 2,104 | 66 |
| v2.2 | `references/09_default_template.md` | 6,473 | 3,835 | 102 |
| v2.2 | `assets/content_template.json` | 1,983 | 1,655 | 34 |
| v2.2 | `assets/worksheets.md` | 3,070 | 1,855 | 103 |
| v2.3 | `SKILL.md` | 6,349 | 3,115 | 77 |
| v2.3 | `references/core.md` | 5,061 | 2,311 | 63 |
| v2.3 | `references/default_layout.md` | 5,103 | 2,564 | 77 |
| v2.3 | `references/indicators.md` | 1,442 | 650 | 25 |
| v2.3 | `references/layout_render.md` | 2,791 | 1,678 | 47 |
| v2.3 | `references/template.md` | 1,864 | 836 | 30 |
| v2.3 | `references/visuals.md` | 3,930 | 1,878 | 48 |
| v2.3 | `assets/content_template.json` | 1,937 | 1,585 | 34 |
| v2.3 | `assets/work_ledger.md` | 2,266 | 1,279 | 74 |

| 조합 | v2.2 파일 | v2.2 문자 | v2.3 파일 | v2.3 문자 | 감소 | 감소율 |
|---|---:|---:|---:|---:|---:|---:|
| A | 12 | 45,098 | 7 | 14,410 | 30,688 | 68.0% |
| AB | 11 | 41,263 | 7 | 12,682 | 28,581 | 69.3% |
| AC | 12 | 45,098 | 8 | 15,060 | 30,038 | 66.6% |
| AD | 12 | 45,098 | 7 | 14,410 | 30,688 | 68.0% |
| ABC | 11 | 41,263 | 8 | 13,332 | 27,931 | 67.7% |
| ABD | 11 | 41,263 | 7 | 12,682 | 28,581 | 69.3% |
| ACD | 12 | 45,098 | 8 | 15,060 | 30,038 | 66.6% |
| ABCD | 11 | 41,263 | 8 | 13,332 | 27,931 | 67.7% |

v2.3에서 C가 있으면 `indicators.md`, B가 있으면 `template.md`, B가 없고 보고서를 만들면 `default_layout.md`를 읽는다. 모든 보고서에서는 그림 후보·표시 자리를 판단해야 하므로 `visuals.md`, 결과물 생성 시 `layout_render.md`를 읽는다. 도움말은 `SKILL.md`만, 구성안은 렌더링 문서를 제외한다.

## 5. 적용한 경량화와 근거

| 변경 | 직접 줄이는 것 | 품질 보존 장치 |
|---|---|---|
| 공통·C·B·기본 지면·시각·렌더 문서 분리 | 조건에 맞지 않는 지침 입력 | `SKILL.md` 라우팅 표와 원칙 고정 |
| v2.2의 보정표를 최종 규칙 위치로 합침 | 중복·충돌 지침 | 기본 지면·시각 정책을 각 한 파일에서만 정의 |
| 6개 중간 Markdown을 작업 원장 하나로 통합 | 생성 출력·후속 재독 | 사실 ID·출처·충돌·비교·그림 사유 필드 유지 |
| PDF 전체 연락판을 `--pdf-pages` 선택 옵션으로 변경 | 이미지 처리·도구 출력 | Claude의 PDF 시각 분석 우선, 필요한 쪽만 자르기 |
| 연락판→선택 원본 순 | 이미지 시각 토큰 | 전수 후보화 표와 제외 사유 유지 |
| 렌더·변환·점검을 한 명령으로 통합 | 도구 왕복·로그 | 단계별 실패를 JSON 요약에 남김 |
| 런타임 ZIP 화이트리스트 | 업로드 크기·탐색 범위 | 실행에 필요한 SKILL·refs·scripts·assets 포함 |

v2.2 설치 ZIP은 49개 파일·763,815바이트, v2.3 런타임 ZIP은 21개 파일·52,871바이트다(93.1% 감소). 포함 범위가 다르므로 이는 업로드·보관 크기 감소이지 토큰 절감률이 아니다. 제외한 파일을 Claude가 원래 읽지 않았다면 토큰은 줄지 않는다.

## 6. 전체 사용량 식

한 번의 사전 입력을 단순화하면 다음과 같다.

```text
A     = S_A    + a
AB    = S_AB   + a + b
AC    = S_AC   + a + c
AD    = S_AD   + a + d
ABC   = S_ABC  + a + b + c
ABD   = S_ABD  + a + b + d
ACD   = S_ACD  + a + c + d
ABCD  = S_ABCD + a + b + c + d
```

`S_*`는 해당 경로에서 실제로 읽은 스킬 지침 토큰, `a~d`는 대상 Opus 5.5로 센 각 입력 토큰이다. 파일 MB는 토큰이 아니다. 같은 용량도 텍스트·스캔·이미지 밀도에 따라 다르다.

전체 에이전트 작업은 첫 요청 한 번보다 크다.

```text
T_total = Σ(request input + cache creation input + cache read input + output)
```

초기 공통 문맥을 `P0`, 각 턴 뒤 새로 쌓이는 모델 출력·도구 결과를 `Δi`, 호출 수를 `N`이라 하면 개념적으로 다음과 같다.

```text
T_input ≈ Σ[j=1..N] (P0 + Σ[i<j] Δi)
```

따라서 초반에 줄인 공통 지침과 큰 중간 출력은 여러 후속 호출에 반복되어 영향을 줄 수 있다. 실제 값은 제품의 캐시·자동 요약·컨텍스트 편집과 도구 경로에 따라 달라지므로 실행 로그가 필요하다.

## 7. 연구 논문을 적용한 범위

- Liu et al., [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/)는 긴 문맥에서 관련 정보의 위치에 따라 검색 성능이 크게 달라질 수 있음을 보였다. 모든 참고문서를 한꺼번에 넣기보다 필요한 규칙의 밀도를 높이는 근거로 사용했다.
- Jiang et al., [LongLLMLingua](https://aclanthology.org/2024.acl-long.91/)는 장문 프롬프트 압축이 특정 벤치마크에서 비용·지연을 줄일 수 있음을 보였다.
- Pan et al., [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/)는 충실한 압축을 별도 학습·평가 문제로 다룬다.

이 스킬에는 사실성·수치·계획/완료 같은 규칙이 많으므로 자동 토큰 삭제나 의미 압축을 바로 적용하지 않았다. 먼저 조건부 로딩과 중복 제거를 적용하고 품질 회귀를 검증한다. 위 논문의 다른 모델·벤치마크 절감률을 Opus 5.5 보고서 작업의 예상 절감률로 옮겨 쓰지 않는다.

## 8. 재현 방법

로컬 문자·바이트 계측:

```powershell
python research/token_audit.py --skill-dir . --scenario ABCD --task report
```

A/B/C/D까지 공식 사전 토큰 계측:

```powershell
$env:ANTHROPIC_API_KEY = "환경 변수에만 설정"
python research/token_audit.py --skill-dir . --scenario ABCD --task report `
  --A work/A.txt --B work/B.pdf --C work/C.txt --D work/D.txt --count-tokens --json
```

PDF와 이미지는 API에 직접 보낼 수 있다. DOCX·XLSX·PPTX·HWP는 실제 작업과 같이 `read_inputs.py`로 추출한 텍스트와 Claude가 실제로 볼 그림만 넘긴다.

## 9. 실제 전후 검증 설계

먼저 1회 파일럿, 이상이 없으면 조건당 3회 독립 실행한다.

고정 조건:

- 새 대화에서 시작
- 동일 Opus 5.5, 동일 effort
- 동일 사용자 요청, A/B/C/D, 도구, 결과 형식·쪽수
- v2.2/v2.3 이름을 가리고 결과 품질 평가

기록값:

- 입력·캐시 생성·캐시 읽기·출력 토큰
- 총 시간, API 처리 시간, 모델 턴, 도구 호출 수
- claude.ai 시험이면 시작·종료 사용률과 벽시계 시간(토큰과 별도)

품질 통과 조건:

- 원문에 없는 사실·수치 0건
- 모든 보고서 수치·날짜의 출처 추적
- 계획/완료, 목표/실적 오류 0건
- C 필수 항목 누락 0건 또는 자료 부족 명시
- B 구조·말투·지면과 D 제약 준수
- 최상단 BEST PRACTICE 미생성, 중제목 `B.P` 정책 준수
- 원자료 그림·`[이미지 삽입]` 정책과 지정 쪽수 준수
- 핵심 메시지·제목 흐름의 블라인드 품질 비열등

v2.3의 성공은 문자·ZIP 크기만으로 판정하지 않는다. 실제 토큰·시간이 줄고 위 품질 조건을 통과해야 한다.

### 현재 로컬 검증 결과

- 공식 `skill-creator` 구조 검사: 원본 폴더와 배포 ZIP을 다시 푼 폴더 모두 통과
- Python 8개 AST 구문, JavaScript 2개 구문, JSON 2개 파싱: 통과
- PDF 텍스트 추출: `pdftotext`가 없는 환경에서 `pypdf` 대체 경로로 2쪽·2,035자 추출
- PDF 전체 페이지 연락판: 기본 실행에서 생성되지 않고 `--pdf-pages`에서만 생성됨
- DOCX 내장 그림: 데모 파일에서 유효 그림 4개와 연락판 추출
- `content_template.json` HTML·Word 렌더: 최상단 BEST PRACTICE 없음, 중제목 `B.P`와 `[이미지 삽입]` 표시 렌더 확인
- Edge 기반 A4 PDF 생성·페이지 이미지 육안 점검: 첫 쪽 제목→평가내용→핵심성과→대제목 순서, 잘림·바닥글 겹침 없음
- 배포 ZIP: 21개 파일·52,871바이트, 최상위 `performance-report-writer-v2-3/`, README·연구·예시·개발 도구·토큰 파일 없음
- 배포 ZIP SHA-256: `7C39786D0806F4CE237B972CB95D8074F4C64C9F9369F4D6AA34729338ECE8C5`
- Opus 5.5 실제 전후 토큰·시간·블라인드 품질: 미실행

## 10. 알 수 없는 것과 추가로 필요한 것

- 실제 Opus 5.5 토큰 표를 채우려면 Anthropic API 키가 필요하다. 키는 환경 변수로만 사용한다.
- 사용자가 실제로 쓰는 claude.ai의 효과는 동일 A/B/C/D와 같은 요청으로 v2.2·v2.3 ZIP을 각각 실행해야 확인할 수 있다.
- 8개 조합을 모두 실험하려면 비식별 A와 B/C/D 시험 파일이 각각 필요하다.
- Claude Code/API 결과를 claude.ai 5시간 한도의 정확한 토큰으로 환산할 수 없다.

## 11. 출처

- Anthropic, [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Anthropic, [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Anthropic, [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- Anthropic, [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- Anthropic, [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)
- Anthropic, [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)
- Anthropic, [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
- Anthropic, [Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- Anthropic, [Upload files to Claude](https://support.claude.com/en/articles/8241126-upload-files-to-claude)
- Anthropic, [Model effort and thinking settings](https://support.claude.com/en/articles/8664678-change-the-model-effort-and-thinking-settings)
- Liu et al. 2024, [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/)
- Jiang et al. 2024, [LongLLMLingua](https://aclanthology.org/2024.acl-long.91/)
- Pan et al. 2024, [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/)
