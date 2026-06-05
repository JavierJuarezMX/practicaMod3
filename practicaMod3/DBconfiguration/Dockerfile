FROM postgres:latest
COPY init.sql /docker-entrypoint-initdb.d/01_init.sql
COPY save.data.sql /docker-entrypoint-initdb.d/02_save_data.sql