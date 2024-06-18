import sys
import os
from constants import gRPC_PORT
from concurrent import futures
import grpc

sys.path.insert(
    0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'generated_bufs')
    )
)

# flake8: noqa
from generated_bufs.recommendations_pb2_grpc import (
    PingService,
    add_PingServiceServicer_to_server
)


class UnitsService:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_PingServiceServicer_to_server(PingService(), self.server)
        self.server.add_insecure_port(f'[::]:{gRPC_PORT}')

    def start(self):
        print(f'gRPC listening on port {gRPC_PORT}')
        self.server.start()
        self.server.wait_for_termination()


if __name__ == '__main__':
    UnitsService().start()
