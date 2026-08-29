# coding=utf-8
u"""
属性连接工具
============

功能：
    1. 批量连接 Translate / Rotate / Scale / Matrix
    2. 批量断开 Translate / Rotate / Scale / Matrix
    3. 从 Maya Channel Box 读取驱动属性和被驱动属性
    4. 创建 / 断开自定义属性连接
    5. 复制一个物体已有的输入连接到其它物体
    6. 断开 Channel Box 中选中属性的输入连接

说明：
    - Maya 2023 优先使用 PySide2。
    - 场景操作统一使用 maya.cmds，不依赖 pymel。
    - main() 只创建并返回 QWidget，窗口生命周期由 window_manager 管理。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...config import icon_dir
from ....core import attrUtils


class ConnectionsTool(QWidget):
    """Maya 属性连接工具窗口。"""

    def __init__(self, parent=None):
        super(ConnectionsTool, self).__init__(parent)

        self.window_name = "ConnectionsTool"
        self.window_title = u"Connections Tool（连接工具）"

        self.setWindowTitle(self.window_title)
        self.setMinimumWidth(460)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    # -------------------------------------------------------------------------
    # 创建界面
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建所有界面部件。"""

        # 默认 Transform 属性连接。
        self.default_connection_label = QLabel(
            u"--------------- 连接默认属性 ---------------"
        )
        self.default_connection_label.setStyleSheet(
            u"color: rgb(169, 255, 175);"
        )

        self.translate_checkbox = QCheckBox("Translate")
        self.rotate_checkbox = QCheckBox("Rotate")
        self.scale_checkbox = QCheckBox("Scale")
        self.matrix_checkbox = QCheckBox("Matrix")

        self.reset_default_button = QPushButton(
            QIcon(icon_dir + "/reset.png"),
            "Reset"
        )
        self.reset_default_button.setToolTip(u"清空默认属性连接选项")

        self.connect_default_button = QPushButton(
            QIcon(":parentConstraint.png"),
            "Create SRT Connection"
        )
        self.connect_default_button.setToolTip(
            u"第一个选择物体作为驱动者，其余选择物体作为被驱动者"
        )

        self.break_default_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            "Break SRT Connection"
        )
        self.break_default_button.setToolTip(u"断开当前选择的默认属性连接")

        # 自定义属性连接。
        self.custom_connection_label = QLabel(
            u"--------------- 连接自定义属性 ---------------"
        )
        self.custom_connection_label.setStyleSheet(
            u"color: rgb(85, 255, 255);"
        )

        self.driver_attr_label = QLabel(u"Driver（驱动者）：")
        self.driver_attr_line = QLineEdit()
        self.driver_attr_line.setReadOnly(True)

        self.pick_driver_attr_button = QPushButton(
            QIcon(icon_dir + "/select.png"),
            "Pick"
        )
        self.pick_driver_attr_button.setToolTip(
            u"选择一个物体，并在 Channel Box 中选择一个驱动属性"
        )

        self.driven_attr_label = QLabel(u"Driven（被驱动者）：")
        self.driven_attr_line = QLineEdit()
        self.driven_attr_line.setReadOnly(True)

        self.pick_driven_attr_button = QPushButton(
            QIcon(icon_dir + "/select.png"),
            "Pick"
        )
        self.pick_driven_attr_button.setToolTip(
            u"选择一个或多个物体，并在 Channel Box 中选择被驱动属性"
        )

        self.connect_custom_button = QPushButton(
            QIcon(":parentConstraint.png"),
            "Create Connection"
        )
        self.connect_custom_button.setToolTip(u"创建自定义属性连接")

        self.break_custom_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            "Break Connection"
        )
        self.break_custom_button.setToolTip(u"断开自定义属性连接")

        # 复制 / 删除已有连接。
        self.copy_break_connection_label = QLabel(
            u"--------------- 复制 / 删除属性连接 ---------------"
        )
        self.copy_break_connection_label.setStyleSheet(
            u"color: rgb(170, 255, 128);"
        )

        self.copy_connection_button = QPushButton(
            QIcon(icon_dir + "/copy.png"),
            "Copy Driven Connection"
        )
        self.copy_connection_button.setToolTip(
            u"第一个选择物体作为来源，把 Channel Box 中属性的输入连接复制给其余物体"
        )

        self.break_connection_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            "Break Driven Connection"
        )
        self.break_connection_button.setToolTip(
            u"断开所选物体 Channel Box 选中属性的输入连接"
        )

    def create_layouts(self):
        """创建窗口布局。"""

        # 默认连接区域。
        self.default_attr_layout = QHBoxLayout()
        self.default_attr_layout.addWidget(self.translate_checkbox)
        self.default_attr_layout.addWidget(self.rotate_checkbox)
        self.default_attr_layout.addWidget(self.scale_checkbox)
        self.default_attr_layout.addWidget(self.matrix_checkbox)
        self.default_attr_layout.addWidget(self.reset_default_button)

        self.default_operate_layout = QHBoxLayout()
        self.default_operate_layout.addWidget(self.connect_default_button)
        self.default_operate_layout.addWidget(self.break_default_button)

        self.default_connection_layout = QVBoxLayout()
        self.default_connection_layout.addLayout(self.default_attr_layout)
        self.default_connection_layout.addLayout(self.default_operate_layout)

        # 自定义连接区域。
        self.driver_attr_layout = QHBoxLayout()
        self.driver_attr_layout.addWidget(self.driver_attr_label)
        self.driver_attr_layout.addWidget(self.driver_attr_line)
        self.driver_attr_layout.addWidget(self.pick_driver_attr_button)

        self.driven_attr_layout = QHBoxLayout()
        self.driven_attr_layout.addWidget(self.driven_attr_label)
        self.driven_attr_layout.addWidget(self.driven_attr_line)
        self.driven_attr_layout.addWidget(self.pick_driven_attr_button)

        self.custom_operate_layout = QHBoxLayout()
        self.custom_operate_layout.addWidget(self.connect_custom_button)
        self.custom_operate_layout.addWidget(self.break_custom_button)

        self.custom_connection_layout = QVBoxLayout()
        self.custom_connection_layout.addLayout(self.driver_attr_layout)
        self.custom_connection_layout.addLayout(self.driven_attr_layout)
        self.custom_connection_layout.addLayout(self.custom_operate_layout)

        # 复制 / 删除连接区域。
        self.copy_break_connection_layout = QHBoxLayout()
        self.copy_break_connection_layout.addWidget(self.copy_connection_button)
        self.copy_break_connection_layout.addWidget(self.break_connection_button)

        # 主布局。
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.default_connection_label)
        self.main_layout.addLayout(self.default_connection_layout)
        self.main_layout.addStretch()

        self.main_layout.addWidget(self.custom_connection_label)
        self.main_layout.addLayout(self.custom_connection_layout)
        self.main_layout.addStretch()

        self.main_layout.addWidget(self.copy_break_connection_label)
        self.main_layout.addLayout(self.copy_break_connection_layout)
        self.main_layout.addStretch()

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
            self.clicked_reset_default_button
        )
        self.connect_default_button.clicked.connect(
            self.clicked_connect_default_button
        )
        self.break_default_button.clicked.connect(
            self.clicked_break_default_button
        )

        self.pick_driver_attr_button.clicked.connect(
            self.clicked_pick_driver_attr_button
        )
        self.pick_driven_attr_button.clicked.connect(
            self.clicked_pick_driven_attr_button
        )
        self.connect_custom_button.clicked.connect(
            self.clicked_connect_custom_button
        )
        self.break_custom_button.clicked.connect(
            self.clicked_break_custom_button
        )

        self.copy_connection_button.clicked.connect(
            self.clicked_copy_connection_button
        )
        self.break_connection_button.clicked.connect(
            self.clicked_break_connection_button
        )

    # -------------------------------------------------------------------------
    # 通用检查
    # -------------------------------------------------------------------------

    def get_selected_objects(self, minimum_count=1):
        """读取 Maya 当前选择，并检查最少数量。"""

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

    def get_selected_channel_attrs(self):
        """读取 Maya Channel Box 当前选中的属性。"""

        selected_attrs = attrUtils.Attr.get_channelBox_attrs()

        if selected_attrs is None:
            selected_attrs = []

        if not selected_attrs:
            cmds.warning(u"请先在 Channel Box 中选择属性。")
            return []

        return selected_attrs

    def get_default_attr_pairs(self):
        """根据复选框状态生成需要连接的属性对。"""

        attr_pairs = []

        if self.translate_checkbox.isChecked():
            attr_pairs.append(("translate", "translate"))

        if self.rotate_checkbox.isChecked():
            attr_pairs.append(("rotate", "rotate"))

        if self.scale_checkbox.isChecked():
            attr_pairs.append(("scale", "scale"))

        if self.matrix_checkbox.isChecked():
            # 保留旧工具原本的连接方式：
            # driver.matrix -> driven.offsetParentMatrix。
            attr_pairs.append(("matrix", "offsetParentMatrix"))

        return attr_pairs

    def connect_plugs(self, source_plug, destination_plug, force=False):
        """安全地连接两个完整属性 plug。"""

        if not cmds.objExists(source_plug):
            cmds.warning(u"驱动属性不存在：{}".format(source_plug))
            return False

        if not cmds.objExists(destination_plug):
            cmds.warning(u"被驱动属性不存在：{}".format(destination_plug))
            return False

        if cmds.isConnected(source_plug, destination_plug):
            return True

        input_connections = cmds.listConnections(
            destination_plug,
            source=True,
            destination=False,
            plugs=True
        )

        if input_connections and not force:
            cmds.warning(
                u"被驱动属性已经存在输入连接：{}".format(destination_plug)
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

    def disconnect_plugs(self, source_plug, destination_plug):
        """安全地断开指定的两个完整属性 plug。"""

        if not cmds.objExists(source_plug):
            return False

        if not cmds.objExists(destination_plug):
            return False

        if not cmds.isConnected(source_plug, destination_plug):
            return False

        try:
            cmds.disconnectAttr(
                source_plug,
                destination_plug
            )
        except RuntimeError as error:
            cmds.warning(str(error))
            return False

        return True

    # -------------------------------------------------------------------------
    # 默认 Transform 属性连接
    # -------------------------------------------------------------------------

    def changed_matrix_checkbox(self):
        """选择 Matrix 时，取消 Translate / Rotate / Scale。"""

        if not self.matrix_checkbox.isChecked():
            return

        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)

    def changed_transform_checkbox(self):
        """选择普通 Transform 属性时，取消 Matrix。"""

        transform_checked = False

        if self.translate_checkbox.isChecked():
            transform_checked = True

        if self.rotate_checkbox.isChecked():
            transform_checked = True

        if self.scale_checkbox.isChecked():
            transform_checked = True

        if transform_checked:
            self.matrix_checkbox.setChecked(False)

    def clicked_reset_default_button(self):
        """清空所有默认属性选项。"""

        self.translate_checkbox.setChecked(False)
        self.rotate_checkbox.setChecked(False)
        self.scale_checkbox.setChecked(False)
        self.matrix_checkbox.setChecked(False)

    def clicked_connect_default_button(self):
        """连接第一个选择物体到其余选择物体。"""

        attr_pairs = self.get_default_attr_pairs()

        if not attr_pairs:
            cmds.warning(u"没有选择需要连接的默认属性。")
            return

        selected_objects = self.get_selected_objects(minimum_count=2)

        if not selected_objects:
            return

        driver_object = selected_objects[0]
        driven_objects = selected_objects[1:]

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolCreateDefault"
        )

        try:
            for driven_object in driven_objects:
                for source_attr, destination_attr in attr_pairs:
                    source_plug = "{}.{}".format(
                        driver_object,
                        source_attr
                    )
                    destination_plug = "{}.{}".format(
                        driven_object,
                        destination_attr
                    )

                    self.connect_plugs(
                        source_plug,
                        destination_plug,
                        force=False
                    )
        finally:
            cmds.undoInfo(closeChunk=True)

    def clicked_break_default_button(self):
        """断开第一个选择物体到其余选择物体的指定连接。"""

        attr_pairs = self.get_default_attr_pairs()

        if not attr_pairs:
            cmds.warning(u"没有选择需要断开的默认属性。")
            return

        selected_objects = self.get_selected_objects(minimum_count=2)

        if not selected_objects:
            return

        driver_object = selected_objects[0]
        driven_objects = selected_objects[1:]

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolBreakDefault"
        )

        try:
            for driven_object in driven_objects:
                for source_attr, destination_attr in attr_pairs:
                    source_plug = "{}.{}".format(
                        driver_object,
                        source_attr
                    )
                    destination_plug = "{}.{}".format(
                        driven_object,
                        destination_attr
                    )

                    self.disconnect_plugs(
                        source_plug,
                        destination_plug
                    )
        finally:
            cmds.undoInfo(closeChunk=True)

    # -------------------------------------------------------------------------
    # 自定义属性连接
    # -------------------------------------------------------------------------

    def clicked_pick_driver_attr_button(self):
        """读取一个驱动物体和一个 Channel Box 属性。"""

        selected_objects = self.get_selected_objects(minimum_count=1)

        if not selected_objects:
            return

        selected_attrs = self.get_selected_channel_attrs()

        if not selected_attrs:
            return

        driver_object = selected_objects[0]
        driver_attr = selected_attrs[0]
        driver_plug = "{}.{}".format(
            driver_object,
            driver_attr
        )

        self.driver_attr_line.setText(driver_plug)

    def clicked_pick_driven_attr_button(self):
        """读取一个或多个被驱动物体及 Channel Box 属性。"""

        selected_objects = self.get_selected_objects(minimum_count=1)

        if not selected_objects:
            return

        selected_attrs = self.get_selected_channel_attrs()

        if not selected_attrs:
            return

        driven_plugs = []

        for driven_object in selected_objects:
            for driven_attr in selected_attrs:
                driven_plug = "{}.{}".format(
                    driven_object,
                    driven_attr
                )

                if not cmds.objExists(driven_plug):
                    continue

                driven_plugs.append(driven_plug)

        if not driven_plugs:
            cmds.warning(u"没有找到可以加载的被驱动属性。")
            return

        driven_text = ", ".join(driven_plugs)
        self.driven_attr_line.setText(driven_text)

    def get_custom_connection_data(self):
        """检查并返回自定义连接输入框中的完整属性。"""

        source_plug = self.driver_attr_line.text().strip()
        destination_text = self.driven_attr_line.text().strip()

        if not source_plug:
            cmds.warning(u"未加载驱动属性。")
            return None, []

        if not destination_text:
            cmds.warning(u"未加载被驱动属性。")
            return None, []

        if not cmds.objExists(source_plug):
            cmds.warning(u"驱动属性不存在：{}".format(source_plug))
            return None, []

        destination_plugs = []
        destination_items = destination_text.split(",")

        for destination_item in destination_items:
            destination_plug = destination_item.strip()

            if not destination_plug:
                continue

            if not cmds.objExists(destination_plug):
                cmds.warning(
                    u"被驱动属性不存在：{}".format(destination_plug)
                )
                continue

            destination_plugs.append(destination_plug)

        if not destination_plugs:
            cmds.warning(u"没有有效的被驱动属性。")
            return None, []

        return source_plug, destination_plugs

    def clicked_connect_custom_button(self):
        """创建自定义属性连接。"""

        source_plug, destination_plugs = self.get_custom_connection_data()

        if source_plug is None:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolCreateCustom"
        )

        try:
            for destination_plug in destination_plugs:
                self.connect_plugs(
                    source_plug,
                    destination_plug,
                    force=False
                )
        finally:
            cmds.undoInfo(closeChunk=True)

    def clicked_break_custom_button(self):
        """断开自定义属性连接。"""

        source_plug, destination_plugs = self.get_custom_connection_data()

        if source_plug is None:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolBreakCustom"
        )

        try:
            for destination_plug in destination_plugs:
                self.disconnect_plugs(
                    source_plug,
                    destination_plug
                )
        finally:
            cmds.undoInfo(closeChunk=True)

    # -------------------------------------------------------------------------
    # 复制 / 删除已有输入连接
    # -------------------------------------------------------------------------

    def clicked_copy_connection_button(self):
        """
        把第一个选择物体指定属性的输入连接复制给其它选择物体。

        例如：
            multiplyDivide1.outputX -> ctrl_a.customAttr

        选择 ctrl_a、ctrl_b、ctrl_c，并在 Channel Box 选择 customAttr，
        执行后会把同一个上游输出连接到 ctrl_b.customAttr 和 ctrl_c.customAttr。
        """

        selected_objects = self.get_selected_objects(minimum_count=2)

        if not selected_objects:
            return

        selected_attrs = self.get_selected_channel_attrs()

        if not selected_attrs:
            return

        source_object = selected_objects[0]
        target_objects = selected_objects[1:]

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolCopyDriven"
        )

        try:
            for selected_attr in selected_attrs:
                source_destination_plug = "{}.{}".format(
                    source_object,
                    selected_attr
                )

                if not cmds.objExists(source_destination_plug):
                    continue

                input_connections = cmds.listConnections(
                    source_destination_plug,
                    source=True,
                    destination=False,
                    plugs=True
                )

                if not input_connections:
                    cmds.warning(
                        u"属性没有输入连接：{}".format(
                            source_destination_plug
                        )
                    )
                    continue

                source_plug = input_connections[0]

                for target_object in target_objects:
                    target_plug = "{}.{}".format(
                        target_object,
                        selected_attr
                    )

                    self.connect_plugs(
                        source_plug,
                        target_plug,
                        force=False
                    )
        finally:
            cmds.undoInfo(closeChunk=True)

    def clicked_break_connection_button(self):
        """断开所选物体 Channel Box 选中属性的全部输入连接。"""

        selected_objects = self.get_selected_objects(minimum_count=1)

        if not selected_objects:
            return

        selected_attrs = self.get_selected_channel_attrs()

        if not selected_attrs:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziConnectionsToolBreakDriven"
        )

        try:
            for selected_object in selected_objects:
                for selected_attr in selected_attrs:
                    destination_plug = "{}.{}".format(
                        selected_object,
                        selected_attr
                    )

                    if not cmds.objExists(destination_plug):
                        continue

                    input_connections = cmds.listConnections(
                        destination_plug,
                        source=True,
                        destination=False,
                        plugs=True
                    )

                    if not input_connections:
                        continue

                    for source_plug in input_connections:
                        self.disconnect_plugs(
                            source_plug,
                            destination_plug
                        )
        finally:
            cmds.undoInfo(closeChunk=True)


# 保留旧类名，避免历史代码在迁移期间失效。
Connections_Tool = ConnectionsTool


def main():
    """创建连接工具并返回 QWidget。"""
    window = ConnectionsTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
