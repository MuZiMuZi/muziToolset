# coding=utf-8
u"""
这是一个用来对属性进行各种操作的模块

目前已有的功能：

lock_and_hide_attrs:锁定或解锁、隐藏或显示属性
add_string_info:添加信息属性.
get_unwanted_attrs:返回不需要的属性名称列表.
add_attr: 添加属性（未写完）
connect_attr:将属性从输出属性连接到输入属性.
set_Limits:设置控制器自身属性的最大值最小值限制.
get_attrs_limits:获取控制器属性的限制值
get_attrs_range:将属性范围作为带键的字典返回 ('{}.{}'.format(ctrl, attr))

"""
from ast import literal_eval
from collections import OrderedDict

import maya.cmds as cmds

from . import pipelineUtils


class Attr () :


    def __init__ (self , object , attr) :
        """
        给定一个物体和需要进行操作的属性
        object(str):需要操作的物体对象
        attr(str):需要操作的属性
        """
        self.object = object
        self.attr = attr
        self.minValue = None
        self.maxValue = None
        self.info = None


    # 锁定或解锁、隐藏或显示属性.
    @staticmethod
    def lock_and_hide_attrs (obj , attrs_list , lock = True , hide = True) :
        u"""锁定或解锁、隐藏或显示属性.

        Args:
            name (str): 具有属性列表的名称需要为“锁定/隐藏”或“解锁/显示”.
            attrs_list (list): 属性列表需要锁定/隐藏或解锁/显示.
            lock (bool): 锁定或解锁属性.
            hide (bool): 隐藏或显示属性.

        """

        for attr in attrs_list :
            if cmds.objExists ('{}.{}'.format (obj , attr)) :
                if lock :
                    cmds.setAttr ("{}.{}".format (obj , attr) , lock = True)
                if hide :
                    cmds.setAttr ("{}.{}".format (obj , attr) , keyable = False , channelBox = False)
                if not lock :
                    cmds.setAttr ("{}.{}".format (obj , attr) , lock = False)
                if not hide :
                    cmds.setAttr ("{}.{}".format (obj , attr) , keyable = True , channelBox = True)


    # 将属性从输出属性连接到输入属性.
    def connect_attr (self , output_attr , input_attr) :
        u"""将属性从输出属性连接到输入属性.

        Args:
            output_attr (str): 输出属性.
            input_attr (str): 输入属性.

        """

        connected_attrs = cmds.listConnections (input_attr , plugs = True , source = True , destination = False)
        if connected_attrs and connected_attrs [0] == output_attr :
            pass
        else :
            cmds.connectAttr (output_attr , input_attr , force = True)


    # 用于获取字符串类型属性的返回值的函数
    def get_string_info (self) :
        """用于获取字符串类型属性的返回值的函数

        Args:
            obj(str):需要操作的物体对象
            attr(str):需要操作的属性

        Returns:
            float/int/str/tuple/list/dict/None: 从属性查询的字符串信息转换而来。.

        """
        # 使用 cmds.self.objectExists 检查对象和属性是否存在。
        if cmds.self.objectExists ('{}.{}'.format (self.object , self.attr)) :
            # 如果属性存在，使用 cmds.getAttr 获取属性的字符串信息。
            string_info_message = cmds.getAttr ('{}.{}'.format (self.object , self.attr))
            # 尝试将字符串信息转换为 Python 对象，使用 literal_eval 函数。
            # 这个函数可以安全地将字符串表示的 Python 字面值（literal）转换为相应的 Python 对象。
            if string_info_message :
                info = literal_eval (string_info_message)
                # 返回转换后的信息。
                return info

            else :
                return None
        ###简单的示例###
        # 假设有一个对象和属性名称
        # object_name = "myObject"
        # attribute_name = "myStringAttribute"
        #
        # # 调用函数获取字符串类型属性的返回值
        #  attr = attrUtils.Attr(object_name,attribute_name)
        #  attr.get_string_info (information_value)
        #
        # # 打印返回值
        # print (result)


    # 用于在 Maya 中添加信息属性的函数
    def add_string_info (self , information) :
        u"""用于在 Maya 中添加信息属性的函数

        Args:
          obj(str):需要操作的物体对象
          attr(str):需要操作的属性
          information (float/int/str/tuple/list/dict): ''要作为此属性的字符串值添加的信息''.

        """
        # 使用 cmds.objExists 检查属性是否已经存在，如果不存在，则使用 cmds.addAttr 添加一个数据类型为 'string' 的属性。
        if not cmds.objExists ('{}.{}'.format (self.object , self.attr)) :
            cmds.addAttr (self.object , ln = self.attr , dt = 'string')

        # 如果传入的 information 为空（None），将其设置为空字符串。
        if not information :
            information = ''
        # 设置属性的设置
        # 使用 cmds.setAttr 设置属性的锁定状态为解锁（lock=False）。
        cmds.setAttr ('{}.{}'.format (self.object , self.attr) , lock = False)

        # 使用 cmds.setAttr 设置属性为关键帧可用（keyable=True）。
        cmds.setAttr ('{}.{}'.format (self.object , self.attr) , e = True , keyable = True)

        # 使用 cmds.setAttr 将传入的信息设置为属性的值。
        cmds.setAttr ('{}.{}'.format (self.object , self.attr) , information , type = 'string')

        # 使用 cmds.setAttr 将属性重新锁定（lock=True）
        cmds.setAttr ('{}.{}'.format (self.object , self.attr) , lock = True)

        ###简单的示例###
        # # 假设有一个对象名称、属性名称和要添加的信息
        # object_name = "myObject"
        # attribute_name = "myStringAttribute"
        # information_value = {"key" : "value"}
        # 
        # # 调用函数添加信息属性
        # attr = attrUtils.Attr(object_name,attribute_name)
        # attr.add_information_attribute (information_value)


    # 根据给定的所需属性列表，返回不需要的属性名称列表。
    def get_unwanted_attrs (self , attrs_list) :
        u"""根据给定的所需属性列表，返回不需要的属性名称列表。
        Args:
            attrs_list (list): 所需属性名称的列表.

        Returns:
            list: 不需要的属性名称列表.

        """
        # 创建一个包含所有可能需要锁定的属性名称的列表 。
        # attrs_to_lock_list，包括 "translateX"、"translateY"、"translateZ"、"rotateX"、"rotateY"、"rotateZ"、"scaleX"、"scaleY" 和 "scaleZ"。
        attrs_to_lock_list = [
            "translateX" , "translateY" , "translateZ" , "rotateX" , "rotateY" , "rotateZ" , "scaleX" , "scaleY" ,
            "scaleZ"
        ]

        # 遍历给定的 attrs_list，如果某个属性在 attrs_to_lock_list 中，则将其从中移除。
        for attr in attrs_list :
            if attr in attrs_to_lock_list :
                attrs_to_lock_list.remove (attr)

        # 返回经过筛选的 attrs_to_lock_list，即不需要的属性名称列表。
        return attrs_to_lock_list

        ###示例###
        # 假设有一个所需属性名称的列表
        # desired_attrs = ["translateX" , "rotateY" , "scaleZ"]
        #
        # # 调用函数获取不需要的属性名称列表
        # unwanted_attrs = get_unwanted_attrs (desired_attrs)
        #
        # # 打印不需要的属性名称列表
        # print (unwanted_attrs)


    # 设置控制器属性的最大值最小值限制.
    def set_attrs_limits (self , attrs_dict) :
        u"""设置控制器属性的最大值最小值限制.
        给定字典键 (self.attribute) 值 (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).
        设置键(self.attr) 基于值的限制(([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).

        Args:
            self.object (str): 控制器设置其自身属性的限制.
            self.attrs_dict (dict): 字典有需要设置的属性键和属性值 (([lower_limit_state, upper_limit_state], [lower_limit,
            upper_limit])).

            self.attrs_dict = { 'translateY': [(1, 1), (60, 120)]}
        """
        for self.attr , (limit_state , limits) in attrs_dict.items () :
            cmds.transformLimits (self.object , **{f"enable{self.attr.capitalize ()}" : limit_state})
            cmds.transformLimits (self.object , **{self.attr : limits})

        # ###示例###
        # my_controller = attrUtils.Attr("myObject",'translateY')
        # limits_dict = {'translateY': [(1, 1), (60, 120)]}
        # my_controller.set_attrs_limits(limits_dict)


    # 用于检索控制器属性的限制。最大值和最小值
    def get_attrs_limits (self) :
        u"""用于检索控制器属性的限制。最大值和最小值
        Given

        Args:
            self.object (str): 获取控制器属性的限制.

        Returns:
            dict:   属性列表为键(attribute)
                  属性的限制值 (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).

        """
        # 获取所有可以 keyable 的属性
        keyable_attrs = cmds.listAttr (self.object , keyable = True)
        # 获取用户定义的 keyable 属性
        custom_attrs = cmds.listAttr (self.object , keyable = True , userDefined = True)
        # 将两个属性列表合并，并去除重复的选项
        default_attrs = pipelineUtils.list_operation (list_a = keyable_attrs , list_b = custom_attrs , operation = '-')
        # 用于存储属性及其限制值的字典
        attrs_limits_dict = OrderedDict ()
        # 遍历每个属性
        for attr in default_attrs :
            # 查询属性的限制状态（是否启用限制）
            limit_state = cmds.transformLimits (self.object , q = True , etx = True , ety = True , etz = True ,
                                                erx = True , ery = True , erz = True , esx = True , esy = True ,
                                                esz = True)
            # 查询属性的具体限制值（例如，lower_limit 和 upper_limit）
            limit_num = cmds.transformLimits (self.object , q = True , tx = True , ty = True , tz = True , rx = True ,
                                              ry = True , rz = True , sx = True , sy = True , sz = True)
            # 将属性及其限制值添加到字典中
            attrs_limits_dict [attr] = (limit_state , limit_num)
        # 返回包含属性及其限制值的字典
        return attrs_limits_dict

        # 示例#
        # # Example usage
        # # Create a cube as a sample controller
        # cube_name = cmds.polyCube () [0]
        #
        # # Create an instance of YourClass
        # your_instance = attrUtils.Attr (cube_name)
        #
        # # Get and print the attribute limits
        # limits_dict = your_instance.get_attrs_limits ()
        # for attr , limits in limits_dict.items () :
        #     print (f"Attribute: {attr}")
        #     print (f"Limit State: {limits [0]}")
        #     print (f"Limit Values: {limits [1]}")
        #     print ("--------")


    # 从Maya的主通道框中检索选定属性的长名称，可以选择通道盒上的属性，也可以选择历史记录上的属性，也可以选择形状历史上的属性
    @staticmethod
    def get_channelBox_attrs () :
        """从Maya的主通道框中检索选定属性的长名称，可以选择通道盒上的属性，也可以选择历史记录上的属性，也可以选择形状历史上的属性
        selAttrs = mel.eval('selectedChannelBoxAttributes')
        return：
        attr_names(list/str): 长属性名称列表，例如[“translateX”，“rotateX”]

        """
        # transfrom节点的属性获取
        # 获取当前主通道框中选择的主要对象（transfrom节点）
        main_objs = cmds.channelBox ("mainChannelBox" , query = True , mainObjectList = True)
        # 获取当前主通道框中选择的主要对象（transfrom节点）选定的属性
        main_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedMainAttributes = True)

        # history历史通道的节点的属性获取
        # 获取当前在主通道框中选择的历史记录（输入历史记录）对象。
        hist_objs = cmds.channelBox ("mainChannelBox" , query = True , historyObjectList = True)
        # 获取当前在主通道框中选择的历史记录（输入历史记录）对象的选定属性
        hist_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedHistoryAttributes = True)

        # shape历史通道的节点的属性获取
        # 获取当前在主通道框中选择的形状对象（几何体节点）
        shape_objs = cmds.channelBox ("mainChannelBox" , query = True , shapeObjectList = True)
        # 获取当前在主通道框中选择的形状对象（几何体节点）的选定属性。
        shape_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedShapeAttributes = True)
        # 现在组合并获得长名称
        attr_names = []
        for pair in ((main_objs , main_attrs) , (hist_objs , hist_attrs) , (shape_objs , shape_attrs)) :
            objs , attrs = pair
            if attrs is not None :
                for nodeName in objs :
                    # 获取长名称，而不是短名称
                    resultList = list ()
                    for attr in attrs :
                        try :
                            longName = cmds.attributeQuery (attr , node = nodeName , longName = True)
                            resultList.append (longName)
                        # 属性可能不存在多个选定对象。
                        except RuntimeError :
                            pass
                    attr_names += resultList
        # 删除重复项
        attr_names = list (set (attr_names))
        if not attr_names :
            cmds.warning ("请在通道盒中选择属性")
        return attr_names


    # 获取通道盒内所有的属性列表，查询需要位移的属性在列表的位置信息，之后进行通道盒属性位移
    @staticmethod
    def move_channelBox_attr (up = True , down = False) :
        """
        获取通道盒内所有的属性列表，查询需要位移的属性在列表的位置信息，之后进行通道盒属性位移
        up(bool):属性是否向上位移,默认为True
        down(bool):属性是否向下位移
        思路：以原本属性列表[A,B,C,D]为例。需要位移的属性为B

        上移的话：[A,B,C,D]---->[B,A,C,D]
                1.删除所选择的需要位移的属性B的上一个属性A，然后撤回，这个时候属性A会在最后一个位置,现在属性列表为[B,C,D,A]
                2.删除在之前列表中位移的属性B之后的所有属性，然后撤回,这个时候属性B会在对应的位置，现在属性列表为[B,A,C,D]


        下移的话: [A,B,C,D]---->[A,C,B,D]
                1.删除所选择的需要位移的属性B，然后撤回，这个时候属性B会在最后一个位置，现在属性列表为[A,C,D,B]
                2.删除在之前列表后位移的属性B后两位到最末尾的属性D，这个时候属性D会在最后一个位置，现在属性列表为[A,C,B,D]
        """
        obj = cmds.ls (sl = 1) [0]
        select_attr = cmds.channelBox ('mainChannelBox' , q = 1 , sma = 1) [0]
        # 先判断选择的属性是否可以被编辑,当属性不可以被编辑的时候报告错误信息并终止运行
        if cmds.getAttr (obj + '.' + select_attr , lock = True) :
            cmds.warning ('{}.{}属性不可以被编辑'.format (obj , select_attr))
            pass
        else :
            # 属性可以被编辑的情况运行下方代码，获取所有可见的属性，以及获取所选择的属性的编号
            attrList = cmds.listAttr (obj , userDefined = True)
            select_attr_index = attrList.index (select_attr)
            # 将撤销队列设置打开
            cmds.undoInfo (openChunk = True)
            ###思路：以原本属性列表[A,B,C,D]为例。需要位移的属性为B###
            # 上移的话：[A , B , C , D] - --->[B , A , C , D]
            if up :
                delete_attr_index = select_attr_index - 1
                if select_attr_index == 0 :
                    pass
                else :
                    # 1.删除所选择的需要位移的属性B的上一个属性A，然后撤回，这个时候属性A会在最后一个位置,现在属性列表为[B,C,D,A]
                    cmds.deleteAttr (obj + "." + attrList [delete_attr_index])
                    cmds.undo ()
                    # 2.删除位移的属性B之后的所有属性，然后撤回,这个时候属性B会在对应的位置，现在属性列表为[B,A,C,D]
                    for index in range ((select_attr_index + 1) , len (attrList)) :
                        cmds.deleteAttr (obj + "." + attrList [index])
                        cmds.undo ()

            # 下移的话: [A , B , C , D] - --->[A , C , B , D]
            if down :
                if select_attr_index == len (attrList) :
                    return
                else :
                    # 1.删除所选择的需要位移的属性B，然后撤回，这个时候属性B会在最后一个位置，现在属性列表为 [A , C , D , B]
                    cmds.deleteAttr (obj + "." + attrList [select_attr_index])
                    cmds.undo ()
                    # 删除在之前列表后位移的属性B后两位到最末尾的属性D，这个时候属性D会在最后一个位置，现在属性列表为[A,C,B,D]
                    for index in range ((select_attr_index + 2) , len (attrList)) :
                        cmds.deleteAttr (obj + "." + attrList [index])
                        cmds.undo ()


    # 锁住物体需要隐藏的属性
    @staticmethod
    def set_lock_attr (node , attr , lock = True) :
        """
        锁住物体需要隐藏的属性
        node(str):maya节点
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        cmds.setAttr ("{}.{}".format (node , attr) , lock = lock , keyable = True)


    # 隐藏物体需要隐藏的属性
    @staticmethod
    def set_hide_attr (node , attr , hide = True) :
        """
        隐藏物体需要隐藏的属性
        node(str):maya节点
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        if hide :
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = False , channelBox = False)
        else :
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = True , channelBox = True)
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = True)


    # 设置属性是否可以k动画帧
    @staticmethod
    def set_key_attr (node , attr , keyable = True) :
        """
        设置属性是否可以k动画帧
        node(str):maya节点，需要锁定或隐藏属性的物体
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        cmds.setAttr ("{}.{}".format (node , attr) , keyable = keyable)


    # 锁定或隐藏需要的属性
    @staticmethod
    def lock_hide_attr (node , attr , lock = True , hide = True) :
        '''
        锁定或隐藏需要的属性
        node(str):需要锁定或隐藏属性的物体
        attr(str)：需要锁定或隐藏属性的属性
        '''
        Attr.set_lock_attr (node , attr , lock = lock)
        Attr.set_hide_attr (node , attr , hide = hide)


    # 重置所选择的物体的默认属性
    @staticmethod
    def reset_attr (node) :

        """
        重置所选择的物体的默认属性
        """
        # 重置 X、Y、Z 轴的平移和旋转属性
        for attr in ['translate' , 'rotate'] :
            for axis in ['X' , 'Y' , 'Z'] :
                try :
                    # 尝试将属性设置为 0
                    cmds.setAttr (node + '.{}{}'.format (attr , axis) , 0)
                except :
                    # 如果属性不存在，则捕获异常
                    pass

        # 重置 X、Y、Z 轴的缩放属性
        for axis in ['X' , 'Y' , 'Z'] :
            try :
                # 尝试将属性设置为 1
                cmds.setAttr (node + '.scale{}'.format (axis) , 1)
            except :
                # 如果属性不存在，则捕获异常
                pass
