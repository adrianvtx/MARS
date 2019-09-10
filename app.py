from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import scrape_mars
import os


app = Flask(__name__)

output_dict = {}
# Use flask_pymongo to set up mongo connection
MongoClient("mongodb://127.0.0.0:27017")# = "mongoclient://localhost:27017/output_dict.mymongodb"
db = output_dict

# mongo = pymongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    data_db = mongo.db.listings.find_one()
    return render_template('index.html', listings=data_db)


@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    mars_data = scrape_mars.scrape()
    listings.update({}, mars_data, upsert=True)
    # for row in listings_data:
    #     listings.update({'headline' : row['headline']}, row, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
