import json
import os
from DbConnection import DbConnection

class Database():

    def __init__(self):
        self.db = DbConnection()

    def getById(self,id):
        return self.db.readQuery("""select * from inventory where product_id = '{}'""".format(id))
    def getByName(self,productName):
        productNameLike = str(productName+"%")
        print(productNameLike)
        return self.db.readQuery("""select * from inventory where name LIKE '{}'""".format(productNameLike))

    def getItems(self):
        return self.db.readQuery("""select * from inventory""")

    def getAllProductIds(self):
        return self.db.readQuery("""select product_id from inventory""")

    def getUser(self, username):
        return self.db.readQuery("""select customer_name from customer_emails where customer_name = '{}'""".format(username))

    def getEmailsInSystem(self):
        return self.db.readQuery("""select * from customer_emails""")

    def getPasswordForUser(self,username):
        return self.db.readQuery("""select password from employee_credentials where username = '{}'""".format(username))

    def getItemsWithLowInventory(self):
        return self.db.readQuery("""select * from inventory where amount_in_stock < 5""")


    def getFromInventoryLogByProductId(self, productId):
        return self.db.readQuery("""select * from inventory_log where product_id = '{}'""".format(productId))

    def writeEmailToDatabase(self, customerName, customerEmail):
        self.db.writeQuery("""insert into customer_emails values ('{}','{}')""".format(customerName,customerEmail))

    def insertNewInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""insert into inventory values ('{}','{}','{}','{}','{}','{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def updateInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""update inventory set name ='{}', product_id = '{}',original_cost = '{}', selling_price = '{}',supplier = '{}',product_type = '{}',amount_in_stock = '{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def insertIntoInventoryLog(self,productId, productsRecieved, productsSold):
        self.db.writeQuery("""insert into inventory_log values ('{}','{}', '{}')""".format(productId, productsRecieved, productsSold))

    def updateInventoryLog(self, productId,howManyPurchased):
        inventoryLogGet = self.getFromInventoryLogByProductId(productId)
        amountBought = inventoryLogGet[0][1] - howManyPurchased
        amountSold =  inventoryLogGet[0][2] - howManyPurchased
        self.db.writeQuery("""update inventory_log set products_recieved = '{}', products_sold = '{}' where product_id = '{}'""".format(amountBought, amountSold, productId))

    def totalItemsSoldFromProductId(self,productId):
        return self.db.readQuery("""select products_sold from inventory_log where product_id = '{}'""".format(productId))

    def totalItemsBoughtFromProductId(self,productId):
        return self.db.readQuery("""select products_recieved from inventory_log where product_id = '{}'""".format(productId))

    def insertNewTransaction(self,transactionId,amountPaid,paymentType,itemsPurchased):
        self.db.writeQuery("""insert into transactions values ('{}','{}','{}','{}')""".format(transactionId, amountPaid, paymentType, itemsPurchased))

    def createSale(self,productId, newPrice):
        self.db.writeQuery("""update inventory set selling_price = '{}' where product_id = '{}'""".format(newPrice, productId))
