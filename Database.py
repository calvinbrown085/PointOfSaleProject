import json
import os
from Query import *

class Database():

    def __init__(self):
        x = {}
        self.items = x
        self.users = {}

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        return readQuery("""select * from inventory""")

    def getUser(self, username):
        return readQuery("""select customer_name from customer_emails where customer_name = '{}'""".format(username))

    def getEmailsInSystem(self):
        return readQuery("""select * from customer_emails""")

    def writeEmailToDatabase(self, customerName, customerEmail):
        writeQuery("""insert into customer_emails values ('{}','{}')""".format(customerName,customerEmail))

    def insertNewInventoryItem(self, name, productId, originalCost, sellPrice, supplier, productType, amountInStock):
        writeQuery("""insert into inventory values ('{}','{}','{}','{}','{}','{}','{}')""".format(name,productId, originalCost, sellPrice, supplier, productType, amountInStock))

    def insertIntoInventoryLog(self,productId, productsRecieved, productsSold):
        writeQuery("""insert into inventory_log values ('{}','{}', '{}')""".format(productId, productsRecieved, productsSold))

    def insertNewManagerCredentials(self,username, password):
        writeQuery("""insert into manager_credentials values ('{}','{}')""".format(username, password))
