from __future__ import unicode_literals , print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds

from core.bake import attrUtils


"""
这是一个针对属性连接的类
"""


class Connection () :

    def __init__ (self,object ) :
        u"""
        初始化当前对象，并准备运行时需要的状态和成员。

        Args:
            object (str):
                需要处理的 Maya 场景对象名称。
        """

        self.object = object


    """
    获得物体的输入连接和输出连接
    get_input_connection：获取物体的输入连接
    get_output_attributes：获取物体的输入连接
    """
    def get_input_connection(self,attr,plus = True ) :
        u"""
        获取物体上的对应属性的输入连接 attr(str):获取输入需要查询连接的属性 return: input_connections 返回所有的输入连接

        Args:
            attr (str):
                Maya Attribute 名称。
            plus (bool):
                控制当前方法中的 `plus` 选项是否启用。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        # 检查属性是否有输入连接
        try :
            connections_list = cmds.listConnections (self.object + '.{}'.format(attr) , source = True , destination = False , plugs = False)[0]
            if connections_list :
                return connections_list
        except ValueError :  # 遇到找不到某些属性的错误
            pass





    # 获取物体上的输出连接
    def get_output_connection (self , object) :
        u"""
        获取物体上的输出连接 self.object(str):获取输出连接的物体 return: self.input_connections 返回所有的输出连接

        Args:
            object (str):
                需要处理的 Maya 场景对象名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        ouput_connections = list ()
        # 列出物体上的所有属性
        object_all_attrs = cmds.listAttr (object , connectable = True , inUse = True)
        # 检查属性是否有输出连接
        for attr in object_all_attrs :
            object_Attr = ".".join ([object , attr])
            try :
                if cmds.listConnections (object_Attr , source = True , destination = False , plugs = True) :
                    ouput_connections.append (object_Attr)
            except ValueError :  # 遇到找不到某些属性的错误
                pass

        if not ouput_connections :
            # 如果物体没有被连接的属性的话，则爆出提示
            om.MGlobal.displayWarning ("{}没有已连接的属性 ".format (object))
            return list ()
        return ouput_connections


    """
    检查连接的可行性：
    cheek_enough_obj_connection：判断是否有足够的对象可以进行连接
    cheek_obj_attrs_connection：判断对象的属性是否可以进行连接
    """


    # 检查是否有足够的对象可以进行连接
    def cheek_enough_obj_connection (self) :
        u"""
        判断选择的对象是否数量足够可以进行连接 return： 返回驱动者和被驱动者:driver_obj,driven_obj_list

        Returns:
            tuple | bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # 获取所有选择的物体对象作为一个列表
        sel_objs = cmds.ls (selection = True , long = True)
        if not sel_objs :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        if len (sel_objs) < 2 :
            cmds.warning ("未选择任何对象。请选择两个或多个对象或节点")
            return False
        # 选择的第一个物体作为驱动者
        driver_obj = sel_objs [0]
        # 选择的第二个物体到最后一个物体作为被驱动者
        driven_obj_list = sel_objs [1 :]
        return driver_obj , driven_obj_list


    # 检查对象的属性是否可以进行连接
    def cheek_obj_attrs_connection (self , driver_obj , source_attr , driven_obj , destination_attr) :
        u"""
        检查：驱动者的属性是否能够成功连接上被驱动者的属性 检查项：1.是否存在对应的属性 2.属性之间的类型是否匹配 3.目标属性是否可以连接 driver_obj(str):作为驱动者的物体 source_attr(str):作为驱动者的...

        Args:
            driver_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_obj` 数据。
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            driven_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driven_obj` 数据。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        cheek_value = True
        driver_attr = driver_obj + '.' + source_attr
        driven_attr = driven_obj + '.' + destination_attr

        # 检查1.判断是否存在对应的属性
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        source_exists = cmds.attributeQuery (source_attr , node = driver_obj , exists = True)
        destination_exists = cmds.attributeQuery (destination_attr , node = driven_obj , exists = True)
        if not source_exists or not destination_exists :
            cmds.warning ('在节点{}或{}上找不到属性'.format (driver_attr , driven_attr))
            cheek_value = False
            return cheek_value
        # 检查2.属性之间的类型是否匹配
        source_type = cmds.attributeQuery (source_attr , node = driver_obj , attributeType = True)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return cheek_value


    """
    创建属性连接
    """


    # 创建驱动者的属性和被驱动者的属性的连接
    def create_connections (self , driver_obj , source_attr , driven_obj , destination_attr) :
        u"""
        驱动者的属性连接上被驱动者的属性 driver_obj(str):作为驱动者的物体 source_attr(str):作为驱动者的物体上驱动的属性 driven_obj(str):作为被驱动者的物体 destination_attr(...

        Args:
            driver_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_obj` 数据。
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            driven_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driven_obj` 数据。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。
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


    # 创建驱动者的需要连接的属性和所有被驱动者需要连接的属性的连接
    def createt_connections_list (self , driver_obj , source_attr , driven_obj_list , destination_attr) :
        u"""
        将驱动者的需要连接的属性连接给所有被驱动者需要连接的属性 driver_obj(str):作为驱动者的物体 source_attr(str):作为驱动者的物体上驱动的属性 driven_obj_list(str):作为被驱动者的物体列...

        Args:
            driver_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_obj` 数据。
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            driven_obj_list (list):
                当前方法需要保持顺序批量处理的数据列表。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。
        """

        # 对被驱动者的物体列表进行循环，连接被驱动者的物体上被驱动的属性
        for driven_obj in driven_obj_list :
            try :
                self.create_connections (driver_obj , source_attr , driven_obj , destination_attr ,
                                         )
                cmds.warning (
                    '已将{}.{}与{}.{}进行连接'.format (driver_obj , source_attr , driven_obj , destination_attr))
            except :
                cmds.warning (
                    '未将{}.{}与{}.{}进行连接'.format (driver_obj , source_attr , driven_obj , destination_attr))


    # 选择多个物体，创建驱动者的需要连接的属性和所有被驱动者需要连接的属性的连接
    def create_connect_connections (self , source_attr , destination_attr) :
        u"""
        选择多个物体，用于在第一个对象和列表中的所有其他对象之间建立连接

        Args:
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。
        """
        # 进行判断检查，检查是否有足够的对象可以进行连接
        driver_obj , driven_obj_list = self.cheek_enough_obj_connection ()
        # 将驱动者的需要连接的属性连接给所有被驱动者需要连接的属性
        self.createt_connections_list (driver_obj , source_attr , driven_obj_list , destination_attr)


    # 选择多个物体，创建驱动者的需要连接的属性和所有被驱动者需要连接的属性的连接
    def create_srt_connections (self , translate = True , rotation = True , scale = True ,
                                matrix = False) :
        u"""
        用于在第一个对象和列表中的所有其他对象之间建立位移，旋转，缩放，矩阵等连接 objList(list):Maya节点名称列表，第一个节点将为驱动物体 translate(bool):是否连接所有位移的值 rotation(bool):...

        Args:
            translate (bool):
                是否处理 Translate 通道。
            rotation (bool):
                Jnt / Transform 使用的 XYZ Rotation。
            scale (bool):
                是否处理 Scale 通道。
            matrix (bool):
                用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。
        """
        if translate :
            self.create_connect_connections (source_attr = "translate" ,
                                             destination_attr = "translate")
        if rotation :
            self.create_connect_connections (source_attr = "rotate" , destination_attr = "rotate")
        if scale :
            self.create_connect_connections (source_attr = "scale" , destination_attr = "scale")
        if matrix :
            self.create_connect_connections (source_attr = "matrix" ,
                                             destination_attr = "offsetParentMatrix")


    """
    断开连接
    """


    @staticmethod
    # 给定需要断开链接的属性列表进行断开链接
    def disconnect_attributes (node , attribute_list) :
        u"""
        #给定需要断开链接的属性列表进行断开链接

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attribute_list (list):
                当前方法需要保持顺序批量处理的数据列表。
        """
        for attr in attribute_list :
            plug = cmds.listConnections (node + attr , s = True , d = False , p = True)
            if plug :
                cmds.disconnectAttr (plug [0] , node + attr)

        # 实例
        # disconnect_attributes (bpjnt , ['.translate' , '.rotate' , '.scale'])


    # 断开所选择的通道盒上的属性的属性连接
    def break_attr_connections (self) :
        u"""
        断开所选择的通道盒上的属性的属性连接
        """
        # 获得选择的通道盒上的属性名称
        driven_attrs = attrUtils.Attr.get_channelBox_attrs ()
        drivens = cmds.ls (sl = True)
        for driven in drivens :
            for driven_attr in driven_attrs :
                # 获取driven_attr的上游属性连接
                driver_obj_attr = cmds.connectionInfo (driven + '.' + driven_attr , sourceFromDestination = True)
                # 断开选择的属性连接
                try :
                    cmds.disconnectAttr (driver_obj_attr , '{}.{}'.format (driven , driven_attr))
                except :
                    pass


    # 断开驱动者的属性和被驱动者的属性连接
    def break_connections (self , driver_obj , source_attr , driven_obj , destination_attr) :
        u"""
        驱动者的属性连接上被驱动者的属性 driver_obj(str):作为驱动者的物体 source_attr(str):作为驱动者的物体上驱动的属性 driven_obj(str):作为被驱动者的物体 destination_attr(...

        Args:
            driver_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_obj` 数据。
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            driven_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driven_obj` 数据。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        driver_attr = driver_obj + '.' + source_attr
        driven_attr = driven_obj + '.' + destination_attr
        try :
            # 断开属性连接
            cmds.disconnectAttr (driver_attr , driven_attr)
            return True
        except RuntimeError :
            pass
        return False


    # 断开驱动者的需要连接的属性和所有被驱动者连接的属性的连接
    def break_connections_list (self , driver_obj , source_attr , driven_obj_list , destination_attr) :
        u"""
        将驱动者的需要连接的属性连接给所有被驱动者需要连接的属性 driver_obj(str):作为驱动者的物体 source_attr(str):作为驱动者的物体上驱动的属性 driven_obj_list(str):作为被驱动者的物体列...

        Args:
            driver_obj (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_obj` 数据。
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            driven_obj_list (list):
                当前方法需要保持顺序批量处理的数据列表。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。
        """

        # 对被驱动者的物体列表进行循环，连接被驱动者的物体上被驱动的属性
        for driven_obj in driven_obj_list :
            try :
                self.break_connections (driver_obj , source_attr , driven_obj , destination_attr ,
                                        )
                cmds.warning (
                    '已将{}.{}与{}.{}断开连接'.format (driver_obj , source_attr , driven_obj , destination_attr))
            except :
                cmds.warning (
                    '未将{}.{}与{}.{}断开连接'.format (driver_obj , source_attr , driven_obj , destination_attr))


    # 选择多个物体，用于在第一个对象和列表中的所有其他对象之间断开连接
    def break_connect_connections (self , source_attr , destination_attr) :
        u"""
        选择多个物体，用于在第一个对象和列表中的所有其他对象之间断开连接

        Args:
            source_attr (str):
                驱动端完整 Maya Plug，例如 `ctrl.translateX`。
            destination_attr (str):
                接收连接的完整 Maya Plug，例如 `jnt.rotateY`。
        """
        # 进行判断检查，检查是否有足够的对象可以进行连接
        driver_obj , driven_obj_list = self.cheek_enough_obj_connection ()
        # 将驱动者的需要连接的属性连接给所有被驱动者需要连接的属性
        self.break_connections_list (driver_obj , source_attr , driven_obj_list , destination_attr)


    # 断开被驱动者上默认属性的断开连接
    def break_connect_srt_connections (self , translate = True , rotation = True , scale = True ,
                                       matrix = False) :
        u"""
        断开被驱动者上默认属性的断开连接 objList(list):Maya节点名称列表，第一个节点将为驱动物体 translate(bool):是否断开连接所有位移的值 rotation(bool):是否断开连接所有旋转的值 scale(...

        Args:
            translate (bool):
                是否处理 Translate 通道。
            rotation (bool):
                Jnt / Transform 使用的 XYZ Rotation。
            scale (bool):
                是否处理 Scale 通道。
            matrix (bool):
                用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。
        """
        if translate :
            self.break_connect_connections (source_attr = "translate" ,
                                            destination_attr = "translate")
        if rotation :
            self.break_connect_connections (source_attr = "rotate" , destination_attr = "rotate")
        if scale :
            self.break_connect_connections (source_attr = "scale" , destination_attr = "scale")
        if matrix :
            self.break_connect_connections (source_attr = "matrix" ,
                                            destination_attr = "offsetParentMatrix")
