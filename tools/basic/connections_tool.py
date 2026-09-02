# coding=utf-8
u"""
Connections Tool
================

Maya 属性连接工具窗口。

模块职责
--------
1. 提供 Translate / Rotate / Scale / Matrix 连接界面；
2. 从 Maya Selection 和 Channel Box 收集用户输入；
3. 把 UI 选择整理成明确 Source / Destination Plug Pair；
4. 调用 ``core.connection_utils`` 执行底层 DG Plug 查询、连接和断开；
5. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

设计边界
--------
- Selection / Channel Box 属于 Tool；
- Plug 是否存在、是否已连接、是否允许覆盖统一由 ``connection_utils`` 处理；
- Tool 不依赖退休的批量 Compatibility API；
- Tool 只组合明确 Plug Pair，不维护第二套 DG 连接规则。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...config import icons_dir as icon_dir
from ...core import connection_utils
from ...core import scene_utils
from ...ui import theme
from ...ui import window_utils


def get_selected_objects(minimum_count=1):
    u"""

        返回 Maya 当前选择，并校验最少数量。

        Args:
            minimum_count (int):
                当前构建、采样或查询过程使用的元素数量。

        Returns:
            object | list:
                按当前 API 约定顺序返回的结果列表。

    """
    selected_objects = scene_utils.get_selected_nodes(
        long=True,
        flatten=True
    )

    if len(selected_objects) < minimum_count:
        cmds.warning(
            u"请至少选择 {} 个物体。".format(
                minimum_count
            )
        )
        return []

    return selected_objects


def get_channel_box_attrs():
    u"""

        返回 Maya Channel Box 当前选中的主属性。

        Returns:
            object:
                当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    attribute_names = cmds.channelBox(
        "mainChannelBox",
        query=True,
        selectedMainAttributes=True
    )

    if attribute_names is None:
        attribute_names = []

    if not attribute_names:
        cmds.warning(
            u"请先在 Channel Box 中选择属性。"
        )

    return attribute_names


def build_attribute_plug_pairs(
        driver,
        driven_objects,
        attribute_pairs
):
    u"""

        把 Tool 层的 Object + Attribute Mapping 展开成明确 Plug Pair。

        Args:
            driver (str):
                作为驱动端的 Maya 节点名称。
            driven_objects (str | list[str]):
                需要批量接收驱动结果的 Driven 节点或节点列表。
            attribute_pairs (list[tuple[str, str]] | dict):
                需要批量建立连接的 Source Plug / Destination Plug 配对数据。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    plug_pairs = []

    for driven_object in driven_objects:
        for source_attribute, destination_attribute in attribute_pairs:
            source_plug = "{}.{}".format(
                driver,
                source_attribute
            )
            destination_plug = "{}.{}".format(
                driven_object,
                destination_attribute
            )
            plug_pairs.append((
                source_plug,
                destination_plug,
            ))

    return plug_pairs


def build_source_plug_pairs(
        source_plug,
        driven_objects,
        attribute_names
):
    u"""

        把一个 Source Plug 展开到多个对象的同名 Attribute。

        Args:
            source_plug (str):
                完整 Maya Plug，例如 `node.translateX`。
            driven_objects (str | list[str]):
                需要批量接收驱动结果的 Driven 节点或节点列表。
            attribute_names (str | list[str]):
                需要查询、复制或批量连接的 Maya Attribute 名称列表。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    plug_pairs = []

    for driven_object in driven_objects:
        for attribute_name in attribute_names:
            destination_plug = "{}.{}".format(
                driven_object,
                attribute_name
            )
            plug_pairs.append((
                source_plug,
                destination_plug,
            ))

    return plug_pairs


