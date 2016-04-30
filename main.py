from flask import Flask, render_template, request, redirect, session
from Database import Database
from UserLoginPackage import *
from DatabaseUtils import *
from SecretKeyGenerator import generateKey
import os
from Errors import *

db = Database()
app = Flask(__name__)

resultList = []
totalAmount = 0
products = []

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY= generateKey()))

@app.route("/")
def singleSlash():
    if (not session.get("logged_in")):
        return redirect("/login")
    else:
        if (db.getManagerStatus()[0][0] == 1):
            return redirect("/pos")
        else:
            return redirect("/managerPage")

@app.route("/managerPage")
def managerPage():
    requireManagerLogin(db)
    logUser("/managerPage")
    return render_template("Managerpage.html", items = session.get("managerSearchList"),lowInv = db.getItemsWithLowInventory())

@app.route("/writeEmail")
def writeEmail():
    name = request.args.get('cardNumber')
    email = request.args.get('exp')
    db.writeEmailToDatabase(name,email)
    return redirect("/checkout")

@app.route("/searchInventoryById", methods=["POST"])
def searchById():
    requireLogin()
    results = db.getById(str(request.form["idSearch"]))
    return render_template("searchResults.html", results = results)

@app.route("/searchInventoryByName", methods=["POST"])
def searchByName():
    requireLogin()
    results = db.getByName(str(request.form["nameSearch"]))
    return render_template("searchResults.html", results = results)

@app.route("/searchEmailsByName", methods=["POST"])
def searchEmailsByName():
    requireLogin()
    results = db.getUser(str(request.form["emailNameSearch"]))
    return render_template("emailSearchResults.html", results = results)

@app.route("/inventory")
def inventory():
    requireLogin()
    logUser("/inventory")
    sortedItems = sorted(db.getItems(), key=lambda x: x[1])
    return render_template("inventory.html", items = sortedItems)

@app.route("/emailList")
def emails():
    requireLogin()
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
    return "Logged in!!"

@app.route("/superSecret")
def superSecret():
    requireManagerLogin(db)
    return "Manager Logged in!!"

@app.route("/pos")
def pos():
    requireLogin()
    logUser("/pos")
    return render_template("POS.html", results = session.get("resultList"),totalPrice = session.get("totalAmount"), searchResults = session.get("searchList"), errorText = session.get("error"))

@app.route("/cart", methods=["POST"])
def cart():
    requireLogin()
    itemNumber = request.form["ItemNumber"]
    if (itemNumber == ""):
        session["error"] = invalidProductId()
        return redirect("/pos")
    searchResult = db.getById(int(itemNumber))
    if (searchResult == []):
        session["error"] = invalidProductId()
        return redirect("/pos")
    elif (request.form["quantity"] == ""):
        session["error"] = invalidAmount()
        return redirect("/pos")
    name = searchResult[0][0]
    quantity = request.form["quantity"]
    if (int(quantity) > int(searchResult[0][6])):
        session["error"] = insufficientInventory()
        return redirect("/pos")
    price = searchResult[0][3] * int(quantity)
    itemList = [itemNumber, name, quantity, str(price)]
    session["resultList"] = session.get("resultList") + [itemList]
    session["totalAmount"] = str(getTotalPrice(session.get("resultList")))
    session["error"] = ""
    return redirect("/pos")

@app.route("/closeError", methods=["POST"])
def closeError():
    session["error"] = ""
    return redirect("/pos")


@app.route("/checkoutError", methods=["POST"])
def checkoutError():
    session["error"] = ""
    return redirect("/checkout")

@app.route("/checkout")
def checkout():
    requireLogin()
    logUser("/checkout")
    if(session.get("resultList") == []):
        session["error"] = cartCantBeEmpty()
        return redirect("/pos")
    return render_template("checkout.html", results = session.get("resultList"), totalPrice = session.get("totalAmount"), errorText = session.get("error"))

@app.route("/payment")
def payment():
    requireLogin()
    logUser("/payment")
    session["error"] = ""
    cash = request.args.get('cashAmount')
    cardNumber = request.args.get('cardNumber')
    exp = request.args.get('exp')
    cvv = request.args.get('CVV')
    itemList = []
    paymentMethod = ""

    if (cash != None):
        paymentMethod = "Cash"
        if(float(cash) != float(session.get("totalAmount"))):
            session["error"] = notEnoughMoney()
            return redirect("/checkout")
    elif (cardNumber != None):
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
    session["error"] = ""
    return redirect("/pos")


@app.route("/search")
def search():
    requireLogin()
    logUser("/search")
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
    session["error"] = ""
    return redirect("/pos")
@app.route("/profitReport")
def profitReport():
    requireManagerLogin(db)
    logUser("/profitReport")
    return render_template("profitReport.html", report = generateReport())

@app.route("/managerSearch")
def managerSearch():
    requireManagerLogin(db)
    logUser("/managerSearch")
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
    requireManagerLogin(db)
    logUser("/createSale")
    productId = request.args.get('productId')
    newSalePrice = request.args.get('newPrice')
    createSale(productId, newSalePrice)
    return redirect("/managerPage")

@app.route("/cartClear")
def clearCart():
    requireLogin()
    logUser("/cartClear")
    session["resultList"] = []
    session["totalAmount"] = 0.00
    session["error"] = ""
    return redirect("/pos")


@app.route("/managerUpdate")
def managerUpdate():
    requireManagerLogin(db)
    logUser("/managerUpdate")
    productId = request.args.get('productId')
    name = request.args.get('Name')
    purchasePrice = request.args.get('purchasePrice')
    sellingPrice = request.args.get('sellingPrice')
    seller = request.args.get('Seller')
    productType = request.args.get('productType')

    userAmount =request.args.get('amountInStock')
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

    if(userAmount == ""):
        userAmount = 0
    amountInStock = db.getById(productId)[0][6]
    db.updateInventoryItem(name,int(productId),float(purchasePrice),float(sellingPrice),seller,productType,int(amountInStock)+int(userAmount))
    db.updateInventoryLogItemsPurchased(int(productId), int(amountInStock))
    return redirect("/managerPage")

@app.route("/transactions")
def transactions():
    requireManagerLogin(db)
    logUser("/transactions")
    return render_template("transactions.html", transactions = db.getTransactions())

@app.route("/orderMoreProducts")
def productOrder():
    logUser("/orderMoreProducts")
    lowInv = db.getItemsWithLowInventory()
    for item in lowInv:
        amount = item[6]
        amount *= 2
        print(amount)
        db.updateInventoryLogItemsPurchased(int(item[1]),int(amount))
        db.orderNewProducts(int(item[1]), int(amount))
    return redirect("/managerPage")

if (__name__ == "__main__"):
    app.run()
