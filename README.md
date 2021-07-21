# NLP-quote-maker
A NLP driven script which will give you a quote according to the sentence you feed it. It pulls data from several API's and makes up a relation by f.e. sentiment of the sentence.

## Start-up
To run the app 
- Clone this repository `git clone git@github.com:grumpyp/NLP-quote-maker.git`
- Setup virtual environment __if required__ `python -m venv venv`
- Install requirements.txt `pip install -r requirements.txt`
- Run app with `python app\main.py`

## ⭐ Current features & Interface
- NLTK SentimentIntensityAnalyzer was used to gpositive/neutral/negative rating scores and normalized into a composite score.
- Entity labelling with spacy was used to attach one or more classes to each quote.
- A text box is provided for user input where text is assessed, rated, matched to existing quotes within a quote database, and outputted with associated rating score.

## 👾 Repo Setup 
Main branches containing all relevant files for use/development are found in the **deployment** and **development** branch respectively.  Proposed changes should be done and pulled on development branch first prior to merge with depolyment.

    app
    ├── src
    │   ├── db.py
    │   └── functions.py
    ├── static
    │   ├── css
    │   │   └── style.css
    │   └── js
    │       └── main.js
    ├── templates
    │   ├── index.html
    │   └── layout.html
    ├── config.py
    ├── main.py   
    └── views.py 


## Support & Contributing

Feature Requests? Please file an [issue](https://github.com/grumpyp/NLP-quote-maker/issues)

**I am happy to see all kind of contributions!**

## ToDo

- [x] Setup Flask environment
- [x] Deployment on Heroku
- [x] Build frontend with dynamic search field
- [x] Find API's for quotes
- [x] Use Twitter / Reddit API
- [x] Find features to do a rating of the sentence
- [x] Find suitable NLP libraries
- [x] Write inital readme
