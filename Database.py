import json
import os
import psycopg2
import urlparse

class Database():

    def __init__(self):
        x = {}
        self.items = x
        self.users = {}

        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse("postgres://ybctfhowlsvtoe:A-UklGRXznn_sknD-imWVH-jb5@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d2e2d5ufv17e36")

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.conn.cursor()

    def getById(self,id):
        try:
            return self.items[id]
        except KeyError:
            return "no match"

    def getItems(self):
        try:
            self.cursor.execute("""select * from inventory""")
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows[0]

    def getUser(self, username):
        try:
            self.cursor.execute("""select customer_name from customer_emails where customer_name = '{}'""".format(username))
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows[0][0]

    def getEmailsInSystem(self):
        try:
            self.cursor.execute("""select * from customer_emails""")
        except:
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows
