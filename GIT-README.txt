git add .                   : stage files
git commit -m 'comment'     : commit
git branch <branch>         : create new branch
git checkout <branch>       : change branch
git merge <branch>          : merge branch into current branch
git branch -d <branch>      : delete branch
git log                     : list commits
git branch                  : list branches
git push -u origin <branch> : push to remote repository

# pull remote branches when they don't exist locally
git fetch origin
git checkout --track origin/<branch>

# to determine value of origin:
git remote -v

# reset username and password on local repository, first determine current value of origin and then:
git remote set-url origin https://<username>:<password>@github.com/seddon-software/raspberry-pi.git

