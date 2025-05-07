import scrapy

class EntrepriseItem(scrapy.Item):
    numero = scrapy.Field()
    source = scrapy.Field()
    kbo = scrapy.Field()
    ejustice = scrapy.Field()
    consult = scrapy.Field()
