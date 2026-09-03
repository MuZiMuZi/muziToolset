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

架构边界：
    - Driver Group 名称解析统一复用 core.rename_utils；
    - Driver Group 的 DAG 插组逻辑统一复用 core.hierarchy_utils；
    - Driver Attribute 创建统一复用 core.attr_utils；
    - Undo Chunk 统一复用 core.scene_utils；
    - Tool 只保留 Face Driven Key 工作流、Set Driven Key 和 UI；
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

from ...core import attr_utils
from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils
from ...ui import theme
from ...ui import window_utils


def _driver_group_name(control):
    u"""
    根据控制器名称生成 Driver Group 名称。

    Args:
        control (str):
            面部动画 Controller Transform。

    Returns:
        str:
            对应 Driver Group 名称。
    """
    # 使用 Rename Core 统一取得 DAG Short Name。
    short_name = rename_utils.get_short_name(
        control
    )

    if short_name.startswith("ctrl_"):
        return short_name.replace(
            "ctrl_",
            "driver_",
            1
        )

    return "{}_driver".format(
        short_name
    )


def add_extra_group(obj, group_name, world_orient=False):
    u"""
    在控制器上方创建或复用 Driver Group。

    实际 DAG 插组逻辑统一复用 ``hierarchy_utils.insert_parent_group``，
    这里只保留 Face Driven Key 的“已有 Group 直接复用”工作流语义。

    Args:
        obj (str):
            需要插入 Driver Group 的 Controller。
        group_name (str):
            Driver Group 名称。
        world_orient (bool):
            是否使用 World Orientation。

    Returns:
        str:
        新建或复用的 Driver Group。

    Raises:
        RuntimeError:
        Controller 不存在时抛出。
    """
    # 使用 Scene Core 统一验证 Controller 是否存在。
    scene_utils.validate_node(
        obj
    )

    if cmds.objExists(group_name):
        return group_name

    # 使用 Hierarchy Core 在 Controller 上方插入 Driver Group。
    return hierarchy_utils.insert_parent_group(
        node=obj,
        group_name=group_name,
        match_rotation=not world_orient
    )


