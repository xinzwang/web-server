# coding=utf-8
import pymysql
import os
import sys

db = pymysql.connect("localhost", "root", "123456", "StuInfo")
cursor = db.cursor()

Rid = sys.argv[1]
sql = 'SELECT * FROM Information WHERE id = "{}" '.format(Rid)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) == 0:
        print(queryToShow.format("未查询到相关信息", "未查询到相关信息", "未查询到相关信息"))
    for row in results:
        Rid = row[0]
        Rname = row[1]
        Rclass = row[2]
    # 打印结果
    # return "学生id:{} \n学生姓名:{} \n学生班级:{}\n".format(Rid, Rname, Rclass)
    print(queryToShow.format(Rid, Rname, Rclass))
except:
    print("Error: unable to fetch data")
