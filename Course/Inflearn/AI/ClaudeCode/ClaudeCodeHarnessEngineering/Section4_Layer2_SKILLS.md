
# Claude Code Skills 심화

## 1. Skills란?

Skills는 Claude가 어떻게 행동할지를 정의한 **Playbook**이다.

- 한 번 만들어두면 여러 대화에서 재사용 가능
- `/skill-name [인수]` 형태로 직접 호출 가능
- 대화 맥락을 보고 Claude가 자동으로 트리거할 수도 있음
- 모든 Skill은 `SKILL.md` 파일로 시작
- YAML Frontmatter → 행동 설정
- Markdown 본문 → 실제 지침

### 기존 방식과 비교

| 방식 | 재사용 | 자동 트리거 | 인수 | 지원 파일 |
|---|---|---|---|---|
| 단순 프롬프트 | ✗ | ✗ | ✗ | ✗ |
| CLAUDE.md | ✓ | ✓ | ✗ | ✗ |
| `.claude/commands/` | ✓ | ✓ | `$ARGUMENTS` | ✗ |
| `.claude/skills/` | ✓ | ✓ | `$ARGUMENTS` | ✓ |

기존 `.claude/commands/` 파일은 계속 동작한다.

Skills는 여기에 다음 기능을 추가한다.

- 지원 파일
- 호출 제어
- Subagent 실행

### Skills를 사용하는 경우

- 반복적으로 사용하는 워크플로우
- 팀과 공유할 지침
- 지원 스크립트나 템플릿이 필요한 작업

---

## 2. Skills 저장 위치

Skills는 4단계 계층으로 저장할 수 있다.

| 계층 | 경로 | 적용 범위 |
|---|---|---|
| Enterprise | 관리자 설정 | 조직 전체 사용자 |
| Personal | `~/.claude/skills/<name>/SKILL.md` | 모든 프로젝트 |
| Project | `.claude/skills/<name>/SKILL.md` | 해당 프로젝트 |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | 플러그인 활성화 위치 |

### 우선순위

```text
Enterprise
    ↓
Personal
    ↓
Project
    ↓
Plugin
````

높은 계층이 낮은 계층을 덮어쓴다.

Plugin Skill은 다음과 같은 namespace를 사용한다.

```text
plugin:skill-name
```

### 중첩 자동 탐색

Monorepo에서 특정 디렉터리의 파일을 작업할 경우 해당 디렉터리의 `.claude/skills/`도 자동으로 검색된다.

예:

```text
packages/frontend/
└── .claude/
    └── skills/
```

---

## 3. Claude Code 기본 탑재 Skills

설치 없이 사용할 수 있는 프롬프트 기반 Playbook이 있다.

### `/batch`

코드베이스 전반의 변경을 여러 작업으로 분해해 병렬 처리한다.

```text
/batch <instruction>
```

### `/simplify`

코드 품질을 검토하고 개선한다.

* 재사용성
* 품질
* 효율성

3개의 리뷰 에이전트를 병렬로 생성한다.

### `/debug`

디버깅 로깅을 활성화하고 세션 로그를 분석해 문제를 진단한다.

```text
/debug [description]
```

### `/loop`

지정한 간격으로 프롬프트를 반복 실행한다.

```text
/loop [interval] <prompt>
```

배포 폴링, PR 모니터링 등에 사용할 수 있다.

### `/claude-api`

코드에서 `anthropic` 또는 `@anthropic-ai/sdk`를 import할 때 자동으로 활성화된다.

Claude API 및 Agent SDK 문서를 로드한다.

---

## 4. 첫 번째 Skill 만들기

### 디렉터리 구조

```text
~/.claude/skills/
└── explain-code/
    ├── SKILL.md
    ├── examples/
    │   └── sample.md
    └── scripts/
        └── helper.sh
```

### SKILL.md

```yaml
---
name: explain-code
description: 코드를 비유와 다이어그램으로 설명.
"이게 왜 이렇게 동작해?", "코드 설명해줘"라고 할 때 사용.
---

## 코드 설명 원칙

