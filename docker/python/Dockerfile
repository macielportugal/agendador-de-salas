FROM python:3.6-alpine
RUN mkdir -p project \
    && apk add --update --no-cache musl-dev bash python3-dev postgresql-dev jpeg-dev gettext zlib-dev g++ gcc libxslt-dev \
    && rm -rf /var/cache/apk/*
WORKDIR /project/app
COPY ./requirements.txt /
COPY ./docker-entrypoint.sh /
COPY ./wait-for-it.sh /
RUN chmod +x /docker-entrypoint.sh
RUN chmod +x /wait-for-it.sh
RUN python -m pip install --no-cache-dir -r /requirements.txt
ENTRYPOINT ["/docker-entrypoint.sh"]