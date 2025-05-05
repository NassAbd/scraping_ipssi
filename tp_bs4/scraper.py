import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from datetime import datetime
from db import insert_article

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        raise Exception(f"Erreur : {str(e)}")

    soup = BeautifulSoup(response.text, 'html.parser')

    header_elem = soup.find('header', class_='entry-header')

    title_elem = header_elem.find('h1', 'entry-title')
    title = title_elem.text.strip() if title_elem else None

    summary_elem = header_elem.select_one('div.article-hat.t-quote')
    summary = summary_elem.text.strip() if summary_elem else None

    date_elem = header_elem.select_one('span.posted-on time')
    date_str = date_elem['datetime'][:10] if date_elem and 'datetime' in date_elem.attrs else None

    author_elem = header_elem.select_one('span.byline a')
    author = author_elem.text.strip() if author_elem else None

    thumbnail_url = None
    image_elem = soup.find('meta', property='og:image')
    if image_elem and 'content' in image_elem.attrs:
        thumbnail_url = image_elem['content']

    # GOOD
    category = None
    cats_list_div = soup.find('div', class_='cats-list')
    if cats_list_div:
        cat_span = cats_list_div.find('span', attrs={'data-cat': True})
        if cat_span:
            category = cat_span['data-cat'].strip()

    # GOOD
    sub_category_elem = soup.find('div', class_='favtag mb-1')
    sub_category = sub_category_elem.text.strip() if sub_category_elem else None

    # GOOD
    images_dict = {}
    for img in soup.find_all('figure'):
        lazy_srcset = img.find('img')
        image_url = ''
        if lazy_srcset.get('data-lazy-srcset'):
            image_url = lazy_srcset.get('data-lazy-srcset').split(',')[0].split(' ')[0]
        elif lazy_srcset.get('src'):
            image_url = lazy_srcset.get('src')
        image_caption = lazy_srcset['alt'].strip()
        images_dict[image_url] = image_caption

    # GOOD
    article_content_elem = soup.find('div', class_='entry-content')
    article_content = article_content_elem.text.strip() if article_content_elem else None

    article_data = {
        'url': url,
        'title': title,
        'thumbnail': thumbnail_url,
        'category': category,
        'sub_category': sub_category,
        'summary': summary,
        'date': date_str,
        'author': author,
        'content': article_content,
        'images': images_dict
    }

    insert_article(article_data)
    print(f"✅ Article enregistré avec succès.")


if __name__ == "__main__":
    url = input("Entrez l'URL de l'article à scraper : ")
    scrape_article(url)
