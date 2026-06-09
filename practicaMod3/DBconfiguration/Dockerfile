FROM postgres:17
COPY init.sql /docker-entrypoint-initdb.d/01_init.sql
COPY save_data.sql /docker-entrypoint-initdb.d/02_save_data.sql
initdb.d/