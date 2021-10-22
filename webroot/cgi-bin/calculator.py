# coding=utf-8
import os
import sys


a = sys.argv[1].split('&')
data1 = a[0].split('=')
data2 = a[1].split('=')

num1 = int(data1[1])
num2 = int(data2[1])


print(str(num1+num2))
