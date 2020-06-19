import mysql.connector
import conn

# create table in sql
mydb = mysql.connector.connect(
  host=conn.host,
  user=conn.user,
  passwd=conn.passwd,
  database=conn.database
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE serial (Date VARCHAR(17) PRIMARY KEY, Link VARCHAR(200), Description VARCHAR(200))")