1. **비유로 시작**: 실생활 비유
2. **다이어그램**: ASCII 흐름도
3. **단계별 분해**: 줄 단위 설명
4. **함정 경고**: 흔한 오해 짚기
```

### 생성

```bash
mkdir -p ~/.claude/skills/explain-code
```

그 후 `SKILL.md`를 만들면 된다.

Claude Code를 재시작하지 않아도 즉시 인식된다.

### 테스트

직접 호출:

```text
/explain-code src/auth/login.ts
```

또는 자연어로:

```text
이 코드 어떻게 동작해?
```

### 권장

`SKILL.md`는 500줄 이하로 유지하고 상세 레퍼런스는 지원 파일로 분리한다.

---

## 5. Frontmatter 핵심 필드

### `name`

슬래시 명령어가 된다.

```yaml
name: my-skill
```

→

```text
/my-skill
```

* 소문자
* 숫자
* 하이픈
* 최대 64자

### `description`

Claude가 자동 트리거 시기를 판단하는 기준이다.

주요 사례를 앞에 배치한다.

250자를 초과하면 잘린다.

### `disable-model-invocation`

```yaml
disable-model-invocation: true
```

Claude가 자동으로 Skill을 로드할 수 없고 사용자만 `/명령어`로 실행할 수 있다.

배포, 커밋처럼 부작용이 있는 작업에 사용한다.

### `user-invocable`

```yaml
user-invocable: false
```

사용자 `/메뉴`에서는 숨겨지고 Claude만 사용할 수 있다.

사용자가 직접 실행할 필요가 없는 배경 지식 Skill에 사용한다.

### `allowed-tools`

Skill 실행 중 추가 승인 없이 사용할 수 있는 도구를 지정한다.

예:

```yaml
allowed-tools: Read Grep Glob Bash(git *)
```

### `context`

```yaml
context: fork
```

격리된 Subagent에서 실행한다.

---

## 6. Skill 호출 제어

| 설정                               | 사용자 호출 | Claude 자동 호출 |
| -------------------------------- | ------ | ------------ |
| 기본값                              | ✓      | ✓            |
| `disable-model-invocation: true` | ✓      | ✗            |
| `user-invocable: false`          | ✗      | ✓            |

### `disable-model-invocation: true`

예:

```text
/deploy
/commit
/send-slack-message
```

Claude가 스스로 배포나 메시지 전송을 실행하면 안 되는 작업에 사용한다.

### `user-invocable: false`

예:

```text
/legacy-system-context
/api-conventions
```

사용자가 직접 실행할 필요는 없지만 Claude가 배경 지식으로 알아야 하는 규칙이나 패턴에 사용한다.

---

## 7. 인수 전달

`$ARGUMENTS`를 사용하면 Skill에 동적 입력을 전달할 수 있다.

### `$ARGUMENTS`

`/skill-name` 뒤에 오는 전체 문자열로 치환된다.

### `$ARGUMENTS[N]`

0부터 시작하는 인덱스로 개별 인수에 접근한다.

```text
$0
$1
$2
```

은 각각

```text
$ARGUMENTS[0]
$ARGUMENTS[1]
$ARGUMENTS[2]
```

의 짧은 별칭이다.

### 예시

```yaml
---
name: migrate-component
description: 컴포넌트를 한 프레임워크에서 다른 프레임워크로 마이그레이션
---

$0 컴포넌트를 $1에서 $2로 마이그레이션하세요.

기존 동작과 테스트를 모두 보존하세요.
```

사용:

```text
/migrate-component SearchBar React Vue
```

결과:

```text
$0 → SearchBar
$1 → React
$2 → Vue
```

### 추가 변수

```text
${CLAUDE_SESSION_ID}
```

→ 현재 세션 ID

```text
${CLAUDE_SKILL_DIR}
```

→ `SKILL.md`가 위치한 디렉터리 경로

---

## 8. 동적 컨텍스트 주입

```text
!`명령어`
```

구문을 사용하면 Skill 내용이 Claude에게 전달되기 전에 셸 명령어가 실행된다.

명령어 출력이 해당 위치의 플레이스홀더를 대체한다.

### 예시

```yaml
---
name: pr-summary
description: PR 변경 내용 요약
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## PR 컨텍스트

- diff: !`gh pr diff`
- 댓글: !`gh pr view --comments`
- 파일: !`gh pr diff --name-only`

## 작업

이 PR의 목적, 주요 변경 사항, 리뷰 포인트를 요약하세요.
```

### 실행 순서

```text
① Skill 호출
   ↓
② !`명령어` 실행
   ↓
③ 결과로 치환
   ↓
④ Claude에 전달
```

이것은 **전처리(pre-processing)**다.

Claude가 나중에 명령어를 실행하는 것이 아니라 Claude에게 전달되기 전에 실행된다.

---

## 9. Subagent에서 Skill 실행

```yaml
context: fork
```

를 설정하면 Skill이 격리된 독립 환경에서 실행된다.

```text
현재 대화
    ↓
context: fork Skill 호출
    ↓
격리된 Subagent
    ↓
SKILL.md = 프롬프트
    ↓
