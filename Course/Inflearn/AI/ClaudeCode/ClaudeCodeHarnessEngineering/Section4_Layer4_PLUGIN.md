# Claude Code Plugins

## 1. Plugin이란?

**Plugin = Claude Code의 기능을 확장하는 표준 패키지**

자주 사용하는 명령, 자동화 스크립트, 외부 도구 연결 등을 하나의 패키지로 묶어 다른 사용자와 공유할 수 있다.

### 핵심 특징

* 기능을 모듈화해 재사용
* 마켓플레이스를 통해 검색 및 설치
* 버전을 관리하고 업데이트·배포
* 팀원들과 동일한 개발 도구와 워크플로우 공유

Plugin은 여러 기능을 하나로 묶어 배포할 수 있게 해주는 패키징 방식이다.

---

## 2. Plugin이 필요한 이유

### 기존 방식의 문제점

기존에는 각자 `.claude/` 디렉터리에 설정과 스크립트를 개별적으로 관리하는 방식으로 기능을 재사용했다.

이 방식은 다음과 같은 불편함이 있다.

* 팀원마다 설정을 복사하고 붙여 넣어야 함
* 기능을 수정할 때 변경 사항을 일괄 적용하기 어려움
* 버전 관리와 배포가 번거로움
* 다른 프로젝트에서 동일한 기능을 재사용하기 어려움

### Plugin을 사용하면?

기능을 표준 패키지로 구성해 설치와 업데이트를 일관되게 관리할 수 있다.

```text
개별 설정과 스크립트
        ↓
기능을 Plugin으로 패키징
        ↓
마켓플레이스에 등록
        ↓
사용자가 설치
        ↓
동일한 기능을 재사용
```

---

## 3. 독립 실행형 기능과 Plugin 비교

사용자 정의 기능을 추가하는 방법은 개별 설정으로 관리하는 방식과 Plugin으로 패키징하는 방식으로 나눌 수 있다.

| 구분     | 독립 실행형 기능         | Plugin               |
| ------ | ----------------- | -------------------- |
| 호출     | `/hello`          | `/my-plugin:hello`   |
| 공유     | 로컬 파일 복사 또는 별도 공유 | 마켓플레이스 및 Plugin 패키지  |
| 버전 관리  | 별도 관리 필요          | 버전 및 배포 단위로 관리       |
| 설치     | 파일을 직접 구성하거나 복사   | `/plugin install`    |
| 네임스페이스 | 이름 충돌 가능          | Plugin 이름을 통한 명령어 구분 |

### 호출 방식

독립 실행형 명령:

```text
/hello
```

Plugin에 포함된 명령:

```text
/my-plugin:hello
```

Plugin 명령은 Plugin 이름을 네임스페이스로 사용해 다른 명령과 구분할 수 있다.

### 버전 관리

Plugin의 버전은 일반적으로 SemVer 형식으로 관리할 수 있다.

```text
MAJOR.MINOR.PATCH
```

* `MAJOR`: 호환되지 않는 변경
* `MINOR`: 하위 호환되는 기능 추가
* `PATCH`: 하위 호환되는 버그 수정

Git SHA 등 특정 커밋을 기준으로 소스를 식별하는 방식과 정식 릴리스 버전 관리는 구분해야 한다.

---

## 4. Plugin에 포함할 수 있는 구성 요소

Plugin은 여러 Claude Code 확장 기능을 하나로 묶을 수 있다.

### ① Skills

반복 작업의 절차와 지침을 정의한다.

```text
skills/
└── code-review/
    └── SKILL.md
```

### ② Agents

특정 역할과 작업 지침을 가진 에이전트를 정의한다.

```text
agents/
└── code-reviewer.md
```

### ③ Hooks

특정 이벤트가 발생했을 때 자동으로 실행할 작업을 정의한다.

```text
hooks/
└── hooks.json
```

### ④ MCP Server

외부 서비스 및 도구와 표준화된 방식으로 연결한다.

MCP 설정을 통해 Claude Code가 외부 시스템의 기능을 활용할 수 있다.

### ⑤ LSP Server

Language Server Protocol을 활용해 코드 진단, 정의 탐색 등 언어별 개발 기능을 연결할 수 있다.

### ⑥ Monitors

백그라운드에서 로그나 상태를 감시하고 변경 시 알림을 보내는 기능을 의미한다.

### ⑦ Themes

터미널이나 관련 인터페이스의 시각적 테마를 제공하는 기능이다.


---

## 5. Plugin의 기본 디렉터리 구조

