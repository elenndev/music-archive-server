from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from dotenv import load_dotenv
from posts import all_posts, new_post, delete_post, update_post, Post, get_post
from middleware import validate_auth
import requests
import os

load_dotenv()

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

@app.get("/get-post")
def get_postById(get_id: str):
    return get_post(get_id)  

@app.post("/create-post")
def create_post(post: Post):
    data = jsonable_encoder(post)
    return new_post(data)

@app.delete("/delete-post")
def delete_postById(get_id: str, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    check = validate_auth(token)
    print("olha chegou aquii")
    if not check:
        print("Token invalido")
        return False
    return delete_post(get_id)
    
    
@app.put("/update-post")
def update_postById(post: Post, get_id: str):
    data = jsonable_encoder(post)
    return update_post(data, get_id)


