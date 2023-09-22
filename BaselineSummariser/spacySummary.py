import nltk
import pytextrank
import spacy

from newspaper import Article
from textblob import TextBlob

# DEFINE TYPICAL SPACY PIPELINE
nlp = spacy.load("en_core_web_lg")

# MODIFY PIPELINE SO THAT IT INCLUDES THE TEXTRANK ALGORITHM
nlp.add_pipe("textrank")

# STORE EXAMPLE TEXT AS A STRING
example_text = """Deep learning is part of a broader family of machine learning methods, which is based on artificial 
neural networks with representation learning. The adjective "deep" in deep learning refers to the use of multiple 
layers in the network. Methods used can be either supervised, semi-supervised or unsupervised. Deep-learning 
architectures such as deep neural networks, deep belief networks, deep reinforcement learning, recurrent neural 
networks, convolutional neural networks and transformers have been applied to fields including computer vision, 
speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image 
analysis, climate science, material inspection and board game programs, where they have produced results comparable 
to and in some cases surpassing human expert performance. Artificial neural networks (ANNs) were inspired by 
information processing and distributed communication nodes in biological systems. ANNs have various differences from 
biological brains. Specifically, artificial neural networks tend to be static and symbolic, while the biological 
brain of most living organisms is dynamic (plastic) and analog."""

example_text = example_text.lower()

# RUN THE SPACY PIPELINE WITH TEXTRANK ALGORITHM
doc = nlp(example_text)

# SHOW TEXT SUMMARY
for sentence in doc._.textrank.summary(limit_phrases=2, limit_sentences=3):
    print(sentence)
    print('-'*100)

print("Phrases and Ranks")
phrases_and_ranks = [(phrase.chunks[0], phrase.rank)for phrase in doc._.phrases]
print(phrases_and_ranks[:10])
