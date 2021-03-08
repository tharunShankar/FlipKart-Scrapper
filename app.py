# doing necessary imports

from flask import Flask, render_template, request, jsonify, Response
import os
from flask_cors import CORS, cross_origin
import requests
from mongoDBOperations import MongoDBManagement
from FlipkratScrapping import FlipkratScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from RepositoryForObject import ObjectRepository
import pymongo
import json

app = Flask(__name__)  # initialising the flask app with the name 'app'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
        expected_review = int(request.form['expected_review'])
        try:
            scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
            db_name = 'Flipkart-Scrapper'
            scrapper_object.openUrl("https://www.flipkart.com/")
            scrapper_object.login_popup_handle()
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                reviews = [i for i in response]
                if len(reviews) > expected_review:
                    return render_template('results.html', rows=reviews)  # show the results to user
                else:
                    scrapper_object.searchProduct(searchString=searchString)
                    actual_product = scrapper_object.actualProductLinks()
                    print(actual_product)
                    reviews = scrapper_object.getReviewsToDisplay(expected_review=expected_review,
                                                                  searchString=searchString, username='Kavita',
                                                                  password='kavita1610', links=actual_product)
                    return Response(stream_template('results.html', rows=reviews))
            else:
                scrapper_object.searchProduct(searchString=searchString)
                actual_product = scrapper_object.actualProductLinks()
                print(actual_product)
                reviews = scrapper_object.getReviewsToDisplay(expected_review=expected_review,
                                                              searchString=searchString, username='Kavita',
                                                              password='kavita1610', links=actual_product)
                return Response(stream_template('results.html', rows=reviews))  # showing the review to the user

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000
