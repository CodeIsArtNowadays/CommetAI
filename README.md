# Автоматическая система управления проектами
<br>
Backend-приложение для автоматической планировки разработки проектов, через подключенный github репозиторий.

Каждый push, полученный от подключенного проекта, обрабатывается AI сервисом для суммаризации комитов и создания задач.

## Демо
// VIDEO 

## Стек используемых технологий:

- python
- FastAPI w/ sqlalchemy, pydantic
- OpenAI
- github API
- postgresql
- redis
- docker

## Запуск локально не предусмотрен в связи с интеграцией Github app

## Архитектура

Проект разбит на логические приложения, используется роут-сервис-репозиторий подход для разделения обработки запросов - бизнес логики - работы с бд.
Каждому приложению соотвествуют свои модели, роуты (при необходимости), схемы и сервис.

Основная логика обработки push событий вынесена в use case. 

Логика обработки запросов к AI вынесена в отдельное приложение и может быть переиспользована, за исключением промптов (prompts.py)

## Структура проекта 

```
backend/
|-- config.py
|-- main.py
`-- src
    |-- ai
    |   |-- dependencies.py
    |   |-- prompts.py
    |   |-- routes.py
    |   `-- service.py
    |-- auth
    |   |-- dependencies.py
    |   |-- exceptions.py
    |   |-- models.py
    |   |-- repository.py
    |   |-- router.py
    |   |-- schemas.py
    |   `-- service.py
    |-- board
    |   |-- dependencies.py
    |   |-- models.py
    |   |-- process_push.py
    |   |-- project_service.py
    |   |-- repository.py
    |   |-- router.py
    |   |-- schemas.py
    |   `-- webhook_service.py
    `-- core
        |-- database.py
        |-- dependencies.py
        |-- exceptions.py
        |-- middleware.py
        `-- mock.py
```

## План на дальнейшее развитие

- Деплой ✅
- Добавления функционала групп
- Усиление обработки не success pipeline
