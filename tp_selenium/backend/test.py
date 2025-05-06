from types import SimpleNamespace
from scraper import scrape_doctolib

# Simule les paramètres d'entrée
params = SimpleNamespace(
    location="paris",
    query="",
    max_results=5,
    assurance=1
)

print(scrape_doctolib(params))
