# Run the app

Be sure that next ports are available: 8000 - for Django app; 5432 - for PostgreSQL. 
Close all application, databases, containers etc on ports if they are conflict. 
Check that you have docker and docker-compose.

`docker-compose up --build`

Application will be available at: `http://localhost:8000/api/short_code`

Configuration parametres could be changed in `settings.py` file

ALPHABET (str 1-300 symbols) - all available symbols
REQUESTED_SHORT_CODE_LENGTH (int 1-30) - requested length of generated string 
CHECK_SHORT_CODE_LENGTH_PROVIDED_BY_USER (boolean) - check length of string provided by user or not

* When you make some changes they will be automatically delivered inside docker container. 
* You could change configuration parameters and see them impact to generated code.
* Tests are running automatically. If you need run test manually.
   docker exec -it django_app_container_wEa2 python3 manage.py test

P.S. This solution based on converting decimal number to another digit base system.
For details see `short_code/converter.py`


TODO:
1. Add queue mechanism for manage write operations (RabbitMQ)
2. Add cache layer for fast access to external links (Redis)
3. Add documentation for API (Swagger)


# Request example

`POST Create new shortcode record`
http://localhost:8000/api/short_code/shorten/

Create new shortcode. In body provide "url" (required), "shortcode" (optional).

`GET Redirect external link by shortcode`
http://localhost:8000/api/short_code/000000

Redirect user to saved url by providing shortcode.

`GET Statistic of shortcode usage`
http://localhost:8000/api/short_code/000000/stats

Show statistic of shortcode.










