from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId
from posts import Post

import os

DB_URL = os.environ.get('MONGODB_URL')

def convert_to_dict(doc):
    doc["_id"] = str(doc["_id"])  
    return doc

def connect_db():
    client = MongoClient(DB_URL)
    db = client["posts"]
    collection = db["drafts"]
    return client, db, collection

def get_drafts(sort: int):
    client, db, collection = connect_db()
    all_drafts = []
    cursor = collection.find({}).sort("created_at", sort)
    for doc in cursor:
        all_drafts.append(convert_to_dict(doc))
    return all_drafts

def create_draft(data: Post):
    client, db, collection = connect_db()
    try:
        result = collection.insert_one(data)
        return {"id": str(result.inserted_id)}
    except PyMongoError as e:
        print(f"Erro ao criar o rascunho")
        return False
    finally:
        client.close()

def update_draft(data: Post, get_id):
    client, db, collection = connect_db()
    try:
        id = ObjectId(get_id)
        result = collection.update_one(
            {'_id': id},
            {'$set': data}
        )
        response = True if result.modified_count > 0 else False
        return response
    except PyMongoError as e:
        print(f"Erro atualziar rascunho: {e}")
    finally:
        client.close()

def delete_draft(get_id):
    client, db, collection = connect_db()
    try:
        id = ObjectId(get_id)
        result = collection.delete_one({'_id': id})
        response = True if result.deleted_count > 0 else False
        return response
    except PyMongoError as e:
        print(f"Erro ao deletar rascunho: {e}")
        return False
    finally:
        client.close()