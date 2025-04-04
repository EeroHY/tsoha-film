FROM postgres:bullseye as base
ENV POSTGRES_DB tsoha_db
COPY schema.sql /docker-entrypoint-initdb.d/
