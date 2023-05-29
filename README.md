# Совкомбанк.Рекрутинг

## Запуск

В файле .env.example приведены рабочие переменные среды в файле .env.example. Для работы нужно переименовать файл и поменять, если необходимо, нужные значения

```
cp .env.example .env
```

### Докер

```
docker-compose up
```

### "Ручками"

```
# БД
python manage.py migrate
python manage.py loaddata fixtures.json

# Сервер
python manage.py runserver

# Celery
celery -A scb_hr beat --loglevel=info
celery -A scb_hr worker --loglevel=info -P gevent

# Telegram
python telegram_polling.py
```

### Данные для входа

Админ (можно войти в django admin)  
email: admin@mail.ru  
password:  admin

### Тестовые данные

При развертывании заносятся тестовые данные из фикстуры:

* организации
* города
* офисы
* специализация вакансии
* требуемый опыт работы для вакансии
* тип занятости для вакансии

Изменить данные можно в Django Admin (данные для входа в предыдущем пункте). А все остальные сущности уже можно
создать/изменить/удалить через сайт

## Права

* Согласовывать резюме - **inspector.change_resume**
* Создавать интервью - **inspector.add_interview**
* Работать с архивом резюме - **inspector.view_resume**
* Полный доступ к вакансиям - **vacancy.change_vacancy**
* Полный доступ к должностям - **position.change_position**
* Парсинг резюме с внешних сайтов - **vacancy.add_vacancy**
* Работать с отчётами - **inspector.add_resume**

На данный момент используются права, которые создаются автоматически, однако ничего не мешает создавать дополнительные права (например, также через фикстуры, чтобы упростить деплой) и работать с ними

## Всякое

### Выгрузить фикстуры

```
python ./manage.py dumpdata --exclude auth.permission --exclude admin.logentry --exclude contenttypes.contenttype --exclude sessions.session
```

### Бэклог

1) Сокращение резюме с помощью нейросети
2) Что-то именно для it (парсинг github?)
3) Пагинация
4) Шаблон ответа
5) Уведомление о согласовании
