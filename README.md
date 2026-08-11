# SportStore

SportStore — учебный проект интернет-магазина, разработанный на Django в рамках курса по веб-разработке.

## Возможности

- Главная страница
- Страница контактов
- Bootstrap 5
- Маршрутизация Django
- Шаблоны с наследованием
- Каталог товаров и категорий
- Управление товарами и категориями через Django Admin
- Работа с PostgreSQL
- Загрузка тестовых данных через фикстуры и кастомную management-команду

## Технологии

- Python 3.13
- Django 6
- PostgreSQL
- Poetry
- Bootstrap 5
- Pillow
- psycopg2-binary

## Структура каталога

Основное приложение проекта — `catalog`.

В приложении реализованы:

- модель `Category` — категории товаров;
- модель `Product` — товары;
- связь товаров с категориями через `ForeignKey`;
- загрузка тестовых данных через JSON-фикстуры;
- кастомная команда для загрузки фикстур;
- настройка моделей в Django Admin.

## Переменные окружения

Для работы проекта необходимо создать файл `.env` в корневой директории проекта.

Пример необходимых переменных находится в файле `.env.example`.

В `.env` указываются:

- `SECRET_KEY` — секретный ключ Django;
- `DATABASE_NAME` — название базы данных PostgreSQL;
- `DATABASE_USER` — пользователь PostgreSQL;
- `DATABASE_PASSWORD` — пароль пользователя PostgreSQL;
- `DATABASE_HOST` — адрес сервера PostgreSQL;
- `DATABASE_PORT` — порт PostgreSQL.

Файл `.env` не должен добавляться в репозиторий.

## Запуск проекта

Установить зависимости:

```bash
poetry install
```
Выполнить миграции:

```bash
poetry run python manage.py migrate
```

Запустить сервер:

```bash
poetry run python manage.py runserver
```

После запуска проект доступен по адресу:

http://127.0.0.1:8000/

## Загрузка тестовых данных

Для загрузки тестовых категорий и продуктов используются фикстуры:

```bash
poetry run python manage.py loaddata catalog/fixtures/categories.json
poetry run python manage.py loaddata catalog/fixtures/products.json
```

Также реализована кастомная команда, которая предварительно очищает существующие данные и загружает фикстуры:

```bash
poetry run python manage.py load_fixtures
```

## Административная панель

Для работы с товарами и категориями используется Django Admin:

http://127.0.0.1:8000/admin/

Для доступа необходимо создать суперпользователя:

```bash
poetry run python manage.py createsuperuser
```