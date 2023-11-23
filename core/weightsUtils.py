# coding=utf-8

u"""
这是一个用来编写权重工具的基本类

目前已有的功能：

 save_skinWeights：       将蒙皮几何体对象的权重保存到给定权重文件夹，权重将保存在对象短名称下，并附加存储其蒙皮影响的文件
 ik_chain_rig：创建ik链的控制器绑定

bind_chain_rig:创建混合IKFk链的bind链控制器绑定
"""
from importlib import reload
import json
import os

import maya.cmds as cmds


class Weights (object) :

    def __init__ (self , geo) :
        self.geo = geo

        self.file_path = cmds.file (q = True , location = True)

        self.weightsFileExt = '.xml'
        self.influencesFileExt = '.infs'

        # 设定蒙皮权重导出的文件名
        self.skinWeights_FileName = 'sc_' + self.geo + self.weightsFileExt
        self.skinWeights_Path = os.path.abspath (self.file_path + "/..")

        # 设定关节影响导出的文件名
        self.influences_FileName = 'sc_' + self.geo + self.influencesFileExt
        self.influences_Path = os.path.join (self.skinWeights_Path , self.influences_FileName)


    def save_skinWeights (self) :
        u'''
       将蒙皮几何体对象的权重保存到给定权重文件夹，权重将保存在对象短名称下，并附加存储其蒙皮影响的文件
        :return:
        '''
        # 查询物体是否有蒙皮节点，没有的话报错
        history = cmds.listHistory (self.geo)
        skin_node_Res = cmds.ls (history , type = 'skinCluster')

        if not skin_node_Res :
            cmds.warning (u'{}这个物体没有蒙皮节点'.format (self.geo))
        else :
            skin_node = skin_node_Res [0]
            # 导出蒙皮权重
            cmds.deformerWeights (self.skinWeights_FileName , path = self.skinWeights_Path , export = True ,
                                  deformer = skin_node)

            # 保存影响的权重
            influences = cmds.skinCluster (skin_node , q = True , inf = True)
            influences_file = open (self.influences_Path , mode = 'w')
            json.dump (influences , influences_file , sort_keys = True , indent = 4 , separators = (',' , ': '))


    def load_skinWeights (self) :
        u'''
       从给定权重文件夹加载蒙皮几何体对象的权重将从与对象短名称匹配的文件名加载权重，并添加其他文件以获取其影响
        :return:
        '''
        # 查询物体是否有蒙皮节点，没有的话报错
        history = cmds.listHistory (self.geo)
        skin_node_Res = cmds.ls (history , type = 'skinCluster')

        if skin_node_Res :
            cmds.delete (skin_node_Res)

        if not os.path.exists (self.skinWeights_Path) :
            cmds.warning (u'{}这个物体没有导出权重的文件'.format (self.geo))
            return

        if not os.path.exists (self.influences_Path) :
            cmds.warning (u'{}这个物体没有导出权重关节影响的文件'.format (self.geo))
            return

        # 获得关节影响
        influences_file = open (self.influences_Path , mode = 'rb')
        influences_Str = influences_file.read ()
        influences = json.loads (influences_Str)
        influences_file.close ()

        # 创建关节蒙皮
        skin_node = cmds.skinCluster (self.geo , influences , tsb = True) [0]

        # 获取蒙皮权重
        cmds.deformerWeights (self.skinWeights_FileName , path = self.skinWeights_Path , im = True ,
                              deformer = skin_node)
        cmds.warning (u'{}这个物体导入权重成功'.format (self.geo))
