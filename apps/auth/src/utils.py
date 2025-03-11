import os
from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient


def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(
        host=host, port=int(port), username=username, password=password
    )
    db_handle = client["db_name"]
    return db_handle, client


username = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
hostname = os.getenv("MONGODB_HOST")
db_name = os.getenv("MONGODB_NAME")
port = os.getenv("MONGODB_PORT")
