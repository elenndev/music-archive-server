from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

import os

class BlogSave(BaseModel):
    info_name: str
    text_value: str

load_dotenv()

DB_URL = os.environ.get('MONGODB_URL')

def connect_db():
    client = MongoClient(DB_URL)
    db = client['blog-infos']
    collection = db['fast-saves']
    return client, db, collection

def get_blogSaves(info_name):
    client, db, collection = connect_db()
    try:
        info = collection.find_one({'info_name': info_name})
        return info
    except PyMongoError as e:
        print(f"Erro ao obter informações do blog: {e}")
    finally:
        client.close()

def set_blogSaves(info: BlogSave):
    client, db, collection = connect_db()
    try:
        result = collection.update_one({'info_name': info['info_name']},
        {'$set':{'text_value': info['text_value']}})
        print(info['info_name'], info['text_value'])
        response = True if result.modified_count > 0 else False
        return response
    except PyMongoError as e:
        print(f"Erro ao atualizar informações do blog: {e}")
        raise
    finally:
        client.close()
