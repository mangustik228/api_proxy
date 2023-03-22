# Proxy-api

Мини-приложение для хранения, получения проплаченных прокси

---

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

--- 

### Миграции 
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
    sqlalchemy.url = sqlite:///./database/db.sqlite
    ```
    если использовать `sqlite:////...` - будет абсолютный путь
    
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
   
    Необходимо изменить sqlalchemy.url там от куда он подсасываеться для create_engine()... В нашем случае `config/config.ini`:
    ```bash
    sqlite+driver:///database/db.sqlite
    ```
    `+driver` - драйвер гуглиться, какой хочеться поставить и ставиться через `pip`. Например для sqlite3 `aiosqlite`  
  
    **Примечение:**  
    - Если мы не ставим драйвер рекомендуемый синхронным SQLAlchemy, то на пример postgresql в файле `alembic.ini` надо поставить указать: 
        ```bash 
        postgresql+driver:/......?async_fallback=True
        ```
    - Здесь `?async_fallback=True` дописываем, потому что `alembic` не предназначен для асинхронки(только в config.ini, если мы снесли драйвер родной.)

---


## .env 
Необходимо создать в корне файл `.env` и внести token, который мы будем посылать для проверки мы это или не мы.
```bash
token=000000000
```

---

## Деплой

### Nginx
Создаем конфигурационный файл для приложения:
```bash
sudo nano /etc/nginx/sites-available/app_proxy
```

Добавляем в `app_proxy` следующее

```bash 
server {
    listen 80;
    server_name subdomen.example.com;

    location / {
        proxy_pass http://127.0.0.1:8033;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
``` 

Создаем символическую ссылку:

```bash
sudo ln -s /etc/nginx/sites-available/app_proxy /etc/nginx/sites-enabled/
```

Проверяем на ошибки:

```bash
sudo nginx -t
```

Перезапускаем nginx: 
```
sudo systemctl restart nginx
```

### Запуск приложения 

Сначала выполняем пункт по миграциям!

```bash
gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker -b :8033 --pythonpath /path/to/your/virtualenv/bin/python
```

создаем файл с приложением:

```bash 
sudo nano /etc/systemd/system/app_proxy.service
```

Прописываем:  

```bash 
[Unit]
Description=Binance unicorn server

[Service]
User=your_user 
WorkingDirectory=/path/to/your/app
Environment=token=your_token
ExecStart=/path/to/your/interpretator/venv/bin/gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8033        
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=app_proxy

[Install]
WantedBy=multi-user.target
```
**Примечание**  
-w 1 - Кол-во воркеров. Т.к. буду пользоваться 1, от силы еще коллега: то прописываю 1.   
--bind 0.0.0.0:8033 порт можно указать другой, даже иногда нужно, если уже занят  
  

Перезапускаем демона: 
```bash 
sudo systemctl daemon-reload
sudo systemctl start app_proxy.service
sudo systemctl enable app_proxy.service
```

Проверяем
```bash 
sudo systemctl status app_proxy.service
```


---
p.s. можно было написать одним файлом, без асинхронки и кучи всего.  
Проект больше учебный и основная цель: посмотреть как работает `SQLAlchemy`

---

created: 2023-03-21 00:15  
author: Vasiliy_mangust228  
email: <a href="mailto:bacek.mangust@gmail.com">bacek.mangust@gmail.com</a>  
tg: https://t.me/mangusik228  


            