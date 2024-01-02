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
    x_negative = [-1 , 0 , 0]
    x_positive = [1 , 0 , 0]
    y_negative = [0 , -1 , 0]
    y_positive = [0 , 1 , 0]
    z_negative = [0 , 0 , -1]
    z_positive = [0 , 0 , 1]


def Rigtype (value) :
    """
    根据给定的值返回相应的绑定类型。

    参数:
        value (str): 要查询的值。

    返回:
        str or None: 如果找到匹配的绑定类型，则返回相应的键；如果未找到匹配，则返回 None。
    """
    # 定义不同的绑定类型的值列表
    # 针对多个关节点的绑定模块，
    # 组件需要的参数有[side,name,jnt_number,jnt_parent,ctrl_parent]
    rigtype_bone = ['bone']

    # 针对不需要预设属性设置修改的绑定模块，
    # 组件需要的参数有[side,name,jnt_parent,ctrl_parent]
    rigtype_base = ['master' , 'brow' , 'nose' , 'cheek' , 'jaw' , 'hand' , 'foot']

    # 针对关节链条的绑定模块，
    # 组件需要的参数有[side,name,length,direction,jnt_parent,ctrl_parent]
    rigtype_chain = ['chainFK' , 'chainIK' , 'chainIKFK' , 'finger' , 'tail']

    # 针对EP曲线关节链条的绑定模块，
    # 组件需要的参数有[side,name,jnt_number,ctrl_number,curve,jnt_parent,ctrl_parent]
    rigtype_chainEP = ['chainEP']

    # 针对身体四肢模块的绑定模块，
    # 组件需要的参数有[side,name,jnt_number,ikctrl_value,fkctrl_value,stretch_value,up_ribbon_value,down_ribbon_value,jnt_parent,ctrl_parent]
    rigtype_limb = ['arm' , 'leg' , 'spine']

    # 针对需要选择上下曲线的脸部的绑定模块，组件需要的参数有[side,name,up_curve,down_curve,jnt_parent,ctrl_parent]
    rigtype_face = ['eye' , 'mouth']

    # 创建一个包含绑定类型的字典
    rigtype_dict = {
        'bone' : rigtype_bone ,
        'base' : rigtype_base ,
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
