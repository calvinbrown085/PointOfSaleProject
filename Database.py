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
        return query("""select * from inventory""")[0]

    def getUser(self, username):
        return query("""select customer_name from customer_emails where customer_name = '{}'""".format(username))

    def getEmailsInSystem(self):
        return query("""select * from customer_emails""")
