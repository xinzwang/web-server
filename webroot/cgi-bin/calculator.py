# coding=utf-8
import os
import sys


# data1 = int(sys.argv[1])
# data2 = int(sys.argv[2])

data1 = 1
data2 = 2

calculToShow = '''
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
                    <p align="center"><font size="6" color="red">结果:{}</font><br /></p>
    
                </body>
            '''

print(calculToShow.format(str(data1+data2)))
