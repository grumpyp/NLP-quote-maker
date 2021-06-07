from flask import Flask
from app.views import view
from app import config
from app.src.functions import sentiment_rating

app = Flask(__name__)

app.register_blueprint(view)

if __name__ == '__main__' and config.production == True:
    app.run()
