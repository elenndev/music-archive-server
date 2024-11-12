from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel

import os

load_dotenv()

class Post(BaseModel):
    id: str
    title: str
    cover_description: str
    content: str
    created_at: datetime

DB_URL: str = os.environ.get('MONGODB_URL') #VER DEPOIS SE FUNCIONA SEM O STR
client = MongoClient(DB_URL)
db = client["posts"]

def convert_to_dict(doc):
    doc["_id"] = str(doc["_id"])  # Converte ObjectId para string pra poder iterar e salvar em array
    return doc


def all_posts(sort: float):
    collection = db["posts"]
    all_posts = []
    cursor = collection.find({})
    for doc in cursor:
        all_posts.append(convert_to_dict(doc))
    return all_posts

def new_post(data: Post):
    result = collection.insert_one(data)
    return {"id": str(result.inserted_id)}