DOCKER_COMPOSE_DOWN = cd ./docker && docker-compose down

ifeq ($(OS), Windows_NT)
	PY_CALL = python
	SET_ENVIRONMENT = set PYTHONPATH=
else
	PY_CALL = python3
	SET_ENVIRONMENT = PYTHONPATH=
endif

run-images:
	docker-compose up -d
	clear
	@echo "Units-Vault docker images are running."

stop-images:
	$(DOCKER_COMPOSE_DOWN)
	@echo "Units-Vault docker images have been stopped."

dev:
	.venv/bin/uvicorn main:app --reload

test:
	.venv/bin/python -m pytest -v

install:
	$(PY_CALL) -m venv .venv
	.venv/bin/python -m pip install -r ./requirements/base.txt
	.venv/bin/python -m pip install -r ./requirements/dev.txt
	clear
	@echo "Units-Vault environment has been created."

uninstall:
	rm -rf .venv
	@clear
	@echo "Units-Vault environment has been removed."

lint:
	.venv/bin/python -m flake8 .
