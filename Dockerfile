FROM tiangolo/uwsgi-nginx-flask:python3.6

# setting up the environment
COPY . /app
WORKDIR /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
EXPOSE 443