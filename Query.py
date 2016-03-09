import psycopg2
import urlparse



urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://ybctfhowlsvtoe:A-UklGRXznn_sknD-imWVH-jb5@ec2-54-83-57-25.compute-1.amazonaws.com:5432/d2e2d5ufv17e36")
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cursor = conn.cursor()

def query(queryStatement):
    try:
        cursor.execute(queryStatement)
    except:
        return "exception Error"
    rows = cursor.fetchall()
    if (rows == []):
        return ""
    else:
        return rows
