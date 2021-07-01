from .functions import Rating, Parallelize
import pandas as pd
from functools import partial
from datetime import datetime

import openpyxl
import pymongo
import logging

from bson.objectid import ObjectId

from app import config

logger = logging.getLogger(__name__)

mongo_client = pymongo.MongoClient(config.mongo_url, username=config.mongo_user,
                                   password=config.mongo_password, ssl=True,
                                   ssl_cert_reqs='CERT_NONE', serverSelectionTimeoutMS=3000)
nlp_db = mongo_client[config.mongo_db_name]


def create_quotes_db():
    """ This method is responsile for loading quotes from excel to Mongo """

    try:
        quotes_col = nlp_db[config.mongo_quotes_coll]
        quotes_col.insert_many(list(read_excel().values()))
        print ("Completed work ", datetime.now())
    except Exception as ex:
        logger.error("Error storing to mongodb", exc_info=True)

def read_excel():
    """ This method is responsible for reading quotes excel file 
        and storing records in mongodb """

    print ("Going to work ", datetime.now())
    file_name = "Motivational Quotes Database.xlsx"
    
    try:
        wb = openpyxl.load_workbook(file_name)
        sheet = wb.active

        data = {}
        rating = Rating()
        for row in sheet.rows:
            if (row[0].value is not None and row[1].value is not None and
                    row[2].value is not None and row[0].value != 'Quotes'):
                id = ObjectId()
                quote = row[0].value

                sen_rating = rating.sentiment_rating(quote)
                sen_entity = rating.entity_rating(quote)
                
                data[id] = {
                    "_id": id,
                    "quote": quote,
                    "author": row[1].value,
                    "tag": [row[2].value.strip()],
                    "rating": 0.0,
                    "rating": rating.rating['rating_test'],
                    "sentiment": rating.rating['sentiment'],
                    "entities": rating.rating['entities']
                }
                del quote, sen_rating, sen_entity
    finally:
        wb.close()

    print("Finished file reading ", datetime.now(), ", records read ", len(data))
    return data


def fetch_all_quotes():
    quotes_col = nlp_db[config.mongo_quotes_coll]

    return list(quotes_col.find())


def fetch_quotes_by_author(author):
    quotes_col = nlp_db[config.mongo_quotes_coll]

    return list(quotes_col.find({"author": author}))

def fetch_quotes_by_ratings(quote, count=5):

    sen_score = Rating.sentence_scores(quote)
    sen_rating = sen_score["rating"]
    logger.debug(f'Rating for quote  {quote} is {sen_score}')
    quotes_col = nlp_db[config.mongo_quotes_coll]

    result = quotes_col.aggregate([
        {
            '$project': {
                'diff': {
                    '$abs': {
                        '$subtract': [
                            sen_rating, '$rating'
                        ]
                    }
                },
                "doc": "$$ROOT"
            }
        }, {
            '$sort': {
                'diff': 1
            }
        }, {
            '$limit': count
        }
    ])
    return list(result)

def test_db():
    return mongo_client.test


if __name__ == "__main__":
    # for a in fetch_quotes_by_author("Mark Twain"):
    #     print(a)
    #create_quotes_db()

    print(fetch_quotes_by_ratings("I am very sad today"))

    ############## Parallelizing rating calc section (for all db items at one time) #############
    # def custom_sentiment_entity(group, cls):
    #     results = list()
    #     for text in group:
    #         results.append((cls.sentiment_rating(
    #             text), cls.entity_rating(text)))
    #     return results

    # process_rating = Rating()
    # f = partial(custom_sentiment_entity, cls=process_rating)
    # quotes = process_rating.get_sentences(
    #     pd.Series([data for data in fetch_all_quotes()]))
    # quotes = process_rating.get_sentences(df['quotes'])
    # parallelize = Parallelize(8, 125, f)
    # results = parallelize.execute(quotes)
    # del process_rating
    ###################################################################################
