from db import find_articles_by_category

def get_articles_by_category(category):
    articles = find_articles_by_category(category)

    if not articles:
        print("Aucun article trouvé.")
        return
    
    return articles

if __name__ == "__main__":
    print(get_articles_by_category('web'))
