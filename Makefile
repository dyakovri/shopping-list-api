up:
	docker-compose up --detach --remove-orphans --force-recreate --build
	make migrate

up-postgres:
	docker-compose up --detach --remove-orphans --force-recreate postgres
	make migrate

down:
	docker-compose down

migrate:
	docker-compose run --rm api bash -c 'alembic upgrade head'

prod:
	docker-compose --file docker-compose.prod.yml up --detach --remove-orphans --force-recreate --build
	docker-compose --file docker-compose.prod.yml run --rm api bash -c 'alembic upgrade head'
