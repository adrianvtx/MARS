import os
import sys

from bson import ObjectId  # For ObjectId to work
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo

import Homework.scrape_mars

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
app = Flask(__name__)

app.config.from_object(os.environ['PythonData'])

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
# client = PyMongo.MongoClient(conn)


# setup mongo connection
conn = "mongodb://localhost:27017"
client = PyMongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.scrape
output_dict = {}


@app.route("/")
def index():
    # data_db = mongo.db.output_dict.find_one()
    renderOut = list(collection.find())
    print(renderOut)
    return render_template('index.html', renVars=renderOut)


@app.route("/scrape")
def scrape():
    
    # db = mongo.mars_db
    output_dict = Homework.scrape_mars.scrape()
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
