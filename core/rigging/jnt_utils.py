import pymel.core as pm
import maya.cmds as cmds
from core.common import hierarchy_utils

class Jnt(object):

    def __init__ (self , name = None , jnt = None) :
        self.name = name
        self.jnt = jnt


    def create_jnt(self) :
        self.jnt = pm.joint (name = self.name)
        return self.jnt


    def match_transform (self , target) :
        """
        使给定的关节对其给定的对象
        """
        cmds.matchTransform (self.joint , target , position = True , rotation = True)

    def set_parent(self, parent_joint):
        """
        设置给定关节的父层级
        """
        hierarchy_utils.parent (self.joint , parent_joint = parent_joint)

    def set_radius(self, radius):
        """
        设置关节的显示大小
        """
        cmds.setAttr(self.jnt + ".radius", radius)


    def reset_joint_orient (self):
        """
        清除关节的关节定向数值
        """
        attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ"
        ]

        for attr in attrs:

            cmds.setAttr(
                "{}.{}".format(
                    self.joint,
                    attr
                ),
                0
            )