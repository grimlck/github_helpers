github_helpers
==============

Little helper scripts to talk to GitHub from the shell

usage: init_github_repo.py [-h] -u Username [-p Password] -n Repository name
                           [-d Description] [-a] [-g Language or Platform]

Inititalize a Github repository

optional arguments:
  -h, --help                show this help message and exit
  -u Username               GitHub account name
  -p Password               GitHub account password
  -n Repository name        Name of the new GitHub repository
  -d Description            Description for the new repository
  -a                        Initialize repository with empty README.md
  -g Language or Platform   Initialize repository with .gitignore for the specified language (e.g.: Python)
