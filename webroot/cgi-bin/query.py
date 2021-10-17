#coding=utf-8
import pymysql
import os
import sys

db = pymysql.connect("localhost", "root", "123456", "StuInfo")
cursor = db.cursor()

Rid = sys.argv[1]
sql = 'SELECT * FROM Information WHERE id = "{}" '.format(Rid)
queryToShow = '''
                <!DOCTYPE html>
                <html lang="en">

                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>RESULT</title>
                <style type="text/css">
                    body {{
                        background-image: linear-gradient(#B0C4DE, #00ffff,#FAEBD7,#FFDAB9,#F5F5DC,#DAA520);
                        background-size:cover;
                        background-attachment:fixed;
                    }}
                </style>

                </head>

                <body>
                    <p align="center"><font size="6" color="red">学号：{}</font><br /></p>
                    <p align="center"><font size="6" color="blue">姓名：{}</font><br /></p>
                    <p align="center"><font size="6" color="green">班级：{}</font><br /></p>
    
                </body>
            '''

try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if len(results) == 0:
        print (queryToShow.format("未查询到相关信息", "未查询到相关信息", "未查询到相关信息"))
    for row in results:
        Rid = row[0]
        Rname = row[1]
        Rclass = row[2]
    # 打印结果
    # return "学生id:{} \n学生姓名:{} \n学生班级:{}\n".format(Rid, Rname, Rclass)
    print (queryToShow.format(Rid, Rname, Rclass))
except:
    print("Error: unable to fetch data")
