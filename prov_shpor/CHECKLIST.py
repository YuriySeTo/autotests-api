"""

# Чек-лист: Создание нового API-клиента

## Шаг 1: Подготовка
- [ ] Открыть Swagger: `http://localhost:8000/docs`
- [ ] Найти нужный раздел (например, `/api/v1/users`)
- [ ] Выписать все эндпоинты раздела (GET, POST, PATCH, DELETE)

## Шаг 2: Для каждого эндпоинта — выписать из Swagger
- [ ] URL (например, `/api/v1/users/{user_id}`)
- [ ] HTTP-метод (GET/POST/PATCH/DELETE)
- [ ] `In` в Parameters:
  - [ ] `(path)` → f-строка
  - [ ] `(query)` → `params=query`
  - [ ] нет → без параметров
- [ ] Request body (какие поля, какие типы)
- [ ] Response (какие поля, какой верхний ключ: `user` / `users`)

## Шаг 3: Создать файл клиента
- [ ] Путь: `clients/<раздел>/<раздел>_client.py`
- [ ] Создать `__init__.py` в папке `<раздел>`

## Шаг 4: Написать TypedDict — запросы
- [ ] `CreateXxxRequestDict` — поля из Request body
- [ ] `UpdateXxxRequestDict` — поля с `| None`
- [ ] `GetXxxQueryDict` — только если есть query

## Шаг 5: Написать TypedDict — сущность
- [ ] `Xxx` — поля из Response (без `password`, с `id`)

## Шаг 6: Написать TypedDict — ответы
- [ ] `GetXxxResponseDict` — `xxx: Xxx`
- [ ] `GetXxxsResponseDict` — `xxxs: list[Xxx]` (если список)
- [ ] `CreateXxxResponseDict` — `xxx: Xxx`
- [ ] `UpdateXxxResponseDict` — `xxx: Xxx`

## Шаг 7: Написать класс клиента
- [ ] `class XxxClient(APIClient):`
- [ ] Методы `*_api`:
  - [ ] `get_xxx_api` (f-строка для path)
  - [ ] `get_xxxs_api` (params=query, если есть)
  - [ ] `create_xxx_api` (json=request)
  - [ ] `update_xxx_api` (f-строка + json=request)
  - [ ] `delete_xxx_api` (f-строка)
  - [ ] Все возвращают `Response`
- [ ] Методы без `_api`:
  - [ ] Вызывают `*_api`
  - [ ] Возвращают `response.json()`
  - [ ] Тип возврата — `XxxResponseDict`

## Шаг 8: Написать Builder
- [ ] `def get_xxx_client(user: AuthenticationUserDict) -> XxxClient:`
- [ ] `return XxxClient(client=get_private_http_client(user))`

## Шаг 9: Проверить (чек-лист ошибок)
- [ ] Все URL начинаются с `/api/v1/<раздел>`?
- [ ] Все имена `TypedDict` переименованы?
- [ ] Поля в `TypedDict` — из Swagger?
- [ ] Имя класса — новое?
- [ ] Builder возвращает новый класс?
- [ ] Docstring — про новый раздел?
- [ ] `params` / f-строки — по Swagger?
- [ ] `user` vs `users` — по Swagger?
- [ ] Нет дубликатов классов?
- [ ] `User` без `password`, с `id`?

## Шаг 10: Проверить через скрипт
- [ ] Написать скрипт `api_client_xxx.py`
- [ ] Запустить: `python -m api_client_xxx`
- [ ] Все запросы прошли успешно?

## Шаг 11: Залить на GitHub
- [ ] `git add .`
- [ ] `git commit -m "..."`
- [ ] `git push`

"""