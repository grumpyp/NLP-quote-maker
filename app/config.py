import os

mongo_user = os.getenv("mongouser")
mongo_password = os.getenv("mongopassword")
reddit_secret = os.environ['REDDIT_SECRET']
reddit_id = os.environ['REDDIT_ID']
reddit_user = os.environ['REDDIT_USER']
reddit_pw = os.environ['REDDIT_PW']

production = True
log_file = "app.log"
mongo_url = "mongodb+srv://cluster0.vzoak.mongodb.net/?retryWrites=true&w=majority"
mongo_db_name = "nlp_quotes"
mongo_quotes_coll = "quotes"