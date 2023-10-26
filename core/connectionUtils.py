from __future__ import unicode_literals , print_function

import json
import os.path
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils
import maya.api.OpenMaya as om


"""
这是一个针对属性连接的类
"""


class Connection (object) :

    def __init__ (self) :
        pass


    """
    获得连接
    """


    def get_obj_driven_attrs_connection (self , driven_obj) :
        """
        获取物体作为被驱动者所连接的属性
        driven_obj(str):作为被驱动者的物体
        """
        self.driven_attrs_connection = list ()
        # 获取物体作为被驱动者的所有属性
        self.current_driven_all_attrs = cmds.listAttr (driven_obj , connectable = True , inUse = True)
        # 获取物体作为被驱动者连接的属性
        for attr in self.current_driven_all_attrs :
            objAttr = ".".join ([driven_obj , attr])
            try :
                if cmds.listConnections (objAttr , destination = False , source = True) :
                    self.driven_attrs_connection.append (objAttr)
            except ValueError :  # 遇到找不到某些属性的错误
                pass

        if not self.driven_attrs_connection :
            # 如果物体没有被连接的属性的话，则爆出提示
            om.MGlobal.displayWarning ("{}没有已连接的属性 ".format (driven_obj))
            return list ()
        return self.driven_attrs_connection


    """
    创建连接
    """


    def cheek_obj_attrs_connection (self , driver_obj , source_attr , driven_obj , destination_attr) :
        """
        检查：驱动者的属性是否能够成功连接上被驱动者的属性
        检查项：1.是否存在对应的属性
        2.属性之间的类型是否匹配
        3.目标属性是否可以连接
        driver_obj(str):作为驱动者的物体
        source_attr(str):作为驱动者的物体上驱动的属性
        driven_obj(str):作为被驱动者的物体
        destination_attr(str):作为被驱动者的物体上被驱动的属性
        """
        cheek_value = True
        driver_attr = driver_obj + '.' + source_attr
        driven_attr = driven_obj + '.' + destination_attr

        # 检查1.判断是否存在对应的属性
        source_exists = cmds.attributeQuery (source_attr , node = driver_obj , exists = True)
        destination_exists = cmds.attributeQuery (destination_attr , node = driven_obj , exists = True)
        if not source_exists or not destination_exists :
            cmds.warning ('在节点{}或{}上找不到属性'.format (driver_attr , driven_attr))
            cheek_value = False
            return cheek_value
        # 检查2.属性之间的类型是否匹配
        source_type = cmds.attributeQuery (source_attr , node = driver_obj , attributeType = True)
        destination_type = cmds.attributeQuery (destination_attr , node = driven_obj , attributeType = True)
        if source_type != destination_type :
            if destination_attr or source_attr == '.matrix' :
                pass
            else :
                cmds.warning ('属性类型{}和{}不匹配'.format (driver_attr , driven_attr))
                cheek_value = False
                return cheek_value
        # 检查3.目标属性是否可以连接
        # 检查目标属性是否是可以连接类型的属性
        destination_connect_able = cmds.attributeQuery (destination_attr , node = driven_obj , connectable = True)
        if not destination_connect_able :
            if destination_attr or source_attr == '.matrix' :
                pass
            else :
                cmds.warning ('属性{}不可以被连接'.format (driven_attr))
                cheek_value = False
                return cheek_value

        # 检查目标属性是否已经具有了传入连接
        source_connections = cmds.listConnections (driven_attr , destination = False , source = True ,
                                                   plugs = True)
        if source_connections :
            cmds.warning ('属性{}已经被{}连接了'.format (driven_attr , source_connections))
            cheek_value = False
            return cheek_value

        return cheek_value


    def makeSafeConnectionsTwoObjs (self , driver_obj , source_attr , driven_obj , destination_attr) :
        """
        驱动者的属性连接上被驱动者的属性
        driver_obj(str):作为驱动者的物体
        source_attr(str):作为驱动者的物体上驱动的属性
        driven_obj(str):作为被驱动者的物体
        destination_attr(str):作为被驱动者的物体上被驱动的属性
        """
        driver_attr = driver_obj + '.' + source_attr
        driven_attr = driven_obj + '.' + destination_attr

        # 进行判断检查，判断驱动者的属性是否能够成功连接上被驱动者的属性
        cheek_value = self.cheek_obj_attrs_connection (driver_obj , source_attr , driven_obj , destination_attr)
        if not cheek_value :
            # 驱动者的属性无法能够成功连接上被驱动者的属性的情况
            cmds.warning ('{}.{}无法与{}.{}进行连接'.format (driver_obj , source_attr , driven_obj , destination_attr))
            pass
        else :
            cmds.connectAttr (driver_attr , driven_attr)


    def safeConnectList (self , objList , source_attr , destination_attr) :
        """将对象列表中的第一个对象安全地连接到其余对象
        driver_obj(str):作为驱动者的物体
        source_attr(str):作为驱动者的物体上驱动的属性
        driven_obj(str):作为被驱动者的物体
        destination_attr(str):作为被驱动者的物体上被驱动的属性
        """

        success = False
        objList = cmds.ls (objList , shortNames = True)
        sourceObj = objList.pop (0)
        for obj in objList :
            if self.makeSafeConnectionsTwoObjs (sourceObj , source_attr , obj , destination_attr ,
                                                ) :
                success = True
        return success


    def safeConnectSelection (self , source_attr , destination_attr) :
        """将第一个选定对象安全地连接到其余选定对象。

        """
        sel_objs = cmds.ls (selection = True , long = True)
        if not sel_objs :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        if len (selObjs) < 2 :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        return safe_connect_List (sel_objs , source_attr , destination_attr)


    def makeConnectionAttrsOrChannelBox (self , driverAttr = "" , drivenAttr = "") :
        """从GUI连接选择列表中的“driver.attr”和“driven.attr”
        第一个选定对象到其余选定对象。
        如果没有给定driverAttr和drivenAttr，则将尝试使用通道框选择的属性来填充任何丢失的数据。
        在通道框中只能选择一个属性
        driverAttr(str):驱动者的属性
        drivenAttr(str)被驱动者的属性
        """
        # 当两个属性都被输入的时候
        if driverAttr and drivenAttr :
            return self.safeConnectSelection (driverAttr , drivenAttr)
        # 未输入的两个名称都来自选定对象和通道盒属性选择
        selObjs = cmds.ls (selection = True , long = True)
        if not selObjs :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        # 获取通道盒属性选择
        selAttrs = mel.eval ('selectedChannelBoxAttributes')
        if not selAttrs :
            cmds.warning ("请同时填写driverAttr和drivenAttr属性，或在通道框中选择")
            return False
        # 缺少驱动属性的情况
        if driverAttr :
            success = True
            drivenAttr = selAttrs [0]
            for attr in selAttrs :
                if not self.safeConnectList (selObjs , driverAttr , attr) :
                    success = False
        # 缺少被驱动属性的情况
        elif drivenAttr :
            if len (selAttrs) != 1 :
                cmds.warning ('只能有一个选择的被驱动属性')
                return False
            driverAttr = selAttrs [0]
            success = safeConnectList (selObjs , driverAttr , drivenAttr , message = message)
        # driverAttr和drivenAttr两者都不存在，因此对驱动程序和被驱动程序都使用通道盒
        else :  # Neither exists so use channel box for both driver and driven -----------------------------------
            driverAttr = selAttrs [0]
            drivenAttr = selAttrs [0]
            success = True
            for attr in selAttrs :
                if not safeConnectList (selObjs , attr , attr , message = message) :
                    success = False
        if success :
            cmds.warning ('已经成功将{}连接到{}'.format (driverAttr , drivenAttr))
        return success


    def makeSrtConnectionsObjs (self , objList , translate = True , rotation = True , scale = True , matrix = False) :
        """用于在第一个对象和列表中的所有其他对象之间建立位移，旋转，缩放，矩阵等连接
        objList(list):Maya节点名称列表，第一个节点将为驱动物体
        translate(bool):是否连接所有位移的值
        rotation(bool):是否连接所有旋转的值
        scale(bool):是否连接所有缩放的值
        matrix(bool):是否连接所有矩阵的值
        """
        translateSuccess = False
        rotateSuccess = False
        scaleSuccess = False
        matrixSuccess = False
        translateMessage = ""
        rotateMessage = ""
        scaleMessage = ""
        matrixMessage = ""
        if translate :
            translateSuccess = self.safeConnectList (objList , "translate" , "translate")
        if rotation :
            rotateSuccess = self.safeConnectList (objList , "rotate" , "rotate")
        if scale :
            scaleSuccess = self.safeConnectList (objList , "scale" , "scale")
        if matrix :
            matrixSuccess = self.safeConnectList (objList , "matrix" , "offsetParentMatrix")
        if translateSuccess :
            translateMessage = "Translation"
        if rotateSuccess :
            rotateMessage = "Rotation"
        if scaleSuccess :
            scaleMessage = "Scale"
        if matrixSuccess :
            matrixMessage = "Matrix"
            if translateSuccess or rotateSuccess or scaleSuccess or matrixSuccess :
                om2.MGlobal.displayInfo ("Success: {} {} {} {} 成功连接了 {}".format (translateMessage ,
                                                                                      rotateMessage ,
                                                                                      scaleMessage ,
                                                                                      matrixMessage ,
                                                                                      objList))
            return translateSuccess , rotateSuccess , scaleSuccess , matrixSuccess


    def makeSrtConnectionsObjsSel (self , translate = False , rotation = False , scale = False , matrix = False) :
        """用于在第一个选定对象和所有其他对象之间建立位移，旋转，缩放，矩阵等连接

                objList(list):Maya节点名称列表，第一个节点将为驱动物体
        translate(bool):是否连接所有位移的值
        rotation(bool):是否连接所有旋转的值
        scale(bool):是否连接所有缩放的值
        matrix(bool):是否连接所有矩阵的值
        """
        selObjs = cmds.ls (selection = True , long = True)
        # 检查是否有足够多的对象进行连接
        if not selObjs :
            cmds.warning ("未选择任何变换对象。请选择两个或多个对象（转换）")
            return
        selTransforms = cmds.ls (selObjs , type = "transform")
        # 断开连接
        if not selTransforms :
            cmds.warning ("未选择任何变换对象。请选择两个或多个对象（转换）")
            return
        if len (selTransforms) < 2 :
            cmds.warning ("请选择两个或多个对象（转换）")
            return
        return self.makeSrtConnectionsObjs (selTransforms , rotation = rotation , translate = translate ,
                                            scale = scale ,
                                            matrix = matrix)


    """
    断开连接
    """
