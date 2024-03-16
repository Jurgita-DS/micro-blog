import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv


# Populates environment variables with values from .env file
load_dotenv()


# Flask app factory function
def create_app():
    app = Flask(__name__)
    # Mango cluster connection
    client = MongoClient(os.getenv("MANGODB_URI"))
    # Connect to Mango microblog database
    app.db = client.microblog



    @app.route("/", methods = ["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b-%d")
            )
            for entry in app.db.entries.find({}) # Return everything in entries collection
        ]    
        return render_template("home.html", entries = entries_with_date)
    
    return app    