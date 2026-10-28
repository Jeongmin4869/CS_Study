# Claude Code Hooks

## 1. Hooks란?

Claude Code가 특정 작업을 수행하는 순간 원하는 명령이나 동작을 자동으로 실행하는 메커니즘.

핵심은 **결정론적 제어**. AI가 실행 여부를 판단하는 방식이 아니라, 지정된 이벤트가 발생했을 때 설정된 동작을 실행하도록 구성 가능.

### Hook 사용 예시

| Hook 없이              | Hook 사용 시                    |
| -------------------- | ---------------------------- |
| 파일 편집 후 직접 포매팅       | 파일 편집 직후 Prettier 자동 실행      |
| 민감한 파일이 실수로 수정될 수 있음 | `.env` 등 특정 파일의 편집 시도 차단     |
| 작업 완료 여부를 직접 확인      | Claude가 입력을 기다릴 때 데스크톱 알림 발송 |

## 2. 이벤트 라이프사이클

Claude Code가 실행되는 동안 여러 시점에 Hook을 삽입 가능. 특정 이벤트가 발생하면 해당 이벤트에 등록된 Hook이 실행되는 구조.

### 주요 이벤트

| 이벤트                              | 호출 시점 및 용도                              |
| -------------------------------- | --------------------------------------- |
| `SessionStart`                   | Claude Code 세션이 시작되거나 재개될 때             |
| `UserPromptSubmit`               | 사용자가 입력한 프롬프트를 처리하기 직전                  |
| `PreToolUse`                     | Claude가 도구를 실행하기 직전. 실행 조건 확인 및 차단에 활용  |
| `PermissionRequest`              | 도구 실행에 대한 사용자 권한 확인이 필요할 때              |
| `PostToolUse`                    | 도구 실행이 성공적으로 끝난 후. 코드 포매팅 등 후속 작업에 활용   |
| `PostToolUseFailure`             | 도구 실행이 실패했을 때                           |
| `Notification`                   | Claude Code가 알림을 발생시킬 때. 작업 대기 알림 등에 활용 |
| `SubagentStart` / `SubagentStop` | 서브에이전트가 시작되거나 작업을 마칠 때                  |
| `TaskCreated` / `TaskCompleted`  | 작업이 생성되거나 완료될 때                         |
| `Stop` / `StopFailure`           | Claude의 응답이 종료되거나 종료 과정에서 실패했을 때        |
| `PreCompact` / `PostCompact`     | 대화 컨텍스트 압축 전후                           |
| `CwdChanged`                     | 현재 작업 디렉터리가 변경될 때                       |
| `FileChanged`                    | 파일 변경 이벤트가 발생할 때                        |
| `ConfigChange`                   | 설정 변경이 감지될 때                            |
| `SessionEnd`                     | Claude Code 세션이 종료될 때                   |

### Pre 이벤트와 Post 이벤트

* **Pre 이벤트**: 작업 실행 전 개입. 실행 조건을 검사하거나 작업 차단에 활용.
* **Post 이벤트**: 작업 실행 후 반응. 포매팅, 알림 등 후속 자동화에 활용.

**핵심 포인트:** `PreToolUse`는 도구 실행 전에 개입하므로 위험한 작업을 사전에 검사하는 가드레일로 활용 가능.

## 3. Hook의 4가지 타입

### ① `command`

* 가장 많이 사용하는 타입
* 셸 명령을 직접 실행
* stdin으로 이벤트 정보를 전달받고, stdout 및 종료 코드로 결과를 전달
* 파일 검사, 코드 포매팅, 알림 등 다양한 자동화에 활용

### ② `http`

* 이벤트 데이터를 HTTP 엔드포인트에 POST
* 외부 서비스와 연동할 때 활용
* 팀 단위 감사 서비스 및 클라우드 함수 연동 등에 적합

### ③ `prompt`

* Claude 모델을 활용해 주어진 상황을 판단
* 규칙으로 표현하기 어려운 조건을 검사할 때 활용
* 예: 특정 작업이 안전한지 여부를 판단

### ④ `agent`

* 별도의 서브에이전트를 생성해 파일을 읽거나 코드를 실행하며 검증
* 실제 코드베이스 상태를 확인해야 할 때 활용
* 강의 자료에서 실험적 타입으로 소개

## 4. Hook 설정 위치와 적용 범위

| 설정 파일 경로                      | 적용 범위          | 팀 공유            |
| ----------------------------- | -------------- | --------------- |
| `~/.claude/settings.json`     | 내 컴퓨터의 모든 프로젝트 | 로컬 전용           |
| `.claude/settings.json`       | 현재 프로젝트        | Git 커밋 가능       |
| `.claude/settings.local.json` | 현재 프로젝트        | `.gitignore` 대상 |
| 관리형 정책 설정                     | 조직 전체          | IT 관리자 중앙 관리    |

### 설정 위치 선택 기준

* **개인 전체 프로젝트에 적용**: `~/.claude/settings.json`
* **팀원과 공유할 프로젝트 설정**: `.claude/settings.json`
* **현재 프로젝트에서 개인적으로만 사용**: `.claude/settings.local.json`
* **조직 차원의 정책 적용**: 관리형 정책 설정

### 설정 확인

Claude Code에서 `/hooks` 명령어를 입력하면 현재 설정된 Hook을 이벤트별로 확인 가능.

## 6. 실습 1 — 작업 완료 알림 받기

Claude Code가 입력을 기다릴 때마다 데스크톱 알림을 보내는 Hook. 다른 작업을 하면서 Claude Code를 계속 모니터링할 필요가 없음.

