

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
