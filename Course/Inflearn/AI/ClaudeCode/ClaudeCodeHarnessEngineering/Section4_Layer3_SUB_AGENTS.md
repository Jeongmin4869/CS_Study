# Claude Code Layer3 Sub-agents 

## 1. Sub-agent란?

**Sub-agent = 특정 역할과 전문성을 갖도록 직접 정의한 독립적인 AI 에이전트**

메인 에이전트가 작업의 일부를 Sub-agent에 위임하면, Sub-agent는 별도의 컨텍스트에서 작업을 수행하고 결과를 메인 대화로 반환한다.

### 핵심 특징

- **독립된 컨텍스트**: 메인 대화와 분리된 환경에서 작업
- **역할 지정**: 시스템 프롬프트로 전문 분야와 작업 원칙 정의
- **도구 제한**: 필요한 도구만 허용하도록 설정
- **모델 지정**: 작업에 맞는 모델 선택
- **재사용**: 한 번 정의한 에이전트를 여러 작업에서 활용

### 왜 사용하는가?

메인 대화에서 모든 파일 탐색, 로그 분석, 테스트 실행을 처리하면 중간 결과와 실패 기록이 컨텍스트를 많이 차지할 수 있다.

Sub-agent에 작업을 위임하면 상세한 작업 과정은 분리하고, 필요한 결과를 메인 대화에서 활용할 수 있다.

---

## 2. Sub-agent와 Skill의 차이

| 구분 | Sub-agent | Skill |
|---|---|---|
| 핵심 개념 | 특정 역할을 수행하는 에이전트 | 특정 작업을 수행하는 방법과 지침 |
| 정의 방법 | 에이전트 설정과 시스템 프롬프트 | `SKILL.md` |
| 주요 역할 | 작업을 분석하고 수행 | 반복 가능한 작업 절차와 지침 제공 |
| 컨텍스트 | 독립된 컨텍스트에서 실행 가능 | 일반 실행 또는 `context: fork`를 통한 격리 실행 |
| 활용 예시 | 코드 리뷰어, 디버거 | 코드 설명, PR 요약 |

### 예시

**Sub-agent: 로그인 버그 수정**

```text
파일 탐색
    ↓
원인 분석
    ↓
코드 수정
    ↓
검증
    ↓
결과 보고
```

**Skill: 코드 설명 지침**

```text
코드 입력
    ↓
정의된 설명 원칙 적용
    ↓
설명 결과 반환
```

Sub-agent는 특정 역할을 수행하는 에이전트이고, Skill은 작업을 수행하는 방법을 정의한 지침이다.

두 기능은 함께 사용할 수도 있다.

---

# 3. Sub-agent를 사용하기 좋은 6가지 상황

## ① 대량 출력 격리

대량의 결과가 메인 컨텍스트를 차지하지 않도록 별도로 분석한다.

| 작업 | Sub-agent의 역할 | 메인 대화로 반환할 결과 |
|---|---|---|
| 테스트 실행 | 전체 테스트 실행 및 실패 분석 | 실패 항목과 오류 메시지 |
| 로그 분석 | 대량 로그 분석 | 이상 패턴과 원인 요약 |
| 코드베이스 탐색 | 여러 파일 탐색 | 관련 파일과 핵심 내용 |

## ② 실패가 예상되는 작업 격리

실패와 재시도가 반복될 가능성이 있는 작업을 별도 컨텍스트에서 수행한다.

예시:

- 외부 API 호출 및 응답 확인
- 실험적인 코드의 동작 검증
- 여러 번의 재시도가 필요한 데이터 변환 및 파싱

실패 기록이 메인 대화에 계속 쌓이는 것을 방지하고, 실패 원인과 다음 시도에 필요한 정보를 정리할 수 있다.

## ③ 독립적인 작업의 병렬 처리

서로 의존하지 않는 작업은 여러 Sub-agent에 나누어 동시에 수행할 수 있다.

```text
              메인 작업
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
   인증 모듈    코드 리뷰    API 분석
       │          │          │
       └──────────┼──────────┘
                  ↓
              결과 취합
```

적합한 상황:

- 작업이 서로 독립적일 때
- 분석 경로가 크게 겹치지 않을 때
- 여러 작업을 동시에 진행하고 싶을 때

주의할 점:

- Sub-agent가 많아질수록 추가적인 컨텍스트와 실행 비용이 발생할 수 있다.
- 각 Sub-agent의 결과를 취합하는 과정이 필요하다.

## ④ 도구 권한 제한

**최소 권한 원칙(Principle of Least Privilege)**에 따라 필요한 도구만 허용한다.

예시:

- 읽기 전용 코드 리뷰어
- DB 쿼리 분석 전용 에이전트