### 설정 파일: `~/.claude/settings.json`

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude가 준비됐어요!\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

* `Notification`: 알림 이벤트 발생 시 Hook 실행
* `matcher`: 특정 조건을 지정하지 않는 빈 문자열
* `type: command`: 셸 명령어 실행
* `osascript`: macOS에서 데스크톱 알림 표시

**Linux용 명령어**

```bash
notify-send 'Claude Code' 'Claude가 준비됐어요!'
```

### 설정 및 확인 순서

1. 위 설정을 `~/.claude/settings.json`에 추가
2. Claude Code에서 `/hooks` 입력 후 `Notification` 아래에 등록된 Hook 확인
3. Claude에게 작업을 지시한 뒤 다른 탭으로 이동하여 알림 수신 확인

## 7. 실습 2 — 자동 코드 포매터

Claude Code가 파일을 편집한 후 Prettier를 자동 실행하여 코드 스타일을 일관되게 유지하는 Hook.

### 설정 파일: `.claude/settings.json`

프로젝트 루트에 설정.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### 주요 설정 설명

* `PostToolUse`: 도구 실행이 끝난 후 Hook 실행
* `matcher: Edit|Write`: `Edit` 또는 `Write` 도구 실행 후에만 적용
* `jq -r '.tool_input.file_path'`: stdin으로 전달된 JSON에서 파일 경로 추출
* `xargs npx prettier --write`: 추출한 파일 경로를 Prettier에 전달하여 포매팅

### jq란?

Hook은 이벤트 정보를 JSON 형태로 stdin에 전달. `jq`는 JSON에서 원하는 값을 추출하는 명령줄 도구.

### 왜 `PostToolUse`인가?

파일 편집이 완료된 이후에 포매팅해야 하기 때문. `PreToolUse`를 사용하면 Claude의 편집이 아직 적용되지 않은 파일을 포매팅하게 될 수 있음.

## 8. 실습 3 — 파일 보호 가드레일

`.env`, `package-lock` 등 보호 대상 파일의 편집을 사전에 차단하는 Hook.

### ① 보호 스크립트 작성

파일 경로: `.claude/hooks/protect-files.sh`

```bash
#!/bin/bash

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

PROTECTED=(".env" "package-lock.json")

for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "차단: $pattern 수정은 허용되지 않습니다." >&2
    exit 2
  fi
done

exit 0
```

**주요 코드 설명**

* `#!/bin/bash`: Bash 스크립트 실행 지정
* `INPUT=$(cat)`: stdin으로 전달된 JSON 전체를 읽음
* `jq -r '.tool_input.file_path'`: 편집 대상 파일 경로 추출
* `PROTECTED`: 수정 금지 파일 패턴 목록
* `for pattern in ...`: 보호 대상 패턴을 하나씩 검사
* `exit 2`: 편집 차단 신호 반환
* `exit 0`: 차단 대상이 아니므로 진행 허용

※ 강의 자료의 코드 이미지는 일부 글자가 잘려 있어, 위 스크립트는 보이는 구조를 바탕으로 실행 가능한 형태로 정리한 코드. 실제 적용 전 보호할 파일 패턴과 메시지 확인 필요.

### ② 실행 권한 부여

```bash
chmod +x .claude/hooks/protect-files.sh
```

`chmod +x`를 사용해 스크립트에 실행 권한 부여.

### ③ `.claude/settings.json`에 등록

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

* `PreToolUse`: 파일 편집 도구 실행 전 검사
* `matcher: Edit|Write`: 파일 편집 도구에 적용
* `CLAUDE_PROJECT_DIR`: 프로젝트 디렉터리를 기준으로 스크립트 경로 지정

### 차단 시 동작

`exit 2`로 종료하면 Claude Code가 작업을 차단하고 stderr 메시지를 피드백으로 전달. Claude는 전달받은 이유를 참고해 접근 방식을 바꾸어 다시 시도할 수 있음.

## 9. Hook과 Claude의 소통 방식

Hook은 Claude Code에서 발생한 이벤트 데이터를 전달받아 스크립트를 실행하고, 실행 결과를 반환하는 구조.

### 동작 흐름

`이벤트 발생 → JSON 데이터 전달(stdin) → Hook 스크립트 실행 → 종료 코드 및 출력(stdout/stderr) → Claude가 결과 처리`

### stdin으로 전달되는 JSON 예시

`PreToolUse` 이벤트에서 전달되는 데이터 구조.

```json
{
  "session_id": "abc123",
  "cwd": "/Users/dev/myproject",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

| 필드                | 의미                             |
| ----------------- | ------------------------------ |
| `session_id`      | 세션 고유 ID                       |
| `cwd`             | 현재 작업 디렉터리                     |
| `hook_event_name` | 발생한 Hook 이벤트 이름                |
| `tool_name`       | 실행 대상 도구                       |
| `tool_input`      | 도구에 전달되는 입력값. 예시에서는 실행할 명령어 포함 |

### 종료 코드에 따른 동작

| 종료 코드    | 동작                                  |
| -------- | ----------------------------------- |
| `exit 0` | 진행 허용. stdout 출력은 Claude의 컨텍스트에 추가  |
| `exit 2` | 작업 차단. stderr 메시지가 Claude에 피드백으로 전달 |
| 기타 종료 코드 | 작업은 진행되며 오류 공지가 트랜스크립트에 표시          |

**핵심 포인트:** Hook은 이벤트에 따라 명령을 실행할 뿐 아니라, 종료 코드와 출력 메시지를 통해 Claude Code의 작업 흐름을 제어할 수 있음.

