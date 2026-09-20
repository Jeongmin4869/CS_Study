
# Claude Code 핵심 개념 정리

---

# 01. CLAUDE.md - 에이전트의 헌법

이 프로젝트에서 취하는 모든 행동의 기준이 된다.

다른 AI의 경우 `AGENTS.md`와 같은 방식으로 사용한다.

* 모든 세션의 출발점
* 프롬프트 없이 규칙이 자동 적용되는 영구 메모리
* 항상 켜져 있는 규칙

## 두 가지 범위

### 1. Global CLAUDE.md

```text
~/.claude/CLAUDE.md
```

모든 프로젝트에 공통 적용

* 응답 언어
* 코드 스타일 기본값
* 개인 작업 방식
* 선호 도구
* 코드 설명
* 주석 등 전역적인 규칙

### 2. Project CLAUDE.md

```text
.claude/CLAUDE.md
```

프로젝트 레벨

* 이 저장소만의 아키텍처 규칙
* 디렉터리 맵
* 팀이 커밋하여 함께 공유
* 테스트 정책
* 금지된 패턴
* 프로젝트 내에서 반드시 지켜야 하는 규칙

## 작성 시 주의점

`CLAUDE.md`는 짧고 선명하게 유지하여 컨텍스트를 낭비하지 않도록 한다.

상세한 가이드는 `Skills` 또는 다른 에이전트에 분리하는 것이 좋다.

---

# 02. Skills - 필요할 때만 꺼내는 전문 지식

* 항상 켜져 있는 방식(Always-on)이 아닌 온디맨드(On-demand)
* 메인 컨텍스트 창을 깔끔하게 유지

## Skills 자동 호출의 원리

* 폴더명 = 호출명
* 예: `/code-review`
* 서브에이전트에서 격리 실행하여 메인 컨텍스트 보호

## 폴더 구조

`.claude` 아래에 `skills` 폴더를 만들고, 그 아래 스킬 이름으로 폴더를 생성한다.

```text
.claude/
└── skills/
    └── code-review/
        ├── SKILL.md
        ├── scripts/
        │   └── review.sh
        ├── references/
        │   └── guide.md
        └── assets/
            └── template.md
```

* `scripts` : 실행 스크립트
* `references` : 참고 문서
* `assets` : 템플릿 등 리소스

## SKILL.md

```markdown
---
description: PR 리뷰, 코드 품질 점검, 보안 취약점 분석 시 사용
---

# 코드 리뷰 스킬

다음 순서대로 분석하세요.

1. **보안**
   - 주입 공격
   - 하드코딩된 비밀값

2. **예외 처리**
   - 예외 누락
   - 콜백 부재

3. **테스트**
   - 커버리지
   - 엣지 케이스

4. **스타일**
   - 네이밍
   - 불필요한 코드

대상 파일: $ARGUMENTS
```

### `description`

이 필드를 잘 작성해야 한다.

LLM이 `description`을 보고 해당 스킬을 현재 상황에서 사용해야 하는지 판단한다.

따라서 **이 스킬을 언제 사용하는지 구체적으로 작성**해야 한다.

`description`이 모호하면 클로드가 엉뚱하게 사용하거나, 아예 사용하지 않을 수 있다.

### `$ARGUMENTS`

스킬 뒤에 입력한 값이 argument로 들어온다.

---

# 03. Hooks - AI 없는 결정론적 통제

```text
이벤트 발생 → 매처 확인 → 명령 실행
```

LLM이 개입하지 않는 순수 자동화

* 이벤트 발생 시 조건에 맞으면 해당 명령을 실행
* 예측 가능하고 결정론적
* AI 에이전트의 특정 행동 전후에 자동으로 무언가를 실행

## 주요 라이프사이클 이벤트

### 1. `SessionStart`

세션 시작 시 환경 점검

* 필요한 환경변수 확인
* 의존성 점검

### 2. `PreToolUse`

도구 실행 전 검증 및 차단

* 도구가 실행되기 직전 위험한 명령어를 차단하는 보안 게이트로 활용

### 3. `PostToolUse`

도구 완료 후 포맷 및 알림

* 도구 실행 직후 자동 린트, 포맷팅 등에 활용

### 4. `Stop`

응답 완료 후 알림

* Claude가 응답을 완료했을 때 Slack과 같은 완료 통보에 사용

### 5. `SubagentStop`

서브에이전트 완료 감지

* 서브에이전트 작업 완료 시 후속 작업 등에 활용

