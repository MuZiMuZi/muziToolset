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
import maya.mel as mel
from importlib import reload
from ..core import pipelineUtils
import maya.api.OpenMaya as om


"""
这是一个针对属性连接的类
"""


class Connection () :

    def __init__ (self , object) :
        """
        object(str):给定的一个对象
        """
        self.object = object
        # 列出物体上的所有属性
        self.object_all_attrs = cmds.listAttr (self.object , connectable = True , inUse = True)


    """
    获得连接
    """


    def get_input_connection (self) :
        """
        获取物体上的输入连接
        self.object(str):获取输入连接的物体
        return: self.input_connections
                返回所有的输入连接
        """
        self.input_connections = list ()
        # 检查属性是否有输入连接
        for attr in self.object_all_attrs :
            self.object_Attr = ".".join ([self.object , attr])
            try :
                if cmds.listConnections (self.object_Attr , source = True , destination = False , plugs = True) :
                    self.input_connections.append (self.object_Attr)
            except ValueError :  # 遇到找不到某些属性的错误
                pass

        if not self.input_connections :
            # 如果物体没有被连接的属性的话，则爆出提示
            om.MGlobal.displayWarning ("{}没有已连接的属性 ".format (self.object))
            return list ()
        return self.input_connections


    def get_output_attributes (self) :
        """
        获取物体上的输出连接
        self.object(str):获取输出连接的物体
        return: self.input_connections
                返回所有的输出连接
        """
        self.ouput_connections = list ()
        # 检查属性是否有输出连接
        for attr in self.object_all_attrs :
            self.object_Attr = ".".join ([self.object , attr])
            try :
                if cmds.listConnections (self.object_Attr , source = True , destination = False , plugs = True) :
                    self.ouput_connections.append (self.object_Attr)
            except ValueError :  # 遇到找不到某些属性的错误
                pass

        if not self.ouput_connections :
            # 如果物体没有被连接的属性的话，则爆出提示
            om.MGlobal.displayWarning ("{}没有已连接的属性 ".format (self.object))
            return list ()
        return self.ouput_connections


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


    def create_attribute_connections (self , driver_obj , source_attr , driven_obj , destination_attr) :
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


    def create_connect_list (self , driver_obj , source_attr , driven_obj_list , destination_attr) :
        """将驱动者的需要连接的属性连接给所有被驱动者需要连接的属性
        driver_obj(str):作为驱动者的物体
        source_attr(str):作为驱动者的物体上驱动的属性
        driven_obj_list(str):作为被驱动者的物体列表
        destination_attr(str):作为被驱动者的物体上被驱动的属性
        """

        # 对被驱动者的物体列表进行循环，连接被驱动者的物体上被驱动的属性
        for driven_obj in driven_obj_list :
            try :
                self.create_attribute_connections (driver_obj , source_attr , driven_obj , destination_attr ,
                                                   )
                cmds.warning (
                    '已将{}.{}与{}.{}进行连接'.format (driver_obj , source_attr , driven_obj , destination_attr))
            except:
                cmds.warning (
                    '未将{}.{}与{}.{}进行连接'.format (driver_obj , source_attr , driven_obj , destination_attr))


    def safeConnectSelection (self , source_attr , destination_attr) :
        """将第一个选定对象安全地连接到其余选定对象。

        """
        sel_objs = cmds.ls (selection = True , long = True)
        if not sel_objs :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        if len (sel_objs) < 2 :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        return self.create_connect_list (driver_obj , source_attr , driven_obj_list , destination_attr)


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
                if not self.create_connect_list (selObjs , driverAttr , attr) :
                    success = False
        # 缺少被驱动属性的情况
        elif drivenAttr :
            if len (selAttrs) != 1 :
                cmds.warning ('只能有一个选择的被驱动属性')
                return False
            driverAttr = selAttrs [0]
            success = self.create_connect_list (selObjs , driverAttr , drivenAttr)
        # driverAttr和drivenAttr两者都不存在，因此对驱动程序和被驱动程序都使用通道盒
        else :  # Neither exists so use channel box for both driver and driven -----------------------------------
            driverAttr = selAttrs [0]
            drivenAttr = selAttrs [0]
            success = True
            for attr in selAttrs :
                if not self.create_connect_list (selObjs , attr , attr) :
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
            translateSuccess = self.create_connect_list (objList , "translate" , "translate")
        if rotation :
            rotateSuccess = self.create_connect_list (objList , "rotate" , "rotate")
        if scale :
            scaleSuccess = self.create_connect_list (objList , "scale" , "scale")
        if matrix :
            matrixSuccess = self.create_connect_list (objList , "matrix" , "offsetParentMatrix")
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


    def breakAttr (self , objectAttribute) :
        """根据右键单击通道框中的断开连接，断开单个属性的连接
        objectAttribute(str): 需要断开连接的单个物体属性
        """
        # 获取该属性的连接
        oppositeAttrs = cmds.listConnections (objectAttribute , plugs = True)
        if not oppositeAttrs :
            return False
        try :
            cmds.disconnectAttr (oppositeAttrs [0] , objectAttribute)
            return True
        except RuntimeError :
            pass
        return False


    def breakAttrList (self , objAttrList) :
        """仅使用一个属性断开连接，如在列表上的通道框中右键单击断开连接：

            objAttrList: ["pCube1.rotateX", "pCube1.translateY"]

        objAttrList(list/str): 具有属性名称的对象列表，即[“pCube1.rotateX”，“pCube1-translateY”]
        """
        success = False
        for objAttr in objAttrList :
            if breakAttr (objAttr) :
                success = True
        return success


    def breakConnectionSourceDestination (self , sourceObj , sourceAttr , destinationObj , destinationAttr) :
        """断开连接，并检查连接是否存在。必须按照正确的source、destination和存在性
            如果不知道源和目标顺序，可以使用breakConnectionsTwoObj()

        sourceObj(str):  作为驱动者的物体
        sourceAttr(str): 作为驱动者的物体上驱动的属性
        destinationObj(str):作为被驱动者的物体
        destinationAttr(str): 作为被驱动者的物体上被驱动的属性
        """
        destinationObjAttr = "{}.{}".format (destinationObj , destinationAttr)
        sourceObjAttr = "{}.{}".format (sourceObj , sourceAttr)
        sourceConnections = cmds.listConnections (destinationObjAttr , destination = False , source = True ,
                                                  plugs = True)
        if sourceConnections :
            if sourceObjAttr in sourceConnections :  # then yes confirmed
                cmds.disconnectAttr (sourceObjAttr , destinationObjAttr)
                return True
        return False


    def breakConnectionsTwoObj (self , objOne , objOneAttr , objTwo , objTwoAttr) :
        """断开连接，并检查连接是否存在。目的地/来源顺序无关紧要，两者都尝试。
        objOne(str): 驱动者的节点名称
        objOneAttr(str): 驱动者的节点名称的属性

        objTwo(str): 被驱动者的节点名称

        objTwoAttr(str): 被驱动者的节点名称的属性


        """
        if not self.breakConnectionSourceDestination (objOne , objOneAttr , objTwo , objTwoAttr) :  # Try the inverse
            if not self.breakConnectionSourceDestination (objTwo , objTwoAttr , objOne , objOneAttr) :
                return False
        return True


    def breakConnectionsList (self , objList , sourceAttr , destinationAttr) :
        """安全地断开第一个对象与其余对象之间的连接。
        objList(list/str): Maya节点的列表
        sourceAttr(str): 仅第一个对象的源属性（from属性）
        destinationAttr(str): 要连接到所有剩余对象上的目标属性（不是第一个）

        """
        success = False
        objList = cmds.ls (objList , shortNames = True)
        sourceObj = objList.pop (0)
        for obj in objList :
            if self.breakConnectionsTwoObj (sourceObj , sourceAttr , obj , destinationAttr) :
                success = True
        return success


    def breakConnectionsSelection (self , sourceAttr , destinationAttr) :
        """安全地断开第一个对象与选择中其余对象之间的连接

        sourceAttr(str): 仅第一个对象的源属性（from属性）

        destinationAttr(str): 要连接到所有剩余对象上的目标属性（不是第一个）

        """
        selObjs = cmds.ls (selection = True , long = True)
        if not selObjs :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        if len (selObjs) < 2 :
            cmds.warning ("请选择两个或多个对象或节点")
            return False
        return self.breakConnectionsList (selObjs , sourceAttr , destinationAttr)


    def breakConnectionAttrsOrChannelBox (self , driverAttr = "" , drivenAttr = "" , message = True) :
        # 当给定了driverAttr和drivenAttr的值的时候
        if driverAttr and drivenAttr :
            return self.breakConnectionsSelection (driverAttr , drivenAttr)
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
        # 缺少驱动者属性的时候
        if driverAttr :
            drivenAttr = selAttrs [0]
            mel.eval ('channelBoxCommand -break;')
            success = True

        elif drivenAttr :  # Then driver attr is missing -----------------------------------
            if len (selAttrs) != 1 :
                if message :
                    cmds.warning ("请在属性栏里只选择一个频道，只能有一个驱动的属性")
                return False
            driverAttr = selAttrs [0]
            success = self.breakConnectionsList (selObjs , driverAttr , drivenAttr)
        else :  # Neither exists so just break channel selection -----------------------------------
            driverAttr = selAttrs [0]
            drivenAttr = selAttrs [0]
            mel.eval ('channelBoxCommand -break;')
            success = True
        if success :
            cmds.warning ("成功打断了 `{}` 到 `{}` for `{}` ".format (driverAttr , drivenAttr , selObjs))
        return


    def breakAllDrivenOrChannelBoxSel (self) :
        """断开所选内容上的所有连接，如果通道盒具有属性选择，则仅断开那些选定的连接
        """
        selObjs = cmds.ls (selection = True , long = True)
        # 判断是否有不符合要求的情况
        if not selObjs :
            cmds.warning ("未选择任何对象。请选择对象和通道框属性来进行断开连接")
            return False
        # 从通道盒中获取选择
        selAttrs = mel.eval ('selectedChannelBoxAttributes')
        # 在通道框中选择属性
        if selAttrs :
            mel.eval ('channelBoxCommand -break;')
            cmds.warning ("与通道盒断开了选择连接的属性")
            return True
        # 未选择属性，因此全部打断
        return self.breakAllConnectionsObjList (selObjs)


    def breakAllConnectionsObj (self , obj) :
        """断开对象或节点的所有受驱动连接

        obj(list/str): Maya对象或节点
        """
        success = True
        destinationAttrs = self.get_input_connection (obj)
        for objAttr in destinationAttrs :
            if not breakAttr (objAttr) :
                success = False
                cmds.warning ("`{}`无法断开连接".format (objAttr))
        cmds.warning ("断开的所有属性{}`".format (obj))
        return success


    def breakAllConnectionsObjList (self , objList) :
        """断开对象列表中的所有受驱动连接

        objList(list/str): Maya对象或节点的列表
        """
        success = True
        for obj in objList :
            if not self.breakAllConnectionsObj (obj) :
                success = False
        cmds.warning ("断开的所有属性`{}`".format (objList))
        return success


    def breakAllConnectionsSel (self , objList) :
        """断开所有选定对象的所有受驱动连接

        objList(list/str): Maya对象或节点的列表
        """
        selObjs = cmds.ls (selection = True , long = True)
        # 判断是否有选定对象
        if not selObjs :
            cmds.warning ("No objects selected. Please select object/s to break connections")
            return False
        return self.breakAllConnectionsObjList (objList)


    def breakSrtConnectionsObjs (self , objList , translate = False , rotation = False , scale = False ,
                                 matrix = False) :
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
        masterObj = objList.pop (0)
        for obj in objList :
            if translate :
                translateSuccess = self.breakConnectionsTwoObj (masterObj , "translate" , obj , "translate")
            if rotation :
                rotateSuccess = self.breakConnectionsTwoObj (masterObj , "rotate" , obj , "rotate")
            if scale :
                scaleSuccess = self.breakConnectionsTwoObj (masterObj , "scale" , obj , "scale")
            if matrix :
                matrixSuccess = self.breakConnectionsTwoObj (masterObj , "matrix" , obj , "offsetParentMatrix")
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


    def delSrtConnectionsObjsSel (self , translate = False , rotation = False , scale = False , matrix = False ,
                                  ) :
        """用于在第一个选定对象和所有其他对象之间断掉位移，旋转，缩放，矩阵等连接

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
        return self.breakSrtConnectionsObjs (selTransforms , rotation = rotation , translate = translate ,
                                             scale = scale ,
                                             matrix = matrix)


    def copyDrivenConnectedAttrs (self , obj) :
        """复制受驱动的属性

        返回:

            1.连接属性的来源，来自驱动对象列表（object.attribute）

            2.所有受驱动的属性，即具有进入节点列表的连接的属性（attributeNames）

        obj(str): 具有传入连接的节点。一个受驱动的对象


        """
        destinationAttrs = list ()
        sourceObjAttrs , destObjAttrs = self.get_destination_source_attrs (obj)
        for obAttr in destObjAttrs :
            destinationAttrs.append (obAttr.split (".") [1])
        if destinationAttrs :
            self.makeConnectionAttrsOrChannelBox (driverAttr = sourceObjAttrs [0] ,
                                                  drivenAttr = destinationAttrs [0])
            cmds.warning (
                "成功复制了`{}` 连接的属性 `{}`".format (sourceObjAttrs , destinationAttrs))
        else :
            cmds.warning ("在这个节点上面找不到传入的链接`{}`,未复制任何数据.".format (obj))
        return sourceObjAttrs , destinationAttrs


    def copyDrivenConnectedAttrsSel (self) :
        """复制第一个选定对象的受驱动属性。
        返回:

        1.连接属性的来源，来自驱动对象列表（object.attribute）

        2.所有受驱动的属性，即具有进入节点列表的连接的属性（attributeNames）


        """
        selObjs = cmds.ls (selection = True , long = True)
        if not selObjs :
            cmds.warning ("未选择要复制连接属性的对象。请重新选择需要复制的对象")
            return list () , list ()
        return self.copyDrivenConnectedAttrs (selObjs [0])
