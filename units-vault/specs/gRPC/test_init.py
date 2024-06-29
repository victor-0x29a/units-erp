import pytest

from gRPC_services.init_pb2 import PingRequest
from gRPC_services.init_pb2_grpc import PingService


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from gRPC_services.init_pb2_grpc import add_PingServiceServicer_to_server

    return add_PingServiceServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    from gRPC_services.init_pb2_grpc import PingServiceServicer

    return PingServiceServicer()


@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    from gRPC_services.init_pb2_grpc import PingServiceStub

    return PingServiceStub(grpc_channel)


def test_some(grpc_stub):
    request = PingRequest()
    response = grpc_stub.Ping(request)

    assert response.name == f'test-{request.name}'
