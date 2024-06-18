import os
from dotenv import load_dotenv

load_dotenv()

gRPC_PORT = int(os.getenv("GRPC_PORT"))
