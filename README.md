# 🗃️ Org Structure API

API для управления организационной структурой компании: подразделениями и сотрудниками с поддержкой древовидной иерархии департаментов.

---

# 🎯 Описание проекта

Система позволяет:

- создавать подразделения (Department)
- строить иерархическое дерево подразделений
- создавать сотрудников внутри подразделений
- перемещать подразделения в дереве
- удалять подразделения (cascade / reassignment)
- получать структуру с сотрудниками и вложенными подразделениями
---

# 🏛️ Архитектура
📜 Принципы:
- Clean Architecture (DDD-light)
- строгая слоистость (domain / infrastructure / interfaces)
- dependency inversion через Protocol
- бизнес-логика изолирована от БД и интерфейса
- "тонкий" HTTP слой
- транзакции управляются инфраструктурой

⚖️ Компромиссы:
- ORM-модели используются как доменные сущности
- `➖` домен зависит от ORM
- `➕` не нужен маппинг `domain entities` <--> `ORM-модели`
- ✅ допустимое упрощение:    
    - основной функционал - CRUD
    - нет переходов между состояниями
---

# 🩻 Структура проекта

```
src/org_struct/
│
├── domain/  # <------------------ БИЗНЕС-ЛОГИКА
│   ├── errors.py                  # доменные исключения
│   ├── models.py                  # ORM-модели (доменные сущности)
│   ├── repo_interface.py          # протоколы репозиториев   
│   └── services.py                # защита инвариантов, функционал
│
│
├── infrastructure/  # <---------- БД И ORM 
│   └── db/                        
│       ├── repositories.py        # реализация репозиториев
│       └── sqlalchemy_session.py  # ORM-сессия
│
│
├── interfaces/  # <-------------- HTTP API (FastAPI)
│   └── http_api/
│       ├── dependencies.py        # DI (session, repositories)
│       ├── exceptions.py          # маппинг ошибок в HTTP ответы
│       └── routes.py              # FastAPI эндпоинты
│
│
└── shared/  # <------------------ DTO, enums, validators
    ├── enums.py
    ├── request_dtos.py
    ├── response_dtos.py
    └── validators.py
```

---

# 🛠️ Технологии
- Python 3.13.5
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- Docker / docker-compose

---

# 🐳 Запуск проекта

```bash
docker compose up --build
```
✅  Миграции выполняются автоматически при запуске приложения  
⚠️  Нужен файл `.env` с переменными окружения (образец в репозитории) 