불필요한 파일 수정이나 의도하지 않은 DB 쓰기 등의 위험을 줄일 수 있다.

## ⑤ 비용 최적화

작업의 복잡도에 맞춰 모델을 선택한다.

| 작업 유형 | 모델 선택 예시 |
|---|---|
| 단순한 작업 | Haiku |
| 일반적인 작업 | Sonnet |
| 복잡한 작업 및 심층 분석 | Opus |

모든 작업에 가장 높은 성능의 모델을 사용할 필요는 없다.

## ⑥ 도메인 특화 및 재사용

특정 분야의 전문 지식과 작업 원칙을 에이전트에 정의해 여러 작업에서 재사용한다.

예시:

- **Code Reviewer**: 코드 품질, 보안, 성능 검토
- **Debugger**: 오류와 테스트 실패 원인 분석
- **DB Analyst**: SQL 작성 및 데이터 분석

---

# 4. Sub-agent 직접 정의하기

Sub-agent는 Markdown 파일로 직접 정의할 수 있다.

파일의 **Frontmatter에는 에이전트 설정을, 본문에는 시스템 프롬프트를 작성**한다.

## 4-1. 저장 위치

저장 위치에 따라 에이전트를 사용할 수 있는 범위가 달라진다.

| 저장 위치 | 적용 범위 | 특징 |
|---|---|---|
| `~/.claude/agents/` | 모든 프로젝트 | 개인용 에이전트 |
| `.claude/agents/` | 해당 프로젝트 | 프로젝트 전용 에이전트, Git으로 팀 공유 가능 |

### 개인용 에이전트

```text
~/.claude/
└── agents/
    ├── code-reviewer.md
    ├── debugger.md
    └── style-checker.md
```

여러 프로젝트에서 공통으로 사용할 에이전트를 저장한다.

### 프로젝트 전용 에이전트

```text
my-project/
└── .claude/
    └── agents/
        ├── code-reviewer.md
        └── test-runner.md
```

해당 프로젝트에 특화된 에이전트를 저장한다.

프로젝트 설정을 Git에 커밋하면 팀원들과 공유할 수 있다.

---

## 4-2. Sub-agent 정의 파일 작성

예시 파일:

```text
.claude/agents/swift-reviewer.md
```

파일 내용:

```markdown
---
name: swift-reviewer
description: Swift 코드 품질 리뷰 전문가. 코드 변경 후 즉시 사용.
tools: Read, Grep, Glob
---

너는 10년 차 시니어 iOS 개발자임.

다음 원칙으로 코드를 리뷰함.

1. [weak self] 누락 여부 철저히 검사
2. View 내 비즈니스 로직은 ViewModel로 분리 권고
3. 함수 길이 30줄 이내 유지 제안
```

이 파일을 저장하면 `swift-reviewer`라는 에이전트의 역할과 작업 규칙을 정의할 수 있다.

### 파일 구성 이해하기

```text
Frontmatter
    ├── name
    ├── description
    ├── tools
    └── model 등 설정
          ↓
시스템 프롬프트
    ├── 에이전트의 역할
    ├── 작업 원칙
    └── 결과 작성 방식
```

---

## 4-3. Frontmatter 주요 필드

| 필드 | 의미 |
|---|---|
| `name` | 에이전트 이름 |
| `description` | 에이전트의 역할과 사용 시점 |
| `tools` | 사용할 수 있는 도구 |
| `model` | 사용할 모델 |

### `name`

```yaml
name: swift-reviewer
```

에이전트의 이름을 정의한다.

### `description`

```yaml
description: Swift 코드 품질 리뷰 전문가. 코드 변경 후 즉시 사용.
```

Claude가 에이전트의 역할을 이해하고 적절한 작업에 위임할 수 있도록 설명한다.

### `tools`

```yaml
tools: Read, Grep, Glob
```

에이전트가 사용할 도구를 지정한다.

예를 들어 코드 리뷰어에게 읽기와 검색 도구만 제공하면 코드 수정 없이 분석하도록 구성할 수 있다.

### `model`

```yaml
model: sonnet
```

에이전트가 사용할 모델을 지정한다.

작업의 복잡도와 요구 성능에 맞춰 모델을 선택한다.

---

## 4-4. 시스템 프롬프트 작성

Frontmatter 아래에는 에이전트의 역할과 작업 지침을 작성한다.

예시:

```markdown
너는 10년 차 시니어 iOS 개발자임.

다음 원칙으로 코드를 리뷰함.

1. [weak self] 누락 여부 철저히 검사
2. View 내 비즈니스 로직은 ViewModel로 분리 권고
3. 함수 길이 30줄 이내 유지 제안
```

