import scrapy
from tp_scrapy.items import EntrepriseItem
from tp_scrapy.utils import lire_numeros

class EjusticeSpider(scrapy.Spider):
    name = "ejustice"

    def start_requests(self):
        for numero in lire_numeros():
            url = f"https://www.ejustice.just.fgov.be/cgi_tsv/list.pl?btw={numero}"
            yield scrapy.Request(url, callback=self.parse, meta={'numero': numero})

    def parse(self, response):
        item = EntrepriseItem()
        item["numero"] = response.meta["numero"]
        item["source"] = "ejustice"
        item["ejustice"] = []

        for block in response.css('div.list-item'):
            title_parts = block.css('p.list-item--subtitle font::text').get()
            description = block.css('p.list-item--subtitle::text').getall()
            description = ''.join(description).strip()

            lines = block.css('a.list-item--title ::text').getall()
            lines = [line.strip() for line in lines if line.strip()]

            address = lines[0] if len(lines) > 0 else ''
            pub_type = lines[2] if len(lines) > 2 else ''

            pub_date, pub_number = '', ''
            if len(lines) > 3 and '/' in lines[3]:
                parts = lines[3].split('/')
                if len(parts) == 2:
                    pub_date = parts[0].strip()
                    pub_number = parts[1].strip()

            image_url = block.css('a.standard::attr(href)').get()
            if image_url and not image_url.startswith('http'):
                image_url = response.urljoin(image_url)

            publication =  {
                'titre': f"{title_parts} {description}".strip(),
                'adresse': address,
                'type_publication': pub_type,
                'date_publication': pub_date,
                'numero_publication': pub_number,
                'image_url': image_url
            }

            item["ejustice"].append(publication)

        yield item
