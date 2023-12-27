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
import pymel.core as pm
from PySide2.QtWidgets import *
from pymel.core.nodetypes import Joint

from . import controlUtils , pipelineUtils , qtUtils , hierarchyUtils , snapUtils
from . import nameUtils


class Joint (object) :


    def __init__ (self , jnt , *args , **kwargs) :

        """
        jnt(str)：关节对象
        实例化jnt对象，用pymel.core.nodetypes.Joint类
        """
        self.jnt = jnt
        self.suffix = None
        self.jnt_parent = None
        self.joints_chain = None
        self.driven_joint = None
        self.driver_joint = None
        self.avg_jnt = None
        self.bp_joints = None

        # 实例化jnt对象，用pymel.core.nodetypes.Joint类
        self.jnt_obj = Joint (self.jnt)


    def get_AngleZ (self) :
        print (self.jnt_obj.getAngleZ ())


    #    在选定的关节上创建新的avg关节用于旋转约束连接
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


    # 基于曲线上的点创建关节(rigging版本)
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


    # 基于曲线上的点创建关节(通用版本)
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


    # 通过放置的模板关节生成相应的IK、FK和Bindjoint
    @staticmethod
    def create_chain (bp_joints , suffix , jnt_parent = None) :
        '''通过放置的模板关节生成相应的IK、FK和Bindjoint

        bp_joints(list): 用于放置模板的关节列表。
        suffix(str):要添加到关节的后缀.
        jnt_parent(str):关节的父层级物体.

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
            if jnt_parent :
                cmds.parent (jnt_new , jnt_parent)
            jnt_parent = jnt_new
            joints_chain.append (jnt_new)
        cmds.setAttr (bp_joints [0] + '.visibility' , 0)
        return joints_chain


    # 创建mateHuman的IK,FK 的关节链
    @staticmethod
    def create_mateHuman_chain (drv_jnts , prefix , jnt_parent = None , constraint = False) :
        '''创建mateHuman的IK,FK 的关节链

        drv_jnts(list): 用于放置模板的关节列表。mateHuman的drv_jnts
        prefix(str):要添加到关节的前缀.
        jnt_parent(str):关节的父层级物体.
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
            if jnt_parent :
                cmds.parent (jnt_new , jnt_parent)
            jnt_parent = jnt_new
            joints_chain.append (jnt_new)
        cmds.setAttr (joints_chain [0] + '.visibility' , 0)
        return joints_chain


    # 给定关节的列表自动进行关节定向,正常关节定向为X轴指向下一关节，末端关节定向为世界方向
    @staticmethod
    def joint_orientation (jnt_list) :
        u'''
        给定关节的列表自动进行关节定向,正常关节定向为X轴指向下一关节，末端关节定向为世界方向
        jnt_list（list）:需要进行关节定向的列表
        '''
        # 删除关节上的约束信息
        cmds.select (jnt_list,replace = True)
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


    # 显示选择的关节的关节方向
    @staticmethod
    def show_joint_axis_select () :
        """
        显示指定的关节的关节方向
        """
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)


    # 显示选择的层级关节的关节轴向
    @staticmethod
    def show_joint_axis_hirerarchy () :
        """
        显示选择的层级关节的关节轴向
        """
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)
            # 获取选定的关节底下是否还有子关节
            child_list = cmds.listRelatives (jnt , children = True , type = 'joint' , allDescendents = True)
            if child_list :
                for child in child_list :
                    cmds.setAttr (child + '.displayLocalAxis' , 1)
            else :
                return


    # 显示场景里所有关节的关节轴向
    @staticmethod
    def show_joint_axis_all () :
        """
        显示场景里所有关节的关节轴向
        """
        joints = cmds.ls (type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 1)


    # 隐藏选择的关节的关节方向
    @staticmethod
    def hide_joint_axis_select () :
        """
        隐藏选择的关节的关节方向
        """
        joints = cmds.ls (sl = True , type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 0)


    # 隐藏选择的层级关节的关节轴向
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


    # 隐藏场景里所有关节的关节轴向
    @staticmethod
    def hide_joint_axis_all () :
        # 隐藏场景里所有关节的关节轴向
        joints = cmds.ls (type = 'joint')
        for jnt in joints :
            cmds.setAttr (jnt + '.displayLocalAxis' , 0)


    # 设置场景里所有关节的关节大小
    @staticmethod
    def set_jointSize (value) :
        joints = cmds.ls (type = 'joint')
        for joint in joints :
            cmds.setAttr (joint + '.radius' , value)


    # 选择点或者物体组件创建关节
    @staticmethod
    def create_snap_joint () :
        """
        选择点或者物体组件创建关节
        """
        objs_list = cmds.ls (selection = True , flatten = True)
        if len (objs_list) >= 1 :
            obj = cmds.createNode ('joint' , name = 'jnt_' + objs_list [0])
            combo_txt = 'Position + Rotation'
            jnt = snapUtils.Snap (obj , objs_list , combo_txt)
            jnt.snap ()
        else :
            cmds.warning ("请选择一个或以上的物体或者Cv点")


    # 在选择对象的下层创建子关节
    @staticmethod
    def create_child_joint () :
        """
        在选择对象的下层创建子关节
        返回：
            child_jnt：子关节
        """
        objs_list = cmds.ls (selection = True , flatten = True)
        child_jnt_list = []
        if len (objs_list) >= 1 :
            for obj in objs_list :
                child_jnt = cmds.createNode ('joint' , name = obj + '_childJoint')
                cmds.matchTransform (child_jnt , obj)
                cmds.parent (child_jnt , obj)
                child_jnt_list.append (child_jnt)
        else :
            cmds.warning ("请选择一个或以上的物体")
        return child_jnt_list


    # 关节重采样工具
    @staticmethod
    def create_more_joint () :
        """
        关节重采样工具
        """
        try :
            window.close ()  # 关闭窗口
            window.deleteLater ()  # 删除窗口
        except :
            pass
        window = Joint_Resampling ()  # 创建实例
        window.show ()  # 显示窗口


    # 关节重采样，选择起始关节和末端关节，在二者中间重新构建指定数量的关节链条
    @staticmethod
    def resample_joint (startJoint , endJoint , jnt_number) :
        """
        关节重采样，选择起始关节和末端关节，在二者中间重新构建指定数量的关节链条
        startJoint(str):起始关节
        endJoint(str):末端关节
        jnt_number(int)：指定数量的关节链条
        """
        jnt_parent = startJoint
        # 获取起始关节与末端关节之间的距离
        try :
            cmds.parent (endJoint , startJoint)
        except :
            pass
        tx_value = cmds.getAttr (endJoint + '.translateX') / jnt_number
        cmds.parent (endJoint , world = True)
        cmds.delete (cmds.listRelatives (startJoint , children = True))
        # 根据指定的关节数量，循环创建对应的关节
        for index in range (jnt_number) :
            jnt = cmds.createNode ('joint' , name = startJoint + '_{:03d}'.format (index))
            cmds.matchTransform (jnt , startJoint)
            cmds.parent (jnt , jnt_parent)
            cmds.setAttr (jnt + '.translateX' , tx_value)
            jnt_parent = jnt
        cmds.parent (endJoint , startJoint + '_{:03d}'.format (jnt_number - 1))


    # 按照选择的顺序将关节组成关节链条
    @staticmethod
    def joint_To_Chain_Selection () :
        """
        按照选择的顺序将关节组成关节链条
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for i in range (len (jnt_list) - 1 , 0 , -1) :
            pm.parent (jnt_list [i] , jnt_list [i - 1])


    # 根据模型上所选择的边生成新的曲线，生成关节链条
    @staticmethod
    def create_chain_on_polyToCurve () :
        """
        根据模型上所选择的边生成新的曲线，生成关节链条
        """
        # 根据模型上所选择的边，模型的边到曲线生成新的曲线
        curve = pipelineUtils.Pipeline.create_curve_on_polyToCurve ('curve_polyToCurve' , degree = 3)
        cmds.select (curve , replace = True)
        # 选择生成后的曲线创建关节
        Joint.create_joints_on_curve ()


    # 打开选择的关节的分段比例补偿
    @staticmethod
    def open_joint_scaleCompensate () :
        """
        打开选择的关节的分段比例补偿
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for jnt in jnt_list :
            cmds.setAttr (jnt + '.segmentScaleCompensate' , 1)


    # 关闭选择的关节的分段比例补偿
    @staticmethod
    def close_joint_scaleCompensate () :
        """
        关闭选择的关节的分段比例补偿
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for jnt in jnt_list :
            cmds.setAttr (jnt + '.segmentScaleCompensate' , 0)


    # 选择关节，批量制作约束。不需要新添加创建关节来蒙皮物体
    @staticmethod
    def batch_Constraints_joint () :
        u"""
        选择关节，批量制作约束。不需要新添加创建关节来蒙皮物体		"""
        sel_list = cmds.ls (sl = True , type = 'joint')
        for sel in sel_list :
            cmds.undoInfo (openChunk = True)  # 批量撤销的开头
            # 创建对应的控制器组
            ctrl = controlUtils.Control (n = 'ctrl_' + sel , s = 'cube' , r = 1)
            ctrl_transform = '{}'.format (ctrl.transform)
            sub_ctrl = controlUtils.Control (n = 'ctrlSub_' + sel , s = 'cube' , r = 1 * 0.7)
            sub_ctrl.set_parent (ctrl.transform)
            sub_ctrl_transform = '{}'.format (sub_ctrl.transform)
            # 添加上层层级组
            offset_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = ctrl_transform , grp_name = '{}'.format (ctrl_transform.replace ('ctrl' , 'offset')) ,
                world_orient = False)
            connect_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = offset_grp , grp_name = offset_grp.replace ('offset' , 'connect') , world_orient = False)
            driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = connect_grp , grp_name = connect_grp.replace ('connect' , 'driven') , world_orient = False)
            zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
                obj = driven_grp , grp_name = driven_grp.replace ('driven' , 'zero') , world_orient = False)

            # 创建output层级组
            output = cmds.createNode ('transform' , name = ctrl_transform.replace ('ctrl_' , 'output_') ,
                                      parent = ctrl_transform)

            # 连接次级控制器的属性
            cmds.connectAttr (sub_ctrl.transform + '.translate' , output + '.translate')
            cmds.connectAttr (sub_ctrl.transform + '.rotate' , output + '.rotate')
            cmds.connectAttr (sub_ctrl.transform + '.scale' , output + '.scale')
            cmds.connectAttr (sub_ctrl.transform + '.rotateOrder' , output + '.rotateOrder')
            cmds.addAttr (ctrl_transform , attributeType = 'bool' , longName = 'subCtrlVis' ,
                          niceName = U'次级控制器显示' ,
                          keyable = True)
            cmds.connectAttr (ctrl_transform + '.subCtrlVis' , sub_ctrl_transform + '.visibility')
            # 将控制器组吸附到对应的关节位置。并且进行约束
            cmds.matchTransform (zero_grp , sel)
            cmds.parentConstraint (sub_ctrl_transform , sel , mo = True)
            cmds.scaleConstraint (sub_ctrl_transform , sel , mo = True)
            cmds.undoInfo (openChunk = False)  # 批量撤销的开头


    # 将选中的关节的关节定向数值添加到通道盒里
    @staticmethod
    def show_joint_orient () :
        """
        将选中的关节的关节定向数值添加到通道盒里
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for jnt in jnt_list :
            cmds.setAttr (jnt + '.jointOrientX' , keyable = True)
            cmds.setAttr (jnt + '.jointOrientY' , keyable = True)
            cmds.setAttr (jnt + '.jointOrientZ' , keyable = True)


    # 将选中的关节的关节定向数值从通道盒里隐藏
    @staticmethod
    def hide_joint_orient () :
        """
        将选中的关节的关节定向数值从通道盒里隐藏
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for jnt in jnt_list :
            cmds.setAttr (jnt + '.jointOrientX' , keyable = False)
            cmds.setAttr (jnt + '.jointOrientY' , keyable = False)
            cmds.setAttr (jnt + '.jointOrientZ' , keyable = False)


    # 将选中的关节的关节定向数值清零
    @staticmethod
    def clear_joint_orient () :
        """
        将选中的关节的关节定向数值清零
        """
        jnt_list = cmds.ls (sl = True , type = 'joint')
        for jnt in jnt_list :
            cmds.setAttr (jnt + '.jointOrientX' , 0)
            cmds.setAttr (jnt + '.jointOrientY' , 0)
            cmds.setAttr (jnt + '.jointOrientZ' , 0)


    # 创建次级控制器的次级关节，用于做衣服的次级控制器
    # 思路：在关节下面创建一个子关节，子关节保持和父关节相同的位置，然后被次级控制器连接所有属性
    @staticmethod
    def create_secondary_joint () :
        """
        创建次级控制器的次级关节，用于做衣服的次级控制器
        思路：在关节下面创建一个子关节，子关节保持和父关节相同的位置，然后被次级控制器连接所有属性
        """
        # 选择需要创建次级控制器的关节
        jnts = cmds.ls (sl = True , type = 'joint')

        # 对关节创建控制器
        pipelineUtils.Pipeline.batch_Constraints_joint ()

        # 断开关节的约束
        cmds.select (jnts , replace = True)
        pipelineUtils.Pipeline.delete_constraints ()

        # 对所有选中的关节进行循环，对其创建子关节并且连接子关节的属性
        # 在选择的关节下创建子关节
        Joint.create_child_joint ()
        for jnt in jnts :
            for attr in ['translate' , 'rotate'] :
                for axis in ['X' , 'Y' , 'Z'] :
                    ctrl = 'ctrl_' + jnt
                    child_jnt = jnt + '_childJoint'
                    # 将子关节的属性清空
                    cmds.setAttr (child_jnt + '.{}{}'.format (attr , axis) , 0)
                    # 将次级控制器的属性与生成的次级关节进行连接
                    cmds.connectAttr (ctrl + '.{}{}'.format (attr , axis) , child_jnt + '.{}{}'.format (attr , axis))


    # 根据关节的名称，该脚本将关节的一些属性进行设置，根据关节的名称，设置了关节的 side、type 和 otherType 属性。
    def tag_joint (self) :
        """
        根据关节的名称，该脚本将关节的一些属性进行设置，根据关节的名称，设置了关节的 side、type 和 otherType 属性。
        1.获取场景中所有类型为 'joint' 的关节对象。
        2.遍历每个关节对象，根据关节名称的一部分（使用下划线 _ 分割）来确定关节的侧（left、right 或未知）。
        3.根据关节的侧设置 side 属性的值。如果侧为 'l'，则设置为 1；如果侧为 'r'，则设置为 2；否则设置为 0。
        4.设置 type 属性的值为 18。
        5.将关节名称的其他部分连接起来，并将结果设置为 otherType 属性，其类型为字符串。
        Args:
            self.jnt (str): 需要设置关节的名称
        """

        name_parts = self.jnt.split ('_')

        if name_parts [1] == 'l' :
            side_index = 1
        elif name_parts [1] == 'r' :
            side_index = 2
        else :
            side_index = 0

        cmds.setAttr (self.jnt + '.side' , side_index)
        cmds.setAttr (self.jnt + '.type' , 18)
        cmds.setAttr (self.jnt + '.otherType' , name_parts [2] + name_parts [3] , type = 'string')


class Joint_Resampling (QDialog) :
    """
    关节重采样工具的页面编写
    """


    def __init__ (self , parent = qtUtils.get_maya_window ()) :
        super (Joint_Resampling , self).__init__ (parent)
        self.setWindowTitle ("关节重采样工具")
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        # 在start_layout里面添加控件
        self.start_label = QLabel ('startJoint:')
        self.start_line = QLineEdit ()
        self.start_pick_btn = QPushButton ('拾取起始关节')

        # 在end_layout里面添加控件
        self.end_label = QLabel ('endJoint:')
        self.end_line = QLineEdit ()
        self.end_pick_btn = QPushButton ('拾取末端关节')

        # 在jnt_number_layout 里面添加控件
        self.jnt_number_label = QLabel ('jnt_number:')
        self.jnt_number_spine = QSpinBox ()
        self.jnt_number_spine.setValue (2)

        #
        self.resample_btn = QPushButton ('resample')


    def create_layouts (self) :
        # 添加页面布局
        self.start_layout = QHBoxLayout ()
        self.start_layout.addWidget (self.start_label)
        self.start_layout.addWidget (self.start_line)
        self.start_layout.addWidget (self.start_pick_btn)

        self.end_layout = QHBoxLayout ()
        self.end_layout.addWidget (self.end_label)
        self.end_layout.addWidget (self.end_line)
        self.end_layout.addWidget (self.end_pick_btn)

        self.joint_layout = QHBoxLayout ()
        self.joint_layout.addWidget (self.jnt_number_label)
        self.joint_layout.addWidget (self.jnt_number_spine)
        self.joint_layout.addStretch ()

        self.main_layout = QVBoxLayout (self)

        self.main_layout.addLayout (self.start_layout)
        self.main_layout.addLayout (self.end_layout)
        self.main_layout.addLayout (self.joint_layout)
        self.main_layout.addWidget (self.resample_btn)


    def create_connections (self) :
        self.start_pick_btn.clicked.connect (self.pick_startJoint_line)
        self.end_pick_btn.clicked.connect (self.pick_endJoint_line)

        self.resample_btn.clicked.connect (self.clicked_resample_btn)


    # 拾取起始关节
    def pick_startJoint_line (self) :
        """
        拾取起始关节
        """
        startJoint = cmds.ls (sl = True , type = 'joint')
        if len (startJoint) != 1 :
            pm.warning ("选择了多个关节，请只选择一个关节作为关节重采样的起始关节 " + startJoint)
            return
        else :
            self.start_line.setText (startJoint [0])
            pm.warning ("设定了{}为关节重采样的起始关节 ".format (startJoint [0]))


    # 拾取末端关节
    def pick_endJoint_line (self) :
        """
                拾取末端关节
                """
        endJoint = cmds.ls (sl = True , type = 'joint')
        if len (endJoint) != 1 :
            pm.warning ("选择了多个关节，请只选择一个关节作为关节重采样的起始关节 " + endJoint)
            return
        else :
            self.end_line.setText (endJoint [0])
            pm.warning ("设定了{}为关节重采样的起始关节 ".format (endJoint [0]))


    def clicked_resample_btn (self) :
        startJoint = self.start_line.text ()
        endJoint = self.end_line.text ()
        jnt_number = self.jnt_number_spine.value ()

        Joint.resample_joint (startJoint , endJoint , jnt_number)
