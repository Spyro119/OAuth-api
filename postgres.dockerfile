FROM postgres:15.1-alpine

LABEL author="Jubinvilles"
LABEL description="OAuth manager Postgres Image"
LABEL version="1.0"

COPY *.sql /docker-entrypoint-initdb.d/