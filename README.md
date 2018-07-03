[![Maintainability](https://api.codeclimate.com/v1/badges/04db8a89d03f899cb0c5/maintainability)](https://codeclimate.com/github/CodeTheChangeUBC/reBOOT/maintainability)   [![Test Coverage](https://api.codeclimate.com/v1/badges/04db8a89d03f899cb0c5/test_coverage)](https://codeclimate.com/github/CodeTheChangeUBC/reBOOT/test_coverage)
# reBOOT
Welcome to the reBOOT Canada database project, created by Code the Change UBC! This is the development repository for the project. The project entails developing a database web application with the ability to generate CRA-compliant tax receipts.

The main functionalities:

1. Data storage
2. CRA-compliant tax receipt generation
3. Data analytics tool
4. User permission control

## Tech/Frameworks

- **Front-End:** HTML5, CSS3, jQuery3/JavaScript
- **Back-End:** Python `2.7.x`, Django `1.11.x`
- **Database:** PostgreSQL on Heroku

## Humans

#### Lead Developers

- **Seung Won [Tom] Lee** - @leesw98 - Team Lead, Full-stack

#### Developers

- **Omar Tsai** - @omar2535 - Developer, Front-End + Back-End
- **Michelle Huh** - @michellehuh - Developer,Front-End + Back-End
- **Vincent Lin** - @Csignore - Developer, Back-End + DB
- **Gaurav Vasudev** - @gauravnv - Developer, Back-End + DB
- **David Kim** - @yuubd - Developer, Back-End + Front-End
- **Joon Hur** - @hurjun1995 - Developer, Back-End + Front-End

# Installation

## 1) Installing Environment

- Install the required python version 2.7.x
- Install `pip` according to your OS
- Install _virtualenv_ using `pip install virtualenv`
- Install _virtualenvwrapper_ using `pip install virtualenvwrapper-win` for Windows and `pip install virtualenvwrapper` otherwise
- Create virtualenv and use `workon env_name` command to activate the virtualenv
  - Check out a tutorial if you're unsure

## 2) Getting the project

Clone the repo:

- **HTTPS** `git clone https://github.com/CodeTheChangeUBC/ReBOOT.git`
- **SSH** `ssh git@github.com:CodeTheChangeUBC/ReBOOT.git`

Install Requirements:

- `cd project_directory`
- `pip install -r requirements.txt`
- Install postgres through the GUI installer: https://www.postgresql.org/download/
- Install rabbitmq: https://www.rabbitmq.com/download.html

## Contributing
Coding contributions are to be made by members of **Code the Change UBC** only.

When making a **contribution**, make sure to do the following:

1. Assign yourself to an issue
2. **Make sure** you `git pull` the latest changes to the master branch
3. Checkout a new branch `git checkout -b [name_of_your_new_branch]` to commit your changes to
4. Make (and test!) your changes.
5. `git commit -m "ADD A DESCRIPTION OF YOUR CHANGES"` to commit your changes to the branch
6. `git push origin [name_of_your_branch]` to push your changes to the repo
7. Create a **Pull Request** into the master branch
8. After approval from **at least one** supervisor (**@leesw98** or **@michellehuh** or **@gauravnv**) merge branch into master.

## Running the server and website

To use the website, you need to run the server using this command in terminal after activating virtualenv:

`cd project_directory`

```bash
python manage.py runserver
```

To use different databases, you can use the following command:

```bash
DJANGO_DATABASE=[insert_db_name] ./manage.py [COMMAND]
```

To be able parse data from csv files, you also need to run the rabbitmq server from terminal using this command:

```bash
celery -A reboot worker -l info
```

The command allows us to use multiple workers to run tasks.

## Git Hook

`cp hooks/* .git/hooks/`

## Found a Bug?

To provide **suggestions** or **report bugs**, open an **issue** first to discuss potential changes/additions.


## Contacts

#### Code the Change UBC

- Homepage: https://codethechangeubc.org/
- Email: codethechangeubc@gmail.com
- Facebook: https://www.facebook.com/codethechangeubc/

_README.md file has been imported and modified from the Represent the 10 project. Originally by @EWaterman_
