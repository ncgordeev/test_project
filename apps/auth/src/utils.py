import os

from dotenv import load_dotenv

load_dotenv()

from pymongo import MongoClient


def get_db_handle():
    client = MongoClient(
        host=os.getenv("MONGODB_HOST"),
        port=int(os.getenv("MONGODB_PORT")),
        username=os.getenv("MONGODB_USER"),
        password=os.getenv("MONGODB_PASSWORD"),
    )
    db_handle = client[os.getenv("MONGODB_NAME")]
    return db_handle, client


db, connect = get_db_handle()
users_collection = db["users"]
