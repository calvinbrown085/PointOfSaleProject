from Database import Database


db = Database()


def moneyMadeFromProduct(productId):
    productBuyPrice = db.getById(productId)[0][2]
    productSellPrice = db.getById(productId)[0][3]
    howManySold = db.totalItemsSoldFromProductId(productId)[0][0]
    howManyBought = db.totalItemsBoughtFromProductId(productId)[0][0]
    boughtAmount = howManyBought * productBuyPrice
    soldAmount = howManySold * productSellPrice
    profit = soldAmount - boughtAmount
    return profit
