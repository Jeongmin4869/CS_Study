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

Hook은 Claude Code에서 이벤트가 발생했을 때 실행되는 스크립트. Claude Code는 Hook에 이벤트 관련 정보를 전달하고, Hook은 실행 결과를 다시 Claude Code에 반환하는 방식으로 동작.

즉, Hook은 단순히 명령어를 실행하는 기능이 아니라 **이벤트 정보와 실행 결과를 주고받으며 Claude Code의 작업 흐름에 개입하는 구조**.

### ① 전체 동작 흐름

```text
① Claude Code에서 이벤트 발생
          ↓
② 이벤트 관련 JSON 데이터 전달
   (stdin)
          ↓
③ Hook 스크립트 실행
          ↓
④ 실행 결과 반환
   (종료 코드 + stdout/stderr)
          ↓
⑤ Claude Code가 결과 처리
```

각 단계의 역할은 다음과 같음.

1. **이벤트 발생**: Claude Code에서 `PreToolUse`, `PostToolUse` 등의 이벤트 발생
2. **JSON 데이터 전달**: 어떤 이벤트가 발생했는지, 어떤 도구를 실행하려는지 등의 정보를 JSON으로 전달
3. **Hook 스크립트 실행**: 전달받은 JSON을 읽고 필요한 검사나 명령 실행
4. **실행 결과 반환**: 종료 코드와 표준 출력(stdout), 표준 오류(stderr)를 통해 결과 전달
5. **결과 처리**: Claude Code가 반환된 결과에 따라 작업을 허용하거나 차단하고, 메시지를 컨텍스트에 반영

### ② stdin으로 전달되는 JSON 데이터

`PreToolUse` 이벤트에서 전달되는 JSON 예시.

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

Hook은 이 JSON을 표준 입력(stdin)으로 전달받음.

| 필드 | 의미 |
|---|---|
| `session_id` | 현재 세션의 고유 ID |
| `cwd` | 현재 작업 디렉터리 |
| `hook_event_name` | 발생한 Hook 이벤트 이름 |
| `tool_name` | 실행하려는 도구 이름 |
| `tool_input` | 해당 도구에 전달되는 입력값 |

**예시 해석**

위 JSON은 다음과 같은 상황을 의미함.

- 현재 세션 ID는 `abc123`
- 작업 디렉터리는 `/Users/dev/myproject`
- `PreToolUse` 이벤트 발생
- Claude가 `Bash` 도구를 사용하려는 상황
- 실행하려는 명령어는 `npm test`

따라서 Hook 스크립트는 이 데이터를 읽고 `npm test` 실행을 허용할지, 특정 조건을 검사할지 등을 판단 가능.

### ③ stdin, stdout, stderr의 차이

Hook과 Claude Code는 표준 입출력 스트림을 통해 데이터를 주고받음.

| 구분 | 데이터 전달 방향 | 역할 |
|---|---|---|
| `stdin` | Claude Code → Hook | 이벤트 정보가 담긴 JSON 전달 |
| `stdout` | Hook → Claude Code | Hook 실행 결과 및 구조화된 JSON 전달 |
| `stderr` | Hook → Claude Code | 오류 메시지 및 차단 사유 등의 피드백 전달 |

- **stdin(Standard Input)**: Hook이 입력받는 데이터. Claude Code가 이벤트 정보를 JSON으로 전달
- **stdout(Standard Output)**: Hook이 출력하는 데이터. 일반 텍스트나 구조화된 JSON을 Claude Code에 전달
- **stderr(Standard Error)**: Hook이 출력하는 오류 및 피드백 메시지

### ④ 종료 코드에 따른 동작

Hook 스크립트는 실행이 끝나면 종료 코드와 출력 메시지를 반환. Claude Code는 이 결과를 바탕으로 다음 작업을 결정.

| 종료 코드 | 동작 |
|---|---|
| `exit 0` | 작업 진행 허용. stdout 출력은 Claude의 컨텍스트에 추가 |
| `exit 2` | 작업 차단. stderr 메시지가 Claude에 피드백으로 전달 |
| 기타 종료 코드 | 작업은 진행되며 오류 공지가 트랜스크립트에 표시 |

**각 결과의 의미**

- `exit 0`: Hook 검사가 정상적으로 끝났으며 작업을 계속 진행할 수 있다는 의미
- `exit 2`: Hook에서 작업을 차단해야 한다고 판단했다는 의미. stderr에 작성한 메시지를 통해 차단 이유 전달
- 기타 종료 코드: 일반적인 차단 신호로 사용하지 않으며, 오류 공지가 트랜스크립트에 표시됨

**예시**

```bash
# 작업 허용
echo "검사 완료"
exit 0
```

```bash
# 작업 차단
echo "이 명령어는 실행할 수 없습니다." >&2
exit 2
```

첫 번째 예시는 정상 진행을 허용하고, 두 번째 예시는 작업을 차단하면서 이유를 전달하는 방식.

**핵심:** Hook은 종료 코드로 작업의 진행 여부를 제어하고, stdout/stderr로 Claude Code에 필요한 정보를 전달.

