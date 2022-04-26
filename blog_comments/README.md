# API для системы комментариев блога.

### В проекте используется:
* Django
* DRF
* django-mptt
* PostgreSQL
* Docker
* Docker-compose

Endpoints

| url                                     | method | params                                             | description                                                                                                                                                                                             |
|-----------------------------------------|--------|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /api/articles/                          | GET    |                                                    | Возвращает список статей                                                                                                                                                                                |
| /api/articles/                          | POST   | body: "title": "str", "content": "str"             | Создание статьи. Возвращает статус 201 и title, url(for article), created(data) если усешно, иначе                                                                                                      |
| /api/articles/<article_id:int>/         | GET    | path: "article_id": int                            | Детальная информация о статье. Возвращает статус 200 и title, content, created(data), comments(до 3 уровня вложенности) если статья существует, иначе 404                                               |
| /api/article/<article_id:int>/comments/ | POST   | body: "content": "str"                             | Создание комментария к статье. Возвращает статус 201 и content, created(data) если успешно, инче _или_                                                                                                  |
| /api/comments/<comment_id:int>/         | GET    | path: "comment_id": int                            | Возвращает список всех подкомментариев к комментарию. <br/> Возвращает статус 200 и иерархию все комментариев* к комментарию (все уровни вложенности) если комментарий с таким id существует, иначе 404 |
| /api/comments/<comment_id:int>/         | POST   | path: "comment_id": int<br/>body: "content": "str" | Создание комментария к любому комментарию. Возвращает статус 201 и content, created(data) если успешно, инче _или_                                                                                                                                                             |


## **Для запуска**
* Установите git, docker, docker-compose
* git clone 
* cd block_comments

