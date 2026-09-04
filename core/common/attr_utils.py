import pymel.core as pm


class Attr(object):

    def __init__(self, object=None):
        self.object = None

        if object:
            self.object = pm.PyNode(object)


    def has_attr (self , attr_name) :
        u"""
        检查当前对象是否存在指定属性。

        attr_name(str): 需要检查的属性名称。

        Returns:
            bool: 属性存在返回 True，不存在返回 False。

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")

        result = attr_object.has_attr("follow")

        print(result)
        """
        has_attr_value = self.object.hasAttr (attr_name)
        return has_attr_value

    def add_attr(self, attr_name, attr_type="double", default_value=0, keyable=True):
        if self.object.has_attr():
            return
        else:
            self.object.addAttr(attr_name, attributeType=attr_type, defaultValue=default_value, keyable=keyable)

    def set_value(self, attr_name, value):
        self.object.setAttr(attr_name, value)

    def get_value(self, attr_name):
        value = self.object.getAttr(attr_name)
        return value

    def lock_attr(self, attr_name):
        self.object.setAttr(attr_name, lock=True)

    def unlock_attr(self, attr_name):
        self.object.setAttr(attr_name, lock=False)

    def hide_attr(self, attr_name):
        self.object.setAttr(attr_name, keyable=False, channelBox=False)

    def show_attr(self, attr_name):
        self.object.setAttr(attr_name, keyable=True)

    def lock_hide_attr(self, attr_name):
        self.lock_attr(attr_name)
        self.hide_attr(attr_name)

    def connect_attr(self, attr_name, target_object,target_attr_name):
        pm.connectAttr(self.object.attr(attr_name), target_object.attr(target_attr_name), force=True)

    def disconnect_attr(self, attr_name, target_object,target_attr_name):
        pm.disconnectAttr(self.object.attr(attr_name), target_object.attr(target_attr_name))
