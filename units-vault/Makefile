run:
	PYTHONPATH=$(PYTHONPATH):$(CURDIR)/app python3 app/main.py

install:
	pip install -r ./requirements/base.txt

build:
	python3 -m grpc_tools.protoc -I ./protobufs --python_out=./app/generated_bufs \
         --grpc_python_out=./app/generated_bufs ./protobufs/recommendations.proto