## 10. 구조화된 JSON 출력으로 정밀 제어

앞에서 살펴본 종료 코드는 기본적인 허용과 차단을 제어하는 방식. 하지만 종료 코드만으로는 권한 결정의 종류나 구체적인 거부 사유를 세밀하게 지정하기 어려움.

이때 **구조화된 JSON 출력**을 사용하면 도구 실행에 대한 결정을 더 구체적으로 전달 가능.

### ① PreToolUse에서 JSON으로 거부 사유 전달

다음은 `PreToolUse` 이벤트에서 도구 실행을 거부하고 그 이유를 전달하는 예시.

Hook 스크립트가 실행 결과를 **stdout(표준 출력)에 JSON 형태로 출력**하면 Claude Code가 해당 JSON을 읽고 권한 결정에 반영.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "grep 대신 rg(ripgrep)를 사용하세요"
  }
}
```

위 JSON은 Hook 스크립트가 Claude Code에 반환하는 출력 데이터. 실제 `command` Hook에서는 JSON을 stdout으로 출력해야 함.

각 필드의 역할은 다음과 같음.

| 필드 | 의미 |
|---|---|
| `hookSpecificOutput` | 특정 Hook 이벤트에서 사용할 추가 출력 정보 |
| `hookEventName` | 해당 JSON 출력이 적용되는 이벤트 이름 |
| `permissionDecision` | 도구 실행에 대한 권한 결정 |
| `permissionDecisionReason` | 권한 결정 이유를 Claude에 전달하는 메시지 |

**stdin과 stdout의 차이**

- `stdin`: Claude Code가 Hook에 전달하는 입력 데이터. 이벤트 정보가 담긴 JSON
- `stdout`: Hook이 Claude Code에 반환하는 출력 데이터. 권한 결정 결과가 담긴 JSON

따라서 9번에서 살펴본 `stdin` JSON은 Hook이 전달받는 데이터이고, 여기서 사용하는 JSON은 Hook이 검사 결과를 반환하는 데이터.

**동작 과정**

1. Claude Code에서 `PreToolUse` 이벤트 발생
2. 이벤트 정보가 JSON 형태로 Hook의 `stdin`에 전달
3. Hook 스크립트에서 전달받은 데이터를 검사
4. 검사 결과를 JSON으로 구성하여 `stdout`에 출력
5. Claude Code가 출력된 JSON을 읽고 `permissionDecision`에 따라 처리
6. `deny`인 경우 도구 호출을 취소하고 거부 사유를 Claude에 전달

예를 들어 `grep` 명령어 사용을 거부하면서 `rg(ripgrep)`를 사용하도록 안내하면, Claude가 해당 피드백을 참고해 명령어를 변경할 수 있음.

※ 위 코드 블록은 stdout으로 반환할 JSON 데이터의 구조를 보여주는 예시이며, 셸 스크립트 자체는 아님.

### ② `permissionDecision`의 세 가지 값

| 값 | 동작 | 설명 |
|---|---|---|
| `allow` | 허용 | 권한 확인 프롬프트를 건너뛰고 도구 실행 허용 |
| `deny` | 거부 | 도구 호출 취소 및 거부 이유 전달 |
| `ask` | 사용자 확인 | 사용자에게 권한 확인 프롬프트 표시 |

각 값은 단순히 성공과 실패를 구분하는 것이 아니라, 도구 실행을 어떤 방식으로 처리할지 결정하는 역할.

- `allow`: Hook에서 허용했으므로 권한 확인 단계를 건너뛰는 방향
- `deny`: 도구 실행을 취소하고 Claude에 이유 전달
- `ask`: Hook이 직접 허용하거나 거부하지 않고 사용자에게 판단 요청

### ③ 종료 코드와 JSON 출력의 차이

| 구분 | 종료 코드 | 구조화된 JSON 출력 |
|---|---|---|
| 목적 | 기본적인 진행·차단 제어 | 권한 결정과 사유를 세밀하게 지정 |
| 주요 결과 | `exit 0`, `exit 2` 등 | `allow`, `deny`, `ask` |
| 전달 정보 | stdout/stderr 메시지 | 권한 결정 및 결정 사유 |

**주의:** 강의안에서는 `exit 2`와 JSON 출력을 혼용하지 않도록 안내. `exit 2`로 종료하면 Claude Code가 JSON 출력을 무시하므로, JSON을 이용한 권한 결정과 종료 코드에 의한 차단 방식을 구분해서 사용해야 함.

**핵심:** 종료 코드는 기본적인 허용·차단을 담당하고, 구조화된 JSON 출력은 도구 실행에 대한 권한 결정과 그 이유를 구체적으로 전달하는 방식.

## 11. Matcher 패턴으로 Hook 범위 좁히기

Hook을 특정 이벤트에 등록하면 해당 이벤트가 발생할 때 실행 가능. 하지만 하나의 이벤트에서도 여러 종류의 도구가 실행될 수 있음.

예를 들어 `PreToolUse`는 `Bash`, `Edit`, `Write` 등 여러 도구가 실행되기 전에 발생.

모든 도구 실행에 동일한 Hook을 적용할 필요가 없다면 `matcher`를 사용해 실행 대상을 제한 가능.

**Matcher는 Hook이 어떤 도구 또는 상황에서 실행될지 결정하는 필터 역할.**

### ① Matcher가 없는 경우

특정 이벤트에 Hook을 등록했지만 Matcher를 지정하지 않았다면, 해당 이벤트가 발생할 때마다 Hook이 실행됨.

예를 들어 `PreToolUse`에 Matcher 없이 Hook을 등록하면 `Bash`, `Edit`, `Write` 등 해당 이벤트에 해당하는 도구 실행 전에 Hook이 실행되는 구조.

### ② 도구 이름으로 필터링

Matcher에 도구 이름을 지정하면 특정 도구가 실행될 때만 Hook 적용 가능.

```json
// Edit 또는 Write 도구만
"matcher": "Edit|Write"

