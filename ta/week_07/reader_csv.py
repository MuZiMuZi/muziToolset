# coding=utf-8
'''
# 读取csv文件的方法
'''
import csv

# 读取csv文件的方法
file_name = 'EditorPerfStats.csv'

content = []

# 'r'是读取的意思
with open(file_name,'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        content.append(row)

print(content)