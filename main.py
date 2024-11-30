from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from dotenv import load_dotenv
from posts import all_posts, new_post, delete_post, update_post, Post, get_post
from blogSaves import get_blogSaves, set_blogSaves, BlogSave
from drafts import get_drafts, update_draft, delete_draft, create_draft
from middleware import validate_auth
import requests
import os

load_dotenv()

app = FastAPI()

origins = [
    "https://music-archive-blog.vercel.app",
    "https://music-archive-6nd23x9fr-elenndevs-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/)
def start():
    return "hello!"

@app.get("/all-posts")
def get_allPosts(sort: int):
    return all_posts(sort)

@app.get("/get-post")
def get_postById(get_id: str):
    return get_post(get_id)  

@app.post("/create-post")
def create_post(post: Post):
    data = jsonable_encoder(post)
    print(data)
    return new_post(data)

@app.delete("/delete-post")
def delete_postById(get_id: str):
    return delete_post(get_id)
    
@app.put("/update-post")
def update_postById(post: Post, get_id: str):
    data = jsonable_encoder(post)
    return update_post(data, get_id)

@app.get("/fast-infos")
def get_fastBlogInfos(info_name):
    info = get_blogSaves(info_name)
    if info:
        info['_id'] = str(info['_id'])
    return info

@app.put("/set-fast-infos")
def set_fastBlogInfos(get_info: BlogSave):
    info = jsonable_encoder(get_info)
    return set_blogSaves(info)

@app.get("/get-drafts")
def get_postDrafts(sort: int):
    return get_drafts(sort)

@app.post("/create-draft")
def create_postDraft(post: Post):
    data = jsonable_encoder(post)
    return create_draft(data)

@app.put("/update-draft")
def update_postDraft(post: Post,get_id: str):
    data = jsonable_encoder(post)
    return update_draft(data, get_id)

@app.delete("/delete-draft")
def delete_draftById(get_id: str):
    return delete_draft(get_id)
