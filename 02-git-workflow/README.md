# Exercise 2 (slide 26): Git mini exercise

**Statement:** [gist: git_practice.md](https://gist.github.com/bdallard/8bdbdd70f234f94823c0c2cde9515388)

- This README: the commands and answers for the 11 parts and the reflection questions
- [`install.sh`](install.sh): the bash script from Part 7
- [`bash-installer/`](bash-installer/): the small project from Part 11

---

## Part 1: setup & config

```bash
git --version
git config --global user.name "Sam"
git config --global user.email "my-email@example.com"
git config --list            # check
```

## Part 2: first repository

```bash
mkdir my-first-repo
cd my-first-repo
git init
touch readme.txt
```

## Part 3: first commit

| Question | Command |
| --- | --- |
| Current state of the repository | `git status` |
| Stage `readme.txt` | `git add readme.txt` |
| Commit with a message | `git commit -m "Add readme file"` |
| Commit history | `git log` |

## Part 4: make changes

```bash
echo "My first line" >> readme.txt
git status
```

`git status` now lists `readme.txt` under **"Changes not staged for commit"**: Git knows the file changed since the last commit, but the change is not in the staging area yet.

```bash
git add readme.txt
git commit -m "Add first line to readme"
```

There are now **2 commits** (`git log --oneline` shows them).

## Part 5: exploration

| Command | What it does |
| --- | --- |
| `git diff` | Shows line by line what changed in files that are **not staged yet** (`+` added, `-` removed). `git diff --staged` does the same for staged changes. |
| `git log --oneline` | The history, one commit per line: short hash + message. |

## Part 6: branches

| Question | Command |
| --- | --- |
| List all branches | `git branch` |
| Create `feature-script` | `git branch feature-script` |
| Switch to it | `git switch feature-script` (or `git checkout feature-script`) |
| Create and switch to `dev` in one command | `git switch -c dev` (or `git checkout -b dev`) |
| Back to `feature-script` | `git switch feature-script` |
| Check the current branch | `git branch` (the `*` marks it) or `git status` |

## Part 7: a bash script on a branch

```bash
git switch feature-script
nano install.sh               # content: see install.sh in this folder
chmod +x install.sh
git add install.sh
git commit -m "Add install script"
git log --oneline
```

## Part 8: merge

```bash
git switch main
ls                            # install.sh is NOT here
```

**Why?** `install.sh` was committed on `feature-script` only. Each branch has its own version of the files, and `main` has not received that commit yet.

```bash
git merge feature-script
ls                            # install.sh is now here
git log --oneline             # the "Add install script" commit is now in main's history
git branch -d feature-script  # delete the branch after merging
```

Here the merge is a **fast-forward**: `main` had no new commits, so Git just moved `main` forward to the branch's last commit, without creating a merge commit.

## Part 9: push to GitHub

Create an empty repository `my-first-repo` on github.com (no README), then:

```bash
git remote add origin https://github.com/<user>/my-first-repo.git   # link
git push -u origin main                                             # push
```

Refreshing the GitHub page shows the files and the commit history.

## Part 10: delete and clone

```bash
cd ..
rm -rf my-first-repo                                      # delete the local folder
git clone https://github.com/<user>/my-first-repo.git    # get it back from GitHub
cd my-first-repo && ls                                    # files are all there
```

## Part 11: full workflow

```bash
mkdir bash-installer && cd bash-installer
git init
echo "# bash-installer" > README.md        # + a description
git add README.md && git commit -m "Add README"
git switch -c feature-install
cp ../install.sh .                          # the Part 7 script
git add install.sh && git commit -m "Add install script"
git switch main
git merge feature-install
git branch -d feature-install
git remote add origin https://github.com/<user>/bash-installer.git
git push -u origin main
```

The result is in [`bash-installer/`](bash-installer/).

---

## Reflection questions

**Why is version control useful?**
It keeps the full history of a project: you can see who changed what and when, go back to any previous version when something breaks, work with other people on the same files without overwriting each other, and keep a backup on a remote server.

**Difference between staging and committing?**
`git add` puts changes in the **staging area**: a draft of the next snapshot, where you choose exactly what goes in. `git commit` **saves** that draft permanently in the history with a message. Staging lets you commit only part of your changes.

**When should you commit?**
Each time you finish one small, logical change that works: a feature step, a bug fix. Commit small and often, so that if something breaks you know which change caused it.

**`git init` vs `git clone`?**
`git init` creates a **new, empty** repository in the current folder. `git clone` **copies an existing** repository (all files and history) from a remote, and links it to that remote automatically.

**Why write good commit messages?**
The history becomes readable: you (and your teammates) can find when and why something changed without opening every commit. "Fix null pointer in login handler" tells the story; "updates" tells nothing.

**What are branches for?**
To work on something (a feature, a fix, an experiment) on a separate line of development, without breaking the main code that others use. When it works, you merge it back.

**When to create a branch instead of working on main?**
Whenever the change is not trivial: a new feature, a bug fix that needs testing, an experiment you might throw away, or work in a team where `main` must stay stable (production-ready).
