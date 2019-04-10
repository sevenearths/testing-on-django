FROM ubuntu:latest

# Timezone
RUN /bin/bash -c "export TZ=Europe/London"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# System
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
	python3-dev \
	python3-venv \
	python3-pip \
	libpq-dev \
	postgresql \
	postgresql-contrib \
	nginx

# Python Stuff
RUN pip3 install gunicorn django djangorestframework psycopg2

# New User
#USER root
#RUN useradd -ms /bin/bash switch-user
#USER switch-user
#WORKDIR /home/switch-user
#
#COPY switch /home/switch-user/switch/

# WORKDIR /home/switch-user/switch
## RUN python3 switch/manage.py runserver

# ENTRYPOINT ["bash"]
## ENTRYPOINT ["python3", "switch/manage.py", "test"]
