from BaselineSummariser.config import Config

import logging

import urllib.request
from bs4 import BeautifulSoup


class TextScrapper:
    def __init__(self, url=None):
        self.url = url
        self._fetched_data = self.fetch_data()
        self._article_content = ''

    def fetch_data(self):
        try:
            self._fetched_data = urllib.request.urlopen(self.url)
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            logging.error(err)

    def get_content(self):
        article_r = self._fetched_data.read()
        article_p = BeautifulSoup(article_r, 'html.parser')
        paras = article_p.find_all('p')

        for para in paras:
            self._article_content += para.text

        return self._article_content


logging.basicConfig(filename=Config.LOGS / 'TextScrapper.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s')
