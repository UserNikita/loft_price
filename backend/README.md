# Запуск

1. Сначала запускаем MongoDB. Для этого нужно запустить docker compose

```bash
docker compose up -d --build
```

2. Запускаем aiohttp приложение

```bash
adev runserver . --no-livereload
```


Открыть сваггер http://localhost:8000/api/docs

Открыть редактор данных http://localhost:8081/

