# fastapi-blog
```console
docker-compose up -d
```
## Setup MYSQL
```console
docker exec -it rabbitmq-python-project-mysql-1 /bin/sh
mysql -u root -p
GRANT ALL PRIVILEGES ON *.* TO 'test'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
CREATE DATABASE fastapi_blog;
use fastapi_blog;
```

## Migrations
At `alembic.ini` dir:
```console
alembic upgrade head
```

## Init Database
```consonle
python initial_data.py
```
    FIRST_SUPERUSER: EmailStr = "nguyenvanson@gapo.com.vn"
    FIRST_SUPERUSER_PASSWORD: str = "string11A"


## Create Topic KAFKA
Topic's name is views:
```console
docker compose exec broker \
  kafka-topics --create \
    --topic views \
    --bootstrap-server localhost:29092 \
    --replication-factor 1 \
    --partitions 1
```


## Run app
```console
pipenv run app
```