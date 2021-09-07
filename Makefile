up:
	docker-compose up --detach --remove-orphans --force-recreate --build
	make migrate

up-postgres:
	docker-compose up --detach --remove-orphans --force-recreate postgres
	make migrate

down:
	docker-compose down

migrate:
	docker-compose run api bash -c 'alembic upgrade head'
