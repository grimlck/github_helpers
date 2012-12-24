#github_helpers

Little helper scripts to talk to GitHub from the shell

##init_github_repo.py
    
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

##list_github_repos.py
    
    usage: list_github_repos.py [-h] [-n number] username

    List GitHub repositories by user

    positional arguments:
    username    GitHub username

    optional arguments:
    -h, --help  show this help message and exit
    -n number   Show only first n repositories
