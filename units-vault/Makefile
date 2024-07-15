# TO DO: add virtualenv support

ifeq ($(OS), Windows_NT)
	PY_CALL = python
	SET_ENVIRONMENT = set PYTHONPATH=
else
	PY_CALL = python3
	SET_ENVIRONMENT = PYTHONPATH=
endif

DOCKER_COMPOSE_DOWN = cd ./docker && docker-compose down
PY_VERSION = 3.12.3

dev:
	docker-compose up -d
	fastapi dev main.py

test:
	$(PY_CALL) -m pytest -v

install:
	$(PY_CALL) -m pip install -r ./requirements/base.txt
	$(PY_CALL) -m pip install -r ./requirements/dev.txt

lint:
	$(PY_CALL) -m flake8 .

docker-stop:
	$(DOCKER_COMPOSE_DOWN)
