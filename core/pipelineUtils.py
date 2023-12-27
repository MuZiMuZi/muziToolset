# coding=utf-8
u"""
这是一个用来编写流程工具的类

目前已有的功能：

clear_keys: 清除场景内所有的关键帧
add_face_tag : 将“isFace”标记添加到所选物体的属性上
remove_non_face_objs：移除没有带“isFace”标志的物体
copy_weight：复制蒙皮
rename_bs_sc：批量重命名对象的蒙皮和混合变形节点
distence_between：获取两个对象之间的距离.
reset_control：重置控制器上所有的数值.
list_operation：将两个列表的并集/差分/交集/对称_差分部分作为列表返回.
tag_joint：对选择的关节添加关节标签
batch_Constraints：选中多个物体，批量对物体进行约束
default_grp： 添加绑定的初始层级组，并隐藏连接对应的属性
create_constraints：快速创建约束	用法：先选择需要约束的物体，在选择被约束的物体
delete_constraints：删除所选择物体的所有约束节点
select_sub_objects：快速选择所选物体的所有子物体
finger_Connect：  adv重新生成后手指的驱动可能会消失，于是可以依靠这个代码重新连接
create_node：根据给定的节点类型，在给定的位置生成新的节点。
get_maya_main_window()：获取maya的主窗口
save_file_as：另存为文件
get_current_scene_path ： 获取当前文件的绝对路径
create_reference：在maya里的当前文件创建引用
create_native_script_job:创建回调函数在新场景打开的时候执行回调函数
fbxExport:所选择的物体导出成为fbx文件

"""
import math
import os
import re
import sys
from functools import partial
from functools import wraps
import logging
import os

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from PySide2 import QtWidgets
# noinspection PyUnresolvedReferences
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
from maya import mel
from pymel.util import path
from shiboken2 import wrapInstance
from importlib import reload
from . import controlUtils , hierarchyUtils , qtUtils , jointUtils, nameUtils


reload (jointUtils)


