# Book Market

RESTful API service for e-commerce

On initialization django app will be created few model instances.
Model profile is expansion of standart auth.user model.
There are 2 profile without subscribe, you could manually tested funcionallity.


# Run application

You had two options to run this application

1. With docker: `docker-compose up` (docker should be installed)
2. With makefile (python 3 and unix required)
``` 
python3 -m venv venv
source venv/bin/activate
make all
```

Application will be available at http://127.0.0.1:8000/



# Request example

`POST /api/userprofile/create/`

http://localhost:8000/api/userprofile/create/

Создание нового пользователя. В теле запроса указать username, password

`GET /api/userprofile/all`

http://localhost:8000/api/userprofile/all

Информация по всем пользователям

`GET /api/userprofile/{profile_id}`

http://localhost:8000/api/userprofile/2

Информация по конкретному пользователю

`POST /api/userprofile/subscribe/`

http://localhost:8000/api/userprofile/subscribe/

Создание подписки для пользователя. В теле запроса указать profile_id для которого создается подписка

`GET /api/book/{book_id}/?token=`

http://localhost:8000/api/book/2/?token=0c302b15-39c0-4cfc-8f99-2c56b8d61b97

Информация по конкертной книге. В query-параметре необходимо передать token, полученный при создании пользователя

`GET /api/book/all`

http://localhost:8000/api/book/all

Краткая информация по всем книгам









