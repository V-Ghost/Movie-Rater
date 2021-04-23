from flask import Flask, render_template, request, g
# from flask.ext.sqlalchemy import SQLAlchemy
import main_nltk
import logging
from logging import Formatter, FileHandler
import os
import requests
import json
import math
from omdbapi.movie_search import GetMovie
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db = SQLAlchemy(app)


class Movie(db.Model):
    imdbID = db.Column(db.String(80), primary_key=True)
    Title = db.Column(db.String(80), unique=False, nullable=False)
    Poster = db.Column(db.String(200), unique=True, nullable=False)
    Rating = db.Column(db.String(10), unique=False, nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Review = db.Column(db.String(80), unique=False, nullable=False)
    Rating = db.Column(db.String(10), unique=False, nullable=False)
    MovieID = db.Column(db.String(80), db.ForeignKey('movie.imdbID'),
                        nullable=False)
    Movie = db.relationship('Movie',
                            backref=db.backref('reviews', lazy=True))

# Uncomment this section and run main.py to create the database
# you need to do this ONLY ONCE    
# db.create_all()


def averageRating(movieId):
    payloads = Review.query.filter_by(MovieID=movieId).all()

    total_rating = 0
    count = 0
    for payload in payloads:
        count += 1
        total_rating = total_rating + int(payload.Rating)

    if(count == 0):
        return str(0)

    average_rating = total_rating/count

    average_rating = math.floor(average_rating)
    return str(average_rating)


@app.route('/')
def home():
    r = requests.get(
        'http://www.omdbapi.com/?apikey=[InsertAPIKeyHere]&s=harry&plot=short')
    movies = json.loads(r.text)['Search']
    names = []
    # Uncomment this section and run main.py to populate the database
    # you need to do this ONLY ONCE
    # for movie in movies:
    #     m =Movie(imdbID=movie['imdbID'],Title=movie['Title'],Rating="Not Avaliable",Poster=movie["Poster"])
    #     db.session.add(m)
    #     db.session.commit()

    return render_template('webpage/index.html', movies=movies)


@app.route('/review/<movieId>')
def review(movieId):

    payload = Movie.query.filter_by(imdbID=movieId).first()
    average_rating = averageRating(movieId)

    return render_template('webpage/review.html', movie=payload, rating=average_rating)


@app.route('/rate', methods=["POST"])
def rate():

    data = request.get_json()
    ratings = main_nltk.sentiment_analyse(data['comment'])

    r = Review(Review=data['comment'], Rating=ratings, MovieID=data['movieId'])
    db.session.add(r)
    db.session.commit()

    return ratings

    


app.run(debug=True)
