# 3. Git 
   
![Image](https://github.com/user-attachments/assets/cd0df8c2-2d74-499b-978b-fe247d01e73e)

Git에는 크게 4가지의 작업 공간이 있다.    
   
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
