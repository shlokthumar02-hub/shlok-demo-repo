# shlok-demo-repo
1)Get this below command from https://git-scm.com/install/windows to install git software on windows
	winget install --id Git.Git -e --source winget
2) Create a Directory for your source code
	mkdir demoapp
3) CD into your code dir 
	cd demoapp
4) You should now see C:\Users\shlok\demoapp>
5) Initialize Git 
	git init
6) Create any txt file in the folder
	code.txt
7) Check status of your repo
	git status
8) Add the file above to git for tracking versions (. will add all filed to be track by git)
	git add . 

9) Configure your global env ( Done once per system)
  git config --global user.email "shlokthumar02@gmail.com"
  git config --global user.name "Shlok"

10) Commit your code to git with a comment
 git commit -am "my first version"
11) By Default you will get a master/main branch
12) Create a dev branch for your work( Most developers create there dev branch and work on it and later merge the code back to master/main
git checkout -b shloks-dev
