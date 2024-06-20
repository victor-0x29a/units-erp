import os
from dotenv import load_dotenv

load_dotenv()

gRPC_PORT = int(os.getenv("GRPC_PORT"))


MONGO_HOST = os.getenv("MONGODB_HOST")
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DATABASE = os.getenv("MONGODB_DATABASE")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/?authSource={MONGO_DATABASE}"
