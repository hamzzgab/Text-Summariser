from Summariser.config import Config

import logging, re

import pdfquery, PyPDF2
import urllib.request
from bs4 import BeautifulSoup

import PyPDF2


# logging.basicConfig(filename=Config.LOGS / 'data.log', filemode='w',
#                     level=logging.DEBUG,
#                     format='%(asctime)s [%(levelname)s]: %(message)s')


class PDFScrapper:
    def __init__(self, filename, path=Config.STATIC):
        self._filename = filename
        self._path = path

        self._pdf_path = self._path / 'files' / f'{self._filename}.pdf'

    def get_text_from_pages(self, pn, pm, store=True):
        pdf_in = open(self._pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_in)

        mode = 'w'
        for num in range(pn-1, pm):
            page = pdf_reader.pages[num]
            if store:
                with open(file=Config.STATIC / 'texts' / f'{self._filename}-{pn}_{pm}.txt', mode=mode) as file:
                    file.write(page.extract_text())
                    mode = 'a'

    def clean_text(self):
        with open(file=Config.STATIC / 'texts' / f'{self._filename}.txt', mode='r') as file:
            text = file.read()

        text = re.sub(r'Page\s([0-9]*)\sof\s([0-9]*)', '', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r' \.', '.', text)
        text = re.sub(r' :', ':', text)
        text = re.sub(r' ’', '’', text)
        text = re.sub(r'\n', '', text)
        text = text.strip()

        return text

    def store_text(self, text):
        with open(file=Config.STATIC / 'texts' / f'{self._filename}.txt', mode='w') as file:
            file.write(text)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = val

    @property
    def pdf_path(self):
        return self._pdf_path

    @pdf_path.setter
    def pdf_path(self, val):
        self._pdf_path = val


class WebScrapper:
    def __init__(self, url=None):
        self.url = url
        self._fetched_data = ''
        self._article_content = ''
        self.fetch_data()

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

    @property
    def fetched_data(self):
        return self._fetched_data

    @fetched_data.setter
    def fetched_data(self, val):
        self._fetched_data = val

    @property
    def article_content(self):
        return self._article_content

    @article_content.setter
    def article_content(self, val):
        self._article_content = val

