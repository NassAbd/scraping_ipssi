import pymongo

class MongoPipeline:

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(spider.settings.get("MONGO_URI"))
        self.db = self.client[spider.settings.get("MONGO_DB")]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db["entreprises"]
        collection.update_one(
            {"numero": item["numero"]},
            {"$set": {item["source"]: item[item["source"]]}, "$setOnInsert": {"numero": item["numero"]}},
            upsert=True
        )
        return item
