

# MCP (Model Context Protocol)

## 1. MCP란 무엇인가?

**MCP(Model Context Protocol)** 는 AI 애플리케이션과 외부 도구 및 데이터 소스를 연결하기 위한 오픈 표준 프로토콜이다.

AI 모델이 외부 시스템과 통신하고 기능을 사용할 수 있도록, 데이터와 도구를 주고받는 방식을 표준화한다.

USB-C가 다양한 기기를 공통 규격으로 연결하는 것처럼, MCP는 서로 다른 AI 애플리케이션과 외부 시스템이 공통된 규격으로 연결될 수 있도록 한다.

- Codex, Cursor, Claude Code 등 MCP를 지원하는 다양한 AI 애플리케이션에서 활용 가능
- 오픈 표준으로, 누구나 MCP 서버를 직접 구현 가능
- 데이터베이스, 이슈 트래커, 모니터링 시스템 등 다양한 외부 시스템과 연동 가능

MCP를 사용하면 각 AI 애플리케이션마다 외부 시스템 연동 방식을 새롭게 구현하는 대신, 공통 프로토콜을 통해 연결할 수 있다.

## 2. MCP로 연결할 수 있는 시스템

MCP 서버는 외부 시스템의 기능이나 데이터를 AI 애플리케이션에 제공한다.

- **데이터베이스**: PostgreSQL, MongoDB
- **이슈 트래커**: GitHub, Jira, Linear
- **모니터링**: Sentry, Datadog
- **커뮤니케이션**: Slack, Gmail
- **디자인 도구**: Figma
- **내부 시스템**: 사내 API, 업무 시스템, 자체 개발 도구 등

연동 가능한 시스템은 MCP 서버가 제공하는 기능에 따라 달라진다.

## 3. MCP 이전과 이후

### MCP 이전: 수동으로 데이터 전달

- Jira 이슈를 열어 내용을 복사
- Claude 채팅창에 내용을 붙여넣기
- 결과 코드를 다시 GitHub에 직접 업로드
- Sentry 에러 로그를 직접 찾아 확인
- 필요한 데이터를 매번 수동으로 전달

이 방식은 반복 작업이 많고, 복사 과정에서 실수가 발생할 수 있다. 또한 전달한 데이터가 최신 정보인지 보장하기 어렵다.

### MCP 이후: AI 애플리케이션에서 외부 시스템에 접근

MCP 서버가 필요한 도구와 데이터를 제공하면, AI 애플리케이션은 사용자의 요청에 따라 해당 기능을 호출할 수 있다.

예시:

- “Jira ENG-4521 이슈를 읽고 수정 사항을 정리해줘.”
- “Sentry에서 최근 24시간 동안 발생한 에러를 분석해줘.”
- “PostgreSQL에서 이번 달 매출을 조회해줘.”
- “Slack에서 새 Figma 디자인 관련 내용을 찾아 컴포넌트 업데이트를 도와줘.”

외부 시스템의 데이터를 직접 전달하는 과정을 줄이고, 여러 시스템을 연계한 자동화 워크플로우를 구성할 수 있다.

단, 실제 조회나 변경 작업이 가능한지는 MCP 서버가 제공하는 도구와 권한에 따라 달라진다.

## 4. MCP 아키텍처

MCP는 **Host, Client, Server**를 중심으로 구성된다.

```text
┌───────────────────────────────┐
│         MCP Host              │
│      Claude Code 등           │
│                               │
│   ┌───────────────────────┐   │
│   │      MCP Client       │   │
│   └───────────┬───────────┘   │
└───────────────┼───────────────┘
                │
          MCP Protocol
       (JSON-RPC 기반 메시지)
                │
┌───────────────┼───────────────┐
│          MCP Server           │
│                               │
│   Tools / Resources / Prompts │
└───────────────┬───────────────┘
                │
       외부 시스템 및 데이터
   (DB, GitHub, Slack 등)
```

### 4.1 MCP Host

MCP를 사용하는 AI 애플리케이션이다.

