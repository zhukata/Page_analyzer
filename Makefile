install:
	poetry install

dev:
	poetry run flask --app hexlet-code/page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) hexlet-code/page_analyzer:app