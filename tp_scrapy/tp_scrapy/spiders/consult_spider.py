import scrapy
import json
from tp_scrapy.items import EntrepriseItem
from tp_scrapy.utils import lire_numeros

class ConsultAPISpider(scrapy.Spider):
    name = "consult"

    def start_requests(self):
        for numero in lire_numeros():
            numero_sans_points = numero.replace('.', '')
            url = (
                f"https://consult.cbso.nbb.be/api/rs-consult/published-deposits"
                f"?page=0&size=100&enterpriseNumber={numero_sans_points}&sort=periodEndDate,desc&sort=depositDate,desc"
            )
            yield scrapy.Request(url, callback=self.parse, meta={'numero': numero})

    def parse(self, response):
        data = json.loads(response.text)
        item = EntrepriseItem()
        item["numero"] = response.meta["numero"]
        item["source"] = "consult"
        item["consult"] = []

        for deposit in data.get("content", []):
            publication = {
                "titre": deposit.get("modelName", "").strip(),
                "reference": deposit.get("reference"),
                "date_depot": deposit.get("depositDate", "")[:10],  # 10 first chars YYYY-MM-DD
                "date_fin_exercice": deposit.get("periodEndDate", "")[:10],
                "langue": deposit.get("language"),
            }
            item["consult"].append(publication)

        yield item
