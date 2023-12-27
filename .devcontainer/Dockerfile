FROM mcr.microsoft.com/devcontainers/python:3.9

RUN apt-get update
RUN	apt-get --yes install libcairo2-dev rabbitmq-server
RUN	mkdir --parents /usr/local/var/postgres
RUN chown vscode:vscode /usr/local/var/postgres
