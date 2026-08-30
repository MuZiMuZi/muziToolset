# coding=utf-8
u"""
Face Driven Key Tool
====================

把一组面部控制器当前 Pose 转换成 Driver Group 上的 Set Driven Key。

工作流：
    1. 选择总驱动控制器并拾取；
    2. 输入驱动属性名称；
    3. 把面部控制器摆到最大 Pose；
    4. 选择这些控制器并创建 Driven Key。

驱动范围默认：0 -> 10。

架构：
    - Driver Group 的 DAG 插组逻辑统一复用 core.hierarchy_utils；
    - Tool 只保留 Face Driven Key 工作流与 UI；
    - 用户直接调用 main() 时由 ui.window_utils 负责窗口生命周期。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout

from ...core import hierarchy_utils
from ...ui import theme
from ...ui import window_utils


def _short_name(node):
    """返回 Maya 节点短名称。"""
    return node.split("|")[-1]


def _driver_group_name(control):
    """根据控制器名称生成 Driver Group 名称。"""
    short_name = _short_name(control)

    if short_name.startswith("ctrl_"):
        return short_name.replace("ctrl_", "driver_", 1)

    return "{}_driver".format(short_name)


def add_extra_group(obj, group_name, world_orient=False):
    u"""
    在控制器上方创建或复用 Driver Group。

    实际 DAG 插组逻辑统一复用 ``hierarchy_utils.Hierarchy.add_extra_group``，
    这里只保留 Face Driven Key 的“已有 Group 直接复用”兼容行为。

    Args:
        obj (str):
            当前操作使用的 Maya DAG 节点或场景对象。
        group_name (str):
            `group_name` 对应的 Maya 节点或资源名称。
        world_orient (bool):
            创建 Extra Group 时是否使用 World Orientation，而不是继承目标对象旋转。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    if not cmds.objExists(obj):
        raise RuntimeError(u"对象不存在：{}".format(obj))

    if cmds.objExists(group_name):
        return group_name

    return hierarchy_utils.Hierarchy.add_extra_group(
        obj=obj,
        grp_name=group_name,
        world_orient=world_orient
    )


def _ensure_driver_attribute(driver, attribute_name):
    """确保驱动控制器上存在 0-10 的驱动属性。"""
    if not attribute_name:
        raise RuntimeError(u"驱动属性名称不能为空。")

    if not cmds.objExists(driver):
        raise RuntimeError(u"驱动控制器不存在：{}".format(driver))

    attribute_exists = cmds.attributeQuery(
        attribute_name,
        node=driver,
        exists=True
    )

    if not attribute_exists:
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
    u"""
    把当前 Pose 记录到 maximum，默认状态记录到 minimum。

    Args:
        driver (str):
            作为驱动端的 Maya 节点名称。
        driver_attribute (str):
            驱动 Set Driven Key / 属性关系的 Driver Plug，例如 `ctrl.smile`。
        driven_controls (str | list[str]):
            接收 Driver Attribute 结果的 Driven Controller 列表。
        minimum (float):
            数值 Attribute、Remap 或 UI 控件使用的最小值。
        maximum (float):
            数值 Attribute、Remap 或 UI 控件使用的最大值。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
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

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziFaceDrivenKey"
    )

    try:
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

        if not driver_groups:
            raise RuntimeError(u"没有找到可以创建 Driven Key 的控制器。")

        cmds.setAttr(driver_plug, maximum)

        for driver_group in driver_groups:
            for attr_name in transform_attrs:
                plug = "{}.{}".format(
                    driver_group,
                    attr_name
                )
                cmds.setDrivenKeyframe(
                    plug,
                    currentDriver=driver_plug
                )

        cmds.setAttr(driver_plug, minimum)

        for driver_group in driver_groups:
            for attr_name in transform_attrs:
                plug = "{}.{}".format(
                    driver_group,
                    attr_name
                )
                cmds.setAttr(
                    plug,
                    default_values[attr_name]
                )
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
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(FaceDrivenKeyTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"面部 Driven Key",
            minimum_width=520
        )
        self.resize(540, 360)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        self.title_label = theme.make_title(u"面部 Driven Key")
        self.subtitle_label = theme.make_subtitle(
            u"把当前面部控制器 Pose 固化到 Driver Group，并建立 0 → 10 驱动关系。"
        )

        self.driver_label = QLabel(u"驱动控制器")
        self.driver_line = QLineEdit()
        self.driver_line.setReadOnly(True)
        self.driver_line.setPlaceholderText(u"选择一个总驱动控制器")
        self.driver_pick_button = QPushButton(u"拾取")

        self.attribute_label = QLabel(u"驱动属性")
        self.attribute_line = QLineEdit()
        self.attribute_line.setPlaceholderText(
            u"例如 smile / browUp / mouthOpen"
        )

        self.pose_info_label = QLabel(
            u"把需要驱动的控制器摆到最大 Pose 后保持选择，再执行创建。"
        )
        self.pose_info_label.setWordWrap(True)
        theme.set_role(self.pose_info_label, "muted")

        self.execute_button = QPushButton(u"创建 Driven Key")
        self.execute_button.setToolTip(
            u"当前选择作为被驱动控制器，创建 0 和 10 两个驱动状态"
        )
        theme.style_primary(self.execute_button)

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        driver_card, driver_layout = theme.make_card(self)
        driver_layout.addWidget(
            theme.make_section_title(u"Driver")
        )

        driver_row = QHBoxLayout()
        driver_row.setContentsMargins(0, 0, 0, 0)
        driver_row.addWidget(self.driver_label)
        driver_row.addWidget(self.driver_line, 1)
        driver_row.addWidget(self.driver_pick_button)
        driver_layout.addLayout(driver_row)

        attribute_row = QHBoxLayout()
        attribute_row.setContentsMargins(0, 0, 0, 0)
        attribute_row.addWidget(self.attribute_label)
        attribute_row.addWidget(self.attribute_line, 1)
        driver_layout.addLayout(attribute_row)

        pose_card, pose_layout = theme.make_card(self)
        pose_layout.addWidget(
            theme.make_section_title(u"Driven Pose")
        )
        pose_layout.addWidget(self.pose_info_label)
        pose_layout.addWidget(self.execute_button)

        main_layout.addWidget(driver_card)
        main_layout.addWidget(pose_card)
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接按钮。
        """
        self.driver_pick_button.clicked.connect(
            self.pick_driver
        )
        self.execute_button.clicked.connect(
            self.execute
        )

    def pick_driver(self):
        u"""
        拾取唯一选择的驱动控制器。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) != 1:
            cmds.warning(u"请只选择一个驱动控制器。")
            return

        self.driver_line.setText(selections[0])
        cmds.select(clear=True)

    def execute(self):
        u"""
        创建当前 Pose 的 Driven Key。
        """
        driver = self.driver_line.text().strip()
        attribute_name = self.attribute_line.text().strip()
        driven_controls = cmds.ls(
            selection=True,
            long=True
        )

        if driven_controls is None:
            driven_controls = []

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

            cmds.select(
                groups,
                replace=True
            )

            print(
                u"[Face Driven Key] 已创建 {} 个 Driver Group。".format(
                    len(groups)
                )
            )
        except Exception as error:
            cmds.warning(str(error))


def main():
    u"""
    显示并返回 Face Driven Key 窗口。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.face.face_select_key_tool",
        FaceDrivenKeyTool
    )


__all__ = [
    "FaceDrivenKeyTool",
    "create_driven_key_setup",
    "main",
]
