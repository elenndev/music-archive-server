from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from posts import all_posts, new_post, delete_post, update_post, Post, get_post
from blogSaves import get_blogSaves, set_blogSaves, BlogSave
from drafts import get_drafts, update_draft, delete_draft, create_draft

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://music-archive-elenndevs-projects.vercel.app",
    "https://music-archive-blog.vercel.app",
    "http://localhost:5173",
    "https://music-archive-6nd23x9fr-elenndevs-projects.vercel.app"
],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
def start():
    return "hello!"

@app.get("/sitemap", response_class = Response)
def sitemap() -> Response:
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://music-archive-blog.vercel.app</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
      </url>
      <url>
        <loc>https://music-archive-blog.vercel.app/todas-publicacoes</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
      </url>
      <url>
        <loc>https://music-archive-blog.vercel.app/ler/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
      </url>
      <url>
        <loc>https://music-archive-blog.vercel.app/sobre-mim</loc>
        <changefreq>yearly</changefreq>
        <priority>0.6</priority>
      </url>
    </urlset>"""
    return Response(
        content=sitemap_xml.strip(),
        media_type="application/xml",
        headers={"Cache-Control": "max-age=3600"}
    )


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
