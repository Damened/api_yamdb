Технологии:
Python==3.9.10;
Django==3.2.16;
Django rest framework==3.12.4.
Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:Damened/api_yamdb.git
cd api_yamdb

Cоздать и активировать виртуальное окружение:

python3 -m venv venv
source venv/Scripts/activate
Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python manage.py migrate
Запустить проект:

python manage.py runserver