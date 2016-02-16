from flask import Flask, render_template, request, redirect
from Database import MyDatabase
import sqlite3
db = MyDatabase()
app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/form", methods=["POST"])
def form():
    email = request.form["email"]
    db.storeEmail(email)

    return redirect("/")

@app.route("/searchById", methods=["POST"])
def searchById():
    results = [db.getById(str(request.form["idSearch"]))]
    return render_template("searchResults.html", results = results)

@app.route("/searchByName", methods=["POST"])
def searchByName():
    results = [db.getByName(str(request.form["nameSearch"]))]
    return render_template("searchResults.html", results = results)

@app.route("/inventory")
def inventory():
    return render_template("inventory.html", items = db.getItems())

@app.route("/emailList")
def emails():
    return render_template("emailList.html", items = db.getEmailsInSystem())

if (__name__ == "__main__"):
    app.run()
