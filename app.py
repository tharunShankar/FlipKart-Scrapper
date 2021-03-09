# doing necessary imports
import threading
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
from mongoDBOperations import MongoDBManagement
from FlipkratScrapping import FlipkratScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

rows = {}
collection_name = None

app = Flask(__name__)  # initialising the flask app with the name 'app'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


class threadClass:

    def __init__(self, expected_review, searchString, scrapper_object, review_count):
        self.expected_review = expected_review
        self.searchString = searchString
        self.scrapper_object = scrapper_object
        self.review_count = review_count
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name
        collection_name = self.scrapper_object.getReviewsToDisplay(expected_review=self.expected_review,
                                                                   searchString=self.searchString, username='Kavita',
                                                                   password='kavita1610',
                                                                   review_count=self.review_count)

@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
        expected_review = int(request.form['expected_review'])
        try:
            review_count = 0
            scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
            db_name = 'Flipkart-Scrapper'
            scrapper_object.openUrl("https://www.flipkart.com/")
            scrapper_object.login_popup_handle()
            scrapper_object.searchProduct(searchString=searchString)
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                reviews = [i for i in response]
                if len(reviews) > expected_review:
                    result = [reviews[i] for i in range(0, expected_review)]
                    scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv", dataframe=pd.DataFrame(reviews))
                    return render_template('results.html', rows=result)  # show the results to user
                else:
                    review_count = len(reviews)
                    threadClass(expected_review=expected_review, searchString=searchString,
                                scrapper_object=scrapper_object, review_count=review_count)

                    return redirect(url_for('feedback'))
            else:
                threadClass(expected_review=expected_review, searchString=searchString, scrapper_object=scrapper_object,
                            review_count=review_count)
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    try:
        global collection_name
        print(collection_name)
        if collection_name is not None:
            scrapper_object = FlipkratScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
            rows = mongoClient.findAllRecords(db_name="Flipkart-Scrapper", collection_name=collection_name)
            reviews = [i for i in rows]
            scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv", dataframe=pd.DataFrame(reviews))
            return render_template('results.html', rows=reviews)
        else:
            return render_template('results.html', rows=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))


if __name__ == "__main__":
    app.run()  # running the app on the local machine on port 8000
