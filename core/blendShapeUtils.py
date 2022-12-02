# coding=utf-8
u"""
这是一个blendshape的类。用来对混合变形进行一系列修改的操作。

实现的功能：
get_blendshape_node:获取bs节点
get_blendshape_name：获取bs节点名称
get_blendshape_weight：获取bs节点权重
get_blendshape_weight_list：：获取bs节点权重列表
"""
import maya.cmds as cmds
class BlendShape():
    def __init__(self,modle_ndoe):
        self.modle_ndoe = modle_ndoe
        self.blendshape_node = None
        self.blendshape_name = None
        self.blendshape_weight = None
        self.blendshape_weight_list = None


        self.get_blendshape_node()
        self.get_blendshape_name()
        self.get_blendshape_weight()
        self.get_blendshape_weight_list()

    def get_blendshape_node(self):
        self.blendshape_node = cmds.listConnections(model_name + '.worldMesh[0]', type = 'blendShape')

    def get_blendshape_name(self):
        self.blendshape_name = cmds.listAttr(self.blendshape_node, m = True)

    def get_blendshape_weight(self):
        self.blendshape_weight = cmds.getAttr(self.blendshape_node + '.' + self.blendshape_name)

    def get_blendshape_weight_list(self):
        self.blendshape_weight_list = []
        for i in range(len(blendshape_weight)):
            self.blendshape_weight_list.append(blendshape_weight[i])