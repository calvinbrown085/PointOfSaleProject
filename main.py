from flask import Flask, render_template, request, redirect, session
from Database import Database
from UserLoginPackage import *
from DatabaseUtils import *
import os

db = Database()
app = Flask(__name__)

resultList = []
totalAmount = 0
products = []

app.config.update(dict(
    # DEBUG=True,
    SECRET_KEY= os.environ["Key"]))

@app.route("/")
def singleSlash():
    if (not session.get("logged_in")):
        return redirect("/login")
    else:
        return redirect("/index")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/managerPage")
def managerPage():
    return render_template("Managerpage.html", items = session.get("managerSearchList"),results = db.getItemsWithLowInventory())

@app.route("/form", methods=["POST"])
def form():
    email = request.form["email"]
    db.storeEmail(email)
    return redirect("/")

@app.route("/writeEmail", methods=["POST"])
def writeEmail():
    newCustomer(str(request.form["customer_name"]),str(request.form["customer_email"]))
    return redirect("/")

@app.route("/writeTransaction", methods=["POST"])
def writeTransaction():
    return "This is a stub to be filled in later"

@app.route("/writeNewInventoryItem", methods=["POST"])
def writeNewInventoryItem():
    return "This is a stub to be filled in later"

@app.route("/searchInventoryById", methods=["POST"])
def searchById():
    results = db.getById(str(request.form["idSearch"]))
    return render_template("searchResults.html", results = results)

@app.route("/searchInventoryByName", methods=["POST"])
def searchByName():
    results = db.getByName(str(request.form["nameSearch"]))
    return render_template("searchResults.html", results = results)

@app.route("/searchEmailsByName", methods=["POST"])
def searchEmailsByName():
    results = db.getUser(str(request.form["emailNameSearch"]))
    return render_template("emailSearchResults.html", results = results)

@app.route("/inventory")
def inventory():
    requireLogin()
    return render_template("inventory.html", items = db.getItems())

@app.route("/emailList")
def emails():
    return render_template("emailSearchResults.html", results = db.getEmailsInSystem())

@app.route("/login", methods=["GET","POST"])
def signIn():
    return login(db)

@app.route("/logout")
def signOut():
    return logout()

@app.route("/secret")
def secret():
    requireLogin()
    print(session.get("logged_in"))
    return "Logged in!!"

@app.route("/superSecret")
def superSecret():
    requireManagerLogin(db)
    print(session.get("logged_in"))
    return "Manager Logged in!!"

@app.route("/pos")
def pos():
    requireLogin()
    return render_template("POS.html", results = session.get("resultList"),totalPrice = session.get("totalAmount"), searchResults = session.get("searchList"))

@app.route("/cart", methods=["POST"])
def cart():
    requireLogin()
    itemNumber = request.form["ItemNumber"]
    searchResult = db.getById(int(itemNumber))
    if (searchResult == [] or request.form["quantity"] == ""):
        return redirect("/pos")
    name = searchResult[0][0]
    quantity = request.form["quantity"]
    price = searchResult[0][3] * int(quantity)
    itemList = [itemNumber, name, quantity, str(price)]
    session["resultList"] = session.get("resultList") + [itemList]
    session["totalAmount"] = str(getTotalPrice(session.get("resultList")))
    return redirect("/pos")

@app.route("/checkout")
def checkout():
    return "This will be the checkout page"

@app.route("/methodOfPayment")
def payment():
    return "Stub implementation"

@app.route("/search")
def search():
    userInput = request.args.get('ItemNumber')
    searchBy = request.args.get('items')
    session["searchList"] = []
    if (searchBy == "price"):
        query = db.getItemsByPrice(str(userInput))
        session["searchList"] = session.get("searchList") + addToSearchQuery(query)
    elif (searchBy == "id"):
        query = db.getById(str(userInput))
        session["searchList"] = session.get("searchList") + addToSearchQuery(query)
    elif (searchBy == "name"):
        query = db.getByName(str(userInput))
        session["searchList"] = session.get("searchList") + addToSearchQuery(query)
    elif (searchBy == "supply"):
        query = db.getBySupplier(str(userInput))
        session["searchList"] = session.get("searchList") + addToSearchQuery(query)

    return redirect("/pos")
@app.route("/profitReport")
def profitReport():
    requireLogin()
    return render_template("profitReport.html", report = generateReport())

@app.route("/managerSearch")
def managerSearch():
    searchType = request.args.get('ProductID')
    userInput = request.args.get('text')
    session["managerSearchList"] = []
    if(searchType == "Name"):
        query = db.getByName(str(userInput))
        session["managerSearchList"] = session.get("managerSearchList") + addToManagerSearchQuery(query)
    elif(searchType == "ProductID"):
        query = db.getById(str(userInput))
        session["managerSearchList"] = session.get("managerSearchList") + addToManageSearchQuery(query)
    return redirect("/managerPage")


@app.route("/createSale")
def createManagerSale():
    productId = request.args.get('productId')
    newSalePrice = request.args.get('newPrice')
    createSale(productId, newSalePrice)
    return redirect("/managerPage")


@app.route("/cartClear")
def clearCart():
    session["resultList"] = []
    session["totalAmount"] = 0.00
    return redirect("/pos")
if (__name__ == "__main__"):
    app.run()
