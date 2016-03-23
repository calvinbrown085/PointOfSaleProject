import json
import os
from DbConnection import DbConnection

class Database():

    def __init__(self):
        self.db = DbConnection()

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        return self.db.readQuery("""select * from inventory""")

    def getUser(self, username):
        return self.db.readQuery("""select customer_name from customer_emails where customer_name = '{}'""".format(username))

    def getEmailsInSystem(self):
        return self.db.readQuery("""select * from customer_emails""")

    def printCreds(self):
        print(self.db.readQuery("""select * from manager_credentials"""))

    def getPasswordForUser(self,username):
        return self.db.readQuery("""select manager_password from manager_credentials where manager_username = '{}'""".format(username))

    def writeEmailToDatabase(self, customerName, customerEmail):
        self.db.writeQuery("""insert into customer_emails values ('{}','{}')""".format(customerName,customerEmail))

    def insertNewInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        self.db.writeQuery("""insert into inventory values ('{}','{}','{}','{}','{}','{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def insertIntoInventoryLog(self,productId, productsRecieved, productsSold):
        self.db.writeQuery("""insert into inventory_log values ('{}','{}', '{}')""".format(productId, productsRecieved, productsSold))
