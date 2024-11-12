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
from posts import all_posts, new_post, delete_post

load_dotenv()

class Post(BaseModel):
    title: str
    cover: str
    cover_description: str
    content: str
    created_at: datetime

app = FastAPI()

origins = [
    "https://music-archive-blog.vercel.app",
    "http://localhost:5173",
    "https://music-archive-6nd23x9fr-elenndevs-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)


@app.get("/all-posts")
def get_allPosts(sort: float):
    return all_posts(sort)

@app.post("/create-post")
def create_post(post: Post):
    data = jsonable_encoder(post)
    return new_post(data)

@app.delete("/delete-post")
def delete_postById(get_id: str):
    return delete_post(get_id)
    