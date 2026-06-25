# Django_Docker

Простий HTTP-сервер на Python (стандартна бібліотека `http.server`), що реалізує CRUD API для користувачів. Запакований у Docker.

## API ендпоінти

| Метод | Шлях | Опис |
|-------|------|------|
| GET | `/users` | Отримати список усіх користувачів |
| GET | `/user/<username>` | Отримати користувача за `username` |
| GET | `/reset` | Скинути дані до початкового стану |
| POST | `/user` | Створити користувача |
| POST | `/user/createWithList` | Створити кількох користувачів зі списку |
| PUT | `/user/<id>` | Оновити користувача за `id` |
| DELETE | `/user/<id>` | Видалити користувача за `id` |

## Запуск у Docker

Потрібен встановлений [Docker](https://www.docker.com/).

```bash
# 1. Клонувати репозиторій
git clone https://github.com/POM-Django-Docker/ap-4755-Sam-uch.git
cd ap-4755-Sam-uch

# 2. Зібрати Docker-образ з Dockerfile
docker build -t sam-uch-app .

# 3. Запустити контейнер (порт 8000 прокинуто на хост)
docker run -d --name sam-uch-container -p 8000:8000 sam-uch-app

# 4. Перевірити, що сервер працює
curl http://localhost:8000/users
```

Сервер буде доступний за адресою `http://localhost:8000`.

### Зупинка та видалення контейнера

```bash
docker rm -f sam-uch-container
```

## Запуск без Docker (локально)

```bash
python main.py          # запуск на порту 8000 за замовчуванням
python main.py 5000     # запуск на вказаному порту
```

## Тести

```bash
pip install -r requirements.txt
python -m unittest tests.py
```
