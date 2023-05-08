## Проект "YaMDb"
Проект представляет собой API, предназначенный для взаимодействия бэкенда и фронтенда проекта YaMDb.

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/Damened/api_yamdb.git
```

```sh
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```sh
python3 -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

Выполнить миграции:

```sh
python3 manage.py makemigrations
```

```sh
python3 manage.py migrate
```

Заполнить базу данных тестовыми данными (при необходимости):

```sh
python3 manage.py startimport
```

Запустить проект:

```sh
python3 manage.py runserver
```

### Доступные эндпоинты:

#### Регистрация пользователей и выдача токенов

* Регистрация нового пользователя (POST-запрос)

```
/api/v1/auth/signup/
```

* Получение JWT-токена (POST-запрос)

```
/api/v1/auth/token/
```

#### Категории (типы) произведений

* Получение списка всех категорий (GET-запрос)

```
/api/v1/categories/
```

* Добавление новой категории (POST-запрос)

```
/api/v1/categories/
```

* Удаление категории (DELETE-запрос)

```
/api/v1/categories/{slug}/
```

#### Категории жанров

* Получение списка всех жанров (GET-запрос)

```
/api/v1/genres/
```

* Добавление жанра (POST-запрос)

```
/api/v1/genres/
```

* Удаление жанра (DELETE-запрос)

```
/api/v1/genres/{slug}/
```

#### Произведения, к которым пишут отзывы (определенный фильм, книга ли песенка)

* Получение списка всех произведений (GET-запрос)

```
/api/v1/titles/
```

* Добавление произведения (POST-запрос)

```
/api/v1/titles/
```

* Получение информации о произведении (GET-запрос)

```
/api/v1/titles/{titles_id}/
```

* Частичное обновление информации о произведении (PATCH-запрос)
```
/api/v1/titles/{titles_id}/
```

* Удаление произведения (DELETE-запрос)

```
/api/v1/titles/{titles_id}/
```

#### Отзывы

* Получение списка всех отзывов (GET-запрос)

```
/api/v1/titles/{title_id}/reviews/
```

* Добавление нового отзыва (POST-запрос)

```
/api/v1/titles/{title_id}/reviews/
```

* Получение отзыва по id (GET-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/
```

* Частичное обновление отзыва по id (PATCH-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/
```

* Удаление отзыва по id (DELETE-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/
```

#### Комментарии к отзывам

* Получение списка всех комментариев к отзыву (GET-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

* Добавление комментария к отзыву (POST-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

* Получение комментария к отзыву (GET-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

* Частичное обновление комментария к отзыву (PATCH-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

* Удаление комментария к отзыву (DELETE-запрос)

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

#### Пользователи

* Получение списка всех пользователей (GET-запрос)

```
/api/v1/users/
```

* Добавление пользователя (POST-запрос)

```
/api/v1/users/
```

* Получение пользователя по username (GET-запрос)

```
/api/v1/users/{username}/
```

* Изменение данных пользователя по username (PATCH-запрос)

```
/api/v1/users/{username}/
```

* Удаление пользователя по username (DELETE-запрос)

```
/api/v1/users/{username}/
```

* Получение данных своей учетной записи (GET-запрос)

```
/api/v1/users/me/
```

* Изменение данных своей учетной записи (PATCH-запрос)

```
/api/v1/users/me/
```