// Bash 도구만
"matcher": "Bash"

// MCP GitHub 서버 도구
"matcher": "mcp__github__.*"
```

| Matcher | 적용 대상 |
|---|---|
| `Edit|Write` | Edit 또는 Write 도구 |
| `Bash` | Bash 도구 |
| `mcp__github__.*` | 이름이 해당 패턴과 일치하는 MCP GitHub 도구 |

**예시: 파일 편집 후 자동 포매팅**

앞서 작성한 자동 코드 포매터를 다시 살펴보면 다음과 같음.

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
    }
  ]
}
```

여기서는 `Edit|Write`를 Matcher로 지정했기 때문에 Claude가 파일을 편집하거나 작성하는 도구를 사용한 경우에만 Prettier 실행.

Bash 명령어를 실행하거나 다른 도구를 사용하는 경우에는 이 Hook이 실행되지 않음.

### ③ `if` 필드로 인수까지 필터링

도구 이름만으로는 실행 조건을 충분히 구체화하기 어려운 경우가 있음.

예를 들어 `Bash` 도구를 사용하는 모든 상황이 아니라, 그중에서도 `git` 명령어를 실행할 때만 특정 Hook을 실행하고 싶은 경우.

강의안에서는 다음과 같이 `if` 필드를 사용한 예시를 제시.

```json
{
  "type": "command",
  "if": "Bash(git *)",
  "command": "./check-git-policy.sh"
}
```

- `if`: 도구 입력값에 대한 추가 조건
- `Bash(git *)`: Bash 도구 중 `git`으로 시작하는 명령어를 대상으로 지정
- `command`: 조건에 해당할 때 실행할 스크립트

예를 들어 다음과 같은 명령어를 구분하는 상황.

```bash
git status
git commit -m "update"
npm test
```

`Bash(git *)` 조건이라면 `git status`, `git commit`처럼 `git`으로 시작하는 명령어가 대상이며, `npm test`는 대상에서 제외되는 형태.

※ `if` 필드 예시는 강의안에 제시된 문법을 그대로 정리한 것. 실제 설정에 적용할 때는 사용 중인 Claude Code 버전의 Hook 설정 문법 확인 필요.

### ④ 이벤트별 Matcher 기준

Matcher는 모든 이벤트에서 동일한 대상을 필터링하는 것이 아님. 이벤트의 종류에 따라 필터링 기준이 달라짐.

| 이벤트 | Matcher가 필터링하는 항목 | 예시 |
|---|---|---|
| `PreToolUse`, `PostToolUse` | 도구 이름 | `Bash`, `Edit`, `Write` |
| `SessionStart` | 세션 시작 방식 | `startup`, `resume`, `compact` |
| `FileChanged` | 감시할 파일명 | `.envrc`, `.env` |
| `ConfigChange` | 설정 소스 | `user_settings`, `project_settings` |

예를 들어 다음과 같은 차이가 있음.

- `PreToolUse`: 어떤 도구를 실행하려는지에 따라 Hook 실행 여부 결정
- `SessionStart`: 새 세션인지, 이전 세션 재개인지, 컨텍스트 압축 후 재시작인지에 따라 Hook 실행 여부 결정
- `FileChanged`: 어떤 파일이 변경되었는지에 따라 Hook 실행 여부 결정
- `ConfigChange`: 어떤 설정이 변경되었는지에 따라 Hook 실행 여부 결정

### ⑤ Matcher 사용 시 보안 주의사항

Matcher는 가능한 한 구체적으로 지정하는 것이 중요.

예를 들어 파일 편집 도구만 검사하면 되는 Hook에 모든 도구를 대상으로 하는 Matcher를 사용하면 불필요한 실행이 발생할 수 있음.

또한 Matcher는 **Hook이 실행될 대상을 결정하는 필터**이지, 그 자체로 도구 실행 권한을 허용하거나 거부하는 설정은 아님.

따라서 다음 두 가지를 구분해야 함.

- Matcher: 어떤 상황에서 Hook을 실행할 것인가?
- Hook의 반환 결과: 실행된 Hook이 작업을 허용할 것인가, 차단할 것인가?

**핵심:** Matcher로 Hook의 실행 범위를 좁히고, Hook의 반환 결과로 실제 작업의 허용·차단 여부를 제어.
