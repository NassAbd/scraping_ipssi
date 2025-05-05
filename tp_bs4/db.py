from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['tp_scraping']
collection = db['articles']

def insert_article(data):
    collection.insert_one(data)

def find_articles_by_category(category):
    return list(collection.find({
        '$or': [
            {'category': {'$regex': f'^{category}$', '$options': 'i'}},
            {'sub_category': {'$regex': f'^{category}$', '$options': 'i'}}
        ]
    }))

def find_all_articles():
    return list(collection.find())