FROM ruby:2.7.2-alpine3.12

COPY . /app
WORKDIR /app

RUN apk add --update build-base sqlite-dev mariadb-dev nodejs postgresql-dev zlib-dev jpeg-dev imagemagick

RUN bundle install --deployment --without development test
