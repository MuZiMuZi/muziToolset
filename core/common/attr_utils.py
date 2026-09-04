import pymel.core as pm


class Attr(object):

    def __init__(self, object=None):
        self.object = None

        if object:
            self.object = pm.PyNode(object)

    def add_attr(self, attr_name, attr_type="double", default_value=0, keyable=True):
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