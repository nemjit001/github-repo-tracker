FROM tiangolo/uwsgi-nginx-flask:python3.6

# setting up the environment
COPY . /app
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# set up necessary environment variablers
ENV API_VERSION='1.0.0'

EXPOSE 80:80