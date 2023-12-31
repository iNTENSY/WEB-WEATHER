# Веб-сайт WeatherFinder

----

Данный веб-сервис является ***pet***-проектом. Основная задача была в
реализации сайта, позволяющий узнать погоду в определенном городе.
В данном проекте реализована система подписки с подключенным сервисом ***ЮКасса***.
Также реализована система подсчета поисков определенного города и с выводом их
в списке. Имеется автодокументация ***API*** сервиса с помощью ***swagger***.

`Автор: Даценко Дмитрий Игоревич`

---
### Библиотеки
- Django 4.2.3
- Django REST Framework 3.14.0
- PostgreSQL 13.0
- Djoser 2.2.0
- Celery 5.3.1
- Yookassa 2.4.0
- Django-redis 5.3.0 
- Drf-yasg 1.21.7
- Django Debug Toolbar 4.2.0
- Django environ 0.10.0

---

### Установка и запуск контейнера в docker
Создайте локально папку, в которую вы склонируете репозиторий

```
git clone https://github.com/iNTENSY/WEB-WEATHER.git
```

Чтобы запустить эту программу, у вас должен быть включен Docker. Воспользуйтесь
следующими командами ниже.

```docker
docker-compose build
docker-compose up
```

Для того чтобы создать базу данных, Вам обязательно нужно указать команду ниже
```docker
docker-compose exec web python manage.py migrate --noinput 
```

Для того чтобы создать супер-пользователя, Вам нужно указать команду ниже

```docker
docker-compose exec web python manage.py createsuperuser
```

---