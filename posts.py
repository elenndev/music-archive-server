from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

import os

load_dotenv()

class Post(BaseModel):
    title: str
    cover: str
    cover_description: str
    content: str
    created_at: datetime

DB_URL = os.environ.get('MONGODB_URL')

def convert_to_dict(doc):
    doc["_id"] = str(doc["_id"])  
    return doc

def connect_db():
    client = MongoClient(DB_URL)
    db = client["posts"]
    collection = db["posts"]
    return client, db, collection


def all_posts(sort: int):
    client, db, collection = connect_db()
    all_posts = []
    cursor = collection.find({}).sort("created_at", sort)
    for doc in cursor:
        all_posts.append(convert_to_dict(doc))
    return all_posts

def new_post(data: Post):
    client, db, collection = connect_db()
    try:
        result = collection.insert_one(data)
        return {"id": str(result.inserted_id)}
    except PyMongoError as e:
        print(f"Erro ao criar novo post: {e}")
        raise
    finally: 
        client.close()

def delete_post(get_id):
    client, db, collection = connect_db()
    try:
        id = ObjectId(get_id)
        result = collection.delete_one({'_id': id})
        response = True if result.deleted_count > 0 else False
        return response
    except PyMongoError as e:
        print(f"Erro ao deletar post: {e}")
        raise
    finally:
        client.close()
    
def update_post(data: Post, get_id):
    client, db, collection = connect_db()
    try:
        id = ObjectId(get_id)
        result = collection.update_one(
            {'_id': id},
            {'$set': data})
        response = True if result.modified_count > 0 else False
        return response
    except PyMongoError as e:
        print(f"Erro ao atualizar post: {e}")
        raise
    finally:
        client.close()

def get_post(get_id):
    client, db, collection = connect_db()
    try:
        id = ObjectId(get_id)
    except Exception as e:
    # Tratar erro de conversão
        return {"error": f"Invalid ObjectId: {e}"}
    doc = collection.find_one({'_id': id})
    return convert_to_dict(doc)