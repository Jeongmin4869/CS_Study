# 3. Git 
   
![Image](https://github.com/user-attachments/assets/cd0df8c2-2d74-499b-978b-fe247d01e73e)

## 01 - Git의 작업공간 
      
#### 1. Workspace
- 작업하는 일반적인 공간
- git을 쓰기 이전 처음 상태
- git add 명령어 이전에는 변경 사항들이 workspace에 기록된다.  
   
#### 2. Index
- 변경되는 모든 파일 및 폴더들을 추적하는 공간
- Staging area라고도 한다.
- git add 명령어를 통해 workspace 공간에 있는 작업물을 이 공간으로 보낸다.
- 최종적으로 커밋하고자 하는 작업물을 이 공간에 둔다
- 한번 index에 올라갔던 파일들은 git에서 계속 추적한다. 
   
#### 3. Local repository
- 커밋된 작업물들이 놓이는 공간
- git commit 명령어로 index에 있는 파일들을 이 공간으로 보낸다.
- 최종적으로 작업한 내용이 이 공간에 기록된다 
   
#### 4. Remote repository
- Git 호스팅 공간으로, 인터넷으로 연결된 별도의 공간
- 최종 작업물을 이곳에 저장하면 다른 사람들과 공유할 수 있다.
- git push 령령어로 local repository 공간에 있는 작업물을 이 공간으로 보낸다.
- git fetch 나 git pull 명령어로 이 공간에 있는 작업물을 local repository로 가져올 수 있다.
- Git-hub, BitBucket, GitLab등이 이 공간을 구현한 Git 호스팅 서비스이다. 
     
```bash
   # workspace -> index
   git add

   # index -> local repository
   git commit

   # local repository -> remote repository
   git push

   #remote repository -> local repository 
   git pull
   git fetch

   #기록된 커밋 로그 확인
   git log

   # workspace 공간에 있는 작업물 확인
   git status 
```

   
   
--- 
## 02 - 브랜치
   
<img width="968" height="496" alt="Image" src="https://github.com/user-attachments/assets/9e11dc8b-4b89-4577-912b-9233e8e3f833" />
   
- 브랜치는 사용자가 독립적으로 작업을 진행할 수 있도록 돕는 작업 흐름이다. 
- 하나의 브랜치는 독립된 workspace, index, local repository, remote repository 공간을 가진다.
- 브랜치를 이용하면 하나의 프로젝트에서 여러 사람이 동시에 본인의 작업을 진행할 수 있다.
   
> git switch -c {새로운 브랜치 이름} {기준 브랜치}  : 커밋 기준으로 브랜치 생성   
> git merge user : user 브랜치를 현재 브랜치(main)에 합친다    
   
- 브랜치를 통해 하나의 프로젝트에서 독립된 작업 공간을 가질 수 있다.
- 각 브랜치별로 4가지 공간을 갖게 된다.
- 협업할 때는 보통 각자 작업할 브랜치를 만들고 그 위에서 작업한다.
- Remote repository에서 각자 브랜치 작업을 리뷰받은 뒤 메인 브랜치로 머지한다. 
    
   
## 03 - [log & reflog] 이전 commit 내역들과 변경사항을 확인
   
### HEAD
- HEAD는 커밋 내역에서 현재 커밋(보통 가장 최신 커밋)을 가리키는 심볼릭 링크(포인터)이다.
- 보통 명령어에 커밋ID 대신 HEAD 포인터를 활용한다.
- HEAD 이전 커밋들을 확인하고 싶을 땐 HEAD^ 혹은 HEAD~으로 포인팅이 가능하다.
- HEAD로부터 3개 이전 커밋에 접근하고 싶다면 HEAD^^^ 혹은 HEAD~3으로 표헌할 수 있다. 
    
   
    
### git log
- 커밋 내역을 확인
   
```bash
$ git log

commit c008c4785eeb14a395b4aa6cf9fa3b9e5896f5a4 (HEAD -> main)
Author: grab <grab@gmail.com>
Date:   Tue Aug 17 21:21:45 2021 +0900

    a 파일을 수정한다

commit b014111c82fa239b771b2b6d6bdc567282e7b325
Author: grab <grab@gmail.com>
Date:   Tue Aug 17 20:34:32 2021 +0900

    a 파일을 추가한다
```
   
- oneline으로 간략하게 보거나, -n으로 특정 개수만의 커밋 내역을 확인할 수 있다.
    
```bash
$ git log --oneline

c008c47 (HEAD -> main) a 파일을 수정한다
b014111 a 파일을 추가한다

$ git log -n 10
# 최근 10개의 커밋들만 보여줍니다. 
```

- git을 그래프 형태로 확인할 수 있다.
     
```bash
git log --oneline --decorate --graph
```

       
### git show
- 가장 최근 커밋의 정보를 확인할 수 있다. 
- 특정 커밋 정보를 확인하려면 git show 커밋해시를 붙이면 된다.
     
```bash
$ git show

commit c008c4785eeb14a395b4aa6cf9fa3b9e5896f5a4 (HEAD -> main)
Author: grab <grab@gmail.com>
Date:   Tue Aug 17 21:21:45 2021 +0900

    a 파일을 수정한다

diff --git a/a b/a
index e69de29..9e365c8 100644
--- a/a
+++ b/a
@@ -0,0 +1 @@
+this is a

$ git show c008c4785eeb14a395b4aa6cf9fa3b9e5896f5a4
$ git show HEAD^ #HEAD 포인터 활용

```
   
       
### git reflog
- git reflog명령어로 git reset, git rebase 명령어를 통해 삭제된 커밋을 포함한 모든 커밋 히스토리를 확인할 수 있다. 
- git은 이전 명령어(ex. git reset —hard)를 취소하고 싶을 때 유용하다. 
   
```bash
$ git reflog

c008c47 (HEAD -> main) HEAD@{0}: commit: a 파일을 수정한다
b014111 HEAD@{1}: commit (initial): a 파일을 추가한다

$ git reset 0379a06 --hard

HEAD의 현재 위치는 0379a06입니다 b 파일을 추가한다

$ git reflog

0379a06 (HEAD - my-branch) HEAD@{0}: reset: moving to 0379a069b014afc2c256f3d94c4fb93fd833003e
c7591af HEAD@{1}: checkout: moving from main to my-branch
9cb8a3b (main) HEAD@{2}: rebase (finish): returning to refs/heads/main
9cb8a3b (main) HEAD@{3}: rebase (pick): d 파일을 추가한다
c7591af HEAD@{4}: rebase (start): checkout my-branch
31b3b73 HEAD@{5}: reset: moving to 31b3b73dc282d37a30b9d0242f18dfaf69878c0b

$ git reset c7591af --hard
```
      
   
---       
## 04 - [restore & reset] 변경사항, 커밋을 초기화
   
- Git reset 명령어는 특정 커밋의 시점으로 돌아갈 때 해당 커밋 이후의 작업물을 어떻게 처리하느냐에 따라 3가지 옵션이 있다. 
   - hard
   - mixed
   - soft
   
   
### git reset —hard {커밋ID}
- 특정 커밋 시점으로 돌아갈 때 해당 커밋 이후 만들어진 모든 작업물을 삭제한다.
- 현재 작업한 파일들을 모두 날리고 이전 커밋으로 돌아가고 싶을 때 사용한다.
- 기존에 작성하먼 변경사항들도 모두 이전으로 돌아가기 때문에 주의가 필요하다 
   
```bash
$ git reset --hard b014111 

HEAD의 현재 위치는 b014111입니다 a 파일을 추가한다

$ git log --oneline

b014111 a 파일을 추가한다

$ git status

현재 브랜치 main
커밋할 사항 없음, 작업 폴더 깨끗함
```
   
   
### git reset —mixed {커밋ID}
- 특정 커밋 시점으로 돌아갈 때, 해당 커밋 이후 모든 작업물은 workspace 공간에 unstaged 상태로 남게 된다. 
- mixed옵션은 기본옵션으로 git reset만 실행해도 결과는 동일하다.
     
```bash
$ git reset b014111 --mixed

리셋 뒤에 스테이징하지 않은 변경 사항:
M	a

$ git log --oneline

b014111 a 파일을 추가한다

$ git status

현재 브랜치 main
커밋하도록 정하지 않은 변경 사항:
  (무엇을 커밋할지 바꾸려면 "git add <파일>..."을 사용하십시오)
  (use "git restore <file>..." to discard changes in working directory)
	수정함:        a

커밋할 변경 사항을 추가하지 않았습니다 ("git add" 및/또는 "git commit -a"를 사용하십시오)
```
   
   
### git reset —soft {커밋ID}
- 특정 커밋 시점으로 돌아갈 때, 해당 커밋 이후 모든 작업물은 index 공간에 staged상태로 남게 된다.
   
```bash
$ git reset b014111 --soft

$ git log --oneline

b014111 a 파일을 추가한다

$ git status

현재 브랜치  main
커밋할 변경 사항:
  (use "git restore --staged <file>..." to unstage)
	수정함:        a
```
   
   
### git restore {파일경로}
- 특정 파일의 변경사항을 제거하고 HEAD 기준으로 되돌리고 싶을 때 restore을 사용할 수 있다. 
- workspace에 있는 변경 사항을 update 기준으로 되돌릴 때 사용한다. 
- Git restore는 git reset —hard HEAD와 비슷한 결과를 내지만, restore는 새 파일의 변경사항 (새 파일을 추가한 사실)은 되돌릴 수 없다.
     
```bash
# 아직 stage(index)에 올라가지 않은 README.md 파일을 되돌릴 때  
$ git restore README.md
```
   
   
--- 
## 05 - [stash] 변경사항 임시저장
   
### git stash
- 수정 내용을 임시 저장하는 명령어
- 브랜치를 전환해서 작업할 때 사용
- git stash 명령어를 쓰면 현재 변경사항을 별도의 스택 공간에 빼두게 된다. 
   
```bash
$ git stash
Saved working directory and index state WIP on my-branch: b014111 a 파일을 추가한다

$ git stash -m "OOO 변경 사항..."

$ git switch main
'main' 브랜치로 전환합니다
```
   
   
### git stash pop
- 스택에 넣었던 작업 내역을 불러온다 
   
```bash
$ git switch my-branch
'my-branch' 브랜치로 전환합니다

$ git stash pop

현재 브랜치 my-branch
커밋하도록 정하지 않은 변경 사항:
  (무엇을 커밋할지 바꾸려면 "git add <파일>..."을 사용하십시오)
  (use "git restore <file>..." to discard changes in working directory)
	수정함:        a

커밋할 변경 사항을 추가하지 않았습니다 ("git add" 및/또는 "git commit -a"를
사용하십시오)
Dropped refs/stash@{0} (762134d031bbb57b72183e4001ac283b266d3953)
```
   
   
### git stash apply
- git stash pop 과 비슷한 명령어. pop은 스택 공간에서 내역을 제거하고 apply는 제거하지 않는다.
- git stash list로 봐도 작업 내역이 그대로 남아있다.
- 작업 내역 재사용이 가능하다. 
   
   
---    
## 06 - [revert] 이전 커밋의 변경사항 복구
   
### git revert {커밋ID}
- 기존 커밋들은 지우지 않고 현재 커밋 위로 이전 커밋 내용을 다시 되돌리는 커밋을 만든다, 
   
```bash
$ git log --oneline

875a6e6 b 파일을 추가한다
1fc71a0 a 파일을 수정한다
b014111 a 파일을 추가한다

$ git revert 1fc71a0

Revert "a 파일을 수정한다"
This reverts commit 1fc71a0e2b3839cdd0ada557df823609f234610a.

# 변경 사항에 대한 커밋 메시지를 입력하십시오. '#' 문자로 시작하는
# 줄은 무시되고, 메시지를 입력하지 않으면 커밋이 중지됩니다.
#
# 현재 브랜치 main
# 커밋할 변경 사항:
#       수정함:        a
#

$ git log --oneline

dea542b This reverts commit 1fc71a0e2b3839cdd0ada557df823609f234610a.
875a6e6 b 파일을 추가한다
1fc71a0 a 파일을 수정한다
b014111 a 파일을 추가한다

```
   
   
## 07 - [amend commit & rebase] 이전 커밋 내용 변경
   
- 커밋 메세지를 수정하고 싶거나 변경된 파일의 일부를 되돌릴 때 사용
- Git commit —amend : 현재 작업중인 커밋(HEAD)을 수정
- Git rebase —interactive : HEAD 아래에 있는 커밋들 중 일부를 수정하거나 변경할 때 사용
- Git revert는 대상 커밋을 되돌리는 새로운 커밋을 만드는 기능이며, 커밋 자체를 변경하지는 못한다. 
   
   
### git commit —amend
-  —amend는 현재 커밋(HEAD)위에 변경사항을 덮어씌울 때 사용하는 옵션이다.
-  커밋을 한 후 추가적인 변경사항이 생겼거나 커밋 메세지를 변경하고 싶을 때 사용한다.
-  커밋 메세지만 수정하고 싶다면 변경사항 없이 바로 git commit —amend를 사용한다
-  커밋 메세지의 수정을 필요로 하지 않는 경우 —no-edit 옵션을 붙인다 
   
   
```bash
$ git add .

# 만약 커밋 메시지를 변경하고 싶다면 텍스트를 수정한 후 저장을 하면 됩니다.
# 변경이 필요 없다면 바로 :wq로 저장을 하면 됩니다. 
$ git commit --amend

feat: 기존 커밋 메시지...
  
# 변경 사항에 대한 커밋 메시지를 입력하십시오. '#' 문자로 시작하는
# 줄은 무시되고, 메시지를 입력하지 않으면 커밋이 중지됩니다.
#
# 시각:      Sun Sep 26 01:14:25 2021 +0900
#
# 현재 브랜치 main
# 브랜치가 'origin/main'보다 1개 커밋만큼 앞에 있습니다.
#   (로컬에 있는 커밋을 제출하려면 "git push"를 사용하십시오)
...

```
   
   
```bash
$ git commit --amend --no-edit

[main ed58623] feat: 기존 커밋 메시지...
Date: Sun Sep 26 01:14:25 2021 +0900
8 files changed, 112 insertions(+), 107 deletions(-)
...
```
