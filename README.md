# 🚀 Git Setup & Basic Workflow (Windows)

## 1. Install Git
Download Git from:  
👉 https://git-scm.com/install/windows  

Or install using **winget**:
```bash
winget install --id Git.Git -e --source winget
```

---

## 2. Create a Project Directory
```bash
mkdir demoapp
```

---

## 3. Navigate into Your Directory
```bash
cd demoapp
```

You should now see something like:
```
C:\Users\shlok\demoapp>
```

---

## 4. Initialize a Git Repository
```bash
git init
```

---

## 5. Create a File
Create any text file in the folder (example):
```
code.txt
```

---

## 6. Check Repository Status
```bash
git status
```

---

## 7. Add Files to Git Tracking
```bash
git add .
```
> ⚡ This adds **all files** in the directory to Git tracking.

---

## 8. Configure Git (One-Time Setup)
```bash
git config --global user.email "shlokthumar02@gmail.com"
git config --global user.name "Shlok"
```

---

## 9. Commit Your Changes
```bash
git commit -am "my first version"
```

---

## 10. Default Branch
- Git creates a default branch called:
  - `main` (modern)
  - or `master` (older setups)

---

## 11. Create a Development Branch
```bash
git checkout -b shloks-dev
```

> 💡 Best practice:  
> Developers usually work on a **dev branch**, then merge changes back into `main`.

---

## ✅ You’re Ready!
You now have a fully initialized Git repo with your first commit and a dev branch 🎉