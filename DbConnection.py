import psycopg2
import urlparse

class DbConnection():

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse("postgres://ybctfhowlsvtoe:A-UklGRXznn_sknD-imWVH-jb5@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d2e2d5ufv17e36")
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
            return "exception Error"
        rows = self.cursor.fetchall()
        if (rows == []):
            return ""
        else:
            return rows

    def writeQuery(self,queryStatement):
        try:
            self.cursor.execute(queryStatement)
        except:
            return "exception Error"
