# doing necessary imports

from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS, cross_origin
import requests
from mongoDBOperations import MongoDBManagement
from FlipkratScrapping import FlipkratScrapper
from selenium import webdriver
from RepositoryForObject import ObjectRepository
import pymongo
import json

app = Flask(__name__)  # initialising the flask app with the name 'app'

chrome_option = webdriver.ChromeOptions()

chrome_option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_option.add_argument("--headless")
chrome_option.add_argument("--no-sandbox")
chrome_option.add_argument("--disable-dev-sh-usage")


def review(searchString, expected_review):
    try:
        scrapper_object = FlipkratScrapper(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                           chrome_options=chrome_option)
        mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
        url = "https://www.flipkart.com/"
        db_name = 'Flipkart-Scrapper'
        scrapper_object.openUrl(url=url)
        scrapper_object.login_popup_handle()
        scrapper_object.searchProduct(searchString=searchString)

        scrapper_object.getLinkForExpectedReviewCount(searchString=searchString,
                                                      expected_review=expected_review)
        product_name = scrapper_object.getProductName()
        product_searched = scrapper_object.getProductSearched(search_string=searchString)
        price = scrapper_object.getPrice()
        offer_details = scrapper_object.getOfferDetails()
        discount_percent = scrapper_object.getDiscountedPercent()
        EMI = scrapper_object.getEMIDetails()
        response = scrapper_object.getReviewDetailsForProduct(expected_review=expected_review)
        result = scrapper_object.generatingResponse(product_name=product_name,
                                                    product_searched=product_searched, price=price,
                                                    discount_percent=discount_percent, EMI=EMI,
                                                    offer_details=offer_details, result=response)
        scrapper_object.closeConnection()
        dataframe = scrapper_object.createDataFrameIncludingAllColumn(response=result)

        scrapper_object.saveDataFrameToFile(dataframe=dataframe, file_name='ScrappedData.csv')

        mongoClient.saveDataFrameIntoCollection(collection_name=searchString, db_name=db_name,
                                                dataframe=dataframe)

        reviews = mongoClient.getResultToDisplayOnBrowser(db_name=db_name, collection_name=searchString)

        return reviews
    except Exception as e:
        raise Exception(f"(review) - Something went wrong on review.\n" + str(e))
    pass


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
        expected_review = int(request.form['expected_review'])
        # executable_path = os.environ.get("CHROMEDRIVER PATH")
        try:
            # locator = ObjectRepository()
            # driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='Kavita', password='kavita1610')
            db_name = 'Flipkart-Scrapper'
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                response = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                reviews = [i for i in response]
                if len(reviews) > 500:
                    return render_template('results.html', result=reviews)  # show the results to user
                else:
                    reviews = review(searchString, expected_review)
                    return render_template('results.html', result=reviews)
            else:
                reviews = review(searchString, expected_review)
                return render_template('results.html', result=reviews)  # showing the review to the user

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)  # running the app on the local machine on port 8000
