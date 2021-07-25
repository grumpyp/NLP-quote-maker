import nltk
from nltk import sentiment
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from spacy import displacy
from spacy.util import minibatch
from collections import Counter
import pandas as pd
from joblib import Parallel, delayed
from app import config
import requests

# to get the corpora of the libraries please run these commands once in your terminal
# python -m nltk.downloader vader_lexicon
# python -m spacy download en_core_web_sm
# python -m spacy download en


class Parallelize():
    '''
    Creates a parallelizable object for executing customized functions
    Properties:
    - fn: function to include for parallelizing
    - cls_obj: instanced object containing 
    For Parallel class object properties (for more info, please check joblib's Parallel doc info)
    - n_jobs = # of allowable computing processors (-1 indicates use all available processors)
    - backend: parallelization backend implementation - supported are:  'loky' (default), 'multiprocessing', 'threading'
    - prefer: process to support backend function - supported are:  None (default for loky), 'processes' (for multiprocessing), 'threads' (for threading)
    - batch_size: # of tasks to dispatch at once to each worker - 'auto' (default for class's internal heuristic to determine optimal performance), int for own size
    Note: please override existing Parallel properties to suit your computer processing properties before running "execute" method.
    '''
    backend = 'loky'
    prefer = None
    batch_size = 'auto'

    def __init__(self, n_jobs, n_batch_size, fn):
        self.n_jobs = n_jobs
        self.n_batch_size = n_batch_size
        self.fn = fn

    def _setup(self):
        self.delayed = delayed(self.fn)
        self.executor = Parallel(n_jobs=self.n_jobs, backend=self.backend,
                                 prefer=self.prefer, batch_size=self.batch_size)

    def execute(self, data):
        self._setup()
        tasks = (self.delayed(text_chunk)
                 for text_chunk in minibatch(data, size=self.n_batch_size))
        result = self.executor(tasks)
        return result


class Rating():

    nlp_load = spacy.load('en_core_web_sm')
    
    def __init__(self):
        self.rating = {}
        self.sia = SentimentIntensityAnalyzer()

    def _get_sentences(self, sentence):
        if isinstance(sentence, pd.Series):
            self.input = sentence.values
        else:
            self.input = sentence

    def get_ratings(self, sentence):
        self._get_sentences(sentence)
        self.sentiment_rating(sentence)
        self.entity_rating(sentence)
        self.check_rating()

    def sentiment_rating(self, sentence):
        self.sentiment_scores = self.sia.polarity_scores(sentence)
        self.rating["sentiment"] = self.sentiment_scores
        self.rating["rating_test"] = Rating.compute_ratings(self.sentiment_scores)
        return self.sentiment_scores

    def entity_rating(self, sentence):
        self.nlp = self.nlp_load(sentence)
        self.entities = [ent.label_ for ent in self.nlp.ents]
        self.rating["entities"] = self.entities
        return [(ent.text, ent.label_) for ent in self.nlp.ents]

    def check_rating(self):
        print(self.rating)

    @staticmethod
    def compute_ratings(sentiment_scores):
        """ This method computes ratings on the basis of input scores """

        return sentiment_scores["neg"] * -1 + \
            sentiment_scores["neu"] * 0.3 + sentiment_scores["pos"] 

    @staticmethod
    def sentence_rating(sentence):
        """ This method computes ratings of the input sentence. 
            It returns rating value"""

        sa = SentimentIntensityAnalyzer()
        sentiment_scores = sa.polarity_scores(sentence)
        rating = Rating.compute_ratings(sentiment_scores)
        return rating
    
    @staticmethod
    def sentence_scores(sentence):
        """ This method computes ratings of the input sentence. 
            It returns sentiment scores and rating value"""

        sa = SentimentIntensityAnalyzer()
        sentiment_scores = sa.polarity_scores(sentence)
        rating = Rating.compute_ratings(sentiment_scores)
        sentiment_scores["rating"] = rating
        return sentiment_scores

    @staticmethod
    def sentence_entities(sentence):
        """ This method fetches entities from input sentence.
            It returns array of entity text and label """


        nlp = Rating.nlp_load(sentence)
        return [(ent.text, ent.label_) for ent in nlp.ents]

def reddit_quote():
    auth = requests.auth.HTTPBasicAuth(config.reddit_id, config.reddit_secret)

    data = {'grant_type': 'password',
        'username': config.reddit_user,
        'password': config.reddit_pw}
    headers = {'User-Agent': 'NLP-quote-maker'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    res = requests.get("https://oauth.reddit.com/r/quoteporn/new",
                   headers=headers, params={'limit':10})
    result_num = 0
    result_quote = ""
    for count,i in enumerate(res.json()['data']['children']):
        if count == 0:
            result_num = int(i['data']['score'])
        if i['data']['score']:
            print(i['data']['title'])
            if int(i['data']['score']) > result_num:
                result_num = int(i['data']['score'])
                result_quote = i['data']['title']
    return result_quote


if __name__ == '__main__':
    rater = Rating()
    sentence = "Apple is looking at buying U.K. startup for $1 billion it would be a huge win for the company"
    sent2 = "Today I am super sad because of work"
    sent3 = "I am happy because it is the weekend"
    sent4 = "I earned a big bonus today"
    sent5 = "I bought myself a new phone which made me quite happy"
    print(sentence)
    rater.get_ratings(sentence)
    print(sent2)
    rater.get_ratings(sent2)
    print(sent3)
    rater.get_ratings(sent3)
    print(sent4)
    rater.get_ratings(sent4)
    print(sent5)
    rater.get_ratings(sent5)

    print("------------quotes----------")
    quote1 = "Envy of other people shows how they are unhappy. Their continual attention to others behavior shows how they are boring."
    quote2 = "Society tames the wolf into a dog. And man is the most domesticated animal of all."
    quote3 = "There comes a point where we need to stop just pulling people out of the river. We need to go upstream and find out why they’re falling in"
    quote4 = "Don’t postpone joy until you have learned all of your lessons. Joy is your lesson"
    quote5 = "Imagine how you want to feel at the end of the day. Start working towards that now."

    print(quote1)
    rater.get_ratings(quote1)
    print(quote2)
    rater.get_ratings(quote2)
    print(quote3)
    rater.get_ratings(quote3)
    print(quote4)
    rater.get_ratings(quote4)
    print(quote5)
    rater.get_ratings(quote5)