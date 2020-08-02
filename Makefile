default: run

run:
	docker-compose up

build:
	docker-compose build
	
logs:
	docker-compose logs -f

run-with-logs: run logs

migrate:
	docker-compose run --rm web python manage.py migrate

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

index:
	docker-compose run --rm web python manage.py search_index --rebuild

dumpdata:
	docker-compose run --rm web python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission --format=json > fixtures/initial_data.json

loaddata:
	docker-compose run --rm web python manage.py loaddata fixtures/initial_data.json
	
reset_db:
	docker-compose run --rm web python manage.py flush --no-input