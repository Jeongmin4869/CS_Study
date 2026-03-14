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
   
   
### git rebase —interactive {커밋ID}
- git rebase는 브랜치 병합 과정에서 자주 사용된다.
- 동시에 과거 커밋 히스토리를 변경할 수 있는 기능을 —interavtive 옵셕을 통해 제공한다.
- 커밋 히스토리의 수정 범위는 현재 최신 커밋부터 {커밋ID}바로 위 커밋까지 적용된다.
   
```bash

$ git log --oneline

bec1c83 (HEAD -> main) c를 추가한다
bdc0d87 b를 추가한다
1dee32c a를 추가한다


# 두번째커밋 bdc0d87에 b2파일 추가, 마지막 커밋에 c파일 삭제

$ git rebase --interactive 1dee32c # 혹은 HEAD^^ , HEAD~2 로도 표현

edit bdc0d87 b를 추가한다
drop bec1c83 c를 추가한다

# Rebase 1dee32c..bec1c83 onto 1dee32c (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
# .       create a merge commit using the original merge commit's
# .       message (or the oneline, if no original merge commit was
# .       specified). Use -c <commit> to reword the commit message 

```
   
   
- Command
 - pick : 변경사항 없이 커밋을 그대로 유지한다.
 - edit : 해당 커밋의 내용을 수정할 수 있으며 커밋 메시지도 변경할 수 있다.
 - reword : 해당 커밋의 메시지만 수정한다.
 - drop : 해당 커밋을 히스토리에서 제거한다.
   
Interactive rebase는 커밋을 하나씩 다시 적용하는 방식으로 동작하며,   
각 command가 적용되는 커밋으로 HEAD가 이동한다.   
   
특히 edit을 선택하면 Git이 해당 커밋에서 멈추며,   
이 상태에서 코드를 자유롭게 추가/삭제/수정할 수 있다.   
   
   
```bash
edit bdc0d87 b를 추가한다 # 약자로 e를 넣어도 무방합니다. 
pick bec1c83 c를 추가한다

#저장 후 
bdc0d87...  b를 추가한다 # 해당 위치에서 멈췄습니다
You can amend the commit now, with

  git commit --amend

Once you are satisfied with your changes, run

  git rebase --continue

$ git commit --amend

b와 b2를 추가한다  

# 변경 사항에 대한 커밋 메시지를 입력하십시오. '#' 문자로 시작하는
# 줄은 무시되고, 메시지를 입력하지 않으면 커밋이 중지됩니다.
#
# 시각:      Sun Sep 26 16:59:27 2021 +0900
#
```

- git commit —amend : 현재 최신 커밋(HEAD)에 덮어 씌우는 작업을 하게 된다.

```bash
$ git commit --amend

b와 b2를 추가한다  

# 변경 사항에 대한 커밋 메시지를 입력하십시오. '#' 문자로 시작하는
# 줄은 무시되고, 메시지를 입력하지 않으면 커밋이 중지됩니다.
#
# 시각:      Sun Sep 26 16:59:27 2021 +0900
#

```

- git rebase —continue : commit을 마친 후 변경사항을 적용했다면 다음 작업 대상으로 넘어간다 

```bash
 $ git rebase --continue

8f820c0...  c를 추가한다 위치에서 멈췄습니다
You can amend the commit now, with

  git commit --amend

Once you are satisfied with your changes, run

  git rebase --continue

```

- git rebase —skip : 커밋의 변경 사항을 주지 않고 다음으로 넘어간다. 

```bash
 $ git rebase --skip 

# 다음 변경할 commit으로 HEAD가 옮겨갑니다.

```

 - git rebase —abort  : rebase하는 과정 전체를 취소

```bash
$ git rebase --abort

# rebase -i를 주기 전 원래 환경으로 돌아옵니다. 

```
   
   
## 08 - [squash & rebase merge] 커밋 방식에 따른 브랜치
   
브랜치를 합치는 방법
- 기본 Merge
- Squash & Merge
- Rebase & Merge
   
<img width="718" height="376" alt="Image" src="https://github.com/user-attachments/assets/e87ef42c-8671-48ff-b592-6c40fc8d3814" />
   
      
```bash 
$ git switch feature-branch
$ git rebase main

Successfully rebased and updated refs/heads/feature-branch.

$ git log --oneline

9cb8a3b (HEAD -> main, feature-branch) a 파일을 추가한다
c7591af d 파일을 추가한다
fc25d18 c 파일을 추가한다
0379a06 b 파일을 추가한다
b014111 a 파일을 추가한다
```
   
   
### git merge {브랜치이름}
- 가장 기본적인 머지 방식
- 브랜치 생성 후 main에 추가 커밋이 없을 경우 fast-forward. Merge 커밋이 생기지 않고 브랜치의 모든 커밋이 main 브런치로 들어가게 된다.
- 머지 커밋을 통해 명시적으로 브랜치의 병합이 있었다는 것을 표시하고 싶을 때 git merge 방식을 사용한다. 
   
