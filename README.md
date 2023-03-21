# Proxy-api
Мини-приложение для хранения, получения проплаченных прокси

## База данных

### Схема
- `id` id записи
- `create` Дата занесения в бд
- `server` Сервер, формат (`255.255.255.255`)
- `username` Логин для использования прокси
- `password` Пароль для использования прокси
- `port` Порт
- `expire` До какого числа действует прокси 
- `service` Ссылка на сервис, на котором покупались прокси


### Миграции (Памятка для себя)
1. Инициализируем `alembic

    ```bash
    alembic init migrations
    ```

1. В файле alembic.ini меняем:  
    ```python
    sqlalchemy.url = driver://user:pass@localhost/dbname  
    ```
    на  
    ```python
    sqlalchemy.url = sqlite:///database/sqlite.db
    ```

1. Если используем mysql/postgresql:  
    ```python
    sqlalchemy.url = mysql://%(DB_USER)s:%(DB_USER)s@%(DB_HOST)s/%(DB_NAME)s
    ```
    Чтоб передать данные в alembic.ini, необходимо добавить в файле `migrations/env.py`: 

        ```python
        from config import my_config

        # После объявления config = context.config
        section = config.config_ini_section
        config.set_section_option(section, "DB_HOST", my_config.db.host)
        config.set_section_option(section, "DB_PORT", my_config.db.port)
        config.set_section_option(section, "DB_NAME", my_config.db.name)
        config.set_section_option(section, "DB_USER", my_config.db.user)
        config.set_section_option(section, "DB_PASS", my_config.db.pass)
        ```
1. В файле `migrations/env.py`: 
    ```python

    # Импортируем главный класс от которого идет всё наследование
    from database.models import Base

    # Меняем целевые метаданные target_metadata = None на 
    target_metadata = Base.metadata

    ```

1. Делаем ревизию

    ```bash
    # Ревизия. Сверяет текущеее состоянии с состоянием моделей
    # -m Это коммит ревизии
    alembic revision --autogenerate -m "Commit"
    ```

1. Делаем миграцию
    ```bash
    # Делаем upgrade до версии
    alembic upgrade `fed8c4c3ddf7`

    # или до заключительной версии:
    alembic upgrade head
    ```

1. Использование асинхронного движка  
    Необходимо изменить sqlalchemy.url там где он встречаеться:
    ```bash
    sqlite+driver:///database/sqlite.db?async_fallback=True
    ```
- `+driver` - драйвер гуглиться, какой хочеться поставить и ставиться через `pip`. Например для sqlite3 `aiosqlite`
- `?async_fallback=True` дописываем, потому что `alembic` не предназначен для асинхронки


## .env 
Необходимо создать в корне файл `.env` и внести token, который мы будем посылать для проверки мы это или не мы.
```bash
token=000000000
```


---
p.s. можно было написать одним файлом, без асинхронки и кучи всего.  
Проект больше учебный и основная цель: посмотреть как работает `SQLAlchemy`

---

created: 2023-03-21 00:15  
author: Vasiliy_mangust228  
email: <a href="mailto:bacek.mangust@gmail.com">bacek.mangust@gmail.com</a>  
tg: https://t.me/mangusik228  
            