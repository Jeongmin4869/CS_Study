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
     
> git add : workspace -> index   
> git commit : index -> local repository   
> git push : local repository -> remote repository   
> git pull, fetch : remote repository -> local repository    
> git log : 기록된 커밋 로그 확인   
> git status : workspace 공간에 있는 작업물 확인   
   
   
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