결과 요약
    ↓
주 대화로 반환
```

대화 기록 없이 Skill 내용 자체가 Subagent의 프롬프트가 된다.

### Agent 종류

```yaml
agent: Explore
```

→ 읽기 전용 코드베이스 탐색에 최적화

```yaml
agent: Plan
```

→ 구현 전략 설계에 특화

```yaml
agent: general-purpose
```

→ 범용 실행

### 주의

`context: fork`는 **실행 가능한 지침이 있는 Skill**에 의미가 있다.

단순 참조 문서 Skill에 붙이면 Subagent가 빈 결과를 반환할 수 있다.

---

## 10. 지원 파일로 Skill 확장

### 권장 구조

```text
my-skill/
├── SKILL.md
├── reference.md
├── examples/
│   └── sample.md
└── scripts/
    └── helper.py
```

### SKILL.md에서 참조

```yaml
---
name: api-docs
description: API 문서 생성
---

# 핵심 지침만 여기에

## 추가 참조

- API 스펙: [reference.md](reference.md)
- 출력 예시: [examples/sample.md](examples/sample.md)

# 스크립트 실행

!`python ${CLAUDE_SKILL_DIR}/scripts/helper.py`
```

### 파일을 분리하는 이유

`SKILL.md`는 핵심 지침에 집중하고,

* 상세 레퍼런스
* 예제
* 스크립트

등은 필요할 때 활용한다.

이를 통해 불필요한 컨텍스트 낭비를 방지한다.

### `${CLAUDE_SKILL_DIR}`

현재 작업 디렉터리와 관계없이 Skill 번들 파일을 정확하게 참조할 수 있다.

---

## 11. Code Reviewer Skill

```yaml
---
name: code-review
description: 코드 리뷰 수행. 보안·성능·유지보수성 분석.
"코드 리뷰해줘", "이 파일 검토해줘"라고 할 때 사용.
context: fork
agent: Explore
allowed-tools: Read Grep Glob
---
```

### 리뷰 기준

```text
1. 보안
   - 입력 검증 누락
   - 인증 허점
   - 위험 패턴

2. 성능
   - 불필요한 루프
   - N+1 쿼리
   - 메모리 낭비

3. 가독성
   - 함수 길이
   - 중복 코드
   - 모호한 변수명

4. 엣지 케이스
   - 빈 입력
   - null 처리
   - 경계값
```

각 항목을 Severity와 함께 정리한다.

```text
🔴 High
🟡 Medium
🟢 Low
```

마지막에 종합 점수 `/ 10`을 추가한다.

### 사용

```text
/code-review src/auth/login.ts
```

또는

```text
이 파일 보안 리뷰해줘
```

### 이 Skill의 구조

```text
context: fork
→ 격리 실행

agent: Explore
→ 읽기 전용

allowed-tools: Read Grep Glob
→ 코드 리뷰에 필요한 도구만 사용
```

---

## 12. Skills 배포 및 공유

### 프로젝트 커밋

```text
.claude/skills/
```

를 Git에 커밋한다.

팀 전체가 같은 Skill을 공유할 수 있다.

예:

* PR 리뷰 Skill
* 배포 Skill
* 테스트 Skill

### 플러그인 패키징

Plugin의 `skills/` 디렉터리에 추가한다.

```text
plugin:skill-name
```

namespace를 사용해 충돌 없이 배포할 수 있다.

### 관리자 배포

관리 설정을 통해 조직 전체에 배포할 수 있다.

예:

* 코딩 표준
* 보안 정책
* 사내 워크플로우

### Skill이 트리거되지 않을 때

1. `description`에 사용자가 자연스럽게 말할 키워드가 있는지 확인
2. `/skill-name`으로 직접 호출해서 Skill이 인식되는지 테스트

---

# 핵심 5가지

1. **Skill = Playbook**

   * `SKILL.md` 하나로 Claude의 역량을 확장
   * `/명령어` 직접 호출 또는 대화 맥락에서 자동 트리거

2. **4단계 저장 계층**

   * Enterprise
   * Personal
   * Project
   * Plugin

3. **호출 제어**

   * `disable-model-invocation` → 사용자 전용
   * `user-invocable: false` → Claude 전용
   * 부작용이 있는 작업에는 호출 제어를 설정

4. **동적 주입과 인수**

   * `$ARGUMENTS` → 입력 전달
   * `!`command`` → 실시간 데이터를 Claude에 공급

5. **Subagent 격리**

   * `context: fork`
   * 독립 환경에서 실행
   * 복잡한 분석 작업을 메인 대화와 분리해서 위임

---


```
```
