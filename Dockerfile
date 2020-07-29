FROM python:3-buster
COPY . /emotes

RUN apt update && apt install -y build-essential python3-dev
 
RUN pip3 install -r /emotes/requirements.txt

CMD /emotes/start.sh