예를 들어 Claude Code와 같은 애플리케이션이 Host 역할을 한다. Host는 MCP Client를 통해 MCP 서버와 통신하고, 서버가 제공하는 기능을 AI 모델이 활용할 수 있도록 한다.

### 4.2 MCP Client

Host 내부에서 MCP 서버와 통신하는 구성 요소다.

- MCP 서버와 연결을 관리
- MCP 프로토콜에 따라 요청과 응답을 주고받음
- 서버가 제공하는 기능을 확인하고 호출

일반적으로 MCP Client는 연결하는 MCP Server마다 별도의 연결을 관리한다.

### 4.3 MCP Server

외부 시스템의 기능이나 데이터를 MCP 규격에 맞게 제공하는 프로그램이다.

예를 들어 PostgreSQL MCP Server는 데이터베이스 조회 기능을 제공하고, GitHub MCP Server는 저장소나 이슈 관련 기능을 제공할 수 있다.

MCP Server가 제공할 수 있는 주요 기능은 다음과 같다.

- **Tools**: AI가 실행할 수 있는 함수나 작업
- **Resources**: AI 애플리케이션이 읽을 수 있는 데이터
- **Prompts**: 재사용할 수 있는 프롬프트 템플릿

## 5. MCP의 주요 계층

MCP 통신은 크게 Transport, Protocol, 기능 제공 영역으로 이해할 수 있다.

### 5.1 Transport — 통신 방식

Client와 Server가 메시지를 주고받는 통신 채널이다.

대표적인 방식:

- **stdio**: 로컬 프로세스의 표준 입력(stdin)과 표준 출력(stdout)을 이용한 통신
- **Streamable HTTP**: HTTP를 이용한 원격 통신

과거에는 HTTP+SSE 방식도 사용했지만, 현재 표준에서는 Streamable HTTP가 이를 대체하는 방식이다. 기존 SSE 방식은 호환성을 위해 남아 있을 수 있다.

### 5.2 Protocol — 메시지 규약

MCP는 **JSON-RPC 2.0 기반**으로 Client와 Server가 메시지를 주고받는다.

Protocol은 다음과 같은 내용을 정의한다.

- 요청과 응답의 형식
- 메시지의 종류와 전달 방식
- 도구 목록 조회 및 도구 호출
- 오류와 결과를 전달하는 방식

Transport가 메시지를 전달하는 통신 채널이라면, Protocol은 메시지의 구조와 의미를 정의하는 규약이다.

### 5.3 기능 제공 영역 — Tools, Resources, Prompts

MCP Server가 Client에 제공하는 주요 기능이다.

| 기능 | 설명 |
|---|---|
| Tools | AI가 실행할 수 있는 작업. 예: 이슈 조회, SQL 실행, 파일 생성 |
| Resources | 읽을 수 있는 데이터나 컨텍스트. 예: 문서, 설정, 데이터 |
| Prompts | 특정 작업에 재사용할 수 있는 프롬프트 템플릿 |

Tools는 실행이나 외부 시스템 변경을 수반할 수 있지만, Resources는 주로 데이터를 제공하고 Prompts는 작업을 위한 프롬프트 템플릿을 제공한다.


## 6. MCP 연결 방법 — 세 가지 전송 방식

MCP Server와 통신하는 방식은 크게 Stdio, SSE, HTTP로 구분된다.

### 6.1. Stdio — 로컬 프로세스 방식

컴퓨터에서 직접 실행되는 MCP Server 프로세스와 표준 입력(stdin), 표준 출력(stdout)을 통해 통신하는 방식이다.

**적합한 경우**
- 로컬 DB 또는 파일 시스템 접근
- 자체 제작 스크립트 실행
- 인터넷 없이 동작해야 하는 경우

