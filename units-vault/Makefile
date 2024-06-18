ifeq ($(OS), Windows_NT)
	PY_CALL = python
else
	PY_CALL = python3
endif

run:
	PYTHONPATH=$(PYTHONPATH):$(CURDIR)/app $(PY_CALL) app/main.py

install:
	pip install -r ./requirements/base.txt

build:
	$(PY_CALL) -m grpc_tools.protoc -I ./protobufs --python_out=./app/generated_bufs \
         --grpc_python_out=./app/generated_bufs ./protobufs/recommendations.proto