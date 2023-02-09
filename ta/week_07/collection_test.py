# coding=utf-8
from collections import OrderedDict, defaultdict

my_dict = {
    'a': 1,
    'b': 2,
    'c': 3
}

my_ordered_dict = OrderedDict(
    [('a', 1),
     ('b', 2)]
)
# OrderedDict可以进行排序，dict不行
my_ordered_dict.move_to_end('a')

def my_fun():
    return 100

# 创建一个defaultdict
my_default_dict = defaultdict(my_fun)

my_default_dict['a'] = 1
my_default_dict['c'] = 2
my_default_dict['d'] = 3


# 假如获取一个defaultdict里没有的键，这个键返回的值会是之前定义传参的值
my_default_dict['e']

pass
