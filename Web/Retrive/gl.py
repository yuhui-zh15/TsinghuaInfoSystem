# coding=utf-8

import os,sys
os.chdir(os.getcwd())
print os.getcwd()

# 加载数据库
file = open('./list/dict.json', 'r')
s = file.read()
data = eval(s)
m_dict = dict(data)
file.close()

file = open('./list/file2title.json', 'r')
s = file.read()
data = eval(s)
m_file2title = dict(data)
file.close()

file = open('./list/file2time.json', 'r')
s = file.read()
data = eval(s)
m_file2time = dict(data)
file.close()

file = open('./list/file2url.json', 'r')
s = file.read()
data = eval(s)
m_file2url = dict(data)
file.close()

print "数据库加载完毕"



