from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import SearchParams
from .scraper import scrape_doctolib
from .exporter import export_to_csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
def search(params: SearchParams):
    results = scrape_doctolib(params)

    # Filtrage selon le secteur d'assurance demandé
    filtered_results = [
        r for r in results
        if params.assurance in r.get("secteur", "")
    ]

    export_to_csv(filtered_results, "resultats.csv")
    return filtered_results
