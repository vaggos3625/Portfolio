"""
Here we define the logic of our 
web-application: 
a.k.a. here lives the Flask application
"""

from flask import Flask, render_template, request
from movie_recommender_cosine import recommender_cosine
import pandas as pd

movies = pd.read_csv('/home/evangelo/Downloads/ml-latest-small/movies.csv')

# Flask main object that handles the web application and the server 
app = Flask(__name__)

@app.route("/") # <- routing with decorator: mapping Url to what is been displayed on the screen
def landing_page():
    random_5 = movies.title.sample(5)
    #return "Welcome to the Decisions recommender"
    return render_template("landing_page_cosine.html",
                           first_movie = random_5.iloc[0],
                           second_movie = random_5.iloc[1],
                           third_movie = random_5.iloc[2],
                           fourth_movie = random_5.iloc[3],
                           fifth_movie = random_5.iloc[4])


@app.route("/recommendation")
def recommendations_page():
    user_query = request.args.to_dict()
    user_query = {movie:float(rate) for movie, rate in user_query.items()}
    #for i,j in enumerate(list(user_query.keys())):
    #    user_query[random_5.index[i]] = user_query[j]
    #    del user_query[j]
    top5 = recommender_cosine(user_query)
    return render_template("recommendation_cosine.html",
                           movie_list=top5)

if __name__ == "__main__":
    # It starts up the 
    # in-built development Flask server  
    app.run(debug=True,port=5001)