**등록 명령어**
\```bash
claude mcp add --transport stdio myserver -- npx -y server
\```

### 6.2. SSE — 구형 원격 통신 방식

Server-Sent Events 기반의 원격 통신 방식이다.

**주의**
- 공식적으로 deprecated 상태
- 새로운 통합에는 HTTP 방식 사용 권장
- 기존 SSE 서버와의 호환이 필요한 경우 사용

### 6.3. HTTP — 원격 서버 방식

클라우드 등 원격 환경에서 실행되는 MCP Server에 연결하는 방식이다.

**적합한 경우**
- SaaS 도구 연동 (GitHub, Sentry 등)
- 팀 공용 서버
- OAuth 인증이 필요한 서비스

**등록 명령어**
\```bash
claude mcp add --transport http myserver https://mcp.example.com
\```

## 7. Stdio MCP Server 연결 — PostgreSQL

PostgreSQL MCP Server를 등록하고, Claude Code에서 데이터 조회를 요청하는 과정이다.

### 7.1. MCP Server 등록

\```bash
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
\```

**명령어 구성**
- `claude mcp add`: MCP Server 등록
- `--transport stdio`: Stdio 방식으로 연결
- `db`: MCP Server 등록 이름
- `--`: Claude Code 옵션과 서버 실행 명령 구분
- `npx -y @bytebase/dbhub`: 실제 실행할 MCP Server 프로그램
- `--dsn`: PostgreSQL 데이터베이스 주소 및 접속 정보

PostgreSQL 연결 문자열 형식:

\```text
postgresql://사용자명:비밀번호@호스트:포트/데이터베이스명
\```

### 7.2. 연결 상태 확인

Claude Code 내에서 다음 명령어를 실행한다.

\```text
/mcp
\```

`/mcp` 명령어로 등록된 MCP Server의 연결 상태를 확인할 수 있다.

### 7.3. 자연어로 데이터 조회

MCP Server가 정상적으로 연결되면 자연어로 데이터 조회를 요청할 수 있다.

예시:

\```text
이번 달 총 매출은 얼마야?
\```

Claude Code는 MCP Server가 제공하는 데이터베이스 도구를 사용해 요청을 처리한다.

**팁 — `--` 구분자**

`--` 뒤에 오는 내용은 실제 MCP Server 실행 프로그램에 전달되는 영역이다.

- `--` 앞: Claude Code의 옵션과 서버 이름
- `--` 뒤: MCP Server 실행 명령과 해당 프로그램에 전달할 인수

Claude Code 옵션과 서버 옵션이 충돌하지 않도록 구분하는 역할을 한다.







## 8. HTTP MCP Server 연결 — GitHub

SaaS 서비스에서 제공하는 원격 MCP Server에 HTTP 방식으로 연결하는 예시다.

### 8.1 Personal Access Token 생성

GitHub에서 Personal Access Token(PAT)을 생성한다.

**생성 경로**

`GitHub.com` → `Settings` → `Developer settings` → `Personal access tokens`

- GitHub API에 접근하기 위한 인증 토큰 생성
- 사용할 작업에 필요한 최소 권한만 부여
- 생성한 토큰은 외부에 노출되지 않도록 안전하게 관리

### 8.2 MCP Server 등록

GitHub에서 제공하는 MCP Server를 HTTP 방식으로 등록한다.

```bash
claude mcp add --transport http github \
  https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

**명령어 구성**
- `--transport http`: HTTP 방식으로 연결
- `github`: MCP Server 등록 이름
- URL: GitHub MCP Server 엔드포인트
- `--header`: HTTP 요청에 전달할 인증 헤더
- `Authorization: Bearer`: PAT를 이용한 인증 정보 전달

`YOUR_GITHUB_PAT` 부분에는 실제 발급받은 토큰을 사용한다.

### 8.3 실제 활용 예시

MCP Server가 정상적으로 연결되고 필요한 권한이 설정되어 있다면 다음과 같이 요청할 수 있다.

- "PR #456을 검토하고 개선 사항을 제안해줘."
- "이 버그에 대한 새 이슈를 만들어줘."
- "나에게 할당된 열린 PR 목록을 보여줘."

GitHub MCP Server가 제공하는 도구를 통해 PR 조회, 이슈 생성 등 GitHub 작업을 수행할 수 있다.

---

## 9. MCP 설치 범위(Scope) 이해하기

MCP Server를 등록할 때 `--scope` 옵션으로 설정을 저장할 범위를 지정할 수 있다.

설치 범위에 따라 MCP Server를 사용할 수 있는 프로젝트와 팀 공유 여부가 달라진다.

