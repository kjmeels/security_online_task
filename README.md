# Security_Online_Task
API по управлению задачами внутри компании

## ENVs:
```
SITE_HOST=localhost
SECRET_KEY=my_secret_key
DEBUG=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

## Third party packages:
```
rest_framework
drf_spectacular
"phonenumber_field",
"rest_framework_simplejwt",
```

### Локальный запуск проекта 
```shell
docker compose build
docker compose up
```

| Доступ  | Ссылка                          |
|---------|---------------------------------|
| Админка | http://127.0.0.1:8000/admin/    |
| Сваггер | http://127.0.0.1:8000/api/docs/ |
