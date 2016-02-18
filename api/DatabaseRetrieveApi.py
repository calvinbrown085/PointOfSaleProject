from sqlalchemy import create_engine





class DatabaseRetrieveApi():
    def __init__(self):
        #api stuff?
        engine = create_engine('postgresql://localhost/[YOUR_DATABASE_NAME]')

    def getProductByName(self,productName):
        #my sql statement for getting product by name
        return 0

    def getEmailList(self):
        #my sql statement for getting emails for the users
        return 0

    def getProductById(self,productId):
        #my sql statement for getting a product by Id
        return 0
