import os

mongo_user = os.getenv("mongouser")
mongo_password = os.getenv("mongopassword")

production = True
log_file = "app.log"
mongo_url = "mongodb+srv://cluster0.vzoak.mongodb.net/?retryWrites=true&w=majority"
mongo_db_name = "nlp_quotes"
mongo_quotes_coll = "quotes"