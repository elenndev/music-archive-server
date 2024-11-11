from typing import Union
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import bcrypt
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

load_dotenv()

class Post(BaseModel):
    id: str
    title: str
    cover_description: str
    content: str
    created_at: datetime

app = FastAPI()

origins = [
    "https://music-archive-blog.vercel.app",
    "http://localhost:5173",
    "https://music-archive-6nd23x9fr-elenndevs-projects.vercel.app"
]

DB_URL: str = os.environ.get('MONGODB_URL') #VER DEPOIS SE FUNCIONA SEM O STR
client = MongoClient(DB_URL)
db = client["posts"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

def convert_to_dict(doc):
    doc["_id"] = str(doc["_id"])  # Converte ObjectId para string pra poder iterar e salvar em array
    return doc

@app.get("/all-posts")
def get_allPosts(sort: float):
    collection = db["posts"]
    all_posts = []
    cursor = collection.find({})
    for doc in cursor:
        all_posts.append(convert_to_dict(doc))

    return all_posts

