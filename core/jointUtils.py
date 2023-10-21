# coding=utf-8

u"""
jointUtils：这是一个用来编写关节工具的模块

目前已有的功能：
avg_joint：在选定的关节上创建新的avg关节用于旋转约束连接

create_joints_on_curve_rigging：基于曲线上的点创建关节(rigging版本)，还未添加是否为曲线的判断

create_joints_on_curve：基于曲线上的点创建关节(通用版本)，还未添加是否为曲线的判断

create_chain：通过放置的模板关节生成相应的IK、FK和Bindjoint

create_mateHuman_chain：通过放置的模板关节创建mateHuman的IK,FK 的关节链

"""

import maya.cmds as cmds
from . import nameUtils
import pymel.core as pm
from pymel.core.nodetypes import Joint
from . import controlUtils , pipelineUtils


class Joint (object) :


    def __init__ (self , jnt , *args , **kwargs) :

        """
        jnt(str)：关节对象
        实例化jnt对象，用pymel.core.nodetypes.Joint类
        """
        self.jnt = jnt
        self.suffix = None
        self.joint_parent = None
        self.joints_chain = None
        self.driven_joint = None
        self.driver_joint = None
        self.avg_jnt = None
        self.bp_joints = None

        # 实例化jnt对象，用pymel.core.nodetypes.Joint类
        self.jnt_obj = Joint (self.jnt)


    def get_AngleZ (self) :
        print (self.jnt_obj.getAngleZ ())


    def avg_joint (self , driven_joint , weight = 0.5) :
        """
        在选定的关节上创建新的avg关节用于旋转约束连接

        Args:
            driven_joint (list): 选定的关节，选定的关节的父层级关节将成为另一个驱动的关节
            weight (float): 两者之间的权重影响

        Returns:
            avg_jnt(str): avg关节的名称
        """
        name_obj = nameUtils.Name (name = driven_joint)
        self.driven_joint = driven_joint
        name_obj.description = name_obj.description + 'Avg'
        self.avg_jnt = cmds.createNode ('joint' , name = name_obj.name)
        # 选定的关节的父层级关节将成为另一个驱动的关节
        self.driver_joint = cmds.listRelatives (self.driven_joint , parent = True)

        cmds.matchTransform (self.avg_jnt , self.driven_joint , position = True)

        # 执行临时的方向约束以获得平均方向
        cons_node = cmds.orientConstraint (self.driver_joint , self.avg_jnt , maintainOffset = False) [0]
        cmds.setAttr (cons_node + '.interpType' , 2)
        cmds.setAttr ('{}.{}W0'.format (cons_node , self.driver_joint) , weight)
        cmds.setAttr ('{}.{}W1'.format (cons_node , self.driven_joint) , 1 - weight)

        # 删除方向约束节点
        cmds.delete (cons_node)
        # 冻结变换
        cmds.makeIdentity (self.avg_jnt , apply = True , translate = True , rotate = True , scale = True)
        # avg关节作为选定关节的子物体
        cmds.parent (self.avg_jnt , self.driver_joint)

        # 执行方向约束以驱动avg关节
        cons_node = cmds.orientConstraint (self.driver_joint , self.driven_joint , maintainOffset = False) [0]
        cmds.setAttr (cons_node + '.interpType' , 2)
        cmds.setAttr ('{}.{}W0'.format (cons_node , self.driver_joint) , weight)
        cmds.setAttr ('{}.{}W1'.format (cons_node , self.driven_joint) , 1 - weight)


    @staticmethod
    def create_joints_on_curve_rigging () :
        u"""基于曲线上的点创建关节(rigging版本)

          """

        curve = cmds.ls (sl = True) [0]
        # 拆分名称
        obj = nameUtils.Name (name = curve)
        name_side = obj.side
        name_description = obj.description
        name_index = obj.index

        # 创建组
        grp_jnts = cmds.createNode ('transform' ,
                                    name = 'grp_{}_{}Jnts_{:03d}'.format (name_side , name_description , name_index))

        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives (curve , shapes = True) [0]

        # 获取曲线跨度和度数
        spans = cmds.getAttr (curve_shape + '.spans')
        degree = cmds.getAttr (curve_shape + '.degree')

        # 获取曲线的点数目
        cv_num = spans + degree

        # 创建关节并吸附到曲线
        for i in range (cv_num) :
            jnt = cmds.createNode ('joint' , name = 'jnt_{}_{}_{:03d}'.format (name_side , name_description , i + 1))
            # 获取cv位置
            cv_pos = cmds.xform ('{}.cv[{}]'.format (curve , i) , query = True , translation = True , worldSpace = True)
            # 设置关节位置
            cmds.xform (jnt , translation = cv_pos , worldSpace = True)
            cmds.parent (jnt , grp_jnts)


    @staticmethod
    def create_joints_on_curve (is_parent = True) :
        u"""基于曲线上的点创建关节(通用版本)
            还未添加是否为曲线的判断
            is_parent(bool):是否需要将关节放在上一次创建出来的关节层级下
            return：
                jnt_dict：将关节的信息资料存储成一个字典返回出去，方便外部调用
          """

        curve = cmds.ls (sl = True) [0]
        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives (curve , shapes = True) [0]
        # 创建组
        jnt_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}Jnts'.format (curve))

        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives (curve , shapes = True) [0]

        # 获取曲线跨度和度数
        spans = cmds.getAttr (curve_shape + '.spans')
        degree = cmds.getAttr (curve_shape + '.degree')

        # 获取曲线的点数目
        cv_num = spans + degree
        jnt_list = []
        # 创建关节并吸附到曲线
        parent = jnt_grp
        for i in range (cv_num) :
            jnt = cmds.createNode ('joint' , name = 'jnt_{}_{:03d}'.format (curve , i + 1) , parent = parent)
            # 获取cv位置
            cv_pos = cmds.xform ('{}.cv[{}]'.format (curve , i) , query = True , translation = True , worldSpace = True)
            # 设置关节位置
            cmds.xform (jnt , translation = cv_pos , worldSpace = True)
            jnt_list.append (jnt)
            # 判断是否需要修改父层级关节
            if is_parent :
                parent = jnt

        # 创建层级组结构
        node_grp = cmds.createNode ('transform' ,
                                    name = 'grp_{}RigNodes'.format (curve))
        cmds.parent (jnt_grp , curve , node_grp)

        # 将关节的信息资料存储成一个字典返回出去，方便外部调用
        jnt_dict = {
            'jnt_list' : jnt_list ,
            'jnt_grp' : jnt_grp ,
            'node_grp' : node_grp
        }
        return jnt_dict


    @staticmethod
    def create_chain (bp_joints , suffix , joint_parent = None) :
        '''通过放置的模板关节生成相应的IK、FK和Bindjoint

        bp_joints(list): 用于放置模板的关节列表。
        suffix(str):要添加到关节的后缀.
        joint_parent(str):关节的父层级物体.

        :return(list):生成的关节列表.
        '''
        # 创建关节
        joints_chain = []
        for jnt in bp_joints :
            jnt_new = jnt
            jnt_new_name = nameUtils.Name (name = jnt_new)
            jnt_new_name.type = 'jnt'
            jnt_new_name.type = '{}{}'.format (suffix , jnt_new_name.type)
            jnt_new = cmds.createNode ('joint' , name = jnt_new_name.name)
            cmds.matchTransform (jnt_new , jnt , position = True , rotation = True)
            cmds.makeIdentity (jnt_new , apply = True , translate = True , rotate = True , scale = True)
            if joint_parent :
                cmds.parent (jnt_new , joint_parent)
            joint_parent = jnt_new
            joints_chain.append (jnt_new)
        cmds.setAttr (bp_joints [0] + '.visibility' , 0)
        return joints_chain


    @staticmethod
    def create_mateHuman_chain (drv_jnts , prefix , joint_parent = None , constraint = False) :
        '''创建mateHuman的IK,FK 的关节链

        drv_jnts(list): 用于放置模板的关节列表。mateHuman的drv_jnts
        prefix(str):要添加到关节的前缀.
        joint_parent(str):关节的父层级物体.
        constraint(bool)：新创建出来的关节是否需要与旧关节做约束

        :return(list):生成的关节列表.
        '''
        # 创建关节
        joints_chain = []
        for jnt in drv_jnts :
            jnt_new = jnt
            jnt_new_name = prefix + jnt_new
            jnt_new = cmds.createNode ('joint' , name = jnt_new_name)
            cmds.matchTransform (jnt_new , jnt , position = True , rotation = True)
            cmds.makeIdentity (jnt_new , apply = True , translate = True , rotate = True , scale = True)
            if constraint :
                cmds.parentConstraint (jnt_new , jnt , mo = True)
                cmds.scaleConstraint (jnt_new , jnt , mo = True)
            if joint_parent :
                cmds.parent (jnt_new , joint_parent)
            joint_parent = jnt_new
            joints_chain.append (jnt_new)
        cmds.setAttr (joints_chain [0] + '.visibility' , 0)
        return joints_chain


    @staticmethod
    def joint_orientation (jnt_list) :
        u'''
        给定关节的列表自动进行关节定向,正常关节定向为X轴指向下一关节，末端关节定向为世界方向
        jnt_list（list）:需要进行关节定向的列表
        '''
        # 删除关节上的约束信息
        cmds.select (jnt_list)
        pipelineUtils.Pipeline.delete_constraints ()
        # 判断关节是否具有子关节
        for jnt in jnt_list :
            cmds.makeIdentity (jnt , apply = True , translate = 1 , rotate = 1 , scale = 1 , normal = 0 ,
                               preserveNormals = 1)
            jnt_sub = cmds.listRelatives (jnt , children = True , allDescendents = True , type = 'joint')
            # 如果有子关节，则关节定向为X轴指向下一关节
            if jnt_sub :
                cmds.joint (jnt , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'xyz' ,
                            secondaryAxisOrient = 'xup')

            # 无子关节，关节定向为世界方向
            else :
                cmds.joint (jnt , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'none')


    @staticmethod
    def show_joint_axis_select () :
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)


    @staticmethod
    def show_joint_axis_hirerarchy () :
        """
        显示选择的层级关节的关节轴向
        """
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)
            child_list = cmds.listRelatives (jnt , children = True , type = 'joint' , allDescendents = True)
            if child_list :
                for child in child_list :
                    cmds.setAttr (child + '.displayLocalAxis' , 1)
            else :
                return


    @staticmethod
    def show_joint_axis_all () :
        joints = cmds.ls (type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)


    @staticmethod
    def hide_joint_axis_select () :
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 0)


    @staticmethod
    def hide_joint_axis_hirerarchy () :
        """
        隐藏选择的层级关节的关节轴向
        """
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 0)
            child_list = cmds.listRelatives (jnt , children = True , type = 'joint' , allDescendents = True)
            if child_list :
                for child in child_list :
                    cmds.setAttr (child + '.displayLocalAxis' , 0)
            else :
                return


    @staticmethod
    def hide_joint_axis_all () :
        joints = cmds.ls (type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 0)


    @staticmethod
    def set_jointSize (value) :
        joints = cmds.ls (type = 'joint')
        for joint in joints :
            cmds.setAttr (joint + '.radius' , value)


    @staticmethod
    def create_snap_joint():
        """
        吸附创建——关节
        """
        objs_list = cmds.ls (selection = True , flatten = True)
        if len (objs_list) >= 1 :
            obj = cmds.createNode ('joint' , name = 'jnt_' + objs_list [0])
            snap_modle = 'Position + Rotation'
            jnt = snapUtils.Snap (obj , objs_list , snap_modle)
            jnt.snap ()
        else :
            cmds.warning ("请选择一个或以上的物体或者Cv点")


    @staticmethod
    def create_child_joint():
        """
        在选择对象的下层创建子关节
        """
        objs_list = cmds.ls (selection = True , flatten = True)
        if len (objs_list) >= 1 :
            for obj in objs_list:
                child_jnt = cmds.createNode('joint' , name = obj + '_childJoint')
                cmds.matchTransform(child_jnt,obj)
                cmds.parent(child_jnt,obj)
        else :
            cmds.warning ("请选择一个或以上的物体")
