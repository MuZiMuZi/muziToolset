# coding=utf-8
u"""
这是一个blendshape的模块。用来对混合变形进行一系列修改的操作。

实现的功能：
get_blendshape_node: 获取bs节点
get_blendshape_name: 获取bs节点名称
get_blendshape_weight: 获取bs节点权重
get_blendshape_weight_list: 获取bs节点权重列表
"""
import maya.cmds as cmds


class BlendShape () :

    def __init__ (self , model_node) :
        # 初始化方法，传入模型节点名称
        self.model_node = model_node
        self.blendshape_node = None  # 存储混合变形节点的变量
        self.blendshape_name = None  # 存储混合变形节点名称的变量
        self.blendshape_weight = None  # 存储混合变形节点权重的变量
        self.blendshape_weight_list = None  # 存储混合变形节点权重列表的变量

        # 调用以下方法获取混合变形相关信息
        self.get_blendshape_node ()
        self.get_blendshape_name ()
        self.get_blendshape_weight ()
        self.get_blendshape_weight_list ()


    # 获取混合变形的节点
    def get_blendshape_node (self) :
        # 获取混合变形的节点
        self.blendshape_node = cmds.listConnections (self.model_node + '.worldMesh[0]' , type = 'blendShape')
        return self.blendshape_node


    # 获取混合变形节点的名称
    def get_blendshape_name (self) :
        # 获取混合变形节点的名称
        self.blendshape_name = cmds.listAttr (self.blendshape_node [0] , m = True)
        return self.blendshape_name


    # 获取混合变形节点的权重
    def get_blendshape_weight (self) :
        # 获取混合变形节点的权重
        self.blendshape_weight = cmds.getAttr (self.blendshape_node [0] + '.' + self.blendshape_name [0])
        return self.blendshape_weight


    # 获取混合变形节点权重列表
    def get_blendshape_weight_list (self) :
        # 获取混合变形节点权重列表
        self.blendshape_weight_list = []
        for i in range (len (self.blendshape_weight)) :
            self.blendshape_weight_list.append (self.blendshape_weight [i])
        return self.blendshape_weight_list
