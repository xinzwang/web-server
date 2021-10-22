# coding=utf-8
import os
import sys
import json

data = json.loads(sys.argv[1])


num1 = int(data['data1'])
num2 = int(data['data2'])

res = {'res': num1+num2}

print(json.dumps(res))
