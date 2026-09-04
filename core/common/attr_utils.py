# coding=utf-8
u"""
attr_utils：Maya Attribute 基础工具。

方法介绍与使用场景：

    Attr.__init__
        创建一个属性工具对象，并保存需要操作的 Maya 节点。
        适合后续统一处理 Controller、Joint、Group 等节点的属性。

    Attr.has_attr
        检查当前对象是否存在指定属性。
        适合添加自定义属性前进行重复检查。

    Attr.add_attr
        给当前对象添加新的自定义属性。
        适合创建 follow、ikFk、stretch、visibility 等绑定属性。

    Attr.set_value
        设置当前对象指定属性的数值。
        适合程序化修改 Maya 节点属性。

    Attr.get_value
        获取当前对象指定属性的数值。
        适合读取节点状态或后续计算使用。

    Attr.lock_attr
        锁定当前对象指定属性。
        适合限制 Controller 中不需要动画师修改的属性。

    Attr.unlock_attr
        解锁当前对象指定属性。
        适合重新开放已经锁定的属性。

    Attr.hide_attr
        将当前对象指定属性从 Channel Box 中隐藏。
        适合整理 Controller 的动画属性显示。

    Attr.show_attr
        将当前对象指定属性重新设置为可关键帧属性。
        适合重新显示之前隐藏的属性。

    Attr.lock_hide_attr
        同时锁定并隐藏当前对象指定属性。
        适合处理 Controller 的 scale、visibility 等不需要动画的属性。

    Attr.connect_attr
        将当前对象的指定属性连接到目标对象的指定属性。
        适合 Controller 驱动 Joint、Utility Node 或其他绑定节点。

    Attr.disconnect_attr
        断开当前对象指定属性与目标属性之间的连接。
        适合重建绑定或清理已有属性连接。
"""

import pymel.core as pm


