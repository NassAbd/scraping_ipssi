import scrapy
from tp_scrapy.items import EntrepriseItem
from tp_scrapy.utils import lire_numeros

class KBOSpider(scrapy.Spider):
    name = "kbo"
    custom_settings = {'DEFAULT_REQUEST_HEADERS': {'Accept-Language': 'fr'}}

    def start_requests(self):
        for numero in lire_numeros():
            url = f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?lang=fr&nummer={numero}"
            yield scrapy.Request(url, callback=self.parse, meta={'numero': numero})

    def parse(self, response):
        item = EntrepriseItem()
        item["numero"] = response.meta["numero"]
        item["source"] = "kbo"

        generalites = {}
        generalites["statut"] = response.xpath('.//span[@class="pageactief"]/text()').getall()[0]
        generalites["situation_juridique"] = response.xpath('.//span[@class="pageactief"]/text()').getall()[1]
        generalites["date_debut"] = response.xpath('//tr[td[contains(text(), "Date de début")]]/td[2]/text()').get()

        fonctions = response.xpath('//tr[td/h2[contains(text(), "Fonctions")]]/following-sibling::tr[1]//span[@id="klikfctie"]/text()').get()

        capacites = response.xpath('//tr[td/h2[contains(text(), "Capacités entrepreneuriales")]]/following-sibling::tr[1]/td/text()').get()

        qualities = [
                        row.xpath('normalize-space(string())').get()
                        for row in response.xpath(
                            '//tr[td/h2[contains(text(), "Qualités")]]/following-sibling::tr['
                            'following-sibling::tr[td/h2[contains(text(), "Autorisations")]] '
                            'and (contains(td/@class, "QL") or contains(td/@class, "RL"))]'
                        )
                    ]
        
        extern_links = response.xpath('//tr/td/a[@class="external"]/@href').getall()

        item["kbo"] = {
            "generalites": generalites,
            "fonctions": fonctions,
            "capacites": capacites,
            "qualites": qualities,
            "liens_externes": extern_links,
        }
        
        yield item
