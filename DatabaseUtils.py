from Database import Database
from random import randint


db = Database()


def getTotalPrice(cart):
    print(cart)
    totalPrice = 0
    for x in cart:
        totalPrice += x[3]
    return totalPrice


def moneyMadeFromProduct(productId):
    productBuyPrice = db.getById(productId)[0][2]
    productSellPrice = db.getById(productId)[0][3]
    howManySold = db.totalItemsSoldFromProductId(productId)[0][0]
    howManyBought = db.totalItemsBoughtFromProductId(productId)[0][0]
    boughtAmount = howManyBought * productBuyPrice
    soldAmount = howManySold * productSellPrice
    profit = soldAmount - boughtAmount
    return profit


def newCustomer(customerName, customerEmail):
    db.writeEmailToDatabase(customerName, customerEmail)

def newTransaction(paymentMethod,paymentAmount,itemsPurchasedList):
    db.insertNewTransaction(randint(0,1000000),paymentMethod,paymentAmount,listToString(itemsPurchasedList))

def listToString(itemsPurchasedList):
    newString = ""
    for item in itemsPurchasedList:
        newString = newString + ", " + item
    return newString

def createSale(productId, newPrice):
    db.createSale(productId, newPrice)