class Pipeline (object) :

    def __init__ (self) :
        pass


    # 清除场景内所有的关键帧
    @staticmethod
    def clear_keys () :
        u"""
        清除场景内所有的动画关键帧
        :return:
        """
        animCurves = cmds.ls (type = ['animCurveTA' , 'animCurveTL' , 'animCurveTU'])
        if animCurves :
            cmds.delete (animCurves)
            cmds.warning (u"已清除场景内所有的动画关键帧")
        else :
            cmds.warning (u"场景内没有动画关键帧")


    # 将“isFace”标记添加到所选物体的属性上
    @staticmethod
    def add_face_tag () :
        u"""将“isFace”标记添加到所选物体的属性上.

        """

        sel_to_tag_list = cmds.ls (sl = True)

        for sel in sel_to_tag_list :
            if not cmds.objExists ('{}.isFace'.format (sel)) :
                cmds.addAttr (sel , ln = 'isFace' , at = 'bool' , dv = 1)
                cmds.setAttr ('{}.isFace'.format (sel) , keyable = False , channelBox = False)


    # 移除没有带face标志的物体.
    @staticmethod
    def remove_non_face_objs () :
        u"""“移除没有带face标志的物体.

        """

        assemblies = cmds.ls (assemblies = True)

        for assembly in assemblies :
            children = cmds.listRelatives (assembly , allDescendents = True , type = 'transform')
            if children :
                for child in children :
                    if not cmds.objExists ('{}.isFace'.format (child)) or not cmds.getAttr (
                            '{}.isFace'.format (child)) :
                        cmds.delete (child)


    # 获取两个对象之间的距离.
    @staticmethod
    def distence_between (node_a , node_b) :
        u'''获取两个对象之间的距离.
        node_a(str): 对象a.
        node_b(str): 对象b.

        :return
        dist(float):两个对象之间的距离.
        '''
        point_a = cmds.xform (node_a , query = True , worldSpace = True , rotatePivot = True)
        point_b = cmds.xform (node_b , query = True , worldSpace = True , rotatePivot = True)
        dist = math.sqrt (sum ([pow ((b - a) , 2) for b , a in zip (point_a , point_b)]))
        return dist


    # 重置绑定系统的控制器上所有的数值.
    @staticmethod
    def reset_control () :
        u"""重置绑定系统的控制器上所有的数值.



         """
        ctrl_node = cmds.ls ('ctrl_?_*_???')
        attrs = ['translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ']
        scale_attrs = ['scaleX' , 'scaleY' , 'scaleZ']
        for ctrl in ctrl_node :
            for attr in attrs :
                lock_val = cmds.getAttr (ctrl + '.{}'.format (attr) , lock = True)
                if lock_val == 0 :
                    cmds.setAttr (ctrl + '.{}'.format (attr) , 0)
                else :
                    pass
            for scale_attr in scale_attrs :
                lock_val = cmds.getAttr (ctrl + '.{}'.format (scale_attr) , lock = True)
                if lock_val == 0 :
                    cmds.setAttr (ctrl + '.{}'.format (scale_attr) , 1)
                else :
                    pass
        ctrl_IKFKblend = cmds.ls ('ctrl_?_*IKFKBend_???')
        for IKFKblend in ctrl_IKFKblend :
            cmds.setAttr (IKFKblend + '.IkFkBend' , 1)


    # 根据传入的操作符号（|, &, -, ^）返回两个列表的并集、交集、差分或对称差分。
    @staticmethod
    def list_operation (list_a , list_b , operation = '|') :
        u"""将两个列表的并集/差分/交集/对称_差分部分作为列表返回.
        用于执行集合操作的 Python 函数，根据传入的操作符号（|, &, -, ^）返回两个列表的并集、交集、差分或对称差分。
        Args:
            list_a (list/None): 第一个列表.
            list_b (list/None): 第二个列表.
            operation (str): 运算符号为 '|', '&', '-', '^'.

        具体而言，该函数的实现步骤如下：

        1.将传入的两个列表（list_a 和 list_b）转换为集合（set_a 和 set_b）。
        2.根据传入的操作符号执行相应的集合操作。
        3.将结果转换回列表并返回。

        Returns:
            list: 作为列表的两个列表的并集/差分/交集/对称_差分部分.

        """

        # 如果无，则将无转换为[]空列表，仅用于操作
        if not list_a :
            list_a = []
        if not list_b :
            list_b = []

        set_a = set (list_a)
        set_b = set (list_b)

        if operation == '|' :
            return list (set_a.union (set_b))
        elif operation == '&' :
            return list (set_a.intersection (set_b))
        elif operation == '-' :
            return list (set_a.difference (set_b))
        elif operation == '^' :
            return list (set_a.symmetric_difference (set_b))


    # 选择物体，批量制作约束。新添加创建关节来蒙皮物体
    @staticmethod
    def batch_Constraints_modle () :
        u"""
        选择物体，批量制作约束。新添加创建关节来蒙皮物体		"""
        sel_list = cmds.ls (sl = True)
        for sel in sel_list :
            cmds.undoInfo (openChunk = True)  # 批量撤销的开头
            # 创建对应的关节来蒙皮物体
            jnt = cmds.createNode ('joint' , name = 'jnt_' + sel)
            cmds.matchTransform (jnt , sel)
            cmds.skinCluster (jnt , sel)
            # 创建对应的控制器组
            ctrl = controlUtils.Control (n = 'ctrl_' + sel , s = 'hexagon' , r = 1)
            ctrl_transform = '{}'.format (ctrl.transform)
            sub_ctrl = controlUtils.Control (n = 'ctrlSub_' + sel , s = 'hexagon' , r = 1 * 0.7)
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
            cmds.matchTransform (zero_grp , jnt)
            cmds.parentConstraint (sub_ctrl_transform , jnt , mo = True)
            cmds.scaleConstraint (sub_ctrl_transform , jnt , mo = True)
            cmds.undoInfo (openChunk = False)  # 批量撤销的开头


    # 选择关节，批量制作约束。不需要新添加创建关节来蒙皮物体
    @staticmethod
    def batch_Constraints_joint () :
        u"""
        选择关节，批量制作约束。不需要新添加创建关节来蒙皮物体		"""
        sel_list = cmds.ls (sl = True)
        for sel in sel_list :
            cmds.undoInfo (openChunk = True)  # 批量撤销的开头
            # 创建对应的控制器组
            ctrl = controlUtils.Control (n = 'ctrl_' + sel , s = 'hexagon' , r = 1)
            ctrl_transform = '{}'.format (ctrl.transform)
            sub_ctrl = controlUtils.Control (n = 'ctrlSub_' + sel , s = 'hexagon' , r = 1 * 0.7)
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


    # 快速创建约束.用法：先选择需要约束者，在选择被约束者
    @staticmethod
    def create_constraints () :
        u"""
        快速创建约束.
        用法：先选择需要约束者，在选择被约束者
        driver_obj：约束者
        driven_obj：被约束者
        """
        sel = cmds.ls (sl = True)
        driver_obj = sel [0 :-1]
        driven_obj = sel [-1]
        cmds.parentConstraint (driver_obj , driven_obj , mo = True)
        cmds.scaleConstraint (driver_obj , driven_obj , mo = True)


    # 快速选择物体的约束节点
    @staticmethod
    def select_constraints () :
        u'''
        快速选择物体的约束节点
        '''
        sel = cmds.ls (sl = True)
        for obj in sel :
            const = cmds.listConnections (obj , type = 'constraint')
            if const :
                cmds.select (const , replace = True)


    # 快速删除选择物体的约束节点
    @staticmethod
    def delete_constraints () :
        u'''
        快速删除选择物体的约束节点
        '''
        sel = cmds.ls (sl = True)
        for obj in sel :
            const = cmds.listConnections (obj , type = 'constraint')
            if const :
                cmds.delete (const)


    # 这是一个装饰器，用于将一系列操作的撤销 包裹成一个撤销操作
    @staticmethod
    def make_undo (func) :
        """
            这是一个装饰器，用于将一系列操作的撤销 包裹成一个撤销操作
        """


        @wraps (func)
        def wrap (*args , **kwargs) :
            cmds.undoInfo (openChunk = True)
            result = func (*args , **kwargs)
            cmds.undoInfo (closeChunk = True)
            return result


        return wrap


    # 根据给定的节点类型，在给定的位置生成新的节点。常用来创建关节
    @staticmethod
    def create_node (node_type , node_name , match = False , match_node = None) :
        u'''
        根据给定的节点类型，在给定的位置生成新的节点。
        node_type；创建的新的节点类型
        node_name:创建的新的节点名称
        match:是否吸附对应的位置
        match_node:吸附对应的位置
        '''
        new_node = cmds.createNode (node_type , name = node_name)
        if match :
            cmds.matchTransform (new_node , match_node , position = True , rotation = True , scale = True)

        return new_node


    # 创建回调函数在新场景打开的时候执行回调函数
    @staticmethod
    def create_native_script_job (event_name , callback) :
        #############################################################
        # 创建回调函数在新场景打开的时候执行回调函数
        #############################################################
        scene_open_callback_id = om.MEventMessage.addEventCallback (
            event_name , callback)
        # 创建回调函数被销毁的机制，防止重复调用
        return partial (om.MEventMessage.removeCallback , scene_open_callback_id)


    # 这是一个用于在 Maya 中创建约束（constraint）的函数。
    @staticmethod
    def create_constraint (driver , driven , point_value = False , orient_value = False , parent_value = True ,
                           scale_value = False ,
                           mo_value = True) :
        '''

        这是一个用于在 Maya 中创建约束（constraint）的函数。该函数接受以下参数：

        driver(str): 约束的驱动对象。
        driven(str): 被约束的对象。
        point_value(bool): 布尔值，指示是否创建点约束（默认为 False）。
        orient_value(bool): 布尔值，指示是否创建方向约束（默认为 False）。
        parent_value(bool): 布尔值，指示是否创建父级约束（默认为 True）。
        scale_value(bool): 布尔值，指示是否创建缩放约束（默认为 False）。
        mo_value(bool): 布尔值，指示是否使用移动轴心（默认为 True）。
        '''
        if point_value :
            cmds.pointConstraint (driver , driven , mo = mo_value)
        if orient_value :
            cmds.orientConstraint (driver , driven , mo = mo_value)
        if parent_value :
            cmds.parentConstraint (driver , driven , mo = mo_value)
        if scale_value :
            cmds.scaleConstraint (driver , driven , mo = mo_value)


    # 位移物体到指定的位置
    @staticmethod
    def move (obj , pos) :
        """
        位移物体到指定的位置

        :param obj: str. maya的对象
        :param pos: list. 位置信息 x, y and z
        """

        return cmds.move (pos [0] , pos [1] , pos [2] , obj , r = 1)


    # 曲线的总长度为1，给定需要平分的点数量，返回每个点的位置信息
    @staticmethod
    def get_percentages (sample_count) :
        """
        曲线的总长度为1，给定需要平分的点数量，返回每个点的位置信息
        例子：get_percentages(5) == [0.0, 0.25, 0.5, 0.75, 1.0]
        :param sample_count: int. 需要平分的点数量
        :return: list. 返回每个点的位置信息
        """
        if sample_count <= 1 :
            return

        outputs = list ()
        gap = 1.00 / (sample_count - 1)
        for index in range (sample_count) :
            outputs.append (index * gap)

        return outputs


    # 这是一个用于在 Maya 中获取指定节点的 DAG（Directed Acyclic Graph）路径的函数。函数接受一个参数 node，即 Maya 的节点对象（node name），并返回该节点的 DAG 路径（DAG path）。
    @staticmethod
    def get_dag_path (node = None) :
        """
        这是一个用于在 Maya 中获取指定节点的 DAG（Directed Acyclic Graph）路径的函数。函数接受一个参数 node，即 Maya 的节点对象（node name），并返回该节点的 DAG 路径（DAG path）。
        :param node: str. maya的节点对象
        :return: str. DAG 路径
        """
        # 创建一个 MSelectionList 对象，用于存储要查询的节点。
        selection = om.MSelectionList ()

        # 将指定的节点名称添加到 MSelectionList 中。
        selection.add (node)

        # 创建一个 MDagPath 对象，用于存储 DAG 路径。
        dag_path = om.MDagPath ()
        # 使用 getDagPath 方法从 MSelectionList 中获取 DAG 路径，并将结果存储在 MDagPath 对象中。
        selection.getDagPath (0 , dag_path)
        # 返回 DAG 路径。
        return dag_path


    # 获取具有均匀距离的nurbs曲线上的点信息
    @staticmethod
    def get_point_on_curve (curve , sample_count) :
        """
        获取具有均匀距离的nurbs曲线上的点信息
        https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_class_m_fn_nurbs_curve_html

        :param curve: str. nurbs曲线的名称
        :param sample_count: int. 采样点的数量
        :return: tuple. om.MPoint object and om.MVector object
        """
        plists = Pipeline.get_percentages (sample_count)

        points = list ()
        tangents = list ()
        crv_fn = om.MFnNurbsCurve (Pipeline.get_dag_path (curve))
        for percentage in plists :
            parameter = crv_fn.findParamFromLength (crv_fn.length () * percentage)
            point = om.MPoint ()
            crv_fn.getPointAtParam (parameter , point)
            tangent = crv_fn.tangent (parameter)

            points.append (point)
            tangents.append (tangent)

        return points , tangents


    # 在 Maya 中创建均匀分布在曲线上的关节点的函数。
    @staticmethod
    def create_joints_on_curve (curve , sample_count) :
        """
        在 Maya 中创建均匀分布在曲线上的关节点的函数。函数接受两个参数：

        :param curve: str. 曲线的节点名称
        :param sample_count: int. 采样点的数量
        :return: list. 返回创建关节的列表
        """

        jnt_list = list ()
        # 获取具有均匀距离的 nurbs 曲线上的点信息和切线信息。
        points , tangents = Pipeline.get_point_on_curve (curve , sample_count)

        # 遍历每个点，为每个点创建一个关节，并在对应的点上创建一个 transform 组来做目标约束吸附旋转。
        for index in range (len (points)) :
            point = points [index]
            tangent = tangents [index]

            # 在对应的点上创建关节，并且创建个transform组来做目标约束吸附旋转
            # 使用 cmds.createNode('joint') 创建关节，并使用 cmds.createNode('transform') 创建 transform 组。
            jnt = cmds.createNode ('joint')
            jnt_list.append (jnt)
            temp_node = cmds.createNode ('transform')

            # 使用 cmds.xform 设置 transform 组的位置为点坐标加上切线。设置关节的位置为点坐标。
            cmds.xform (
                temp_node ,
                t = [point.x + tangent.x , point.y + tangent.y , point.z + tangent.z]
            )
            cmds.xform (jnt , t = [point.x , point.y , point.z])

            # 使用 cmds.aimConstraint 创建一个 Aim 约束，将 transform 组约束到关节上。
            constraint = cmds.aimConstraint (temp_node , jnt) [0]

            # 删除创建的临时节点和约束。
            cmds.delete ([temp_node , constraint])

        # 返回创建的关节列表。
        return jnt_list

        ###简单的示例
        # # 假设有一个曲线的节点名称和采样点的数量
        # curve_name = "curve1"
        # sample_count = 10
        #
        # # 调用函数创建均匀分布在曲线上的关节点
        # joints_list = create_joints_on_curve (curve_name , sample_count)
        #
        # # 打印创建的关节列表
        # print (joints_list)


    # 根据给定关节点的位置生成曲线的函数
    @staticmethod
    def create_curve_on_joints (jnt_list , curve , degree = 3) :
        u"""
       根据给定关节点的位置生成曲线的函数
        jnt_list(list):关节的列表
        curve（str）：创建出来的曲线的名称
        degree(int)：新曲线的阶数。默认值为3。请注意，您需要（阶数+1）个曲线点来创建可见的曲线跨度。你必须为3度曲线放置4个点。

        return:
            返回创建出来的曲线curve
        """
        # 创建一个列表用来存储点的位置信息
        curve_points = list ()

        # 遍历 jnt_list 中的每个关节点，获取其位置信息，并将位置信息添加到 curve_points 列表中。
        for jnt in jnt_list :
            pos = cmds.xform (jnt , q = 1 , t = 1 , ws = 1)
            curve_points.append (pos)
        # 创建曲线
        curve = cmds.curve (p = curve_points , name = curve , degree = degree)

        return curve

        ##简单的示例
        # # 假设有一个关节点的列表和要创建的曲线名称
        # joint_list = ["joint1" , "joint2" , "joint3"]
        # curve_name = "generated_curve"
        #
        # # 调用函数生成曲线
        # created_curve = generate_curve_from_joints (joint_list , curve_name)
        #
        # # 打印创建的曲线名称
        # print (created_curve)


    # 根据给定的曲线放样生成出曲面
    @staticmethod
    def create_surface_on_curve (curve , surface_node , spans = 4 , offset = 0.2) :
        u"""
        根据给定的曲线放样生成出曲面
        curve(str):给定的曲线名称
        surface_node（str）：生成出来的曲面的名称
        spans（int）:重建后曲线的点数
        offset（float）：曲线偏移的距离值

        return:
            返回曲面的节点
        """
        # # 重建曲线
        # cmds.rebuildCurve (curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 ,
        #                    kt = 0 , spans = spans , d = 3 , tol = 0.01)
        duplicate_crv = cmds.duplicate (curve) [0]
        # 移动定位眉毛曲线和复制出来的曲线准备放样曲线生成曲面
        cmds.setAttr (curve + '.translateY' , offset)
        cmds.setAttr (duplicate_crv + '.translateY' , offset * -1)
        # 放样曲线出曲面
        # 通过两条曲线来放样制作曲面
        surface_node = \
            cmds.loft (curve , duplicate_crv , constructionHistory = False , uniform = True ,
                       degree = 3 ,
                       sectionSpans = 1 ,
                       range = False , polygon = 0 ,
                       name = surface_node) [0]
        cmds.delete (curve , duplicate_crv)
        return surface_node


    # 在给定的曲面上创建毛囊节点和关节节点
    @staticmethod
    def create_joint_follicle_on_surface (surf_node , side , description , jnt_number) :
        """
        在给定的曲面上创建毛囊节点和关节节点
        surf_node（str）:给定的曲面，需要创建毛囊节点和关节节点的曲面
        side（str）:边
        description(str)：描述
        jnt_number(int):需要创建的关节节点数量

        return:follicle_dict:存储数据,fol_grp,jnt_grp,ctrl_grp,connect_list

        """
        # 获得曲面的形状节点

        surf_shape = cmds.listRelatives (surf_node , shapes = True) [0]
        # 创建所有deform的层级组
        deform_grp = cmds.createNode ('transform' ,
                                      name = 'grp_{}_{}Deforms_001'.format (side , description))
        cmds.parent (surf_node , deform_grp)
        cmds.setAttr (surf_node + '.v' , 0)
        # 创建follicle整体层级组的名称
        fol_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}_{}Follicles_001'.format (side , description) , parent = deform_grp)
        # 创建jnt整体层级组的名称
        jnt_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}_{}Jnts_001'.format (side , description) , parent = deform_grp)

        # 创建ctrl整体层级组的名称
        ctrl_grp = cmds.createNode ('transform' ,
                                    name = 'grp_{}_{}Ctrls_001'.format (side , description) , parent = deform_grp)
        connect_list = []

        # 创建skin关节的集合
        skin_jnt_set = 'set_skinJnt'
        make_skin_jnt_set = 'set_' + side + '_' + description + 'Jnt'
        make_skin_jnt_set = cmds.sets (name = make_skin_jnt_set , empty = True)
        if not cmds.objExists (skin_jnt_set) or cmds.nodeType (skin_jnt_set) != 'objectSet' :
            skin_jnt_set = cmds.sets (name = skin_jnt_set , empty = True)
            cmds.sets (make_skin_jnt_set , edit = True , forceElement = skin_jnt_set)
        else :
            cmds.sets (make_skin_jnt_set , edit = True , forceElement = skin_jnt_set)

        # 循环制作
        for index in range (jnt_number) :
            # 创建毛囊
            fol_shape = cmds.createNode ('follicle' , name = 'fol_{}_{}_{:03d}Shape'.format (side , description ,
                                                                                             index + 1))
            # 重命名毛囊的tran节点名称
            fol_node = cmds.listRelatives (fol_shape , parent = True) [0]
            fol_node = cmds.rename (fol_node , fol_shape [:-5])
            # 把毛囊放入对应的层级组
            cmds.parent (fol_node , fol_grp)
            # 连接毛囊属性
            cmds.connectAttr (surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
            # 连接毛囊的形状节点以进行变换
            cmds.connectAttr (fol_shape + '.outTranslate' , fol_node + '.translate')
            cmds.connectAttr (fol_shape + '.outRotate' , fol_node + '.rotate')
            # 设置uv值
            cmds.setAttr (fol_shape + '.parameterU' , 0.5)
            cmds.setAttr (fol_shape + '.parameterV' , float (index) / (jnt_number - 1))

            # 创建关节
            jnt = cmds.createNode ('joint' , name = 'jnt_{}_{}Skin_{:03d}'.format (side , description ,
                                                                                   index + 1))
            cmds.parent (jnt , jnt_grp)
            # 整理层级结构，创建zero组和offset组
            # 创建关节的控制器
            ctrl = controlUtils.Control.create_ctrl (jnt.replace ('jnt' , 'ctrl') , shape = 'ball' , radius = 0.05 ,
                                                     axis = 'X+' , pos = jnt , parent = ctrl_grp)
            cmds.parentConstraint (ctrl.replace ('ctrl' , 'output') , jnt)
            # 让对应的毛囊约束对应的控制器
            cmds.parentConstraint (fol_node , ctrl.replace ('ctrl' , 'driven') , maintainOffset = False)
            # 将偏移组的旋转设置为零
            cmds.xform (ctrl.replace ('ctrl' , 'offset') , rotation = [0 , 0 , 0] , worldSpace = True)
            # 设置关节的大小
            cmds.setAttr (jnt + '.radius' , 0.4)

            # 将connect组添加到connect_list里，方便外部进行调用
            connect_list.append (ctrl.replace ('ctrl' , 'connect'))

            # 将生成的skin关节放在对应的集里方便选择
            cmds.sets (jnt , edit = True , forceElement = make_skin_jnt_set)

            follicle_dict = {
                'jnt_grp' : jnt_grp ,
                'ctrl_grp' : ctrl_grp ,
                'fol_grp' : fol_grp ,
                'connect_list' : connect_list ,
                'deform_grp' : deform_grp
            }
        return follicle_dict


    # 根据模型上所选择的边，模型的边到曲线生成新的曲线，判断场景里是否已经生成过对应的曲线，如果有的话则将其删除，没有的话则新创建
    @staticmethod
    def create_curve_on_polyToCurve (curve_name , degree = 3) :
        u'''
        根据模型上所选择的边，模型的边到曲线生成新的曲线，判断场景里是否已经生成过对应的曲线，如果有的话则将其删除，没有的话则新创建
        Args:
            curve_name(str)：所生成的曲线的名称
            degree(int)：新曲线的阶数。默认值为3。请注意，您需要（阶数+1）个曲线点来创建可见的曲线跨度。你必须为3度曲线放置4个点。

        Returns:
                生成的曲线
        '''

        # 判断场景里是否已经生成过对应的曲线，如果有的话则将其删除，没有的话则新创建
        if cmds.objExists (curve_name) :
            cmds.delete (curve_name)

        # 根据所选择的点创建曲线
        # 获取根据模型上所选择的边的点信息
        curve_point = cmds.ls (sl = True)
        # 创建新的曲线
        curve_node = cmds.polyToCurve (curve_point , name = curve_name , degree = degree ,
                                       conformToSmoothMeshPreview = 1)
        cmds.reverseCurve (curve_name , constructionHistory = 1 , replaceOriginal = 1)
        # 创建出来的曲线删除历史
        cmds.delete (curve_node , constructionHistory = True)

        return curve_name


    # 获取曲线的点数量的函数
    @staticmethod
    def get_curve_number (curve) :
        u"""
        获取曲线的点数量的函数
        curve(str):想要获取点数量的曲线名称
        获得曲线的点数量:spans + degree
        return:
            cv_num：返回曲线的点数量
        """
        # 获得曲线的形状节点
        curve_shape = cmds.listRelatives (curve , shapes = True) [0]

        # 获取曲线跨度和阶数
        spans = cmds.getAttr (curve_shape + '.spans')
        degree = cmds.getAttr (curve_shape + '.degree')

        # 获取cv点数量
        cv_num = spans + degree

        return cv_num


    # 基于cv创建眼睑关节，并使用目标约束附加到曲线
    @staticmethod
    def create_eyelid_joints_on_curve (curve , eye_joint , up_object) :
        """
        基于cv创建眼睑关节，并使用目标约束附加到曲线

        Args:
            curve (str): 眼睑曲线
            eye_joint (str): 眼睛的关节
            up_object(str):向上的目标物体
        """
        # 获得名称规范
        curve_obj = nameUtils.Name (curve)

        # 创建层级组结构

        node_grp = cmds.createNode ('transform' ,
                                    name = 'grp_{}_{}RigNodes_{:03d}'.format (curve_obj.side , curve_obj.description ,
                                                                              curve_obj.index))

        drive_attach_grp = cmds.createNode ('transform' ,
                                            name = 'grp_{}_{}Attaches_{:03d}'.format (curve_obj.side ,
                                                                                      curve_obj.description ,
                                                                                      curve_obj.index) ,
                                            parent = node_grp)

        jnt_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}_{}Jnts_{:03d}'.format (curve_obj.side , curve_obj.description ,
                                                                         curve_obj.index) , parent = node_grp)

        # 整理层级结构
        cmds.parent (curve , node_grp)

        # 获取曲线的点数量
        cv_num = Pipeline.get_curve_number (curve)

        # 获得曲线的形状节点
        curve_shape = cmds.listRelatives (curve , shapes = True) [0]

        # 创建关节并附着到曲线
        for i in range (cv_num) :
            jnt = cmds.createNode ('joint' ,
                                   name = 'jnt_{}_{}_{:03d}'.format (curve_obj.side , curve_obj.description , i + 1))
            cmds.setAttr (jnt + '.radius' , 0.2)
            # 获取cv点的位置信息
            cv_pos = cmds.xform ('{}.cv[{}]'.format (curve , i) , query = True , translation = True , worldSpace = True)
            # 设置关节点的位置信息
            cmds.xform (jnt , translation = cv_pos , worldSpace = True)

            # 获取曲线上最接近的参数，创建nearestPointOnCurve节点查找最近点
            npoc = cmds.createNode ('nearestPointOnCurve')
            cmds.connectAttr (curve_shape + '.worldSpace[0]' , npoc + '.inputCurve')
            cmds.connectAttr (jnt + '.translate' , npoc + '.inPosition')
            parameter = cmds.getAttr (npoc + '.parameter')
            cmds.delete (npoc)

            # 创建附加节点
            attach = cmds.createNode ('transform' ,
                                      name = 'grp_{}_{}Attach_{:03d}'.format (curve_obj.side , curve_obj.description ,
                                                                              i + 1) ,
                                      parent = drive_attach_grp)
            poci = cmds.createNode ('pointOnCurveInfo' , name = attach.replace ('grp' , 'poci'))
            cmds.connectAttr (curve_shape + '.worldSpace[0]' , poci + '.inputCurve')
            cmds.setAttr (poci + '.parameter' , parameter)
            cmds.connectAttr (poci + '.position' , attach + '.translate')

            # 在眼睛关节位置上创建目标节点
            aim_node = cmds.createNode ('transform' ,
                                        name = 'grp_{}_{}Aim_{:03d}'.format (curve_obj.side , curve_obj.description ,
                                                                             i + 1) ,
                                        parent = jnt_grp)
            cmds.matchTransform (aim_node , eye_joint , position = True)

            # 带有附加节点的目标约束
            cmds.aimConstraint (attach , aim_node , aimVector = [1 , 0 , 0] , upVector = [0 , 1 , 0] ,
                                worldUpType = 'objectrotation' , worldUpObject = up_object ,
                                worldUpVector = [0 , 1 , 0] ,
                                maintainOffset = False)

            # 将关节放到目标约束的节点下，并确定关节的方向
            cmds.parent (jnt , aim_node)
            # 将关节定向到zero组的方向
            cmds.matchTransform (jnt , aim_node , position = False , rotation = True)
            cmds.makeIdentity (jnt , apply = True , translate = True , rotate = True , scale = True)


    # 使用pointOnCurveInfo节点在曲线上附加关节
    @staticmethod
    def attach_joints_on_curve (jnt_list , drive_curve , aim_curve , up_object , aim_type = 'object') :
        """
        使用pointOnCurveInfo节点在曲线上附加关节

        Args:
            jnt_list (list): 需要连接的关节列表
            drive_curve (str): 驱动关节的曲线
            aim_curve (str): 目标曲线
            up_object (str): 向上的参考向量的曲线
            aim_type (str): object/curve 物体或者是曲线
        return:
            attach_dict: 将创建出来的attach对象返回出去
        """
        # 获取名称
        name_parts = nameUtils.Name (name = drive_curve)

        # 判断aim_type的类型后，选择是否添加进curves曲线列表里
        if aim_type == 'curve' :
            curves = [drive_curve , aim_curve , up_object]
        else :
            curves = [drive_curve , aim_curve]

        # 创建整理层级的组
        jnts_grp = cmds.createNode ('transform' ,
                                    name = 'grp_{}_{}AttachJnts_{:03d}'.format (name_parts.side ,
                                                                                name_parts.description ,
                                                                                name_parts.index))
        nodes_grp = 'grp_{}_{}RigNodes_{:03d}'.format (name_parts.side , name_parts.description ,
                                                       name_parts.index)
        if not cmds.objExists (nodes_grp) :
            nodes_grp = cmds.createNode ('transform' ,
                                         name = nodes_grp)

        attaches_grp = []
        for crv , part_name in zip (curves , ['Drive' , 'Aim' , 'Up']) :
            attach_grp = cmds.createNode ('transform' ,
                                          name = 'grp_{}_{}{}Attaches_{:03d}'.format (name_parts.side ,
                                                                                      name_parts.description ,
                                                                                      part_name ,
                                                                                      name_parts.index) ,
                                          parent = nodes_grp)
            attaches_grp.append (attach_grp)

        # 获取曲线形状节点
        crv_shapes = []
        for crv in curves :
            crv_shape = cmds.listRelatives (crv , shapes = True) [0]
            crv_shapes.append (crv_shape)

        # 将关节附着到曲线
        for jnt in jnt_list :
            # 获得关节的命名规范
            jnt_name_parts = nameUtils.Name (name = jnt)

            # 获取曲线上最接近的点的位置
            npoc = cmds.createNode ('nearestPointOnCurve')
            cmds.connectAttr (crv_shapes [0] + '.worldSpace[0]' , npoc + '.inputCurve')
            cmds.connectAttr (jnt + '.translate' , npoc + '.inPosition')
            parameter = cmds.getAttr (npoc + '.parameter')
            cmds.delete (npoc)

            # 创建附加节点
            attach_nodes = []
            for crv_shape , part_name , grp in zip (crv_shapes , ['Drive' , 'Aim' , 'Up'] , attaches_grp) :
                attach = cmds.createNode ('transform' ,
                                          name = 'grp_{}_{}{}Attach_{:03d}'.format (jnt_name_parts.side ,
                                                                                    jnt_name_parts.description ,
                                                                                    part_name ,
                                                                                    jnt_name_parts.index) ,
                                          parent = grp)
                poci = cmds.createNode ('pointOnCurveInfo' , name = attach.replace ('grp' , 'poci'))
                cmds.connectAttr (crv_shape + '.worldSpace[0]' , poci + '.inputCurve')
                cmds.setAttr (poci + '.parameter' , parameter)
                cmds.connectAttr (poci + '.position' , attach + '.translate')
                attach_nodes.append (attach)

            # 创建目标约束来约束附加节点
            if aim_type == 'curve' :
                cmds.aimConstraint (attach_nodes [1] , attach_nodes [0] , aimVector = [1 , 0 , 0] ,
                                    upVector = [0 , 1 , 0] ,
                                    worldUpType = 'object' , worldUpObject = attach_nodes [2] ,
                                    worldUpVector = [0 , 1 , 0] ,
                                    maintainOffset = False)
            else :
                cmds.aimConstraint (attach_nodes [1] , attach_nodes [0] , aimVector = [1 , 0 , 0] ,
                                    upVector = [0 , 1 , 0] ,
                                    worldUpType = 'objectrotation' , worldUpObject = up_object ,
                                    worldUpVector = [0 , 1 , 0] ,
                                    maintainOffset = False)

            # 创建关节的zero组，用于整理层级结构
            zero = cmds.createNode ('transform' , name = jnt.replace ('jnt' , 'zero') , parent = jnts_grp)
            cmds.parentConstraint (attach_nodes [0] , zero , maintainOffset = False)

            # 整理关节的层级结构
            cmds.parent (jnt , zero)
            # 将关节定向到zero组的方向
            cmds.matchTransform (jnt , zero , position = False , rotation = True)
        # cmds.makeIdentity(jnt , apply = True , translate = True , rotate = True , scale = True)
        attach_dict = {
            'attach_grp' : attach_grp ,
            'jnts_grp' : jnts_grp ,
            'nodes_grp' : nodes_grp ,
            'attach_nodes' : attach_nodes ,

        }
        return attach_dict


    # 给嘴唇添加拉链嘴的绑定
    @staticmethod
    def create_zip_lip (lip_ctrls , jaw_ctrl , upper_jnts , lower_jnts , zip_height = 0.5 , falloff = 3) :
        '''
        给嘴唇添加拉链嘴的绑定
        Args:
            lip_ctrls(list):嘴唇控制器列表
            jaw_ctrl(str):下巴控制器
            upper_jnts(list):上嘴唇的关节列表
            lower_jnts(list):下嘴唇的关节列表
            zip_height(float):zip的高度，默认为0.5，也就是上下嘴唇闭合到中间的高度
            falloff:平滑值，嘴唇关节之间粘连的过渡值

        Returns:
                zip_lip_dict(dict):返回出创建出来的内容
        '''
        # 添加属性给嘴唇和下巴的控制器
        for ctrl in lip_ctrls :
            cmds.addAttr (ctrl , longName = 'zip' , attributeType = 'float' , minValue = 0 , maxValue = 1 ,
                          keyable = True)
            # 创建一个属性微调嘴角的数值
            cmds.addAttr (ctrl , longName = 'adjust' , attributeType = 'float' , minValue = -0.1 , maxValue = 0.1 ,
                          keyable = True)

        cmds.addAttr (jaw_ctrl , longName = 'zipHeight' , attributeType = 'float' , minValue = 0 , maxValue = 1 ,
                      defaultValue = zip_height , keyable = True)

        height_rvs = cmds.createNode ('reverse' , name = 'rvs_m_lipZipHeight_001')
        cmds.connectAttr (jaw_ctrl + '.zipHeight' , height_rvs + '.inputX')

        # 创建节点的层级组结构,用于整理所有节点的名称
        node_grp = cmds.createNode ('transform' , name = 'grp_m_lipZipNodes_001')

        # 获取关节的数量，因为上下嘴唇的关节一致
        jnts_num = len (upper_jnts)

        # 获取zip_weight的值
        zip_weight = 1 / float (jnts_num)

        # 给每个嘴唇关节循环添加zip设置
        i = 1
        for upper_jnt , lower_jnt in zip (upper_jnts , lower_jnts) :
            # 获取名称规范
            name_parts = nameUtils.Name (name = upper_jnt)
            name_side = name_parts.side
            name_parts.description = ''
            name_index = name_parts.index

            # 创建中间位置的定位器
            upper_grp = cmds.listRelatives (upper_jnt , parent = True) [0]
            lower_grp = cmds.listRelatives (lower_jnt , parent = True) [0]

            mid_loc = cmds.spaceLocator (name = 'loc_{}_{}Zip_{:03d}'.format (name_side , name_parts.description ,
                                                                              name_index)) [0]
            cmds.parent (mid_loc , node_grp)
            cmds.setAttr (mid_loc + '.v' , 0)

            pnt_con = cmds.parentConstraint (upper_grp , lower_grp , mid_loc , maintainOffset = False) [0]
            cmds.setAttr (pnt_con + '.interpType' , 2)
            cmds.connectAttr (jaw_ctrl + '.zipHeight' , '{}.{}W0'.format (pnt_con , upper_grp))
            cmds.connectAttr (height_rvs + '.outputX' , '{}.{}W1'.format (pnt_con , lower_grp))

            # 创建remap节点用来连接控制器的zip属性
            remap_left = cmds.createNode ('remapValue' ,
                                          name = 'remap_{}_{}ZipWeightLeft_{:03d}'.format (name_side ,
                                                                                           name_parts.description ,
                                                                                           name_index))
            remap_right = cmds.createNode ('remapValue' ,
                                           name = 'remap_{}_{}ZipWeightRight_{:03d}'.format (name_side ,
                                                                                             name_parts.description ,
                                                                                             name_index))
            cmds.connectAttr (lip_ctrls [0] + '.zip' , remap_left + '.inputValue')
            cmds.connectAttr (lip_ctrls [1] + '.zip' , remap_right + '.inputValue')

            # 设置remap节点的值
            cmds.setAttr (remap_left + '.value[0].value_Position' , max ([0 , zip_weight * (i - falloff)]))
            cmds.setAttr (remap_left + '.value[1].value_Position' , zip_weight * i)

            cmds.setAttr (remap_right + '.value[0].value_Position' ,
                          max ([0 , zip_weight * (jnts_num - i + 1 - falloff)]))
            cmds.setAttr (remap_right + '.value[1].value_Position' , zip_weight * (jnts_num - i + 1))

            # 把相加后的权重相加为 0-1驱动，通过clamp节点剪除超过的范围
            add = cmds.createNode ('addDoubleLinear' ,
                                   name = 'add_{}_{}ZipWeight_{:03d}'.format (name_side , name_parts.description ,
                                                                              name_index))
            cmds.connectAttr (remap_left + '.outValue' , add + '.input1')
            cmds.connectAttr (remap_right + '.outValue' , add + '.input2')

            clamp = cmds.createNode ('clamp' , name = add.replace ('add' , 'clamp'))
            cmds.connectAttr (add + '.output' , clamp + '.inputR')
            cmds.setAttr (clamp + '.maxR' , 1)

            # 获取反向的权重
            rvs_node = cmds.createNode ('reverse' , name = clamp.replace ('clamp' , 'rvs'))
            cmds.connectAttr (clamp + '.outputR' , rvs_node + '.inputX')

            # 在原始位置和中间位置之间混合距离
            for jnt , jnt_parent in zip ([upper_jnt , lower_jnt] , [upper_grp , lower_grp]) :
                zero = cmds.createNode ('transform' , name = jnt.replace ('jnt' , 'zeroJnt') , parent = jnt_parent)
                offset = cmds.createNode ('transform' , name = jnt.replace ('jnt' , 'offsetJnt') , parent = zero)
                cmds.matchTransform (zero , jnt , position = True , rotation = True)
                cmds.parent (jnt , offset)

                pnt_con = cmds.parentConstraint (mid_loc , zero , offset , maintainOffset = False) [0]
                cmds.setAttr (pnt_con + '.interpType' , 2)
                # 给边角的三个关节增加微调的控制
                if i in [0 , 1 , 2 , 3 , jnts_num - 3 , jnts_num - 2 , jnts_num - 1 , jnts_num] :
                    # 使用控制器的adjus属性来微调嘴角的数值，用于改变嘴巴闭合状态时，嘴角的表演。通常对应的是“嘴角微微上扬”“有些许不快”的这种微表演
                    if i in [0 , 1 , 2 , 3] :
                        cmds.connectAttr (lip_ctrls [0] + '.adjust' , jnt + '.translateY')
                    else :
                        cmds.connectAttr (lip_ctrls [-1] + '.adjust' , jnt + '.translateY')

                else :
                    cmds.connectAttr (clamp + '.outputR' , '{}.{}W0'.format (pnt_con , mid_loc))
                    cmds.connectAttr (rvs_node + '.outputX' , '{}.{}W1'.format (pnt_con , zero))

            i += 1
        zip_lip_dict = {
            'node_grp' : node_grp
        }
        return zip_lip_dict


    # 制作需要调整权重值的约束，驱动的物体和控制器的zero组去约束driven组，并且调整权重值
    @staticmethod
    def create_doble_constraint (driver , ctrl , weight = 0.5) :
        u"""
        制作需要调整权重值的约束，驱动的物体和控制器的zero组去约束driven组，并且调整权重值
        driver(str):驱动的物体
        ctrl(str):被驱动的控制器
        weight(int):约束的权重值
        """
        zero = ctrl.replace ('ctrl' , 'zero')
        driven = ctrl.replace ('ctrl' , 'driven')
        # 给控制器添加约束的权重值的属性设置
        cmds.addAttr (ctrl , ln = 'con_weight' , at = 'double' , min = 0 , max = 1 , dv = weight ,
                      keyable = True)
        # 创建约束节点
        con = cmds.parentConstraint (driver , zero , driven , mo = True) [0]
        # 连接约束的权重值
        cmds.connectAttr (ctrl + '.con_weight' , con + '.{}W0'.format (driver))

        # 创建相乘节点计算另外一个物体的权重值；1-weight
        mult_node = cmds.createNode ('multDoubleLinear' , name = ctrl.replace ('ctrl' , 'mult_weight'))
        cmds.setAttr (mult_node + '.input1' , -1)
        cmds.connectAttr (ctrl + '.con_weight' , mult_node + '.input2')

        add_node = cmds.createNode ('addDoubleLinear' , name = ctrl.replace ('ctrl' , 'add_weight'))
        cmds.setAttr (add_node + '.input1' , 1)
        cmds.connectAttr (mult_node + '.output' , add_node + '.input2')

        cmds.connectAttr (add_node + '.output' , con + '.{}W1'.format (zero))


    # 创建logging日志，用来记录各个模块的日志报错信息，方便于项目排查
    @staticmethod
    def create_logging (logger_name , file_name , formatter = '%(asctime)s -%(name)s - %(levelname)s - %(message)s') :
        """
        创建logging日志，用来记录各个模块的日志报错信息，方便于项目排查
        logger_name(str):用来自定义logger模块的名称
        formatter(str):设置保存日志的信息,例如format = '%(asctime)s -%(name)s - %(levelname)s - %(message)s'
        """
        # 根据自定义logger模块的名称来创建logger
        logger = logging.getLogger (''.format (logger_name))

        # 判断是否已经生成过handler，如果已经生成过的话则进行移除
        for handler in logger.handlers :
            logger.removeHandler (handler)
        for handler in logger.handlers :
            logger.removeHandler (handler)
        # 设置保存日志的信息
        file_formatter = logging.Formatter (formatter)

        # 保存日志的名称(可以采用绝对路径，如果只给名字的话，日志生成的文件会在当前文件夹下)
        file_handle = logging.FileHandler (file_name)

        # level：设置日志的提示级别信息，
        file_handle.setLevel (logging.DEBUG)
        # 设置文件处理器的格式为提供的 formatter。
        file_handle.setFormatter (file_formatter)
        # 将文件处理器添加到 logger 中。
        logger.addHandler (file_handle)

        ##简单实例
        # # 假设有一个自定义的 logger 名称和要保存的日志文件名称
        # logger_name = "my_logger"
        # log_file_name = "my_log_file.log"
        #
        # # 调用函数创建 logger
        # create_logging (logger_name , log_file_name)
        #
        # # 使用创建的 logger 记录日志信息
        # logger = logging.getLogger (logger_name)
        # logger.debug ("This is a debug message.")
        # logger.info ("This is an info message.")
        # logger.warning ("This is a warning message.")
        # logger.error ("This is an error message.")


    # 给指定的对象创建set选择集来方便选择
    @staticmethod
    def create_set (object , set_name , set_parent = None) :
        """
        给指定的对象创建set选择集来方便选择
        object(str)：指定添加到选择集的对象
        set_name(str):创建的选择集名称
        set_parent(str):创建的选择集是否需要指定父对象
        """
        # 将指定的对象添加到对应的选择集
        # 判断选择集是否已经存在，如果没有存在的话需要创建选择集
        if not cmds.objExists (set_name) or cmds.nodeType (set_name) != 'objectSet' :
            select_set = cmds.sets (name = set_name , empty = True)
            cmds.sets ('{}'.format (object) , edit = True , forceElement = set_name)
        # 选择集已经存在的情况，则直接添加指定的对象到对应的选择集
        else :
            cmds.sets ('{}'.format (object) , edit = True , forceElement = set_name)

        # 判断创建的选择集是否需要指定父对象
        if set_parent :
            # 将指定的选择集指定对应的选择集父对象
            if not cmds.objExists (set_parent) or cmds.nodeType (set_parent) != 'objectSet' :
                select_set = cmds.sets (name = set_parent , empty = True)
                cmds.sets ('{}'.format (set_name) , edit = True , forceElement = set_parent)
            # 选择集已经存在的情况，则直接添加指定的对象到对应的选择集
            else :
                cmds.sets ('{}'.format (set_name) , edit = True , forceElement = set_parent)

        return set_name


    # 选择需要创建动力学化的曲线。创建动力学化曲线驱动头发
    @staticmethod
    def create_dynamic_curve_driven () :
        """
        选择需要创建动力学化的曲线。创建动力学化曲线驱动头发
        曲线节点的命名为 模型节点 + '_crv'

        """
        crv_list = cmds.ls (sl = True)
        # 判断是否有动力学化曲线的关节组，没有的话则进行创建
        if not cmds.objExists ('nhair_jnt_grp') :
            nhair_jnt_grp = cmds.createNode ('transform' , name = 'nhair_jnt_grp')
        else :
            nhair_jnt_grp = 'nhair_jnt_grp'

        # 判断是否有动力学化曲线的节点组，没有的话则进行创建
        if not cmds.objExists ('nhair_rigNode_grp') :
            nhair_rigNode_grp = cmds.createNode ('transform' , name = 'nhair_rigNode_grp')
        else :
            nhair_rigNode_grp = 'nhair_rigNode_grp'

        for dynamic_curve_node in crv_list :
            cmds.DeleteHistory (dynamic_curve_node)

            # 取消所有曲线选择后，然后选择这次创建的曲线
            pm.select (dynamic_curve_node , r = True)
            # 根据曲线创建关节链条
            jnt_dict = jointUtils.Joint.create_joints_on_curve ()

            # 头发曲线做动力学化曲线。
            pm.mel.eval ('MakeCurvesDynamic')

            # 获取动力学化曲线生成的毛囊节点 动力学化曲线生成的毛囊需要切换成基础。才能符合头发的动态
            folicile_node = cmds.listRelatives (dynamic_curve_node , p = True) [0]

            # 重命名毛囊节点的名称
            folicile_node = cmds.rename (folicile_node , dynamic_curve_node + folicile_node)
            folicile_shape_node = cmds.listRelatives (folicile_node , s = True) [0]
            # 设置毛囊节点的基础属性
            cmds.setAttr (folicile_node + '.pointLock' , 1)
            #
            # 获取毛囊节点所链接的毛发节点并修改名称
            hair_shape_node = \
                cmds.listConnections (folicile_node + '.currentPosition' , s = True , d = True , p = True ,
                                      t = 'hairSystem') [
                    0].split (
                    '.') [0]
            hair_node = cmds.listRelatives (hair_shape_node , p = True) [0]
            hair_node = cmds.rename (hair_node , dynamic_curve_node + hair_node)

            # 将毛发节点添加到选择集里方便进行选择
            Pipeline.create_set (hair_node , set_name = 'hairSystem_set' , set_parent = None)
            #
            # 获取输出曲线的节点名称并且重命名
            output_curve_shape_node = \
                cmds.listConnections (folicile_shape_node + '.outCurve' , s = True , d = True , p = True) [0].split (
                    '.') [0]
            output_curve_node = cmds.listRelatives (output_curve_shape_node , p = True) [0]

            output_curve_node = cmds.rename (output_curve_node , dynamic_curve_node + '_outputCurve')
            output_curve_grp = cmds.listRelatives (output_curve_node , p = True) [0]
            #
            # 获取之前曲线创建出来的关节
            jnt_list = jnt_dict ['jnt_list']

            # 使用曲线创建出来的关节和输出曲线创建spineIK样条线绑定
            handle_node = \
                cmds.ikHandle (startJoint = jnt_list [0] , endEffector = jnt_list [-1] , sol = 'ikSplineSolver' ,
                               ccv = False ,
                               curve = output_curve_node ,
                               name = dynamic_curve_node + '_handle') [0]
            #
            # # 找到模型的节点名称并且将动力学骨骼蒙皮给模型，曲线节点的命名为 模型节点 + '_crv'
            # modle_node = dynamic_curve_node.split ('_crv') [0]
            # cmds.skinCluster (jnt_list , modle_node)
            #
            # 整理层级结构
            # 创建动力学的层级组
            rigNode_grp = cmds.createNode ('transform' , name = dynamic_curve_node + '_nhair_grp')
            cmds.parent (output_curve_node , output_curve_grp)
            cmds.parent (hair_node , handle_node , rigNode_grp)

            # 整理动力学的层级组
            cmds.parent (jnt_dict ['node_grp'] , nhair_jnt_grp)
            cmds.parent (rigNode_grp , nhair_rigNode_grp)

        # 将输出曲线整理到对应的节点组
        outputCurves_grp = cmds.ls ('hairSystem*OutputCurves' , type = 'transform')
        for outputCurve_grp in outputCurves_grp :
            hierarchyUtils.Hierarchy.parent (outputCurve_grp , nhair_rigNode_grp)
