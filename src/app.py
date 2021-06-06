from flask import Flask
import config
import functions

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__' and config.production == True:
    app.run()