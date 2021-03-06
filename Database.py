import json
import os
from DbConnection import DbConnection
from flask import session

class Database():

    def __init__(self):
        self.db = DbConnection()

    """Get Queries"""

    def getById(self,id):
        return self.db.readQuery("""select * from inventory where product_id = '{}'""".format(id))

    def getNameAndSellingPrice(self,productId):
        return self.db.readQuery("""select name, selling_price from inventory where product_id = '{}'""".format(productId))

    def getByName(self,productName):
        productNameLike = str(productName+"%")
        return self.db.readQuery("""select * from inventory where name LIKE '{}'""".format(productNameLike))

    def getBySupplier(self,supplierName):
        supplierNameLike = str(supplierName+"%")
        return self.db.readQuery("""select * from inventory where supplier LIKE '{}'""".format(supplierNameLike))

    def getItemsByPrice(self, price):
        return self.db.readQuery("""select * from inventory where selling_price = '{}'""".format(price))

    def getItems(self):
        return self.db.readQuery("""select * from inventory""")

    def getAllProductIds(self):
        return self.db.readQuery("""select product_id from inventory""")

    def getItemsWithLowInventory(self):
        return self.db.readQuery("""select * from inventory where amount_in_stock < 5""")

    def getFromInventoryLogByProductId(self, productId):
        return self.db.readQuery("""select * from inventory_log where product_id = '{}'""".format(productId))

    def totalItemsSoldFromProductId(self,productId):
        return self.db.readQuery("""select products_sold from inventory_log where product_id = '{}'""".format(productId))

    def totalItemsBoughtFromProductId(self,productId):
        return self.db.readQuery("""select products_recieved from inventory_log where product_id = '{}'""".format(productId))

    def getTransactions(self):
        return self.db.readQuery("""select * from transactions""")

    def getUserLogs(self):
        return self.db.readQuery("""select * from user_logging""")

    """User Queries"""

    def getUser(self, username):
        usernameLike = str(username+"%")
        return self.db.readQuery("""select * from customer_emails where customer_name LIKE '{}'""".format(usernameLike))

    def getEmailsInSystem(self):
        return self.db.readQuery("""select * from customer_emails""")

    def getPasswordForUser(self,username):
        return self.db.readQuery("""select password from employee_credentials where username = '{}'""".format(username))

    def getManagerStatus(self):
        username = session.get("current_user")
        return self.db.readQuery("""select ismanager from employee_credentials where username = '{}'""".format(username))

    """Insert Queries"""

    def writeEmailToDatabase(self, customerName, customerEmail):
        self.db.writeQuery("""insert into customer_emails values ('{}','{}')""".format(customerName,customerEmail))

    def insertNewInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""insert into inventory values ('{}','{}','{}','{}','{}','{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def insertIntoInventoryLog(self,productId, productsRecieved, productsSold):
        self.db.writeQuery("""insert into inventory_log values ('{}','{}', '{}')""".format(productId, productsRecieved, productsSold))

    def insertNewTransaction(self,transactionId,amountPaid,paymentType,itemsPurchased):
        self.db.writeQuery("""insert into transactions values ('{}','{}','{}','{}')""".format(transactionId, amountPaid, paymentType, itemsPurchased))

    def insertUserLog(self,userName, endpoint, time):
        self.db.writeQuery("""insert into user_logging values ('{}', '{}', '{}')""".format(userName, endpoint, time))

    """Update Queries"""

    def updateInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""update inventory set name ='{}',
        purchase_price = '{}', selling_price = '{}', supplier = '{}', product_type = '{}', amount_in_stock = '{}' where product_id='{}'""".format(name, originalCost, sellPrice, supplier, productType, amountInStock,productId))

    def updateInventoryLog(self, productId,howManyPurchased):
        inventoryLogGet = self.getFromInventoryLogByProductId(productId)
        amountSold =  inventoryLogGet[0][2] + int(howManyPurchased)
        self.db.writeQuery("""update inventory_log set products_sold = '{}' where product_id = '{}'""".format(amountSold, productId))

    def updateInventoryLogItemsPurchased(self, productId,howManyRecieved):
        inventoryLogGet = self.getFromInventoryLogByProductId(productId)
        amountBought =  inventoryLogGet[0][1] + int(howManyRecieved)
        self.db.writeQuery("""update inventory_log set products_recieved = '{}' where product_id = '{}'""".format(amountBought, productId))

    def orderNewProducts(self,productId, howManyPurchased):
        inventoryGet = self.getById(productId)
        amountInStock =  inventoryGet[0][6] + int(howManyPurchased)
        self.db.writeQuery("""update inventory set amount_in_stock = '{}' where product_id = '{}'""".format(amountInStock, productId))

    def createSale(self,productId, newPrice):
        self.db.writeQuery("""update inventory set selling_price = '{}' where product_id = '{}'""".format(newPrice, productId))

    def sellItem(self,productId,howManyPurchased):
        item = self.getById(productId)
        howMany = item[0][6] - int(howManyPurchased)
        self.db.writeQuery("""update inventory set amount_in_stock = '{}' where product_id = '{}'""".format(howMany, productId))
