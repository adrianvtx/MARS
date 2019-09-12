import os
import sys

import pymongo
import pymongo.mongo_client
from bson import ObjectId  # For ObjectId to work
# from eve.io.mongo.flask_pymongo import PyMongo
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.collection import Collection

import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# connect to mongo db and collection
# db = mongo.mars_db
# collection = db.scrape
output_dict = {}

@app.route("/")
def index():
    # data_db = mongo.db.output_dict.find_one()
    renderOut = list(mongo.db.collection.find_one())
    # print(data_db)
    print(renderOut)
    return render_template('index.html', renVars=renderOut)

@app.route("/scrape")
def scrape():
    
    db = mongo.mars_db
    listings = mongo.db.listings

    output_dict = scrape_mars.scrape()
    mongo.db.collection.update({}, output_dict, upsert=True)

    return redirect("/", code=302)

    # for row in listings_data:
    #     listings.update({'headline' : row['headline']}, row, upsert=True)
# Verify results:
# results = db.fruits_db.find()
# for result in results:
#     print(result)



if __name__ == "__main__":
    app.run(debug=True)
