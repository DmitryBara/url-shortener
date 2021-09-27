TAG_NAME = dmitry/DRF

all: requirements migbook migup migrate fixtures run
.PHONY: all


requirements:
	pip install -r requirements.txt

migbook:
	python manage.py makemigrations book

migup:
	python manage.py makemigrations userprofile

migrate:
	python manage.py migrate

fixtures:
	python manage.py loaddata */fixtures/*.json

run:
	python manage.py runserver 0.0.0.0:8000

