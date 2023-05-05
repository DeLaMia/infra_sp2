# Yamdb API 

### Описание проекта
Реализация API для социальной сети Yamdb, собранье ревью на различные произведения

### Шаблон наполнения env-файла
#### В директории infra создайте файл .env с переменными окружения для работы с базой данных:
- DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
- DB_NAME=postgres # имя базы данных
- POSTGRES_USER=postgres # логин для подключения к базе данных
- POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
- DB_HOST=db # название сервиса (контейнера)
- DB_PORT=5432 # порт для подключения к БД

### Описание команд для запуска приложения в контейнерах
Для запуска необходимо выполнить из  папки infra/ команду:
```
sudo docker-compose up -d --build
```
Выполнить миграции:
```
sudo docker-compose exec web python manage.py migrate
```

Создать суперпользователя:
```
sudo docker-compose exec web python manage.py createsuperuser
```
Собрать статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Следующим шагом можете создать резервную копию базы:
```
sudo docker-compose exec web python manage.py dumpdata > fixtures.json
```
либо загрузить в базу данные из файла, например разместив файл fixtures.json в папке проекта с manage.py:
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```