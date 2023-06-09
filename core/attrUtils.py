# coding=utf-8




u"""
这是一个用来对属性修改的类

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
from collections import OrderedDict
from ast import literal_eval
import maya.cmds as cmds
from ast import literal_eval
# import pipelineUtils
from collections import OrderedDict
import maya.cmds as cmds
# import fileManage as fileManage


class Attr(object):
    def __init__(self):

        self.attr = None
        self.minValue = None
        self.maxValue = None
        self.info = None

    @staticmethod
    def lock_and_hide_attrs(obj,attrs_list, lock=True, hide=True):
        u"""锁定或解锁、隐藏或显示属性.

        Args:
            name (str): 具有属性列表的名称需要为“锁定/隐藏”或“解锁/显示”.
            attrs_list (list): 属性列表需要锁定/隐藏或解锁/显示.
            lock (bool): 锁定或解锁属性.
            hide (bool): 隐藏或显示属性.

        """

        for attr in attrs_list:
            if cmds.objExists('{}.{}'.format(obj, attr)):
                if lock:
                    cmds.setAttr("{}.{}".format(obj , attr), lock=True)
                if hide:
                    cmds.setAttr("{}.{}".format(obj , attr), keyable= False, channelBox = False)
                if not lock:
                    cmds.setAttr("{}.{}".format(obj , attr), lock=False)
                if not hide:
                    cmds.setAttr("{}.{}".format(obj, attr), keyable=True, channelBox = True)

    @staticmethod
    def connect_attr(output_attr, input_attr):
        u"""将属性从输出属性连接到输入属性.

        Args:
            output_attr (str): 输出属性.
            input_attr (str): 输入属性.

        """

        connected_attrs = cmds.listConnections(input_attr, plugs=True, source=True, destination=False)
        if connected_attrs and connected_attrs[0] == output_attr:
            pass
        else:
            cmds.connectAttr(output_attr, input_attr, force=True)

    @staticmethod
    def get_string_info(obj,attr=''):
        """字符串类型属性的返回值.

        Args:
            obj (str): 对象具有此字符串类型属性.
            attr (str): 属性名称.

        Returns:
            float/int/str/tuple/list/dict/None: 从属性查询的字符串信息转换而来。.

        """

        if cmds.objExists('{}.{}'.format(obj, attr)):
            string_info_message = cmds.getAttr('{}.{}'.format(obj, attr))
            if string_info_message:
                info = literal_eval(string_info_message)
                return info

            else:
                return None

        return None

    @staticmethod
    def add_attr(obj,longName,attributeType,niceName = None,minValue = None,maxValue =None,defaultValue = None):
        cmds.addAttr(obj,longName = longName,niceName = niceName,attributeType = attributeType,minValue = minValue,
                     maxValue =maxValue,defaultValue = defaultValue)

    def add_string_info(self, attr, information):
        u"""添加信息属性.

        Args:
          information (float/int/str/tuple/list/dict): ''要作为此属性的字符串值添加的信息''.
          self.name (str): 要在其上添加字符串类型属性的名称.
          attr (str): 属性名称.

        """

        if not cmds.nameExists('{}.{}'.format(self.name, attr)):
            cmds.addAttr(self.name, ln=attr, dt='string')

        if not information:
            information = ''

        cmds.setAttr('{}.{}'.format(self.name, attr), lock=False)
        cmds.setAttr('{}.{}'.format(self.name, attr), e=True, keyable=True)
        cmds.setAttr('{}.{}'.format(self.name, attr), information, type='string')
        cmds.setAttr('{}.{}'.format(self.name, attr), lock=True)

    def get_unwanted_attrs(self, attrs_list):
        u"""返回不需要的属性名称列表.
        给定所需属性名称的列表['translateX', 'translateY', 'translateZ'],
        返回不需要的属性名称列表 ['rotateX', 'rotateY' 'rotateZ', 'scaleX', 'scaleY', 'scaleZ'].

        Args:
            attrs_list (list): 所需属性名称的列表.

        Returns:
            list: 不需要的属性名称列表.

        """

        attrs_to_lock_list = [
            "translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"
        ]
        for attr in attrs_list:
            if attr in attrs_to_lock_list:
                attrs_to_lock_list.remove(attr)

        return attrs_to_lock_list

    def set_attrs_limits(self, attr, attrs_dict):
        u"""设置控制器自身属性的最大值最小值限制.
        给定字典键 (self.attribute) 值 (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).
        设置键(self.attribute) 基于值的限制(([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).

        Args:
            self.name (str): 控制器设置其自身属性的限制.
            self.attrs_dict (dict): 字典有需要设置的属性键和属性值 (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).

            self.attrs_dict = { 'translateY': [(1, 1), (60, 120)]}
        """
        self.attr = attr
        for self.attr, value in attrs_dict.items():
            if self.attr == "translateX" :
                cmds.transformLimits(self.name, enableTranslationX=value[0])
                cmds.transformLimits(self.name, translationX=value[1])
            if self.attr == "translateY":
                cmds.transformLimits(self.name, enableTranslationY=value[0])
                cmds.transformLimits(self.name, translationY=value[1])
            if self.attr == "translateZ":
                cmds.transformLimits(self.name, enableTranslationZ=value[0])
                cmds.transformLimits(self.name, translationZ=value[1])

            if self.attr == "rotateX":
                cmds.transformLimits(self.name, enableRotationX=value[0])
                cmds.transformLimits(self.name, rotationX=value[1])
            if self.attr == "rotateY":
                cmds.transformLimits(self.name, enableRotationY=value[0])
                cmds.transformLimits(self.name, rotationY=value[1])
            if self.attr == "rotateZ":
                cmds.transformLimits(self.name, enableRotationZ=value[0])
                cmds.transformLimits(self.name, rotationZ=value[1])

            if self.attr == "scaleX":
                cmds.transformLimits(self.name, enableScaleX=value[0])
                cmds.transformLimits(self.name, scaleX=value[1])
            if self.attr == "scaleY":
                cmds.transformLimits(self.name, enableScaleY=value[0])
                cmds.transformLimits(self.name, scaleY=value[1])
            if self.attr == "scaleZ":
                cmds.transformLimits(self.name, enableScaleZ=value[0])
                cmds.transformLimits(self.name, scaleZ=value[1])

    def get_attrs_limits(self):
        u"""获取控制器属性的限制
        Given

        Args:
            self.name (str): 获取控制器属性的限制.

        Returns:
            dict:   属性列表为键(attribute)
                  属性的限制值 (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit])).

        """
        keyable_attrs = cmds.listAttr(self.name, keyable=True)
        custom_attrs = cmds.listAttr(self.name, keyable=True, userDefined=True)
        default_attrs = pipelineUtils.list_operation(list_a=keyable_attrs, list_b=custom_attrs, operation='-')

        attrs_limits_dict = OrderedDict()
        for attr in default_attrs:

            #  query default transformation attributes
            if attr == "translateX":
                limit_state = cmds.transformLimits(self.name, q=True, etx=True)
                limit_num = cmds.transformLimits(self.name, q=True, tx=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "translateY":
                limit_state = cmds.transformLimits(self.name, q=True, ety=True)
                limit_num = cmds.transformLimits(self.name, q=True, ty=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "translateZ":
                limit_state = cmds.transformLimits(self.name, q=True, etz=True)
                limit_num = cmds.transformLimits(self.name, q=True, tz=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "rotateX":
                limit_state = cmds.transformLimits(self.name, q=True, erx=True)
                limit_num = cmds.transformLimits(self.name, q=True, rx=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "rotateY":
                limit_state = cmds.transformLimits(self.name, q=True, ery=True)
                limit_num = cmds.transformLimits(self.name, q=True, ry=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "rotateZ":
                limit_state = cmds.transformLimits(self.name, q=True, erz=True)
                limit_num = cmds.transformLimits(self.name, q=True, rz=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "scaleX":
                limit_state = cmds.transformLimits(self.name, q=True, esx=True)
                limit_num = cmds.transformLimits(self.name, q=True, sx=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "scaleY":
                limit_state = cmds.transformLimits(self.name, q=True, esy=True)
                limit_num = cmds.transformLimits(self.name, q=True, sy=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

            if attr == "scaleZ":
                limit_state = cmds.transformLimits(self.name, q=True, esz=True)
                limit_num = cmds.transformLimits(self.name, q=True, sz=True)

                attrs_limits_dict[attr] = (limit_state, limit_num)

        return attrs_limits_dict

    def get_attrs_range(self, return_custom_attrs=True):
        u"""将属性范围作为带键的字典返回 ('{}.{}'.format(ctrl, attr)),
        value (((lower_limit_state, (0.0, lower_limit_num)), (upper_limit_state, (0.0, upper_limit_num)))).

        Args:
            self.name (str): 控制器查询属性范围.
            return_custom_attrs (bool): 是否返回自定义属性范围.

        Returns:
            dict: A dictionary {
            '{}.{}'.format(ctrl, attr):
            ((lower_limit_state, (0.0, lower_limit_num)), (upper_limit_state, (0.0, upper_limit_num)))
            }.

        """

        keyable_attrs = cmds.listAttr(self.name, keyable=True)
        custom_attrs = cmds.listAttr(self.name, keyable=True, userDefined=True)
        default_attrs = pipelineUtils.list_operation(list_a=keyable_attrs, list_b=custom_attrs, operation='-')

        if not return_custom_attrs:
            custom_attrs = []

        # 从默认属性查询属性范围
        ctrl_attrs_range = OrderedDict()
        for attr in default_attrs:
            limit_state = [False, False]
            limit_num = [-1, 1]

            #  query default transformation attributes
            if attr == "translateX":
                limit_state = cmds.transformLimits(self.name, q=True, etx=True)
                limit_num = cmds.transformLimits(self.name, q=True, tx=True)
            if attr == "translateY":
                limit_state = cmds.transformLimits(self.name, q=True, ety=True)
                limit_num = cmds.transformLimits(self.name, q=True, ty=True)
            if attr == "translateZ":
                limit_state = cmds.transformLimits(self.name, q=True, etz=True)
                limit_num = cmds.transformLimits(self.name, q=True, tz=True)

            if attr == "rotateX":
                limit_state = cmds.transformLimits(self.name, q=True, erx=True)
                limit_num = cmds.transformLimits(self.name, q=True, rx=True)
            if attr == "rotateY":
                limit_state = cmds.transformLimits(self.name, q=True, ery=True)
                limit_num = cmds.transformLimits(self.name, q=True, ry=True)
            if attr == "rotateZ":
                limit_state = cmds.transformLimits(self.name, q=True, erz=True)
                limit_num = cmds.transformLimits(self.name, q=True, rz=True)

            if attr == "scaleX":
                limit_state = cmds.transformLimits(self.name, q=True, esx=True)
                limit_num = cmds.transformLimits(self.name, q=True, sx=True)
            if attr == "scaleY":
                limit_state = cmds.transformLimits(self.name, q=True, esy=True)
                limit_num = cmds.transformLimits(self.name, q=True, sy=True)
            if attr == "scaleZ":
                limit_state = cmds.transformLimits(self.name, q=True, esz=True)
                limit_num = cmds.transformLimits(self.name, q=True, sz=True)

            ctrl_attrs_range['{}.{}'.format(self.name, attr)] = (
                (limit_state[0], (0.0, limit_num[0])), (limit_state[1], (0.0, limit_num[1]))
            )

        # 从自定义属性查询属性范围
        if custom_attrs:
            for attr in custom_attrs:
                try:
                    limit_num = cmds.attributeQuery(attr, node=self.name, range=True)
                    if limit_num and limit_num != [0.0, 0.0]:
                        limit_state = [False if limit_num[0] == 0.0 else True,
                                       False if limit_num[1] == 0.0 else True]

                        ctrl_attrs_range['{}.{}'.format(self.name, attr)] = (
                            (limit_state[0], (0.0, limit_num[0])), (limit_state[1], (0.0, limit_num[1]))
                        )
                except:
                    continue

        return ctrl_attrs_range

        # def import_ctrls_attrs_limits(self):
        #     """Import all the controllers limits dict, and set them on selected controllers
        #        with key(ctrl),
        #        value(
        #        a dictionary with key (attribute), value (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit]))
        #        )
        #
        #     """
        #
        #     # get current maya working path
        #     current_path = fileManage.current_maya_path()
        #
        #     ctrls_attrs_limits_dict = fileManage.read_file_info_from_json(
        #         path=current_path, user_file='ctrls_attrs_limits.json'
        #     )
        #
        #     if ctrls_attrs_limits_dict:
        #         ctrls_to_import = pipelineUtils.list_operation(list_a=self.name, list_b=ctrls_attrs_limits_dict.keys(), operation='&')
        #         if ctrls_to_import:
        #             for self.name in ctrls_to_import:
        #                 # lock unwanted attrs
        #                 ctrl_attrs = ctrls_attrs_limits_dict[self.name].keys()
        #                 attrs_to_lock = self.get_unwanted_attrs(attrs_list=ctrl_attrs)
        #                 self.lock_and_hide_attrs(ctrl_attrs, lock = False, hide=False)
        #                 self.lock_and_hide_attrs(attrs_to_lock, lock = True, hide=True)
        #                 # set attrs limits
        #                 self.set_Limits(ctrls_attrs_limits_dict[self.name])
        #
        #             print("Controllers attrs limits data imported from {}".format(current_path))
        #
        #         else:
        #             cmds.warning("Controllers attrs limits data file doesn't exists!")
        #     else:
        #         cmds.warning("Controllers attrs limits data file doesn't exists!")
        #
        # def export_ctrls_attrs_limits(self):
        #     """Export all the controllers limits as dict
        #        with key(ctrl),
        #        value(
        #        a dictionary with key (attribute), value (([lower_limit_state, upper_limit_state], [lower_limit, upper_limit]))
        #        )
        #
        #     """
        #
        #     # get current maya working path
        #     current_path = fileManage.current_maya_path()
        #     ctrls_attrs_limits_dict = {}
        #
        #     attrs_limits_dict = self.get_attrs_limits()
        #     ctrls_attrs_limits_dict[self.name] = attrs_limits_dict
        #
        #     fileManage.version_up(path=current_path, user_file='ctrls_attrs_limits.json')
        #     fileManage.export_file_info_as_json(
        #         path=current_path, user_file='ctrls_attrs_limits.json', data=ctrls_attrs_limits_dict)
        #     print ("Controllers attrs limits data exported at {}".format(current_path))
        #
        # # def get_string_info(self, attr):
        # #     """Return value from string type attribute.
        # #
        # #     Args:
        # #        self.name(str): name has this string type attribute.
        # #         attr (str): Attribute name.
        # #
        # #     Returns:
        # #         float/int/str/tuple/list/dict/None: Converted from string information which is queried from attribute.
        # #
        # #     """
        # #     attr = attr
        # #     if cmds.nameExists('{}.{}'.format(self.name , attr)):
        # #         string_info_message = cmds.getAttr('{}.{}'.format(self.name, attr))
        # #         if string_info_message:
        # #             self.info = literal_eval(string_info_message)
        # #             return self.info
        # #         else:
        # #             return None
        #
        #
        # # def get_string_info(name, attr=''):
    #     """Return value from string type attribute.
    #
    #     Args:
    #         name (str): name has this string type attribute.
    #         attr (str): Attribute name.
    #
    #     Returns:
    #         float/int/str/tuple/list/dict/None: Converted from string information which is queried from attribute.
    #
    #     """
    #
    #     if cmds.nameExists('{}.{}'.format(name, attr)):
    #         string_info_message = cmds.getAttr('{}.{}'.format(name, attr))
    #         if string_info_message:
    #             info = literal_eval(string_info_message)
    #             return info
    #
    #         else:
    #             return None


