import subprocess

spiders = ["ejustice", "consult", "kbo"]

for spider in spiders:
    print(f"\n=== Lancement du spider: {spider} ===")
    try:
        subprocess.run(["scrapy", "crawl", spider], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {spider}: {e}")
