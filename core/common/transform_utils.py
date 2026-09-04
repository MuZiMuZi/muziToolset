# coding=utf-8

import pymel.core as pm
class Transform(object):
    def __init__(self, object=None):
        self.object = None

        if object:
            self.object = pm.PyNode(object)

    def match_transform(self,target,position=True,rotation=True,scale=True):
        """
        给定一个对象和目标对象,匹配他们的位移，旋转，缩放
        """
        pm.matchTransform(self.object,target,position=position,rotation=rotation,scale=scale)


    def get_world_matrix (self):
        """
        给定一个对象获取对象的世界矩阵
        """
        self.world_matrix = self.object.getMatrix (worldSpace = True)
        return self.world_matrix

    def set_world_matrix(self,matrix):
        self.world_matrix  = self.object.setMatrix(matrix, worldSpace=True)


    def reset_transform (self , translate = True , rotate = True , scale = True) :

        if translate :
            self.object.translate.set ((0 , 0 , 0))

        if rotate :
            self.object.rotate.set ((0 , 0 , 0))

        if scale :
            self.object.scale.set ((1 , 1 , 1))


    def get_transform (self) :
        u"""
        获取当前对象对应的 Transform 节点。

        如果当前对象本身就是 Transform，则直接返回。
        如果当前对象是 Shape，则返回它的父 Transform。

        Returns:
            PyNode: 当前对象对应的 Transform 节点。

        Maya 使用示例：

        from muziToolset.core.common import transform_utils

        transform_object = transform_utils.Transform(
            "ctrl_lf_eye_main_001Shape"
        )

        transform = transform_object.get_transform()

        print(transform)
        """

        if isinstance (self.object , pm.nodetypes.Transform) :
            return self.object

        parent_object = self.object.getParent ()

        return parent_object

