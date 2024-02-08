SHELL=./make-venv
export RABBITMQ_CONFIG_FILE=rabbitmq.conf

all: env static server

# List all commands
.PHONY: ls
ls:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

.PHONY: shell
shell:
	python3 manage.py shell

.PHONY: heroku
heroku:
	heroku local

.PHONY: install
install:
	pip install -r requirements.txt
	make migrate
	make groups
	make static

.PHONY: install-dev
install-dev:
	pip install -r requirements-dev.txt

.PHONY: static
static:
	python3 manage.py collectstatic -c --no-input

.PHONY: server
server:
	python3 manage.py runserver

.PHONY: env
env:
	sh scripts/start_db.sh
	sh scripts/create_db.sh
ifeq ($(USER),vscode)
	sudo rabbitmq-server -detached
else
	rabbitmq-server -detached
endif
	@echo "RabbitMQ Status: Online"

.PHONY: env-python
env-python:
	python3 -m venv venv
	pip install -U pip

.PHONY: stopenv
stopenv:
ifeq ($(USER),vscode)
	sudo rabbitmqctl stop --idempotent
else
	rabbitmqctl stop --idempotent
endif
	@echo "RabbitMQ Status: Offline"
	sh scripts/stop_db.sh

.PHONY: migrate
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

.PHONY: celery
celery:
	CELERY_TRACE_APP=1 celery --app reboot worker --without-heartbeat --without-gossip --without-mingle

.PHONY: clean
clean:
	rm -rf venv
	rm -rf staticfiles

.PHONY: groups
groups:
	python3 manage.py creategroups

.PHONY: codespace
codespace:
	find /usr/local/var/postgres -maxdepth 0 -empty -exec initdb {} \;
	sudo cp ./rabbitmq-devcontainer.conf /etc/rabbitmq/rabbitmq.conf
	make .env
	make .git/hooks/pre-commit
	make env
	make env-python
	make install
	make install-dev
	nohup bash -c 'make celery &'

.PHONY: test
test:
	coverage run --source=./app ./manage.py test

.PHONY: coverage
coverage:
	coverage report --sort=miss --show-missing

.PHONY: format-check
format-check:
	autopep8 --diff --recursive --aggressive --aggressive --exit-code ./app ./reboot

.PHONY: format-fix
format-fix:
	autopep8 --in-place --recursive --aggressive --aggressive ./app ./reboot

.PHONY: lint-check
lint-check:
	ruff check --unsafe-fixes ./app ./reboot

.PHONY: lint-fix
lint-fix:
	ruff check --fix --unsafe-fixes ./app ./reboot

.env:
	cp .env.sample .env

.git/hooks/pre-commit:
	cp hooks/pre-commit .git/hooks/pre-commit
