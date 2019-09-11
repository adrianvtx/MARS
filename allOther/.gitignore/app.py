from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/output_dict"
mongo = pymongo(app)
client = pymongo.MongoClient(conn)

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
