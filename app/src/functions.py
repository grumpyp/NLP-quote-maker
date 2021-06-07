import nltk
from nltk import sentiment
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from spacy import displacy
from collections import Counter


#to get the corpora of the libraries please run these commands once in your terminal
#python -m nltk.downloader vader_lexicon
#python -m spacy download en_core_web_sm
#python -m spacy download en

def sentiment_rating(sentence):
    tokenize = nltk.word_tokenize
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(sentence)
    return sentiment_scores

def entity_rating(sentence):
    nlp_load = spacy.load('en_core_web_sm')
    nlp = nlp_load(sentence)
    return [(ent.text, ent.label_) for ent in nlp.ents]



if __name__ == '__main__':

    print(sentiment_rating("This girl is really demanding but I like her more or less"))
    print(entity_rating("Apple is looking at buying U.K. startup for $1 billion"))