class ConnectionsTool(QWidget):
    """属性连接工具窗口。"""

    def __init__(self, parent=None):
        u"""
        创建 Connections Tool。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """
        super(ConnectionsTool, self).__init__(parent)

        self.driver_plug = None
        self.driven_attr_names = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Connections Tool",
            minimum_width=560
        )
        self.resize(590, 560)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"属性连接")
        self.subtitle_label = theme.make_subtitle(
            u"管理 Transform、自定义属性和已有输入连接。"
        )

        self.translate_checkbox = QCheckBox("Translate")
        self.rotate_checkbox = QCheckBox("Rotate")
        self.scale_checkbox = QCheckBox("Scale")
        self.matrix_checkbox = QCheckBox("Matrix")

        self.reset_default_button = QPushButton(
            QIcon(icon_dir + "/reset.png"),
            u"重置"
        )
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_ghost(self.reset_default_button)

        self.connect_default_button = QPushButton(u"创建默认连接")
        theme.style_primary(self.connect_default_button)

        self.break_default_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            u"断开默认连接"
        )
        theme.style_danger(self.break_default_button)

        self.driver_line = QLineEdit()
        self.driver_line.setReadOnly(True)
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.driver_line.setPlaceholderText(u"Driver Plug")
        self.pick_driver_button = QPushButton(u"拾取 Driver")

        self.driven_line = QLineEdit()
        self.driven_line.setReadOnly(True)
        self.driven_line.setPlaceholderText(u"Driven Attribute")
        self.pick_driven_button = QPushButton(u"拾取 Driven")

        self.connect_custom_button = QPushButton(u"创建自定义连接")
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_primary(self.connect_custom_button)

        self.break_custom_button = QPushButton(u"断开自定义连接")
        theme.style_danger(self.break_custom_button)

        self.copy_connection_button = QPushButton(
            QIcon(icon_dir + "/copy.png"),
            u"复制输入连接"
        )

        self.break_selected_input_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            u"断开所选属性输入"
        )
        theme.style_danger(self.break_selected_input_button)

        self.status_label = QLabel(u"准备就绪")
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        u"""
        创建界面布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        default_card, default_layout = theme.make_card(self)
        default_layout.addWidget(
            theme.make_section_title(u"Transform 连接")
        )

        default_option_layout = QHBoxLayout()
        default_option_layout.setContentsMargins(0, 0, 0, 0)
        default_option_layout.addWidget(self.translate_checkbox)
        default_option_layout.addWidget(self.rotate_checkbox)
        default_option_layout.addWidget(self.scale_checkbox)
        default_option_layout.addWidget(self.matrix_checkbox)
        default_option_layout.addStretch(1)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        default_option_layout.addWidget(self.reset_default_button)
        default_layout.addLayout(default_option_layout)

        default_action_layout = QHBoxLayout()
        default_action_layout.setContentsMargins(0, 0, 0, 0)
        default_action_layout.addWidget(self.break_default_button)
        default_action_layout.addStretch(1)
        default_action_layout.addWidget(self.connect_default_button)
        default_layout.addLayout(default_action_layout)

        custom_card, custom_layout = theme.make_card(self)
        custom_layout.addWidget(
            theme.make_section_title(u"自定义属性")
        )

        custom_grid = QGridLayout()
        custom_grid.setHorizontalSpacing(8)
        custom_grid.setVerticalSpacing(8)
        custom_grid.addWidget(QLabel(u"Driver"), 0, 0)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        custom_grid.addWidget(self.driver_line, 0, 1)
        custom_grid.addWidget(self.pick_driver_button, 0, 2)
        custom_grid.addWidget(QLabel(u"Driven"), 1, 0)
        custom_grid.addWidget(self.driven_line, 1, 1)
        custom_grid.addWidget(self.pick_driven_button, 1, 2)
        custom_grid.setColumnStretch(1, 1)
        custom_layout.addLayout(custom_grid)

        custom_action_layout = QHBoxLayout()
        custom_action_layout.setContentsMargins(0, 0, 0, 0)
        custom_action_layout.addWidget(self.break_custom_button)
        custom_action_layout.addStretch(1)
        custom_action_layout.addWidget(self.connect_custom_button)
        custom_layout.addLayout(custom_action_layout)

        existing_card, existing_layout = theme.make_card(self)
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        existing_layout.addWidget(
            theme.make_section_title(u"已有连接")
        )

        existing_info = QLabel(
            u"复制：第一个对象是来源，其余对象是目标；"
            u"断开：对当前对象 Channel Box 中选中的属性执行。"
        )
        existing_info.setWordWrap(True)
        theme.set_role(existing_info, "muted")
        existing_layout.addWidget(existing_info)

        existing_action_layout = QHBoxLayout()
        existing_action_layout.setContentsMargins(0, 0, 0, 0)
        existing_action_layout.addWidget(self.copy_connection_button)
        existing_action_layout.addWidget(self.break_selected_input_button)
        existing_layout.addLayout(existing_action_layout)

        main_layout.addWidget(default_card)
        main_layout.addWidget(custom_card)
        main_layout.addWidget(existing_card)
        main_layout.addWidget(self.status_label)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接界面信号。
        """
        self.matrix_checkbox.stateChanged.connect(
            self.changed_matrix_checkbox
        )
        self.translate_checkbox.stateChanged.connect(
            self.changed_transform_checkbox
        )
        self.rotate_checkbox.stateChanged.connect(
            self.changed_transform_checkbox
        )
        self.scale_checkbox.stateChanged.connect(
            self.changed_transform_checkbox
        )
        self.reset_default_button.clicked.connect(
            self.reset_default_options
        )
        self.connect_default_button.clicked.connect(
            self.connect_default_attrs
        )
        self.break_default_button.clicked.connect(
            self.break_default_attrs
        )
        self.pick_driver_button.clicked.connect(
            self.pick_driver_attr
        )
        self.pick_driven_button.clicked.connect(
            self.pick_driven_attrs
        )
        self.connect_custom_button.clicked.connect(
            self.connect_custom_attrs
        )
        self.break_custom_button.clicked.connect(
            self.break_custom_attrs
        )
        self.copy_connection_button.clicked.connect(
            self.copy_input_connections
        )
        self.break_selected_input_button.clicked.connect(
            self.break_selected_inputs
        )

    def changed_matrix_checkbox(self):
        u"""
        Matrix 和普通 SRT 连接互斥。
        """
        if not self.matrix_checkbox.isChecked():
            return

        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)

    def changed_transform_checkbox(self):
        u"""
        普通 SRT 被勾选时取消 Matrix。
        """
        checked = False

        if self.translate_checkbox.isChecked():
            checked = True
        if self.rotate_checkbox.isChecked():
            checked = True
        if self.scale_checkbox.isChecked():
            checked = True

        if checked:
            self.matrix_checkbox.setChecked(False)

    def reset_default_options(self):
        u"""
        重置 Transform 连接选项。
        """
        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)
        self.matrix_checkbox.setChecked(False)

    def get_default_attr_pairs(self):
        u"""

                返回当前勾选的默认属性映射。

                Returns:
                    object:
                        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        """
        attribute_pairs = []

        if self.translate_checkbox.isChecked():
            attribute_pairs.append(("translate", "translate"))
        if self.rotate_checkbox.isChecked():
            attribute_pairs.append(("rotate", "rotate"))
        if self.scale_checkbox.isChecked():
            attribute_pairs.append(("scale", "scale"))
        if self.matrix_checkbox.isChecked():
            attribute_pairs.append(("matrix", "offsetParentMatrix"))

        return attribute_pairs

    def connect_default_attrs(self):
        u"""
        第一个选择驱动其余选择。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        attribute_pairs = self.get_default_attr_pairs()

        if not attribute_pairs:
            cmds.warning(
                u"请先选择需要连接的属性类型。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        selected_objects = get_selected_objects(2)

        if not selected_objects:
            return

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        plug_pairs = build_attribute_plug_pairs(
            selected_objects[0],
            selected_objects[1:],
            attribute_pairs
        )

        scene_utils.open_undo_chunk(
            "MuziConnectDefaultAttrs"
        )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            created_count = connection_utils.connect_plug_pairs(
                plug_pairs,
                force=False
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已创建 {} 条连接".format(
                created_count
            )
        )

    def break_default_attrs(self):
        u"""
        断开选择对象对应的默认属性连接。
        """
        attribute_pairs = self.get_default_attr_pairs()

        if not attribute_pairs:
            cmds.warning(
                u"请先选择需要断开的属性类型。"
            )
            return

        selected_objects = get_selected_objects(2)

        if not selected_objects:
            return

        plug_pairs = build_attribute_plug_pairs(
            selected_objects[0],
            selected_objects[1:],
            attribute_pairs
        )

        scene_utils.open_undo_chunk(
            "MuziBreakDefaultAttrs"
        )

        try:
            disconnected_count = connection_utils.disconnect_plug_pairs(
                plug_pairs
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        self.status_label.setText(
            u"已断开 {} 条连接".format(
                disconnected_count
            )
        )

    def pick_driver_attr(self):
        u"""
        拾取唯一 Driver Object + Channel Box Attr。
        """
        selected_objects = get_selected_objects(1)
        attribute_names = get_channel_box_attrs()

        if len(selected_objects) != 1:
            cmds.warning(
                u"拾取 Driver 时请只选择一个对象。"
            )
            return

        if len(attribute_names) != 1:
            cmds.warning(
                u"拾取 Driver 时请只选择一个 Channel Box 属性。"
            )
            return

        self.driver_plug = "{}.{}".format(
            selected_objects[0],
            attribute_names[0]
        )
        self.driver_line.setText(
            self.driver_plug
        )

    def pick_driven_attrs(self):
        u"""
        记录 Driven Channel Box 属性名。
        """
        attribute_names = get_channel_box_attrs()

        if not attribute_names:
            return

        self.driven_attr_names = []

        for attribute_name in attribute_names:
            self.driven_attr_names.append(
                attribute_name
            )

        self.driven_line.setText(
            ", ".join(self.driven_attr_names)
        )

    def connect_custom_attrs(self):
        u"""
        把 Driver Plug 连接到当前选择对象的 Driven Attr。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.driver_plug:
            cmds.warning(
                u"请先拾取 Driver 属性。"
            )
            return

        if not self.driven_attr_names:
            cmds.warning(
                u"请先拾取 Driven 属性。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        driven_objects = get_selected_objects(1)

        if not driven_objects:
            return

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        plug_pairs = build_source_plug_pairs(
            self.driver_plug,
            driven_objects,
            self.driven_attr_names
        )

        scene_utils.open_undo_chunk(
            "MuziConnectCustomAttrs"
        )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            created_count = connection_utils.connect_plug_pairs(
                plug_pairs,
                force=False
            )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已创建 {} 条自定义连接".format(
                created_count
            )
        )

    def break_custom_attrs(self):
        u"""
        断开当前选择对象对应的自定义属性输入。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.driven_attr_names:
            cmds.warning(
                u"请先拾取 Driven 属性。"
            )
            return

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        driven_objects = get_selected_objects(1)

        if not driven_objects:
            return

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        disconnected_count = 0
        scene_utils.open_undo_chunk(
            "MuziBreakCustomAttrs"
        )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            for driven_object in driven_objects:
                for attribute_name in self.driven_attr_names:
                    destination_plug = "{}.{}".format(
                        driven_object,
                        attribute_name
                    )
                    disconnected_count += connection_utils.disconnect_input(
                        destination_plug
                    )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已断开 {} 条自定义连接".format(
                disconnected_count
            )
        )

    def copy_input_connections(self):
        u"""
        复制来源对象 Channel Box 选中属性的输入连接。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        selected_objects = get_selected_objects(2)
        attribute_names = get_channel_box_attrs()

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not selected_objects or not attribute_names:
            return

        source_object = selected_objects[0]
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        target_objects = selected_objects[1:]
        copied_count = 0

        # -------------------------------------------------------------------------
        # Step 04：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        scene_utils.open_undo_chunk(
            "MuziCopyInputConnections"
        )

        try:
            for attribute_name in attribute_names:
                source_destination_plug = "{}.{}".format(
                    source_object,
                    attribute_name
                )
                input_plugs = connection_utils.get_input_connections(
                    source_destination_plug
                )

                if not input_plugs:
                    continue

                source_plug = input_plugs[0]

                for target_object in target_objects:
                    target_plug = "{}.{}".format(
                        target_object,
                        attribute_name
                    )

                    if connection_utils.connect_plugs(
                            source_plug,
                            target_plug,
                            force=True
                    ):
                        copied_count += 1
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已复制 {} 条输入连接".format(
                copied_count
            )
        )

    def break_selected_inputs(self):
        u"""
        断开当前选择对象 Channel Box 属性的输入。
        """
        selected_objects = get_selected_objects(1)
        attribute_names = get_channel_box_attrs()

        if not selected_objects or not attribute_names:
            return

        disconnected_count = 0
        scene_utils.open_undo_chunk(
            "MuziBreakSelectedInputs"
        )

        try:
            for selected_object in selected_objects:
                for attribute_name in attribute_names:
                    destination_plug = "{}.{}".format(
                        selected_object,
                        attribute_name
                    )
                    disconnected_count += connection_utils.disconnect_input(
                        destination_plug
                    )
        except Exception as error:
            cmds.warning(
                str(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        self.status_label.setText(
            u"已断开 {} 条输入连接".format(
                disconnected_count
            )
        )


def main():
    u"""

        创建或恢复 Connections Tool，立即显示并返回 QWidget。

        Returns:
            object:
                当前工具入口创建并显示的窗口或执行结果。

    """
    return window_utils.show_window(
        "tools.basic.connections_tool",
        ConnectionsTool
    )


__all__ = [
    "ConnectionsTool",
    "main",
]