| 범위 | 키워드 | 저장 위치 | 팀 공유 | 적절한 상황 |
|---|---|---|---|---|
| 로컬 | `local` | `~/.claude.json` (프로젝트별 설정) | X | 개인 실험, 개발 도구 |
| 프로젝트 | `project` | `.mcp.json` (프로젝트 루트) | O (Git 공유) | 팀 공용 도구 |
| 사용자 | `user` | `~/.claude.json` (사용자 설정) | X | 모든 프로젝트에서 사용하는 개인 도구 |

### 9.1 Local 범위 — 기본값

현재 프로젝트에서만 사용하는 개인 MCP Server 설정이다.

```bash
claude mcp add --transport http stripe \
  https://mcp.stripe.com
```

- `--scope`를 생략하면 기본적으로 `local` 범위로 등록된다.
- 현재 프로젝트에서만 사용할 수 있다.
- 설정은 `~/.claude.json`에 저장되며 프로젝트별로 관리된다.

### 9.2 Project 범위 — 팀 공유

프로젝트 구성원 모두가 동일한 MCP Server 설정을 사용할 수 있도록 등록하는 방식이다.

```bash
claude mcp add --transport http --scope project paypal \
  https://mcp.paypal.com/mcp
```

- 프로젝트 루트의 `.mcp.json`에 설정이 저장된다.
- `.mcp.json`을 Git에 커밋하면 팀원과 공유할 수 있다.
- 팀원은 해당 프로젝트에서 동일한 MCP Server 설정을 사용할 수 있다.

### 9.3 User 범위 — 전체 프로젝트

현재 사용자의 모든 프로젝트에서 공통으로 사용하는 MCP Server 설정이다.

```bash
claude mcp add --transport http --scope user hubspot \
  https://mcp.hubspot.com
```

- `~/.claude.json`의 사용자 공통 설정에 저장된다.
- 프로젝트마다 별도로 등록할 필요가 없다.
- 개인적으로 자주 사용하는 도구에 적합하다.

### 9.4 설정 우선순위

동일한 이름의 MCP Server가 여러 범위에 등록되어 있다면 다음 우선순위가 적용된다.

`local` → `project` → `user`

우선순위가 높은 설정이 사용되며, 여러 범위의 설정이 하나로 합쳐지는 것은 아니다.

---

## 10. .mcp.json 팀 공유 및 환경변수

`.mcp.json`은 프로젝트 범위의 MCP Server 설정을 저장하는 파일이다.

프로젝트 루트에 위치하며, Git에 커밋하면 팀원과 MCP Server 설정을 공유할 수 있다.

