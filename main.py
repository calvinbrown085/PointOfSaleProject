from flask import Flask, render_template, request, redirect, session
from Database import Database
import sqlite3
from UserLoginPackage import login,logout,requireLogin
from DatabaseUtils import *
from OneOffInventoryLog import *
db = Database()
app = Flask(__name__)

app.config.update(dict(
    # DEBUG=True,
    SECRET_KEY='A Very Very Secret Key'))
@app.route("/")
def singleSlash():
    if (not session.get("logged_in")):
        return redirect("/login")
    else:
        return redirect("/index")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/form", methods=["POST"])
def form():
    email = request.form["email"]
    db.storeEmail(email)

    return redirect("/")

@app.route("/writeEmail", methods=["POST"])
def writeEmail():
    newCustomer(str(request.form["customer_name"]),str(request.form["customer_email"]))

@app.route("/writeTransaction", methods=["POST"])
def writeTransaction():
    return "This is a stub to be filled in later"

@app.route("/writeNewInventoryItem", methods=["POST"])
def writeNewInventoryItem():
    return "This is a stub to be filled in later"


@app.route("/searchInventoryById", methods=["POST"])
def searchById():
    results = [db.getById(str(request.form["idSearch"]))]
    return render_template("searchResults.html", results = results)

@app.route("/searchInventoryByName", methods=["POST"])
def searchByName():
    results = [db.getByName(str(request.form["nameSearch"]))]
    return render_template("searchResultsByName.html", results = results)

@app.route("/searchEmailsByName", methods=["POST"])
def searchEmailsByName():
    results = [db.getUser(str(request.form["emailNameSearch"]))]
    results = results[0]
    print(results)
    return render_template("searchResultsByName.html", results = results)

@app.route("/pos")
def posTest():
    print("test")

    return render_template("POS.html")

@app.route("/inventory")
def inventory():
    return render_template("inventory.html", items = db.getItems())

@app.route("/emailList")
def emails():
    return render_template("emailList.html", items = db.getEmailsInSystem())


@app.route("/login", methods=["GET","POST"])
def signIn():
    return login(db)

@app.route("/logout")
def signOut():
    return logout()

@app.route("/secret")
def secret():
    requireLogin()
    return "Logged in!!"

@app.route("/methodOfPayment")
def payment():
    return "Stub implementation"


if (__name__ == "__main__"):
    app.run()
