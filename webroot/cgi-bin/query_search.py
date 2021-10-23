import os
import sys
import json
import pymysql

data = json.loads(sys.argv[1])
ustr = data['ustr']

db = pymysql.connect(host="localhost", user="root",
                     password="123456", database="db_student")
cursor = db.cursor()

sql = ""
if ustr != "":
    sql = "SELECT unumber,uname,uclass from student where unumber="+ustr
else:
    sql = "SELECT unumber,uname,uclass from student"

rsp = {}
rsp['table_data'] = []
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        rsp['table_data'].append(
            {'unumber': row[0], 'uname': row[1], 'uclass': row[2]})
        rsp['msg'] = "success"
except:
    rsp['msg'] = "failed"

print(json.dumps(rsp))