시스템 프롬프트에는 다음 내용을 구체적으로 정의할 수 있다.

- 어떤 전문가 역할을 수행하는지
- 어떤 기준으로 작업하는지
- 무엇을 검사해야 하는지
- 작업 결과를 어떤 방식으로 보고해야 하는지

**핵심은 에이전트의 역할과 작업 원칙을 명확하게 정의하는 것**이다.

---

## 4-5. `/agents` 명령어로 관리하기

Claude Code에서 다음 명령어를 입력한다.

```text
/agents
```

이를 통해 에이전트 목록을 확인하고 UI에서 에이전트를 생성하거나 편집할 수 있다.

```text
/agents
    ↓
에이전트 목록 확인
    ↓
에이전트 생성 또는 편집
```

직접 Markdown 파일을 작성하는 방법 외에도 `/agents`를 이용해 관리할 수 있다.

---

# 5. Sub-agent 호출 방법

Sub-agent는 다음 세 가지 방식으로 호출할 수 있다.

## ① 자동 호출

Claude가 에이전트의 `description`을 판단해 적합한 작업을 위임한다.

예를 들어 코드 변경 후 리뷰를 수행하도록 설명되어 있다면 코드 리뷰가 필요한 상황에서 해당 에이전트를 사용할 수 있다.

## ② `@mention`으로 직접 지정

에이전트 이름을 직접 지정한다.

```text
@swift-reviewer
```

예시:

```text
@swift-reviewer 방금 변경한 Swift 코드를 리뷰해줘.
```

## ③ 자연어로 요청

에이전트의 역할에 맞는 작업을 자연어로 요청한다.

```text
방금 변경한 코드를 리뷰해줘.
```

에이전트의 `description`이 구체적일수록 Claude가 적절한 에이전트를 선택하는 데 도움이 된다.

---

# 6. Description 작성법

`description`은 Claude가 에이전트를 선택할 때 참고하는 설명이다.

에이전트의 역할뿐 아니라 **언제 사용해야 하는지**도 명시하는 것이 중요하다.

## ① 역할을 구체적으로 작성

모호한 설명:

```text
Helps with code tasks and reviews.
```

구체적인 설명:

```text
Expert code reviewer. Checks code quality,
security, and performance without making changes.
```

두 번째 예시는 코드 리뷰, 보안, 성능이라는 역할과 수정하지 않는다는 제한을 함께 설명한다.

## ② 호출 조건 포함

어떤 상황에서 사용해야 하는지 명시한다.

```text
Use proactively after writing or modifying code.
```

코드를 작성하거나 수정한 뒤 적극적으로 사용하도록 유도하는 예시다.

## ③ 능동적인 호출 유도

```text
Use proactively when ...
```

처럼 적절한 작업 상황에서 적극적으로 사용하도록 표현할 수 있다.

## ④ 짧고 명확하게 작성

길고 모호한 설명보다 역할과 호출 조건이 명확한 설명을 작성한다.

### Description 예시

| 에이전트 | 설명에 포함할 내용 |
|---|---|
| Code Reviewer | 코드 변경 후 사용, 품질·보안·성능 검토, 수정 없이 제안 |
| DB Analyst | 읽기 전용 분석, SQL 작성, 데이터 리포팅 |
| Test Analyst | 코드 변경 후 테스트 실행, 실패 항목과 Stack Trace 보고 |

---

# 7. 실습 1: Code Reviewer 만들기

코드 리뷰어는 코드 변경 후 품질, 보안, 성능 등을 검토하고 개선 사항을 제안한다.

## 정의 파일

```text
.claude/agents/code-reviewer.md
```

## 설정 예시

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
---

You are an expert code reviewer.

Review code quality, security, and best practices.

Do not make changes unless explicitly required.
```

### 호출

```text
@code-reviewer
```

또는:

```text
방금 변경한 코드를 리뷰해줘.
```

### 리뷰 결과 분류

```text
Must fix
→ 반드시 수정해야 하는 문제

Should fix
→ 수정하는 것이 좋은 문제

Consider improving
→ 개선을 고려할 수 있는 사항
```

---

# 8. 실습 2: Debugger 만들기

Debugger는 오류나 테스트 실패가 발생했을 때 원인을 분석하고 수정 방안을 제시한다.

## 정의 파일

```text
.claude/agents/debugger.md
```

## 설정 예시

```markdown
---
name: debugger
description: Debugging specialist. Use proactively when errors or test failures occur.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger.

When invoked:

1. Capture the error and stack trace.
2. Identify reproduction steps.
3. Isolate the failure location.
4. Implement a minimal fix.
5. Verify that the solution works.

Provide:
- Root cause
- Evidence
- Code fix
- Prevention tip
```

### 작업 순서

```text
오류 및 Stack Trace 수집
          ↓