```bash
$ git switch -c feature-branch

새로 만든 'feature-branch' 브랜치로 전환합니다

$ git log --oneline

7404163 (HEAD -> main, feature-branch) c 파일을 추가한다
c315709 b 파일을 추가한다
b014111 a 파일을 추가한다

# ... 파일 수정 작업
$ git commit -m "a 파일을 수정합니다"

 
$ git switch main

'main' 브랜치로 전환합니다

$ git merge feature-branch

업데이트 중 b014111..c7591af
Fast-forward
 a | 1 +
 b | 0
 c | 0
 3 files changed, 1 insertion(+)
 create mode 100644 b
 create mode 100644 c

```
   
- mani브랜치에 새로운 커밋이 생겼을 경우, git merge명령어를 입력하면 merge를 위한 머지 커밋이 생성된다. 
   
```bash
$ git merge feature-branch

Merge branch 'feature-branch'
# Please enter a commit message to explain why this merge is necessary,
# especially if it merges an updated upstream into a topic branch.
#
# Lines starting with '#' will be ignored, and an empty message aborts
# the commit.
Merge made by the 'recursive' strategy.
 a | 1 +
 b | 0
 c | 0
 3 files changed, 1 insertion(+)
 create mode 100644 b
 create mode 100644 c

# git log로 확인하면 Merge 내용을 나타내는 커밋이 생성되게 됩니다.
$ git log --oneline

85c04dc (HEAD -> main) Merge branch 'feature-branch'
31b3b73 d 파일을 추가한다
c7591af (feature-branch) a 파일을 수정한다
fc25d18 c 파일을 추가한다
0379a06 b 파일을 추가한다
b014111 a 파일을 추가한다

```
   
   
### Merge conflict
- 머지할 때 두 브랜치가 다음과 같은 상황일 때 git은 충돌이 발생하며, 이를 merge conlict라고 한다.
	- 한 파일의 같은 라인을 수정했을 때
	- 한 브랜치에서는 파일을 삭제하고, 한 브랜치에서는 파일을 변경할 때 
- 이 경우 conflict가 난 파일을 해결(resolve) 한 후 merge를 진행해야 한다. 
   
   
### git merge {브랜치 이름} —squash
- 머지 커밋을 만들지 않고 변경사항만 병합할 경우 사용
- 머지커밋을 남기지 않으면서 해당 브랜치에서 작업한 모든 내용을 하나의 커밋으로 묶는다.
- 작업한 커밋들을 하나의 커밋으로 만들어 main브런치에서 합친다 .
- 하나의 커밋으로 묶어 병합하면 브랜치의 구조를 깔끔하게 유지할 수 있다
- 다만 롤백 처리를 할 때 커밋을 한번에 처리하는 게 불가능해지는 문제가 있다. 
   
```bash
$ git merge feature-branch --squash

커밋 합치기 -- HEAD를 업데이트하지 않습니다
자동 병합이 잘 진행되었습니다. 요청한대로 커밋 전에 중지합니다

$ git commit -m "feature-branch 브랜치에서 작업한 내용을 합친다" 

...
[main 1b8874f] feature-branch 브랜치에서 작업한 내용을 합친다
 3 files changed, 1 insertion(+)
 create mode 100644 b
 create mode 100644 c

$ git log --oneline

1b8874f (HEAD -> main) feature-branch 브랜치에서 작업한 내용을 합친다
31b3b73 d 파일을 추가한다
b014111 c 파일을 추가한다
b014111 b 파일을 추가한다
b014111 a 파일을 추가한다

```
   
   
### git rebase {브랜치 이름}
- merge할때 merge커밋을 남기지 않으면서도, merge되는 브랜치의 모든 커밋 내역을 가져온다.
- 두 머지 방식과 다르게 rebase의 경우 병합이 될 브런치에서 git rebase {대상브랜치}를 사용한다.
- git rebase는 별다른 커밋을 생성하지 않고 커밋 구조를 변경한다.
- 코드를 보는 입장에서는 깔끔할 수 있지만, 브랜치의 병합 히스토리가 명시적으로 잘 남아있지 않아 히스토리 추적 시 불편할 수 있다. 
   
```bash

$ git log --oneline

c7591af (feature-branch) a 파일을 수정한다
fc25d18 c 파일을 추가한다
0379a06 b 파일을 추가한다
b014111 a 파일을 추가한다

$ git switch feature-branch
$ git rebase main 

Successfully rebased and updated refs/heads/feature-branch.

$ git switch main
# main이 HEAD를 바라보고 있지 않을 경우 merge
$ git merge feature-branch 
$ git log --oneline

9cb8a3b (HEAD -> main, feature-branch) a 파일을 추가한다
c7591af d 파일을 추가한다
fc25d18 c 파일을 추가한다
0379a06 b 파일을 추가한다
b014111 a 파일을 추가한다

```
   
