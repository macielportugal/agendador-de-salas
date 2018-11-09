FROM python:3.6-alpine
RUN mkdir -p project \
    && apk add --update --no-cache musl-dev python3-dev postgresql-dev jpeg-dev gettext zlib-dev g++ gcc libxslt-dev \
    && rm -rf /var/cache/apk/*
WORKDIR /project
COPY ./requirements.txt /
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
RUN python -m pip install --no-cache-dir -r /requirements.txt
ENTRYPOINT ["/docker-entrypoint.sh"]