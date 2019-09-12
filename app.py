import os
import string
import sys

import html5lib
import html5lib.html5parser
import pymongo
import pymongo.mongo_client
from bson import ObjectId  # For ObjectId to work
from eve.io.mongo.flask_pymongo import PyMongo
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from prettytable import from_html
from pymongo import MongoClient
from pymongo.collection import Collection
from werkzeug.debug.tbtools import render_console_html

import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# connect to mongo db and collection
# db = mongo.mars_db
# collection = db.scrape
output_dict = {}
output_dict["collection"] = "Please Press Scrape"


@app.route('/')
def index():
    output_dict = mongo.db.output_dict.find_one()
    # renderOut = list(mongo.db.collection.find_one())
    # print(data_db)
    landImage = "static/mission_to_mars.png"
    return render_template('index.html', output_dict=output_dict)

@app.route("/scrape")
def scrape():
    output_dict = mongo.db.output_dict
    data1 = scrape_mars.scrape()
    output_dict.update(
        {},
        data1, 
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
