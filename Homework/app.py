from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def home():
    data_db = mongo.db.collection()
    return render_template("index.html", dict=data_db)


@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    listings_data = scrape_mars.scrape()
    # listings.update({}, listings_data, upsert=True)
    for row in listings_data:
        listings.update({'headline' : row['headline']}, row, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