Plugin은 구성 요소를 하나의 디렉터리 구조로 패키징한다.

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── code-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
└── README.md
```

### 주요 파일

| 파일·디렉터리                      | 역할            |
| ---------------------------- | ------------- |
| `.claude-plugin/plugin.json` | Plugin의 메타데이터 |
| `skills/`                    | Skill 정의      |
| `agents/`                    | Sub-agent 정의  |
| `hooks/`                     | Hook 설정       |
| `.mcp.json`                  | MCP 서버 설정     |
| `README.md`                  | 사용법과 설명       |

`plugin.json`에는 Plugin 이름, 버전, 설명 등 메타데이터를 작성할 수 있다.

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "팀 공통 개발 도구 모음"
}
```

---

## 6. 설치부터 호출까지

Plugin은 마켓플레이스에 등록된 패키지를 설치해 사용할 수 있다.

### 전체 흐름

```text
Marketplace 등록
       ↓
Plugin 설치
       ↓
Plugin 파일 및 설정 로드
       ↓
구성 요소 등록
       ↓
Skill·Agent·Hook 등의 기능 사용
```

### 설치 예시

마켓플레이스를 추가한다.

```text
/plugin marketplace add owner/repo
```

Plugin을 설치한다.

```text
/plugin install my-plugin@my-marketplace
```

설치 후 Plugin에 포함된 명령이나 기능을 사용한다.

예:

```text
/my-plugin:hello
```

실제 설치 명령과 네임스페이스는 마켓플레이스 이름, Plugin 이름, 포함된 기능에 따라 달라진다.

### 업데이트와 제거

Plugin은 설치 후에도 업데이트하거나 제거할 수 있다. 구체적인 명령은 사용 중인 Claude Code 버전의 Plugin 관리 기능을 따른다.

---

## 7. Plugin의 핵심 메커니즘

강의에서 강조한 핵심 개념은 캐시 격리, 네임스페이스, Hot Reload다.

### ① 캐시 격리

Plugin을 설치할 때 원본 저장소와 별도로 로컬 캐시 영역에 파일을 관리할 수 있다.

```text
Marketplace / Git 저장소
          ↓
     Plugin 설치
          ↓
     로컬 캐시
          ↓
    Plugin 기능 로드
```

캐시는 Plugin을 설치하고 로드하기 위한 파일 관리와 관련된 개념이다.

캐시가 존재한다고 해서 실행 환경이나 보안 경계까지 완전히 격리된다는 뜻은 아니다.

### ② 네임스페이스

Plugin에 포함된 명령을 Plugin 이름으로 구분한다.

```text
/my-plugin:hello
/another-plugin:hello
```

서로 다른 Plugin이 동일한 명령 이름을 사용하더라도 네임스페이스를 통해 구분할 수 있다.

### ③ Hot Reload

Hot Reload는 변경 사항을 재시작 없이 반영하는 동작을 의미한다.


---

## 8. Plugin을 사용하기 좋은 경우

### 개인 작업 환경 표준화

자주 사용하는 Skill, 명령, 자동화 기능을 하나의 패키지로 관리한다.

### 팀 공통 개발 도구 공유

팀에서 공통으로 사용하는 코드 리뷰 기준, 테스트 워크플로우 등을 배포한다.

### 반복 작업 자동화

Hooks, Skills, Agents 등을 조합해 반복적인 개발 작업을 자동화한다.

### 외부 시스템 연동

MCP 서버 설정을 Plugin에 포함해 외부 서비스와 연동하는 환경을 구성한다.

---

# 핵심 정리

1. **Plugin은 Claude Code 확장 기능을 묶는 패키지다.**
2. **개별 설정을 복사하는 대신 기능을 표준화해 공유할 수 있다.**
3. **Skills, Agents, Hooks, MCP 등의 구성 요소를 패키징할 수 있다.**
4. **마켓플레이스를 통해 설치하고 버전 관리 및 배포를 할 수 있다.**
5. **네임스페이스는 Plugin 간 명령 이름 충돌을 줄여준다.**
6. **캐시와 Hot Reload는 각각 파일 관리와 변경 반영에 관한 개념이며, 모든 기능의 완전한 격리나 무조건적인 실시간 갱신을 뜻하지는 않는다.**

## 전체 흐름

```text
기능 개발
   ↓
Plugin 패키징
   ↓
Marketplace 등록
   ↓
설치 및 로드
   ↓
네임스페이스를 통해 호출
   ↓
기능 사용 및 버전 업데이트
```
