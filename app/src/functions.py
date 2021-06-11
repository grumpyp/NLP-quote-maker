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

class rating():
    def __init__(self, sentence):
        self.sentence = sentence
        self.rating = {}
        self.sentiment_rating(sentence)
        self.entity_rating(sentence)
        self.check_rating()


    def sentiment_rating(self,sentence):
        self.tokenize = nltk.word_tokenize
        self.sia = SentimentIntensityAnalyzer()
        self.sentiment_scores = self.sia.polarity_scores(sentence)
        self.rating["sentiment"] = self.sentiment_scores
        self.rating["rating_test"] = self.sentiment_scores["neg"] * -1 + self.sentiment_scores["neu"] * 0.3 + self.sentiment_scores["pos"] 
        return self.sentiment_scores

    def entity_rating(self,sentence):
        self.nlp_load = spacy.load('en_core_web_sm')
        self.nlp = self.nlp_load(sentence)
        self.entities = [ent.label_ for ent in self.nlp.ents]
        self.rating["entities"] = self.entities
        return [(ent.text, ent.label_) for ent in self.nlp.ents]
    
    def check_rating(self):
        print(self.rating)



if __name__ == '__main__':
    sentence = "Apple is looking at buying U.K. startup for $1 billion it would be a huge win for the company"
    sent2 = "Today I am super sad because of work"
    sent3 = "I am happy because it is the weekend"
    sent4 = "I earned a big bonus today"
    sent5 = "I bought myself a new phone which made me quite happy"
    print(sentence)
    rating(sentence)
    print(sent2)
    rating(sent2)
    print(sent3)
    rating(sent3)
    print(sent4)
    rating(sent4)
    print(sent5)
    rating(sent5)

    print("------------quotes----------")
    quote1 = "Envy of other people shows how they are unhappy. Their continual attention to others behavior shows how they are boring."
    quote2 = "Society tames the wolf into a dog. And man is the most domesticated animal of all."
    quote3 = "There comes a point where we need to stop just pulling people out of the river. We need to go upstream and find out why they’re falling in"
    quote4 = "Don’t postpone joy until you have learned all of your lessons. Joy is your lesson"
    quote5 = "Imagine how you want to feel at the end of the day. Start working towards that now."

    print(quote1)
    rating(quote1)
    print(quote2)
    rating(quote2)
    print(quote3)
    rating(quote3)
    print(quote4)
    rating(quote4)
    print(quote5)
    rating(quote5)



    #print(sentiment_rating("This girl is really demanding but I like her more or less"))
    #print(entity_rating("Apple is looking at buying U.K. startup for $1 billion"))

