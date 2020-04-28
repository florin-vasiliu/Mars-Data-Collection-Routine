#Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

#Create an instance of the Flask app
app = Flask(__name__)

#connection path
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

@app.route('/')
def index():
    mars_latest_info=db.mars.find_one()
    print(mars_latest_info)

    return render_template('index.html', mars_latest_info=mars_latest_info)

@app.route("/scrape")
def scraper():
    scrape_mars.scrape_and_store()
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)