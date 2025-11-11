# Library Management System API

REST API для управления библиотекой с полным CRUD, отчетами и бизнес-правилами.


## Быстрый старт
```bash
git clone https://github.com/demented10/restful_library_new.git

docker-compose up -d --build
```

## Генерация тестовых данных

```bash
docker-compose exec api python utils/generate_fixtures.py
```

## Документация
```
http://localhost:8000/docs
```

## Возможности

- CRUD для книг, издательств, читателей и выдач
- Бизнес правила - максимум 5 книг на читателя, срок возврата 20 дней
- Отчет в CSV/XLSX формате с генераторами

## Архитектура
```
app/
├── api/           # FastAPI роуты
├── core/          # Конфигурация и БД
├── models/        # SQLalchemy модели
├── repositories/  # Доступ к данным
├── schemas/       # Pydantic схемы
└── services/      # Бизнес логика
```
Визуализация архитектуры находится в файле Architecture.drawio