def _ensure_driver_attribute(driver, attribute_name):
    u"""
    确保驱动控制器上存在 0-10 的 Keyable Driver Attribute。

    Args:
        driver (str):
            Driver Controller。
        attribute_name (str):
            需要创建或复用的驱动属性名。

    Returns:
        str:
            完整 Driver Plug。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not attribute_name:
        raise RuntimeError(
            u"驱动属性名称不能为空。"
        )

    # 使用 Scene Core 统一检查 Driver 节点。
    # -------------------------------------------------------------------------
    # Step 02：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(
        driver
    )

    driver_attr = attr_utils.Attr(
        driver
    )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not driver_attr.attr_exists(
            attribute_name
    ):
        # 使用 Attr Core 创建 0～10 的 Driver Attribute。
        driver_attr.add_attr(
            attribute_name,
            attr_type="double",
            lock=False,
            hide=False,
            default_value=0.0,
            min_value=0.0,
            max_value=10.0
        )

    plug = "{}.{}".format(
        driver,
        attribute_name
    )

    # Driver Attribute 必须对动画师可 Key。
    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.getAttr(
            plug,
            keyable=True
    ):
        cmds.setAttr(
            plug,
            keyable=True
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return plug


@scene_utils.undo_chunk
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
            作为驱动端的 Maya Controller。
        driver_attribute (str):
            Driver Attribute 名称。
        driven_controls (list[str]):
            需要建立 Driver Group 和 Driven Key 的 Controller 列表。
        minimum (float):
            默认状态 Driver Value。
        maximum (float):
            当前 Pose 对应的最大 Driver Value。

    Returns:
        list[str]:
        创建或复用的 Driver Group。

    Raises:
        RuntimeError:
        输入为空或没有可构建 Controller 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not driven_controls:
        raise RuntimeError(
            u"请选择一个或以上需要被驱动的控制器。"
        )

    # 创建或复用 Driver Controller 上的驱动属性。
    driver_plug = _ensure_driver_attribute(
        driver,
        driver_attribute
    )

    driver_groups = []

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    # 为每个 Driven Controller 创建或复用独立 Driver Group。
    for control in driven_controls:
        if not cmds.objExists(control):
            continue

        group_name = _driver_group_name(
            control
        )

        driver_group = add_extra_group(
            obj=control,
            group_name=group_name,
            world_orient=False
        )

        if driver_group not in driver_groups:
            driver_groups.append(
                driver_group
            )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not driver_groups:
        raise RuntimeError(
            u"没有找到可以创建 Driven Key 的控制器。"
        )

    # -------------------------------------------------------------------------
    # Maximum Pose
    # -------------------------------------------------------------------------
    # 把 Driver 切到 Maximum，当前 Driver Group Pose 记录为最大状态。
    cmds.setAttr(
        driver_plug,
        maximum
    )

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

    # -------------------------------------------------------------------------
    # Default Pose
    # -------------------------------------------------------------------------
    # 把 Driver 切回 Minimum，并把 Driver Group 恢复标准 TRS 默认值。
    # -------------------------------------------------------------------------
    # Step 04：应用并更新当前阶段需要的属性或状态
    # -------------------------------------------------------------------------
    cmds.setAttr(
        driver_plug,
        minimum
    )

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

    # 最终保持 Driver 在默认状态。
    cmds.setAttr(
        driver_plug,
        minimum
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return driver_groups


class FaceDrivenKeyTool(QDialog):
    """面部 Driven Key 创建窗口。"""

    def __init__(self, parent=None):
        u"""
        创建 Face Driven Key 窗口。

        Args:
            parent (QWidget | None):
                Qt 父窗口。
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
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"面部 Driven Key")
        self.subtitle_label = theme.make_subtitle(
            u"把当前面部控制器 Pose 固化到 Driver Group，并建立 0 → 10 驱动关系。"
        )

        self.driver_label = QLabel(u"驱动控制器")
        self.driver_line = QLineEdit()
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.driver_line.setReadOnly(True)
        self.driver_line.setPlaceholderText(u"选择一个总驱动控制器")
        self.driver_pick_button = QPushButton(u"拾取")

        self.attribute_label = QLabel(u"驱动属性")
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.attribute_line = QLineEdit()
        self.attribute_line.setPlaceholderText(
            u"例如 smile / browUp / mouthOpen"
        )

        self.pose_info_label = QLabel(
            u"把需要驱动的控制器摆到最大 Pose 后保持选择，再执行创建。"
        )
        self.pose_info_label.setWordWrap(True)
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.pose_info_label, "muted")

        self.execute_button = QPushButton(u"创建 Driven Key")
        self.execute_button.setToolTip(
            u"当前选择作为被驱动控制器，创建 0 和 10 两个驱动状态"
        )
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_primary(self.execute_button)

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        driver_card, driver_layout = theme.make_card(self)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        driver_layout.addWidget(
            theme.make_section_title(u"Driver")
        )

        driver_row = QHBoxLayout()
        driver_row.setContentsMargins(0, 0, 0, 0)
        driver_row.addWidget(self.driver_label)
        driver_row.addWidget(self.driver_line, 1)
        driver_row.addWidget(self.driver_pick_button)
        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        driver_layout.addLayout(driver_row)

        attribute_row = QHBoxLayout()
        attribute_row.setContentsMargins(0, 0, 0, 0)
        attribute_row.addWidget(self.attribute_label)
        attribute_row.addWidget(self.attribute_line, 1)
        driver_layout.addLayout(attribute_row)

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        pose_card, pose_layout = theme.make_card(self)
        pose_layout.addWidget(
            theme.make_section_title(u"Driven Pose")
        )
        pose_layout.addWidget(self.pose_info_label)
        pose_layout.addWidget(self.execute_button)

        main_layout.addWidget(driver_card)
        main_layout.addWidget(pose_card)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
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
        selections = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if len(selections) != 1:
            cmds.warning(
                u"请只选择一个驱动控制器。"
            )
            return

        self.driver_line.setText(
            selections[0]
        )

        cmds.select(
            clear=True
        )

    def execute(self):
        u"""
        创建当前 Pose 的 Driven Key。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        driver = self.driver_line.text().strip()
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        attribute_name = self.attribute_line.text().strip()

        driven_controls = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not driver:
            cmds.warning(
                u"请先拾取驱动控制器。"
            )
            return

        if not attribute_name:
            cmds.warning(
                u"请输入驱动属性名称。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not driven_controls:
            cmds.warning(
                u"请选择需要被驱动的面部控制器。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 05：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            # 调用参数化 Driven Key Workflow，UI 不直接实现 Rig 逻辑。
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
            cmds.warning(
                str(error)
            )


def main():
    u"""
    显示并返回 Face Driven Key 窗口。

    Returns:
        QDialog:
        Face Driven Key 窗口。
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
