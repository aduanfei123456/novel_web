import pymysql
#default port=3306
db=pymysql.connect(host="localhost",user="root",password="",db="test",port=3306)
cur=db.cursor()