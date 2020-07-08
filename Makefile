default: run

run:
	docker-compose up

logs:
	docker-compose logs -f

run-with-logs: run logs

migrate:
	docker-compose run --rm web python manage.py migrate

makemigrations:
	docker-compose run --rm web python manage.py makemigrations
