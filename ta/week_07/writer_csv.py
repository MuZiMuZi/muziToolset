# coding=utf-8
'''
写入csv文件的方法
两个方法
1通过创建writer对象，主要用到2个方法。一个是writerow，写入一行。另一个是writerows写入多行
2使用DictWriter 可以使用字典的方式把数据写入进去
'''
import csv

file_name = 'example_01.csv'


titles = ['Name','Branch','Year','CGPA']

#字符串必须要添加''，数值可以不需要引号
content = [
    ['NIkkels','acasv','5','7.5'],
    ['Asvas', 'sacasa', '3', '10.5'],
    ['ASVAA', 'qwsf', '1', '2.5'],
    ['BASVAS', 'cscasv', '2', '1.5'],
]

with open(file_name,'w') as csv_file:
    csv_pen = csv.writer(csv_file)
    # 注意：   writerow只能写一个列表，writerows可以写多个列表
    csv_pen.writerow(titles)

    csv_pen.writerows(content)