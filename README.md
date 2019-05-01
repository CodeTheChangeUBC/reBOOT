<h1 align="center">
  reBOOT
</h1>

<p align="center">
  Donation Management Platform for reBOOT Canada!
</p>


<p align="center">
  <a href="https://codeclimate.com/github/CodeTheChangeUBC/reBOOT/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/04db8a89d03f899cb0c5/maintainability"
      alt="Code Climate Maintainability" />
  </a>
  <a href="https://codeclimate.com/github/CodeTheChangeUBC/reBOOT/test_coverage">
    <img src="https://api.codeclimate.com/v1/badges/04db8a89d03f899cb0c5/test_coverage"
      alt="Code Climate Test Coverage" />
  </a>
</p>
<br>

<p align="center">
  <a href="#family-team"><strong>Team</strong></a> ·
  <a href="#zap-setup"><strong>Setup</strong></a> ·
  <a href="#package-usage"><strong>Usage</strong></a> ·
  <a href="#santa-contributing"><strong>Contributing</strong></a> ·
  <a href="https://github.com/CodeTheChangeUBC/reBOOT/wiki"><strong>Wiki</strong></a>
</p>

Welcome to the reBOOT Canada database project, created by Code the Change UBC! This is the development repository for the project. The project entails developing a database web application with the ability to generate CRA-compliant tax receipts.

|   | Main Features  |
----|-----------------
🚀  | **Simple to use** - focus on your work with the simple and intuitive UI
📦  | **Data storage** - easily add/view/change/delete donor and donation data without worrying about security
🍰  | **Data analytics** - analyze your donation data with useful charts and statitics
🛂  | **User permission controls** - control incremental permissions for managing teams and users
🏷  | **CRA-compliant tax receipts** - generate CRA-compliant tax receipts that provides full detail about donations
👥  | **Built for teams** - provides tools to control team management for volunteers and employees
✉️  | **Email Alerts** - receive detail alert emails about the system if there are any errors
🔑  | **Secure** - secured with HTTPS across the board, as well as features like XSS, CSRF protection

# :family: Team

- **Seung Won [Tom] Lee** - [@leesw98](https://github.com/leesw98) - Team Lead, Full-stack
- **Omar Tsai** - [@omar2535](https://github.com/omar2535) - Developer, Front-End + Back-End
- **Michelle Huh** - [@michellehuh](https://github.com/michellehuh) - Developer, Front-End + Back-End
- **Vincent Lin** - [@Csignore](https://github.com/Csignore) - Developer, Back-End + DB
- **Gaurav Vasudev** - [@gauravnv](https://github.com/gauravnv) - Developer, Back-End + DB
- **David Kim** - [@yuubd](https://github.com/yuubd) - Developer, Back-End + Front-End
- **Joon Hur** - [@hurjun1995](https://github.com/hurjun1995) - Developer, Back-End + Front-End

# :zap: Setup

## 0) Check/Install prereq dependencies

- Install `python==2.7.x`. _Note: macOS defaultly installs python==2.7_
- Check for `pip` in your terminal
- Check for `virtualenv` in your terminal
- Install `postgres` preferable using the command line
- Install rabbitmq: https://www.rabbitmq.com/download.html

## 1) Getting the project

Clone the repo:

- **HTTPS** `git clone https://github.com/CodeTheChangeUBC/reBOOT.git`
- **SSH** `ssh git@github.com:CodeTheChangeUBC/ReBOOT.git`

## 2) Configuring database, job queue, and server dependencies

``` bash
$ cp .env.sample .env
$ make install
```

_Note: You might want to add `127.0.0.1` or `localhost` to `ALLOWED_HOSTS` and set `DEBUG` to `True` if you are running the project locally_

## 3) Running the server
```bash
$ source venv/bin/activate
$ make env
$ make server
```

# :package: Usage

## Running the server and website

To use the website, you need to run the server using this command in terminal after **activating virtualenv**:

```bash
$ source venv/bin/activate
$ make env
$ make server
```

To use different databases, you can use the following command:

```bash
DJANGO_DATABASE=[insert_db_name] ./manage.py [COMMAND]
```

To be able parse data from csv files or generate tax receipts, you also need to run the celery/rabbitmq server from separate terminal instance using this command:

```bash
$ make celery
```

## Git Hooks

`cp hooks/* .git/hooks/`

# :santa: Contributing

When making a **contribution**, make sure to do the following:

1. Assign yourself to an issue
2. **Make sure** you `git pull` the latest changes to the master branch
3. Checkout a new branch `git checkout -b [name_of_your_new_branch]` to commit your changes to
4. Make (and test!) your changes.
5. `git commit -m "ADD A DESCRIPTION OF YOUR CHANGES"` to commit your changes to the branch
6. `git push origin [name_of_your_branch]` to push your changes to the repo
7. Create a **Pull Request** into the master branch
8. After approval from **at least one** supervisor (**@leesw98** or **@michellehuh** or **@gauravnv**) merge branch into master.

## Found a Bug?

To provide **suggestions** or **report bugs**, open an **issue** first to discuss potential changes/additions.

# :bell: Contacts

Homepage: https://codethechangeubc.org/

Email: codethechangeubc@gmail.com

Facebook: https://www.facebook.com/codethechangeubc/

_This README has been strongly inspired by [UBC Launch Pad's Inertia project](https://github.com/ubclaunchpad/inertia). Originally by a good friend [@bobheadxi](https://github.com/bobheadxi). As [@bobheadxi](https://github.com/bobheadxi) would say, please star the [inertia project](https://github.com/ubclaunchpad/inertia)._
