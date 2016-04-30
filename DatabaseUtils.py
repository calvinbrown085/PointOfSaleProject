from Database import Database
from random import randint
from time import strftime
from flask import session

db = Database()

x = []

def logUser(endpoint):
    if (session.get("current_user") == "east"):
        print("east was here")
        x.append((session.get("current_user"),endpoint,strftime("%Y-%m-%d %H:%M:%S")))

def writeUserStuff():
    for i in x:
        print(i)
        db.insertUserLog(i[0],i[1], i[2])


def getTotalPrice(cart):
    totalPrice = 0
    for x in cart:
        totalPrice += float(x[3])
    return totalPrice

def newCustomer(customerName, customerEmail):
    db.writeEmailToDatabase(customerName, customerEmail)

def newTransaction(paymentMethod,paymentAmount,itemsPurchasedList):
    db.insertNewTransaction(randint(0,1000000),paymentMethod,paymentAmount,itemsPurchasedList)

def listToString(itemsPurchasedList):
    newString = ""
    for item in itemsPurchasedList:
        newString = newString + ", " + item
    return newString

def createSale(productId, newPrice):
    db.createSale(productId, newPrice)

def moneyMadeFromProduct(item):
    productBuyPrice = item[2]
    productSellPrice = item[3]
    productId = item[1]
    howManySold = db.totalItemsSoldFromProductId(productId)[0][0]
    howManyBought = db.totalItemsBoughtFromProductId(productId)[0][0]
    boughtAmount = howManyBought * productBuyPrice
    soldAmount = howManySold * productSellPrice
    profit = soldAmount - boughtAmount
    return profit

def generateReport():
    profitList = []
    allItems = db.getItems()
    for item in allItems:
        profit = moneyMadeFromProduct(item)
        profitList.append((item[1], item[0], profit))
    return profitList

def purchasedItems(productId,howManyPurchased):
    db.updateInventoryLog(productId,howManyPurchased)

def addToSearchQuery(searchList):
    emptyList = []
    for tup in searchList:
        emptyList.append([tup[1],tup[0],tup[4],str(tup[3])])
    return emptyList

def addToManagerSearchQuery(searchList):
    emptyList = []
    for tup in searchList:
        emptyList.append([tup[0],tup[1],str(tup[2]),str(tup[3]),tup[4],tup[5],tup[6]])
    return emptyList