### 10.1 .mcp.json 기본 구조

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "api-server": {
      "type": "http",
      "url": "${API_URL:-https://api.example.com/mcp}",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**주요 항목**
- `mcpServers`: 등록할 MCP Server 목록
- `type`: 전송 방식 (`http`, `stdio` 등)
- `url`: 원격 MCP Server 주소
- `headers`: HTTP 요청에 전달할 헤더
- `${API_KEY}`: 환경변수에 저장된 인증 정보 참조

### 10.2 환경변수 사용

`.mcp.json`에 API Key나 서버 주소를 직접 작성하면 민감한 정보가 Git에 노출될 수 있다.

이를 방지하기 위해 환경변수 참조 기능을 사용할 수 있다.

| 표현식 | 의미 |
|---|---|
| `${VAR}` | 환경변수 VAR의 값을 사용 |
| `${VAR:-default}` | VAR이 설정되어 있지 않으면 기본값 사용 |

예를 들어 다음 설정은 `API_KEY` 환경변수의 값을 Authorization 헤더에 전달한다.

```json
"headers": {
  "Authorization": "Bearer ${API_KEY}"
}
```

팀원마다 환경변수 값을 별도로 설정하면 `.mcp.json`은 공유하면서 실제 인증 정보는 각자의 환경에서 관리할 수 있다.

> **주의:** `.mcp.json`에 실제 API Key나 비밀번호를 직접 작성하지 않는다. 환경변수에 민감한 정보를 보관하고, 해당 파일에는 변수 참조만 작성한다.

---

## 11. OAuth 2.0 보안 인증 흐름

일부 원격 MCP Server는 API Key 대신 OAuth 2.0 인증을 사용한다.

OAuth는 사용자가 직접 비밀번호나 인증 정보를 MCP Server에 전달하지 않고, 인증 절차를 통해 접근 권한을 부여하는 방식이다.

### 11.1 서버 등록

Sentry MCP Server를 HTTP 방식으로 등록한다.

```bash
claude mcp add --transport http sentry \
  https://mcp.sentry.dev/mcp
```

### 11.2 인증 시작

Claude Code에서 다음 명령어를 실행한다.

```text
/mcp
```

MCP 관리 화면에서 인증이 필요한 서버를 선택하면 브라우저를 통해 로그인 및 권한 승인 절차가 진행된다.

### 11.3 인증 완료

인증이 정상적으로 완료되면 발급된 토큰을 이용해 MCP Server에 접근할 수 있다.

- 인증 정보는 Claude Code가 관리한다.
- 토큰이 만료되면 서버의 인증 방식에 따라 갱신할 수 있다.
- 사용자는 매번 직접 토큰을 입력하지 않고 인증된 연결을 사용할 수 있다.

---

## 12. MCP 프롬프트 명령어 및 리소스

MCP Server는 Tools 외에도 Prompts와 Resources를 제공할 수 있다.

Claude Code에서는 이를 슬래시 명령어와 `@` 멘션으로 활용할 수 있다.

### 12.1 프롬프트 명령어(Prompts)

MCP Server가 제공하는 Prompt는 재사용할 수 있는 프롬프트 템플릿이다.

연결된 MCP Server가 Prompt를 제공하면 Claude Code에서 `/`를 입력했을 때 해당 프롬프트를 명령어로 확인하고 실행할 수 있다.

**명령어 형식**

```text
/mcp__서버명__프롬프트명
```

**사용 예시**

```text
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue 로그인버그 high
```

- `list_prs`: 인수 없이 실행하는 프롬프트 예시
- `pr_review 456`: PR 번호를 인수로 전달하는 예시
- `create_issue 로그인버그 high`: 여러 인수를 전달하는 예시

서버에서 제공하는 Prompt 이름에 공백이 있으면 명령어에서는 밑줄(`_`)로 정규화된다.

프롬프트가 실행되면 해당 템플릿의 내용이 대화에 반영되어 작업을 진행할 수 있다.

### 12.2 리소스 참조(Resources)

MCP Resource는 서버가 제공하는 데이터나 컨텍스트를 파일처럼 참조하는 기능이다.

`@` 멘션을 사용해 연결된 MCP Server의 리소스를 대화에 포함할 수 있다.

**참조 형식**

```text
@서버명:프로토콜://리소스/경로
```

**사용 예시**

```text
@github:issue://123 내용을 분석해줘.
```

```text
@docs:file://api/authentication 내용을 검토해줘.
```

```text
@postgres:schema://users와 @docs:file://user-model을 비교해줘.
```

**특징**
- 리소스를 참조하면 해당 리소스의 내용을 가져와 대화에 활용할 수 있다.
- 하나의 요청에서 여러 리소스를 함께 참조할 수 있다.
- `@` 입력 후 표시되는 검색 기능으로 연결된 리소스를 찾을 수 있다.

실제 리소스 URI와 제공 여부는 MCP Server가 정의한 내용에 따라 달라진다.

---

## 13. MCP 서버 관리 명령어 및 환경변수

### 13.1 서버 관리 명령어

| 명령어 | 설명 |
|---|---|
| `claude mcp list` | 등록된 MCP Server 목록 확인 |
| `claude mcp get github` | 특정 MCP Server 상세 정보 확인 |
| `claude mcp remove github` | MCP Server 제거 |

### 13.2 주요 환경변수

| 환경변수 | 설명 |
|---|---|
| `MCP_TIMEOUT` | MCP Server 시작 대기 시간 설정 (ms) |
| `MAX_MCP_OUTPUT_TOKENS` | MCP 도구 응답의 최대 출력 토큰 수 설정 |
