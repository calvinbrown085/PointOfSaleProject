from Database import Database
from random import randint

db = Database()

def getTotalPrice(cart):
    totalPrice = 0
    for x in cart:
        totalPrice += float(x[3])
    return totalPrice

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
