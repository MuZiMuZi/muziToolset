import maya.cmds as cmds
import pymel.core as pm


class Ctrl(object):

    def __init__(self, name=None, ctrl=None):
        self.name = name
        self.ctrl = None

        if ctrl:
            self.ctrl = pm.PyNode(ctrl)


    def create_ctrl (self , radius = 1.0) :
        self.ctrl = pm.circle (name = self.name , radius = radius , normal = (0 , 1 , 0)) [0]
        return self.ctrl

    def get_ctrl_shape (self ) :
        self.ctrl_shape = self.ctrl.getShape()
        return self.ctrl_shape

    def set_ctrl_color (self,ctrl_color ) :
        self.ctrl_shape = self.get_ctrl_shape()

        self.ctrl_shape.overrideEnabled.set (True)
        self.ctrl_shape.overrideColor.set (ctrl_color)




    def set_ctrl_size (self , ctrl_size) :
        u"""
        设置控制器 Curve Shape 的显示大小。

        ctrl_size(float): 控制器 Shape 的缩放倍率。
        """

        self.ctrl_shape = self.get_ctrl_shape()

        for shape in self.ctrl_shape :
            if isinstance (shape , pm.nodetypes.NurbsCurve) :
                pm.scale (
                    shape.cv [:] ,
                    ctrl_size ,
                    ctrl_size ,
                    ctrl_size ,
                    relative = True ,
                    objectSpace = True
                )