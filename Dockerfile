FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# set the new working directory
WORKDIR /var/www/repository_tracker_api
COPY . /var/www/repository_tracker_api

# install dependencies
RUN pip install -r requirements.txt

# set up necessary environment variablers
ENV API_VERSION='1.0.0'

EXPOSE 80:80