class Attr(object):

    def __init__(self, object=None):
        u"""
        初始化 Attribute 工具对象。

        object(str/PyNode): 需要进行属性操作的 Maya 节点。

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        object = "ctrl_lf_eye_main_001"

        attr_object = attr_utils.Attr(object)

        print(attr_object.object)
        """

        self.object = None

        # 如果传入 Maya 节点，则统一转换成 PyNode 保存。
        if object:
            self.object = pm.PyNode(object)

    def has_attr(self, attr_name):
        u"""
        检查当前对象是否存在指定属性。

        attr_name(str): 需要检查的属性名称。

        Returns:
            bool: 属性存在返回 True，不存在返回 False。

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"

        result = attr_object.has_attr(attr_name)

        print(result)
        """

        # 检查当前节点是否拥有指定属性。
        has_attr_value = self.object.hasAttr(attr_name)

        return has_attr_value

    def add_attr(self, attr_name, attr_type="double", default_value=0, keyable=True):
        u"""
        给当前对象添加一个新的自定义属性。

        如果当前对象已经存在同名属性，则不重复创建。

        attr_name(str): 需要添加的属性名称。
        attr_type(str): 属性类型，默认 "double"。
        default_value(float/int/bool): 属性默认值，默认 0。
        keyable(bool): 是否允许属性设置关键帧，默认 True。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"
        attr_type = "double"
        default_value = 0
        keyable = True

        attr_object.add_attr(attr_name, attr_type, default_value, keyable)
        """

        # 如果属性已经存在，则不重复创建。
        if self.has_attr(attr_name):
            return

        # 给当前节点添加新的自定义属性。
        self.object.addAttr(attr_name, attributeType=attr_type, defaultValue=default_value, keyable=keyable)

    def set_value(self, attr_name, value):
        u"""
        设置当前对象指定属性的数值。

        attr_name(str): 需要设置数值的属性名称。
        value(object): 需要设置给属性的数值。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"
        value = 1

        attr_object.set_value(attr_name, value)
        """

        # 直接通过当前 PyNode 设置指定属性的数值。
        self.object.setAttr(attr_name, value)

    def get_value(self, attr_name):
        u"""
        获取当前对象指定属性的数值。

        attr_name(str): 需要获取数值的属性名称。

        Returns:
            object: 当前属性的数值。

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"

        value = attr_object.get_value(attr_name)

        print(value)
        """

        # 获取当前节点指定属性的数值。
        value = self.object.getAttr(attr_name)

        return value

    def lock_attr(self, attr_name):
        u"""
        锁定当前对象指定属性。

        attr_name(str): 需要锁定的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "scaleX"

        attr_object.lock_attr(attr_name)
        """

        # 将指定属性设置为锁定状态。
        self.object.setAttr(attr_name, lock=True)

    def unlock_attr(self, attr_name):
        u"""
        解锁当前对象指定属性。

        attr_name(str): 需要解锁的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "scaleX"

        attr_object.unlock_attr(attr_name)
        """

        # 将指定属性设置为解锁状态。
        self.object.setAttr(attr_name, lock=False)

    def hide_attr(self, attr_name):
        u"""
        将当前对象指定属性从 Channel Box 中隐藏。

        隐藏时同时关闭属性的 keyable 和 channelBox 显示状态。

        attr_name(str): 需要隐藏的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "visibility"

        attr_object.hide_attr(attr_name)
        """

        # 关闭属性的 Keyable 和 Channel Box 显示。
        self.object.setAttr(attr_name, keyable=False, channelBox=False)

    def show_attr(self, attr_name):
        u"""
        将当前对象指定属性重新设置为可关键帧属性。

        attr_name(str): 需要重新显示的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "visibility"

        attr_object.show_attr(attr_name)
        """

        # 设置为 Keyable 后，属性会重新显示在 Channel Box 中。
        self.object.setAttr(attr_name, keyable=True)

    def lock_hide_attr(self, attr_name):
        u"""
        同时锁定并隐藏当前对象指定属性。

        attr_name(str): 需要锁定并隐藏的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "scaleX"

        attr_object.lock_hide_attr(attr_name)
        """

        # 复用已有方法，先锁定属性。
        self.lock_attr(attr_name)

        # 再将属性从 Channel Box 中隐藏。
        self.hide_attr(attr_name)

    def connect_attr(self, attr_name, target_object, target_attr_name):
        u"""
        将当前对象的指定属性连接到目标对象的指定属性。

        attr_name(str): 当前对象作为输出端的属性名称。
        target_object(str/PyNode): 需要接收连接的目标对象。
        target_attr_name(str): 目标对象作为输入端的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"
        target_object = "jnt_lf_eye_bind_001"
        target_attr_name = "rotateX"

        attr_object.connect_attr(attr_name, target_object, target_attr_name)
        """

        # 将目标对象统一转换成 PyNode。
        target_object = pm.PyNode(target_object)

        # 属性连接本质是 Plug 到 Plug，因此在连接时获取两端属性 Plug。
        pm.connectAttr(self.object.attr(attr_name), target_object.attr(target_attr_name), force=True)

    def disconnect_attr(self, attr_name, target_object, target_attr_name):
        u"""
        断开当前对象指定属性与目标属性之间的连接。

        attr_name(str): 当前对象作为输出端的属性名称。
        target_object(str/PyNode): 需要断开连接的目标对象。
        target_attr_name(str): 目标对象作为输入端的属性名称。

        Returns:
            None

        Maya 使用示例：

        from muziToolset.core.common import attr_utils

        attr_object = attr_utils.Attr("ctrl_lf_eye_main_001")
        attr_name = "follow"
        target_object = "jnt_lf_eye_bind_001"
        target_attr_name = "rotateX"

        attr_object.disconnect_attr(attr_name, target_object, target_attr_name)
        """

        # 将目标对象统一转换成 PyNode。
        target_object = pm.PyNode(target_object)

        # 属性断开同样需要使用连接两端的 Plug。
        pm.disconnectAttr(self.object.attr(attr_name), target_object.attr(target_attr_name))
