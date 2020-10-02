FROM python:3-alpine
COPY . /emotes

RUN apk update && apk add build-base python3-dev jpeg-dev zlib-dev bash supervisor
 
RUN pip3 install -r /emotes/requirements.txt

CMD supervisord -c /emotes/supervisord.conf --loglevel=debug
