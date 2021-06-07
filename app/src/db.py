from .functions import *

import openpyxl
import pymongo
import logging

from bson.objectid import ObjectId

import config

logger = logging.getLogger(__name__)

mongo_client = pymongo.MongoClient(config.mongo_url, ssl=True, ssl_cert_reqs='CERT_NONE')
nlp_db = mongo_client[config.mongo_db_name]

#this method is responsible for loading "quotes" collection
def create_quotes_db():

    try:
        quotes_col = nlp_db[config.mongo_quotes_coll] 
        quotes_col.insert_many(list(read_excel().values()))
    except Exception as ex:
        logger.error("Error storing to mongodb", exc_info=True)
        
#this method is responsible for reading quotes excel file and storing
#records in mongodb
def read_excel():
    file_name = "Motivational Quotes Database.xlsx"
    try:
        wb = openpyxl.load_workbook(file_name) 
        sheet = wb.active

        data = {}
        for row in sheet.rows:
            if (row[0].value is not None and row[1].value is not None and
            row[2].value is not None and row[0].value != 'Quotes'):
                id = ObjectId()
                data[id] = {
                    "_id": id,
                    "quote": row[0].value,
                    "author": row[1].value,
                    "tag": [row[2].value.strip()],
                    "rating": float(0.0)
                }
    finally:
        wb.close()

    return data

def fetch_all_quotes():
    quotes_col = nlp_db[config.mongo_quotes_coll]
    
    return quotes_col.find()

def fetch_quotes_by_author(author):
    quotes_col = nlp_db[config.mongo_quotes_coll]
    
    return quotes_col.find({"author": author})

if __name__ == "__main__":
    for a in fetch_all_quotes():
        print(a)
