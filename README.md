# API для системы комментариев блога

### В проекте используется:
* Django
* DRF
* django-mptt
* PostgreSQL
* Docker
* Docker-compose

### **Запуск приложения**
* Для запуска Вам понадобится git, docker, docker-compose
* склонируйте данный репозиторий с помощью команды: _git clone git@github.com:MARI150994/blog_with_comments.git_
* перейдите в паку blog_with_comments/blog_comments
* соберите и запустите докер образ: _docker-compose up -d --build app_
* если собираете образ первый раз, то примените миграции: _docker-compose exec app python manage.py migrate_
* используйте перечисленные ниже endpoints для тестирования ресурсов API,
приложение по умолчанию запускается на 0.0.0.0:8000, перейдите в браузере по ссылке _http://0.0.0.0:8000/api/<ресурс>/_ либо используйте Postman и тп

### Endpoints

| url                                     | method | params                                             | description                                                                                                                                                                       |
|-----------------------------------------|--------|----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /api/articles/                          | GET    |                                                    | Список статей. Возвращает статус 200 с телом: title, url(for article), created(data) для каждой статьи                                                                            |
| /api/articles/                          | POST   | body: "title": "str", "content": "str"             | Создание статьи. Возвращает статус 201 с телом: title, url(for article), created(data) если успешно, иначе - 400                                                                  |
| /api/articles/<article_id:int>/         | GET    | path: "article_id": int                            | Детальная информация о статье. Возвращает статус 200 с телом: title, content, created(data), comments(c иерархией комментариев см. примечание), если нет статьи с таким id то 404 |
| /api/article/<article_id:int>/comments/ | POST   | path: "article_id": int<br/>body: "content": "str" | Создание комментария к статье. Возвращает статус 201 с телом: content, created(data) если успешно, иначе 400, если нет статьи с таким id то 404                                   |
| /api/comments/<comment_id:int>/         | GET    | path: "comment_id": int                            | Список подкомментариев к комментарию. <br/> Возвращает статус 200 с телом, где детальная информация о каждом комментарии в виде иерархии, если нет комментария с таким id то 404  |
| /api/comments/<comment_id:int>/         | POST   | path: "comment_id": int<br/>body: "content": "str" | Создание комментария к любому комментарию. Возвращает статус 201 с телом: content, created(data) если успешно, иначе 400, если нет комментария с таким id то 404                  |

Примечание. Для каждого комментария отображается иерархия подкомментариев в поле _**children**_. 
Если отображаются комментарии на странице статьи, то для комментария с третьим уровнем вложенности в поле children будет ссылка вида /api/comments/<comment_id:int>/ 
на детальную информацию о всех подкомментариях любого уровня вложенности для данного комментария. Если подкомментариев нет, то список пуст.
