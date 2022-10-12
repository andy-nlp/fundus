import json
from datetime import datetime
from os import makedirs
from os.path import exists
from typing import Optional, Dict
from urllib.parse import urlparse, quote_plus

from dotmap import DotMap

from example_pasrer import MDRParser
from src.common_crawl.crawler import Crawler
from src.html_parser import BaseParser

base_path = ...  # dir where jsons should be saved


def save_article_to_json(parsed_article: DotMap):
    crawl_date = parsed_article.crawl_date

    parsed_url = urlparse(parsed_article.url)
    path = f'{base_path}/{crawl_date.year}/{crawl_date.month}/{parsed_url.netloc}/'

    if not exists(path):
        makedirs(path)

    filename = quote_plus(parsed_article.url) + '.json'
    filepath = path + filename

    with open(filepath, 'w+', encoding='utf8') as file:
        file.write(json.dumps(parsed_article, indent=4, ensure_ascii=False, default=str))


if __name__ == '__main__':
    cc_news_crawler = Crawler()
    mdr_parser = MDRParser()

    mapping: Dict[str, Optional[BaseParser]] = {'www.mdr.de': mdr_parser}

    start_date = datetime(2022, 8, 20)
    end_date = datetime(2022, 8, 21)

    for article in cc_news_crawler.crawl(mapping=mapping, start=start_date, end=end_date):
        save_article_to_json(article)