## hooks.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "node /home/hooks/read_hook.ts"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "node /home/hooks/edit_hook.ts"
          }
        ]
      }
    ]
  }
}
```

---

# 04. Subagents - 전문가에게 맡기는 기술

전문가에게 맡기고 결과만 받는다.

메인 에이전트가 모든 것을 직접 처리하는 것이 아니라 특화된 서브에이전트에게 작업을 위임한다.

* 메인 컨텍스트 보호
* 작업별 독립적인 컨텍스트 사용
* 전문 작업을 별도의 에이전트에 위임

## Explore Agent

* 코드베이스 탐색 전담
* 읽기 전용 도구만 허용

## Test Runner

* 테스트 실행 및 분석
* 자체 컨텍스트로 격리

## Code Reviewer

* 보안 및 품질 리뷰 전담
* 커스텀 모델 지정 가능

### `agent/code-reviewer.yml`

에이전트 정의

```yaml
name: code-reviewer

description: 보안 취약점과 코드 품질을 리뷰할 때 사용

model: claude-opus-4-7

tools:
  - Read
  - Grep

system_prompt: |
  당신은 보안 전문 코드 리뷰어입니다.
  OWASP Top 10 기준으로 취약점을 먼저 분석하세요.
```

서브에이전트는 서브에이전트를 스폰할 수 없다.

→ 무한 재귀 방지가 내장되어 있다.

---

# 05. Plugins - 개인 역량을 팀 인프라로

`CLAUDE.md`, `Skills`, `Hooks`, `Subagents`를 하나의 패키지로 묶어 팀원들이 동일한 환경을 구축할 수 있게 한다.

```text
Skills + Agents + Hooks
        ↓
      Plugin
        ↓
   팀 단위 배포
```

* npm처럼 패키징
* 마켓플레이스로 배포
* 팀원이 동일한 개발 환경을 구축

## Plugin 구조

```text
team-devkit/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── code-reviewer.md
├── hooks/
│   └── hooks.json
└── README.md
```

`.claude-plugin/` 폴더에는 `plugin.json`을 둔다.

다른 컴포넌트는 Plugin의 해당 디렉터리 구조에 맞게 별도로 구성한다.

### plugin.json

```json
{
  "name": "team-devkit",
  "version": "1.2.0",
  "description": "팀 표준 개발 도구 모음",
  "author": {
    "name": "Dev Team"
  }
}
```

GitHub에 push 후 팀에 한 줄만 공유

```text
/plugin install team-devkit@my-org
```

### 설정 파일

`settings.local.json`은 개인 로컬 환경에서 사용하는 설정이므로 Git에 커밋하지 않도록 `.gitignore`에 등록한다.

---

# 06. MCP - Model Context Protocol

Claude가 외부 서비스와 표준화된 방식으로 대화할 수 있게 해주는 프로토콜

MCP 서버를 연결하면 Claude가 해당 서비스의 기능을 자신의 도구처럼 사용할 수 있게 된다.

## `.mcp.json`

```json
{
  "sequential-thinking": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-sequential-thinking"
    ]
  },
  "fetch": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-fetch"
    ]
  }
}
```

---

# 지금 바로 시작하는 6단계

### STEP 1. CLAUDE.md 작성

* 프로젝트 규칙
* 아키텍처
* 네이밍 컨벤션 정의

### STEP 2. 첫 Skill 만들기

* 가장 자주 쓰는 작업 하나를 `SKILL.md`로 작성

### STEP 3. Hook 연결

* `PostToolUse`로 자동 린트 하나부터 시작

### STEP 4. MCP 서버 추가

* 자주 쓰는 외부 서비스 하나를 `.mcp.json`에 등록

### STEP 5. Subagent 정의

* 반복적인 코드 리뷰를 에이전트에 위임

### STEP 6. Plugin으로 팀 배포

* 완성된 구조를 패키징해 팀과 공유

---

# 컨텍스트 관리

```text
메인 컨텍스트가 200K 토큰에 근접
→ Skills / Subagents로 분산

100K 토큰 미만
→ 메인에서 처리 가능
```

---

# Claude Code 5-Layer 구조

### Layer 1 - CLAUDE.md

아키텍처 규칙과 컨벤션을 지속적으로 적용

* 매 세션 프롬프트 입력 불필요

### Layer 2 - Skills

필요한 전문 지식만 모듈 단위로 사용

* 메인 컨텍스트 낭비 최소화

### Layer 3 - Hooks

위험 명령을 차단하고 자동 품질 검사 실행

* LLM 없는 결정론적 보장

### Layer 4 - Subagents

코드 리뷰와 테스트를 독립된 컨텍스트에서 처리

* 결과만 메인에 반환

### Layer 5 - Plugins

전체 역량을 패키징

* 팀이 한 줄 명령으로 동일한 환경 구축
