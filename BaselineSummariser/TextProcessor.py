import logging

import nltk
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

logging.basicConfig(filename='../logs/TextPreProcessor.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s')


nltk.download('stopwords')

_debug = True


class TextProcessor:
    def __init__(self, ip_text=None):
        self._text = ip_text

        self._words = word_tokenize(self._text)
        self._sentences = sent_tokenize(self._text)

        self._freq_table = {}
        self._sentence_score = {}

    def calc_freq_table(self):
        stop_words = stopwords.words('english')
        stem = PorterStemmer()

        logging.info('Frequency Table: STARTED')
        for wd in self._words:
            wd = stem.stem(wd)
            if wd not in stop_words:
                if wd not in punctuation:
                    self._freq_table[wd] = 1 + self._freq_table.get(wd, 0)

        if _debug:
            logging.debug(self._freq_table)

        logging.info('Frequency Table: COMPLETED')

    def calc_sentence_score(self, n_chars=7):
        logging.info('Sentence Score: STARTED')

        if _debug:
            logging.debug(f'Number of Sentences: {len(self._sentences)}')

        for sentence in self._sentences:
            sentence_wc = len(word_tokenize(sentence))

            sentence_wc_sw = 0
            for word in self._freq_table:
                if word in sentence.lower():
                    sentence_wc_sw += 1
                    if sentence[:n_chars] in self._sentence_score:
                        self._sentence_score[sentence[:n_chars]] += self._freq_table[word]
                    else:
                        self._sentence_score[sentence[:n_chars]] = self._freq_table[word]

            self._sentence_score[sentence[:n_chars]] = self._sentence_score[sentence[:n_chars]] / sentence_wc_sw

        if _debug:
            logging.debug(self._sentence_score)

        logging.info('Sentence Score: COMPLETED')

    def get_average_score(self):
        logging.info('Average Score: STARTED')
        sum_values = 0
        for score in self._sentence_score:
            sum_values += self._sentence_score[score]

        average_score = sum_values / len(self.sentence_score)

        logging.info('Average Score: COMPLETED')
        return average_score

    def get_summary(self, n_chars=7, threshold=0):
        logging.info('Summary Creation: STARTED')
        sentence_counter = 0
        article_summary = ''

        for sentence in self._sentences:
            if sentence[:n_chars] in self._sentence_score and self._sentence_score[sentence[:n_chars]] >= threshold:
                article_summary += " " + sentence
                sentence_counter += 1
        logging.info('Summary Creation: COMPLETED')

        return article_summary

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, val):
        self._words = val

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, val):
        self._sentences = val

    @property
    def freq_table(self):
        return self._freq_table

    @freq_table.setter
    def freq_table(self, val):
        self._freq_table = val

    @property
    def sentence_score(self):
        return self._sentence_score

    @sentence_score.setter
    def sentence_score(self, val):
        self._sentence_score = val
