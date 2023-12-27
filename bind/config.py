import os
from enum import Enum , unique


# 项目根目录
project_root = os.path.dirname (__file__)

# UI文件存放目录
ui_dir = os.path.join (project_root , 'ui')

# 图标文件存放目录
icon_dir = os.path.abspath (__file__ + "/../../tools/icon")

# 绑定模块根目录
bind_root = os.path.abspath (__file__ + "/..")

# base模块目录
base_dir = os.path.join (bind_root , 'module/base')

# chain模块目录
chain_dir = os.path.join (bind_root , 'module/chain')

# limb模块目录
limb_dir = os.path.join (bind_root , 'module/limb')

# 所有模块的父目录
module_dir = os.path.join (bind_root , 'module')

# QSS文件存放目录
qss_dir = os.path.abspath (__file__ + "/../../tools/qss")


@unique
class Side (Enum) :
    """
    定义模块的方向。
    """
    left = 'l'
    right = 'r'
    middle = 'm'


@unique
class Direction (Enum) :
    """
    定义模块的轴向。
    """
    y_positive = [0 , 1 , 0]
    y_negative = [0 , -1 , 0]
    x_positive = [1 , 0 , 0]
    x_negative = [-1 , 0 , 0]
    z_positive = [0 , 0 , 1]
    z_negative = [0 , 0 , -1]


def Rigtype (value) :
    """
    根据给定的值返回相应的绑定类型。

    参数:
        value (str): 要查询的值。

    返回:
        str or None: 如果找到匹配的绑定类型，则返回相应的键；如果未找到匹配，则返回 None。
    """
    # 定义不同的绑定类型的值列表
    rigtype_custom = ['base' , 'master' , 'brow' , 'nose' , 'cheek' , 'jaw']
    rigtype_chain = ['chainFK' , 'chainIK' , 'chainIKFK' , 'finger' , 'spine' , 'hand' , 'tail' , 'spine']
    rigtype_chainEP = ['chainEP']
    rigtype_limb = ['arm' , 'leg']
    rigtype_face = ['eye' , 'mouth']

    # 创建一个包含绑定类型的字典
    rigtype_dict = {
        'custom' : rigtype_custom ,
        'chain' : rigtype_chain ,
        'chainEP' : rigtype_chainEP ,
        'limb' : rigtype_limb ,
        'face' : rigtype_face
    }

    # 遍历字典，查找值所在的绑定类型
    for key , val_list in rigtype_dict.items () :
        if value in val_list :
            return key  # 如果找到匹配的值，返回相应的键

    return None  # 如果未找到匹配的值，返回 None
