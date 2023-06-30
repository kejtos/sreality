FROM python:3.10-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY create_database.sql /docker-entrypoint-initdb.d/
COPY . .

ENV DB_HOST=database
ENV DB_PORT=5432
ENV DB_NAME=sreality
ENV DB_USER=luxonis
ENV DB_PASSWORD=luxonis1

EXPOSE 8080

CMD sleep 5 && \
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 || PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;" && \
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1 || PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" && \
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" && \
    scrapy crawl sreality && \
    python http_server/http_server.py