재현 방법 확인
          ↓
실패 위치 파악
          ↓
최소 수정
          ↓
수정 결과 검증
          ↓
원인·근거·수정 내용·재발 방지책 보고
```

Code Reviewer와 달리 Debugger는 오류 원인을 분석하는 것뿐 아니라, 정의된 지침에 따라 코드 수정과 검증까지 수행하도록 설정할 수 있다.

---

# 9. Sub-agent 체인 패턴

여러 Sub-agent를 순차적으로 연결해 작업을 수행하는 방식이다.

### 예시

```text
Code Reviewer
    ↓
성능 이슈 목록 반환
    ↓
Debugger
    ↓
이슈 분석 및 수정
    ↓
수정 결과 검증
```

각 에이전트가 수행한 작업의 결과를 다음 단계에서 활용한다.

- Code Reviewer: 문제를 발견하고 목록화
- Debugger: 문제 원인을 분석하고 수정
- 검증 단계: 수정 결과 확인

이처럼 역할을 분리하면 각 에이전트가 담당하는 작업과 결과를 명확하게 구분할 수 있다.

---

# 10. 고급 기능: PreToolUse Hook

`PreToolUse` Hook은 도구가 실행되기 전에 검증을 수행하는 기능이다.

예를 들어 DB 관련 명령이 실행되기 전에 쓰기 작업이 포함되어 있는지 검사하는 흐름을 구성할 수 있다.

### 동작 흐름

```text
도구 실행 요청
      ↓
PreToolUse Hook
      ↓
명령어 입력 분석
      ↓
허용 여부 검증
      ↓
실행 또는 차단
```

### 예시: 읽기 전용 쿼리 검증

```bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$CMD" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP)\b'; then
    echo "Blocked: read-only only" >&2
    exit 2
fi
```

이 예시는 명령어에 `INSERT`, `UPDATE`, `DELETE`, `DROP` 등이 포함되어 있는지 확인하고 차단하는 방식이다.

> 이 검사는 문자열 패턴을 기준으로 하므로 모든 쓰기 작업을 완벽하게 판별하는 것은 아니다. 실제 사용 시에는 명령어 구조와 실행 환경에 맞는 검증이 필요하다.

---

# 11. 전체 흐름 정리

## Sub-agent 정의부터 실행까지

```text
① Sub-agent 정의
   ├── name
   ├── description
   ├── tools
   ├── model
   └── 시스템 프롬프트
          ↓
② 저장
   ├── ~/.claude/agents/
   └── .claude/agents/
          ↓
③ 관리
   └── /agents
          ↓
④ 호출
   ├── 자동 호출
   ├── @mention
   └── 자연어 요청
          ↓
⑤ 작업 수행
   ├── 독립된 컨텍스트
   ├── 지정된 도구
   └── 정의된 작업 원칙
          ↓
⑥ 결과 반환
```

## 핵심 설정 예시

```markdown
---
name: code-reviewer
description: 코드 변경 후 보안·성능·품질을 검토하는 전문가
tools: Read, Grep, Glob
model: sonnet
---

너는 전문 코드 리뷰어다.

코드의 보안, 성능, 유지보수성을 검토한다.
코드를 직접 수정하지 않고 문제와 개선 방안을 보고한다.
```

이 파일 하나로 에이전트의 이름, 역할, 도구, 모델, 작업 지침을 정의할 수 있다.

---

# 핵심 정리

1. **Sub-agent는 직접 정의할 수 있다.**
   - Markdown 파일에 Frontmatter와 시스템 프롬프트를 작성한다.

2. **저장 위치에 따라 사용 범위가 달라진다.**
   - `~/.claude/agents/`: 개인용
   - `.claude/agents/`: 프로젝트용 및 팀 공유

3. **`/agents`로 관리할 수 있다.**
   - 에이전트 목록을 확인하고 UI에서 생성·편집한다.

4. **호출 방법은 세 가지다.**
   - 자동 호출
   - `@mention`
   - 자연어 요청

5. **Description은 역할과 호출 조건을 명확하게 작성한다.**
   - Claude가 적절한 에이전트를 선택하는 기준이 된다.

6. **도구 권한은 필요한 범위로 제한한다.**
   - 읽기 전용 리뷰어처럼 역할에 맞는 도구만 제공할 수 있다.

7. **여러 Sub-agent를 연결할 수 있다.**
   - 리뷰, 수정, 검증 등 역할을 나눠 순차적으로 작업한다.

8. **Hook을 연동해 실행 전 검증을 추가할 수 있다.**
   - `PreToolUse`로 도구 실행 전에 명령어를 검사하는 흐름을 구성한다.
