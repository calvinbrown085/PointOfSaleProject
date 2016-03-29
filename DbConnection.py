import psycopg2
import urlparse
import os
from DatabaseUrlGenerator import getDatabaseUrl

class DbConnection():

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(getDatabaseUrl())
        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()


    def readQuery(self,queryStatement):
        try:
            self.cursor.execute(queryStatement)
        except:
            return []
        rows = self.cursor.fetchall()
        if (rows == []):
            return []
        else:
            return rows

    def writeQuery(self,queryStatement):
        try:
            self.cursor.execute(queryStatement)
        except:
            return "exception Error"
