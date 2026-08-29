# coding=utf-8
u"""
Face Driven Key Tool
====================

用于把一组面部控制器当前 Pose 转换成驱动组上的 Set Driven Key。

工作流：
    1. 选择总驱动控制器并点击“拾取驱动”；
    2. 输入驱动属性名称；
    3. 把需要的面部控制器摆到最大 Pose；
    4. 选择这些控制器并点击“创建 Driven Key”。

驱动属性默认范围：0 -> 10。
"""

from __future__ import print_function

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils


_window = None


def _short_name(node):
    return node.split("|")[-1]


def _driver_group_name(control):
    short_name = _short_name(control)

    if short_name.startswith("ctrl_"):
        return short_name.replace("ctrl_", "driver_", 1)

    return "{}_driver".format(short_name)


def add_extra_group(obj, group_name, world_orient=False):
    """
    在 obj 上方创建或复用一个额外 Transform 组。

    如果组已存在，会返回已有组，而不是返回 None。
    """
    if not cmds.objExists(obj):
        raise RuntimeError(u"对象不存在：{}".format(obj))

    if cmds.objExists(group_name):
        return group_name

    parent_nodes = cmds.listRelatives(
        obj,
        parent=True,
        fullPath=True
    ) or []

    world_translation = cmds.xform(
        obj,
        query=True,
        worldSpace=True,
        translation=True
    )
    world_rotation = cmds.xform(
        obj,
        query=True,
        worldSpace=True,
        rotation=True
    )
    world_scale = cmds.xform(
        obj,
        query=True,
        worldSpace=True,
        scale=True
    )

    if world_orient:
        world_rotation = [0.0, 0.0, 0.0]

    group = cmds.createNode(
        "transform",
        name=group_name
    )

    cmds.xform(
        group,
        worldSpace=True,
        translation=world_translation,
        rotation=world_rotation,
        scale=world_scale
    )

    if parent_nodes:
        cmds.parent(
            group,
            parent_nodes[0],
            absolute=True
        )

    cmds.parent(
        obj,
        group,
        absolute=True
    )

    return group


def _ensure_driver_attribute(driver, attribute_name):
    if not attribute_name:
        raise RuntimeError(u"驱动属性名称不能为空。")

    if not cmds.objExists(driver):
        raise RuntimeError(u"驱动控制器不存在：{}".format(driver))

    if not cmds.attributeQuery(
            attribute_name,
            node=driver,
            exists=True
    ):
        cmds.addAttr(
            driver,
            longName=attribute_name,
            attributeType="double",
            minValue=0.0,
            maxValue=10.0,
            defaultValue=0.0,
            keyable=True
        )

    plug = "{}.{}".format(driver, attribute_name)

    if not cmds.getAttr(plug, keyable=True):
        cmds.setAttr(plug, keyable=True)

    return plug


def create_driven_key_setup(
        driver,
        driver_attribute,
        driven_controls,
        minimum=0.0,
        maximum=10.0
):
    """
    把 driven_controls 当前 Pose 记录到 maximum，默认状态记录到 minimum。

    Returns:
        list[str]: Driver Group 列表。
    """
    if not driven_controls:
        raise RuntimeError(u"请选择一个或以上需要被驱动的控制器。")

    driver_plug = _ensure_driver_attribute(
        driver,
        driver_attribute
    )

    driver_groups = []

    transform_attrs = [
        "translateX",
        "translateY",
        "translateZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
    ]

    cmds.undoInfo(openChunk=True, chunkName="MuziFaceDrivenKey")
    try:
        # 先把当前控制器 Pose 固化到新建的 driver group。
        for control in driven_controls:
            if not cmds.objExists(control):
                continue

            group_name = _driver_group_name(control)
            driver_group = add_extra_group(
                obj=control,
                group_name=group_name,
                world_orient=False
            )

            if driver_group not in driver_groups:
                driver_groups.append(driver_group)

        # maximum：保留新建 driver group 当前的 Pose。
        cmds.setAttr(driver_plug, maximum)

        for driver_group in driver_groups:
            for attr in transform_attrs:
                plug = "{}.{}".format(driver_group, attr)
                cmds.setDrivenKeyframe(
                    plug,
                    currentDriver=driver_plug
                )

        # minimum：把组归到标准默认值后再记录。
        cmds.setAttr(driver_plug, minimum)

        for driver_group in driver_groups:
            default_values = {
                "translateX": 0.0,
                "translateY": 0.0,
                "translateZ": 0.0,
                "rotateX": 0.0,
                "rotateY": 0.0,
                "rotateZ": 0.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0,
            }

            for attr in transform_attrs:
                plug = "{}.{}".format(driver_group, attr)
                cmds.setAttr(plug, default_values[attr])
                cmds.setDrivenKeyframe(
                    plug,
                    currentDriver=driver_plug
                )

        cmds.setAttr(driver_plug, minimum)

    finally:
        cmds.undoInfo(closeChunk=True)

    return driver_groups


class FaceDrivenKeyTool(QDialog):
    """面部 Driven Key 创建窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(FaceDrivenKeyTool, self).__init__(parent)
        self.setWindowTitle(u"面部拾取驱动工具")
        self.setMinimumWidth(440)

        self.driver_line = QLineEdit()
        self.driver_line.setReadOnly(True)
        self.driver_pick_btn = QPushButton(u"拾取驱动")

        self.attribute_line = QLineEdit()
        self.attribute_line.setPlaceholderText(u"例如 smile / browUp / mouthOpen")
        self.execute_btn = QPushButton(u"选择被驱动控制器并创建 Driven Key")

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        driver_layout = QHBoxLayout()
        driver_layout.addWidget(QLabel(u"驱动控制器:"))
        driver_layout.addWidget(self.driver_line, 1)
        driver_layout.addWidget(self.driver_pick_btn)
        main_layout.addLayout(driver_layout)

        attribute_layout = QHBoxLayout()
        attribute_layout.addWidget(QLabel(u"驱动属性:"))
        attribute_layout.addWidget(self.attribute_line, 1)
        main_layout.addLayout(attribute_layout)

        main_layout.addWidget(self.execute_btn)

    def _create_connections(self):
        self.driver_pick_btn.clicked.connect(self.pick_driver)
        self.execute_btn.clicked.connect(self.execute)

    def pick_driver(self):
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) != 1:
            cmds.warning(u"请只选择一个驱动控制器。")
            return

        self.driver_line.setText(selections[0])
        cmds.select(clear=True)

    def execute(self):
        driver = self.driver_line.text().strip()
        attribute_name = self.attribute_line.text().strip()
        driven_controls = cmds.ls(selection=True, long=True) or []

        if not driver:
            cmds.warning(u"请先拾取驱动控制器。")
            return

        if not attribute_name:
            cmds.warning(u"请输入驱动属性名称。")
            return

        if not driven_controls:
            cmds.warning(u"请选择需要被驱动的面部控制器。")
            return

        try:
            groups = create_driven_key_setup(
                driver=driver,
                driver_attribute=attribute_name,
                driven_controls=driven_controls,
                minimum=0.0,
                maximum=10.0
            )
            cmds.select(groups, replace=True)
            print(
                u"[Face Driven Key] 已创建 {} 个 Driver Group。".format(
                    len(groups)
                )
            )
        except Exception as error:
            cmds.warning(str(error))


# 旧类名兼容。
Select_key_tool = FaceDrivenKeyTool


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = FaceDrivenKeyTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
