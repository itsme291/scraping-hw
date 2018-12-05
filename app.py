#!/usr/bin/env python
# coding: utf-8

# Dependencies
from splinter import Browser
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


@app.route("/scrape")
def scrape_data():
    #get mars data dictionary
    scraped_data = scrape_mars.scrape()    
    db = client.mars
    collection = db.mars_data
    collection.delete_many({})
    collection.insert(scraped_data)
    return redirect("/", code=302)

@app.route("/")
def index():
    db = client.mars
    collection = db.mars_data
    data = collection.find_one()
    print(data)
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)