import nltk
import pytextrank
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

from newspaper import Article
from textblob import TextBlob

url = 'https://en.wikipedia.org/wiki/Deep_learning'

article = Article(url)
article.download()
article.parse()

# DEFINE TYPICAL SPACY PIPELINE
nlp = spacy.load("en_core_web_lg")

# MODIFY PIPELINE SO THAT IT INCLUDES THE TEXTRANK ALGORITHM
# nlp.add_pipe("textrank")

# RUN THE SPACY PIPELINE WITH TEXTRANK ALGORITHM
doc = nlp(article.text)
tokens = [token.text for token in doc]
word_freq = {}

for word in doc:
    if word.text.lower() not in list(STOP_WORDS):
        if word.text.lower() not in punctuation:
            word_freq[word.text] = 1 + word_freq.get(word.text, 0)

max_freq = max(word_freq.values())

for word in word_freq.keys():
    frac = word_freq[word] / max_freq
    word_freq[word] = frac


sentence_tokens = [sent for sent in doc.sents]
sentence_scores = {}

for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_freq.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_freq[word.text.lower()]
            else:
                sentence_scores[sent] += word_freq[word.text.lower()]

select_length = int(len(sentence_tokens)*0.65)
summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
final_summary=[word.text for word in summary]
summary = ''.join(final_summary)
print('-'*10)
print(summary)

# # SHOW TEXT SUMMARY
# for sentence in doc._.textrank.summary(limit_phrases=2, limit_sentences=3):
#     print(sentence)
#     print('-'*100)
#
# print("Phrases and Ranks")
# phrases_and_ranks = [(phrase.chunks[0], phrase.rank)for phrase in doc._.phrases]
# print(phrases_and_ranks[:10])
