import json
import os
from DbConnection import DbConnection

class Database():

    def __init__(self):
        self.db = DbConnection()

    def getById(self,id):
        return self.db.readQuery("""select * from inventory where product_id = '{}'""".format(id))

    def getItems(self):
        return self.db.readQuery("""select * from inventory""")

    def getUser(self, username):
        return self.db.readQuery("""select customer_name from customer_emails where customer_name = '{}'""".format(username))

    def getEmailsInSystem(self):
        return self.db.readQuery("""select * from customer_emails""")

    def writeEmailToDatabase(self, customerName, customerEmail):
        self.db.writeQuery("""insert into customer_emails values ('{}','{}')""".format(customerName,customerEmail))

    def insertNewInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""insert into inventory values ('{}','{}','{}','{}','{}','{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def insertIntoInventoryLog(self,productId, productsRecieved, productsSold):
        self.db.writeQuery("""insert into inventory_log values ('{}','{}', '{}')""".format(productId, productsRecieved, productsSold))

    def insertNewManagerCredentials(self,username, password):
        self.db.writeQuery("""insert into manager_credentials values ('{}','{}')""".format(username, password))

    def insertNewTransaction(self,transactionId,amountPaid,paymentType,itemsPurchased)
