from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from scraper import scrape_article
from db import find_articles_by_category, find_all_articles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleRequest(BaseModel):
    url: str

"""http://127.0.0.1:8000/scrape
{
    "url": "https://www.blogdumoderateur.com/google-ne-supprimera-pas-cookies-tiers-chrome/"
}
"""
@app.post("/scrape/")
def scrape_article_endpoint(data: ArticleRequest):
    try:
        scrape_article(data.url)
        return {"message": "✅ Article scrappé et enregistré avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def serialize_article(article):
    article['_id'] = str(article['_id'])  # Convertir ObjectId
    return article

# http://127.0.0.1:8000/articles?category=web
@app.get("/articles/")
def get_articles(category: str = Query(..., description="Catégorie ou sous-catégorie")):
    try:
        articles = find_articles_by_category(category)
        return [serialize_article(article) for article in articles]
    except Exception as e:
        return {"error": str(e)}

@app.get("/articles/all/")
def get_all_articles():
    try:
        articles = find_all_articles()
        return [serialize_article(article) for article in articles]
    except Exception as e:
        return {"error": str(e)}
