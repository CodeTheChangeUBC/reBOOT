all: env static heroku

# List all commands
.PHONY: ls
ls:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

.PHONY: shell
shell:
	python manage.py shell

.PHONY: heroku
heroku:
	heroku local

.PHONY: setup
setup:
	sh scripts/start_db.sh
	sh scripts/create_db.sh
	virtualenv venv
	( \
		source venv/bin/activate; \
    	pip install -r requirements.txt; \
    )
	make migrate
	make static
	sh scripts/stop_db.sh

.PHONY: static
static:
	python manage.py collectstatic --no-input

.PHONY: server
server:
	python manage.py runserver

.PHONY: env
env:
	sh scripts/start_db.sh
	rabbitmq-server -detached
	@echo "RabbitMQ Status: Online"

.PHONY: exit
exit:
	rabbitmqctl stop
	@echo "RabbitMQ Status: Offline"
	sh scripts/stop_db.sh

.PHONY: migrate
migrate:
	python manage.py migrate
