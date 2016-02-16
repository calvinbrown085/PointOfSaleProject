import json

class MyDatabase():

    def __init__(self):
        databaseList = []
        self.emailList = databaseList
        jsonFile = open("items.json", "r").read()
        jsonData = json.loads(jsonFile)
        x = {}
        y = {}
        for item in jsonData["items"]:
            x[str(item["id"])] = str(item["name"])
            y[str(item["name"])] = str(item["id"])
        self.items = x
        self.itemsName = y


    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"
    def getByName(self,name):

        for item in self.itemsName:
            if item == name:
                return item


    def getItems(self):
        return self.items

    def storeEmail(self,email):
        self.emailList.append(email)
        return self.emailList

    def getEmailsInSystem(self):
        return self.emailList
