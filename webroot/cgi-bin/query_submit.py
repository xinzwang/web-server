import os
import sys
import json
import pymysql

data = json.loads(sys.argv[1])

uname = data['uname']
uclass = data['uclass']
unumber = data['unumber']

db = pymysql.connect(host="localhost", user="root",
                     password="123456", database="db_student")
cursor = db.cursor()

sql = "INSERT INTO student VALUES(0,'"+unumber+"','"+uname+"','"+uclass+"')"

rsp = {}
try:
    cursor.execute(sql)
    db.commit()
    rsp['msg'] = "success"
except:
    db.rollback()  # 错误时回滚
    rsp['msg'] = "failed"

print(json.dumps(rsp))
