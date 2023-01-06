# "Feedback Service API" - сервис отзывов на произведения: "Книги", "Фильмы", "Музыка".
[![Testing API: PEP8 and Pytest](https://github.com/wurikavich/feedback_service_api/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/wurikavich/feedback_service_api/actions/workflows/test.yml) 

## Описание
Проект **Feedback Service API** собирает **отзывы (Review)** пользователей на 
**произведения (Titles)**. 

Произведения делятся на **категории (Category)**: «Книги», «Фильмы», «Музыка». 
Список категорий может быть расширен администратором.

Произведению может быть присвоен **жанр (Genre)**.
Список жанров может быть расширен администратором.


Благодарные или возмущённые пользователи оставляют к произведениям текстовые
**отзывы (Review)** и ставят произведению оценку (от одного до десяти).
Из пользовательских оценок формируется усреднённая оценка произведения — 
**рейтинг**.
На одно произведение пользователь может оставить только один отзыв.

Сами произведения в **Feedback Service API** не хранятся, здесь нельзя 
посмотреть фильм или послушать музыку.

## Функционал
### Пользователи:
- Каждый пользователь имеет свою роль:
   - Анонимный пользователь
   - Аутентифицированный пользователь `(user)`
   - Модератор `(moderator) `
   - Администратор `(admin)`
- Получение данных своей учетной записи
- Получение данных пользователя
- Получение списка всех пользователей
- Регистрация нового пользователя
- Изменение данных своей учетной записи
- Изменение данных пользователя
- Получение токена авторизации
- Удаление пользователя

### Произведения:
- Получение информации о произведении
- Получить список всех публикаций
- Добавление произведения
- Частичное обновление информации о произведении
- Удаление произведения

### Категории:
- Получение списка всех категорий
- Добавление новой категории
- Удаление категории

### Жанры:
- Получение списка всех категорий
- Добавление жанра
- Удаление жанра

### Отзывы:
- Получение отзыва
- Получение списка всех отзывов к произведению
- Добавление нового отзыва
- Частичное обновление отзыва
- Удаление отзыва

### Комментарии:
- Получение комментария к отзыву
- Получение списка всех комментариев к отзыву
- Добавление комментария к отзыву
- Частичное обновление комментария к отзыву
- Удаление комментария к отзыву
 
## Настройка и запуск:
Для развертывания проекта необходимо установить и запустить [Docker](https://www.docker.com/products/docker-desktop/).

1. Клонируем репозиторий на локальную машину:
   ```bash
   git clone git@github.com:wurikavich/feedback_service_api.git
   ```
   
2. В директории infra создаём файл .env, со следующими переменными:
   - Создаём файл:
      ```bash
      cd feedback_service_api\infra  # Переместились в директорию infra
      nano .env  # Создали и открыли файл .env
      ```
   - Прописываем переменное окружения в нём. [Сгенерируйте секретный ключ.](https://djecrety.ir/):
      ```bash
      POSTGRES_ENGINE=django.db.backends.postgresql  # указываем, что работаем с postgresql
      POSTGRES_DB=postgres  # имя базы данных (можете изменить)
      POSTGRES_USER=postgres  # логин для подключения к базе данных (можете изменить)
      POSTGRES_PASSWORD=postgres  # пароль для подключения к БД (можете изменить)
      POSTGRES_HOST=db  # название сервиса-контейнера
      POSTGRES_PORT=5432  # порт для подключения к БД
      SECRET_KEY=  # секретный ключ Django (вставьте сгенерированный ключ)
      DEBUG=  # Если необходимо показывать ошибки то прописываем параметр - True, иначе игнорируем
      ALLOWED_HOSTS=  # при развертывании локально необходимо указать - localhost 127.0.0.1 *
      ```
   - Сохраняем изменения в файле.

3. Запуск контейнеров Docker:
   - Из директории infra необходимо выполнить команду:
      ```bash
      docker-compose up -d --build
      ```
   - Ждем выполнение команды, при успешном выполнении, в терминале должны быть следующии строчки:
      ```bash
      Creating infra_db_1 ... done
      Creating infra_backend_1 ... done
      Creating infra_nginx_1   ... done
      ```

4. Запуск django проекта. Из директории infra, выполняем команды:
   - Создаём и применяем миграции:
      ```bash
      docker-compose exec backend python manage.py makemigrations
      docker-compose exec backend python manage.py migrate
      ```
   - Подключаем статику:
      ```bash
      docker-compose exec backend python manage.py collectstatic --no-input
      ```
   - Загружаем подготовленные данный в базу данных проекта:
      ```bash
      docker-compose exec backend python manage.py loaddata data/fixtures.json
      ```     
   - Создаём супер пользователя django:
      ```bash
      docker-compose exec backend python manage.py createsuperuser
      ```

Приведенные выше инструкции по установке и запуску проекта имеют только 
демонстрационную цель и могут быть использованы только на [localhost](http://localhost/). 

Документация, запустите сервер и перейдите по ссылке: [http://localhost/api/redoc/](http://localhost/api/redoc/).

Панель аднимистратора: [http://localhost/admin/](http://localhost/admin/). 

## Примеры запросов на эндпоинты
### Регистрация нового пользователя:
#### Запрос
```bash
POST - 'http://localhost/api/v1/auth/signup/'
{
    "email": "new_user@mail.ru",
    "username": "new_user"
}
```

#### Ответ
```bash
{
    "email": "new_user@mail.ru",
    "username": "new_user"
}
```

### Получение кода подтверждения:
Сервис отправляет письмо с кодом подтверждения.
Данный проект демонстрационный, письма сохраняются в контейнере "backend", директории "sent_emails"
   - Заходим в контейнер backend. Из директории infra, выполняем команды:
      ```bash
      docker container ls  # смотрим работающие контейнеры, нужен "infra_backend_1"
      docker exec -it <CONTAINER ID или CONTAINER NAMES> bash  # базовая команда для входа в контейнер
      docker exec -it infra_backend_1 bash  # итоговая команда, CONTAINER NAMES может изменятся
      root@7b27219ed6bb:/app#  # при успешном входе, видим такую строку
      ```
   - Получаем код подтверждения:
      ```bash
      cd sent_emails/  # перешли в папку sent_emails
      ls  # выполнив команду для просмотра файлов, увидим - (набор_цифр).log
      cat "Имя файла"  # просмотреть содержимое файла - "Имя файла"
        -----------------------------------------------------------------------
        Subject: Feedback Service - confirmation code.
        From: feedback_service@email.com
        To: new_user@mail.ru
        Date: Fri, 06 Jan 2023 17:14:08 -0000
        Message-ID: <167302524802.38.6271420070826620993@7b27219ed6bb>

        Добро пожаловать! Ваш код подтверждения: "value_confirmation_code".
        -----------------------------------------------------------------------
      ```

### Получение JWT-токена:
#### Запрос
```bash
POST - 'http://localhost/api/v1/auth/token/'
{
    "username": "new_user",
    "confirmation_code": "value_confirmation_code"
}
```

#### Ответ
```bash
{
    "token": "jwt_access_token"
}
```

### Получение данных своей учетной записи:
#### Запрос
```bash
GET - 'http://localhost/api/v1/users/me/'
header 'Authorization: Bearer "jwt_access_token"'
```

#### Ответ
```bash
{
    "username": "new_user",
    "email": "new_user@mail.ru",
    "first_name": "",
    "last_name": "",
    "bio": null,
    "role": "user"
}
```

## Стек технологий
#### Backend:
- Python 3.10
- Django 3.2.16
- Django REST Framework 3.14.0

#### Инфраструктура для запуска:
- Docker-compose
- Nginx
- Gunicorn
- PostgreSQL

## Разработчик
[Александр Гетманов](https://github.com/wurikavich)