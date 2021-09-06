.PHONY: db-migrate
db-migrate:
	poetry run alembic revision --autogenerate

.PHONY: db-upgrade
db-upgrade:
	poetry run alembic upgrade head

.PHONY: run
run:
	poetry run uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --ssl-keyfile /home/sascha/cert/localhost+2-key.pem --ssl-certfile /home/sascha/cert/localhost+2.pem
