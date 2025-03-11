import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
hostname = os.getenv("MONGODB_HOST")
database_name = os.getenv("MONGODB_NAME")
ca_file_path = os.getenv("MONGO_CA_FILE_PATH")

uri = f"mongodb+srv://{username}:{password}@{hostname}/{database_name}?authSource=admin&tls=true&tlsCAFile={ca_file_path}"

client = pymongo.MongoClient(uri)
db = client[database_name]
