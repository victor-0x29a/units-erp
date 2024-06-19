ifeq ($(OS), Windows_NT)
	PY_CALL = python
	SET_ENVIRONMENT = set PYTHONPATH=
else
	PY_CALL = python3
	SET_ENVIRONMENT = PYTHONPATH=
endif

DOCKER_COMPOSE_DOWN = cd ./docker && docker-compose down

dev:
	cd ./docker && docker-compose up -d
	$(SET_ENVIRONMENT)$(PYTHONPATH):$(CURDIR)/app && $(PY_CALL) app/main.py

install-linux:
	$(PY_CALL) -m venv vault-env
	./vault-env/Scripts/activate
	$(PY_CALL) -m pip install -r ./requirements/base.txt

install-win:
	$(PY_CALL) -m venv vault-env
	.\vault-env\Scripts\activate.bat
	$(PY_CALL) -m pip install -r ./requirements/base.txt

#build:
#	$(PY_CALL) -m grpc_tools.protoc -I ./protobufs --python_out=./app/generated_bufs \
         --grpc_python_out=./app/generated_bufs ./protobufs/recommendations.proto

docker-stop:
	$(DOCKER_COMPOSE_DOWN)
