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
    #DEBUG=True,
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
    return render_template("checkout.html", results = session.get("resultList"), totalPrice = session.get("totalAmount"))

@app.route("/payment")
def payment():
    cash = request.args.get('cashAmount')
    cardNumber = request.args.get('cardNumber')
    exp = request.args.get('exp')
    cvv = request.args.get('CVV')
    itemList = []
    paymentMethod = ""
    if(cash != None):
        paymentMethod = "Cash"
    elif(cardNumber != None):
        paymentMethod = "Credit"
    for item in session.get("resultList"):
        itemList.append(item[1])
    newString = listToString(itemList)[2:]
    newTransaction(paymentMethod,session.get("totalAmount"),newString)
    for item in session.get("resultList"):
        db.sellItem(item[0],item[2])
        db.updateInventoryLog(item[0],item[2])

    session["resultList"] = []
    session["totalAmount"] = 0.00
    session["searchList"] = []
    return redirect("/pos")


@app.route("/search")
def search():
    userInput = request.args.get('ItemNumber')
    userInput = userInput.title()
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
    userInput = userInput.title()
    session["managerSearchList"] = []
    if(searchType == "Name"):
        query = db.getByName(str(userInput))
        session["managerSearchList"] = session.get("managerSearchList") + addToManagerSearchQuery(query)
    elif(searchType == "ProductID"):
        query = db.getById(str(userInput))
        session["managerSearchList"] = session.get("managerSearchList") + addToManagerSearchQuery(query)
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


@app.route("/managerUpdate")
def managerUpdate():
    productId = request.args.get('productId')
    name = request.args.get('Name')
    purchasePrice = request.args.get('purchasePrice')
    sellingPrice = request.args.get('sellingPrice')
    seller = request.args.get('Seller')
    productType = request.args.get('productType')
    amountInStock = request.args.get('amountInStock')
    item = db.getById(int(productId))

    if(item == []):

        db.insertNewInventoryItem(int(productId),name,float(purchasePrice),float(sellingPrice),seller,productType,int(amountInStock))
    elif(productId == ""):
        print("Ethan please put an error here")
    if(name == ""):
        name = db.getById(productId)[0][0]

    if(purchasePrice == ""):
        purchasePrice = db.getById(int(productId))[0][2]

    if(sellingPrice == ""):
        sellingPrice = db.getById(productId)[0][3]

    if(seller == ""):
        seller = db.getById(productId)[0][4]

    if(productType == ""):
        productType = db.getById(productId)[0][5]

    if(amountInStock == ""):
        amountInStock = db.getById(productId)[0][6]
    db.updateInventoryItem(name,int(productId),float(purchasePrice),float(sellingPrice),seller,productType,int(amountInStock))
    return redirect("/managerPage")

@app.route("/transactions")
def transactions():
    print(db.getTransactions())
    return render_template("transactions.html", transactions = db.getTransactions())


if (__name__ == "__main__"):
    app.run()
