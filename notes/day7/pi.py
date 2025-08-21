import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="employee"
)
if connection:
    print("database connected")
else:
     print("database not connected")
