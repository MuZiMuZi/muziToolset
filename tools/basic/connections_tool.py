# coding=utf-8
u"""
Connections Tool
================

Maya 属性连接工具。

功能：
    1. Translate / Rotate / Scale / Matrix 批量连接与断开；
    2. 从 Channel Box 拾取 Driver / Driven 属性；
    3. 创建和断开自定义属性连接；
    4. 复制一个对象已有的输入连接到其它对象；
    5. 断开 Channel Box 选中属性的输入连接。
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
from ...core import attrUtils
from ...ui import theme


def get_selected_objects(minimum_count=1):
    """返回当前选择，并校验最少数量。"""
    selected_objects = cmds.ls(
        selection=True,
        long=True
    )

    if selected_objects is None:
        selected_objects = []

    if len(selected_objects) < minimum_count:
        cmds.warning(
            u"请至少选择 {} 个物体。".format(minimum_count)
        )
        return []

    return selected_objects


def get_channel_box_attrs():
    """返回 Maya Channel Box 当前选中的属性。"""
    attrs = attrUtils.Attr.get_channelBox_attrs()

    if attrs is None:
        attrs = []

    if not attrs:
        cmds.warning(u"请先在 Channel Box 中选择属性。")

    return attrs


def connect_plugs(source_plug, destination_plug, force=False):
    """安全连接两个完整 Plug。"""
    if not cmds.objExists(source_plug):
        cmds.warning(u"驱动属性不存在：{}".format(source_plug))
        return False

    if not cmds.objExists(destination_plug):
        cmds.warning(u"被驱动属性不存在：{}".format(destination_plug))
        return False

    if cmds.isConnected(source_plug, destination_plug):
        return True

    existing_inputs = cmds.listConnections(
        destination_plug,
        source=True,
        destination=False,
        plugs=True
    )

    if existing_inputs and not force:
        cmds.warning(
            u"被驱动属性已有输入连接：{}".format(destination_plug)
        )
        return False

    try:
        cmds.connectAttr(
            source_plug,
            destination_plug,
            force=force
        )
    except RuntimeError as error:
        cmds.warning(str(error))
        return False

    return True


def disconnect_input(destination_plug):
    """断开指定 Plug 的全部输入连接。"""
    inputs = cmds.listConnections(
        destination_plug,
        source=True,
        destination=False,
        plugs=True,
        connections=True
    )

    if inputs is None:
        inputs = []

    disconnected_count = 0
    index = 0

    while index + 1 < len(inputs):
        destination = inputs[index]
        source = inputs[index + 1]

        if cmds.isConnected(source, destination):
            try:
                cmds.disconnectAttr(
                    source,
                    destination
                )
                disconnected_count += 1
            except RuntimeError:
                pass

        index += 2

    return disconnected_count


class ConnectionsTool(QWidget):
    """属性连接工具窗口。"""

    def __init__(self, parent=None):
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
        """创建界面控件。"""
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
        self.driver_line.setPlaceholderText(u"Driver Plug")
        self.pick_driver_button = QPushButton(u"拾取 Driver")

        self.driven_line = QLineEdit()
        self.driven_line.setReadOnly(True)
        self.driven_line.setPlaceholderText(u"Driven Attribute")
        self.pick_driven_button = QPushButton(u"拾取 Driven")

        self.connect_custom_button = QPushButton(u"创建自定义连接")
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
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建 Card 布局。"""
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
        main_layout.addStretch(1)

    def create_connections(self):
        """连接界面信号。"""
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
        """Matrix 和普通 SRT 连接互斥。"""
        if not self.matrix_checkbox.isChecked():
            return

        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)

    def changed_transform_checkbox(self):
        """普通 SRT 被勾选时取消 Matrix。"""
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
        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)
        self.matrix_checkbox.setChecked(False)

    def get_default_attr_pairs(self):
        """返回当前勾选的默认属性映射。"""
        pairs = []

        if self.translate_checkbox.isChecked():
            pairs.append(("translate", "translate"))
        if self.rotate_checkbox.isChecked():
            pairs.append(("rotate", "rotate"))
        if self.scale_checkbox.isChecked():
            pairs.append(("scale", "scale"))
        if self.matrix_checkbox.isChecked():
            pairs.append(("matrix", "offsetParentMatrix"))

        return pairs

    def connect_default_attrs(self):
        """第一个选择驱动其余选择。"""
        pairs = self.get_default_attr_pairs()

        if not pairs:
            cmds.warning(u"请先选择需要连接的属性类型。")
            return

        selected_objects = get_selected_objects(2)

        if not selected_objects:
            return

        driver = selected_objects[0]
        driven_objects = selected_objects[1:]
        created_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectDefaultAttrs"
        )

        try:
            for driven in driven_objects:
                for source_attr, destination_attr in pairs:
                    source_plug = "{}.{}".format(driver, source_attr)
                    destination_plug = "{}.{}".format(
                        driven,
                        destination_attr
                    )

                    if connect_plugs(
                            source_plug,
                            destination_plug,
                            force=False
                    ):
                        created_count += 1
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已创建 {} 条连接".format(created_count)
        )

    def break_default_attrs(self):
        """断开选择对象对应的默认属性连接。"""
        pairs = self.get_default_attr_pairs()

        if not pairs:
            cmds.warning(u"请先选择需要断开的属性类型。")
            return

        selected_objects = get_selected_objects(2)

        if not selected_objects:
            return

        driver = selected_objects[0]
        driven_objects = selected_objects[1:]
        disconnected_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziBreakDefaultAttrs"
        )

        try:
            for driven in driven_objects:
                for source_attr, destination_attr in pairs:
                    source_plug = "{}.{}".format(driver, source_attr)
                    destination_plug = "{}.{}".format(
                        driven,
                        destination_attr
                    )

                    if not cmds.objExists(source_plug):
                        continue
                    if not cmds.objExists(destination_plug):
                        continue
                    if not cmds.isConnected(source_plug, destination_plug):
                        continue

                    cmds.disconnectAttr(
                        source_plug,
                        destination_plug
                    )
                    disconnected_count += 1
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已断开 {} 条连接".format(disconnected_count)
        )

    def pick_driver_attr(self):
        """拾取唯一 Driver Object + Channel Box Attr。"""
        selected_objects = get_selected_objects(1)
        attrs = get_channel_box_attrs()

        if len(selected_objects) != 1:
            cmds.warning(u"拾取 Driver 时请只选择一个对象。")
            return

        if len(attrs) != 1:
            cmds.warning(u"拾取 Driver 时请只选择一个 Channel Box 属性。")
            return

        self.driver_plug = "{}.{}".format(
            selected_objects[0],
            attrs[0]
        )
        self.driver_line.setText(self.driver_plug)

    def pick_driven_attrs(self):
        """记录 Driven Channel Box 属性名。"""
        attrs = get_channel_box_attrs()

        if not attrs:
            return

        self.driven_attr_names = []

        for attr in attrs:
            self.driven_attr_names.append(attr)

        self.driven_line.setText(
            ", ".join(self.driven_attr_names)
        )

    def connect_custom_attrs(self):
        """把 Driver Plug 连接到当前选择对象的 Driven Attr。"""
        if not self.driver_plug:
            cmds.warning(u"请先拾取 Driver 属性。")
            return

        if not self.driven_attr_names:
            cmds.warning(u"请先拾取 Driven 属性。")
            return

        driven_objects = get_selected_objects(1)

        if not driven_objects:
            return

        created_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectCustomAttrs"
        )

        try:
            for driven_object in driven_objects:
                for attr_name in self.driven_attr_names:
                    destination_plug = "{}.{}".format(
                        driven_object,
                        attr_name
                    )

                    if connect_plugs(
                            self.driver_plug,
                            destination_plug,
                            force=False
                    ):
                        created_count += 1
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已创建 {} 条自定义连接".format(created_count)
        )

    def break_custom_attrs(self):
        """断开当前选择对象对应的自定义属性输入。"""
        if not self.driven_attr_names:
            cmds.warning(u"请先拾取 Driven 属性。")
            return

        driven_objects = get_selected_objects(1)

        if not driven_objects:
            return

        count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziBreakCustomAttrs"
        )

        try:
            for driven_object in driven_objects:
                for attr_name in self.driven_attr_names:
                    destination_plug = "{}.{}".format(
                        driven_object,
                        attr_name
                    )
                    count += disconnect_input(destination_plug)
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已断开 {} 条自定义连接".format(count)
        )

    def copy_input_connections(self):
        """复制来源对象 Channel Box 选中属性的输入连接。"""
        selected_objects = get_selected_objects(2)
        attrs = get_channel_box_attrs()

        if not selected_objects or not attrs:
            return

        source_object = selected_objects[0]
        target_objects = selected_objects[1:]
        copied_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziCopyInputConnections"
        )

        try:
            for attr_name in attrs:
                source_destination_plug = "{}.{}".format(
                    source_object,
                    attr_name
                )

                source_inputs = cmds.listConnections(
                    source_destination_plug,
                    source=True,
                    destination=False,
                    plugs=True
                )

                if source_inputs is None:
                    source_inputs = []

                if not source_inputs:
                    continue

                source_input_plug = source_inputs[0]

                for target_object in target_objects:
                    target_plug = "{}.{}".format(
                        target_object,
                        attr_name
                    )

                    if connect_plugs(
                            source_input_plug,
                            target_plug,
                            force=True
                    ):
                        copied_count += 1
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已复制 {} 条输入连接".format(copied_count)
        )

    def break_selected_inputs(self):
        """断开当前选择对象 Channel Box 属性的输入。"""
        selected_objects = get_selected_objects(1)
        attrs = get_channel_box_attrs()

        if not selected_objects or not attrs:
            return

        disconnected_count = 0

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziBreakSelectedInputs"
        )

        try:
            for selected_object in selected_objects:
                for attr_name in attrs:
                    destination_plug = "{}.{}".format(
                        selected_object,
                        attr_name
                    )
                    disconnected_count += disconnect_input(
                        destination_plug
                    )
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"已断开 {} 条输入连接".format(disconnected_count)
        )


def main():
    """创建并返回 Connections Tool。"""
    window = ConnectionsTool()
    return window


__all__ = [
    "ConnectionsTool",
    "connect_plugs",
    "disconnect_input",
    "main",
]
