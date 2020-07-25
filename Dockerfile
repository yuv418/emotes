FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY . /app
RUN pip install -r /app/requirements.txt
RUN apt update -y && apt install mysql-client -y
