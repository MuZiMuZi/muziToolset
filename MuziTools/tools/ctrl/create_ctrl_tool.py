# -*- coding: utf-8 -*-
"""
create_ctrl.py
控制器创建工具（精简版）

功能：
- 从 controlUtils 的 tools/image 目录读取可用形状，以单选按钮展示（大图标，文字在下方）
- 创建新的控制器（可吸附到选中对象，支持多选批量创建、层级FK创建）
- 手动设置控制器颜色（颜色索引 0-31）
- 控制器大小、轴向、额外旋转 X 等参数可调

使用方法：
    import create_ctrl
    create_ctrl.main()
"""

from __future__ import print_function
import os

from past.builtins import reload


try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

try:
    from ....core import controlUtils
except ImportError:
    raise ImportError("无法导入 controlUtils，请确保模块在 Maya Python 路径中")

reload(controlUtils)
def get_maya_main_window () :
    """
    获取 Maya 的主窗口对象，作为工具的父窗口
    这样工具窗口就不会跑到 Maya 主窗口的后面去
    """
    # MQtUtil.mainWindow() 返回 Maya 主窗口的内存地址（长整型指针）
    ptr = omui.MQtUtil.mainWindow ()
    # 如果指针有效，用 wrapInstance 把它包装成 Python 的 QWidget 对象
    if ptr is not None :
        return wrapInstance (int (ptr) , QWidget)
    # 如果获取失败，返回 None（一般不会发生）
    return None



# Maya overrideColor 0-31 颜色表（RGB）
MAYA_COLORS = {
    0: (0.467, 0.467, 0.467), 1: (0.000, 0.000, 0.000),
    2: (0.200, 0.200, 0.200), 3: (0.600, 0.600, 0.600),
    4: (0.800, 0.000, 0.000), 5: (0.000, 0.000, 0.400),
    6: (0.000, 0.000, 1.000), 7: (0.000, 0.400, 0.000),
    8: (0.200, 0.000, 0.400), 9: (0.800, 0.400, 0.000),
    10: (0.600, 0.400, 0.200), 11: (0.400, 0.200, 0.000),
    12: (1.000, 1.000, 0.000), 13: (1.000, 0.000, 0.000),
    14: (0.000, 1.000, 0.000), 15: (0.000, 1.000, 1.000),
    16: (1.000, 1.000, 1.000), 17: (1.000, 1.000, 0.000),
    18: (0.000, 0.800, 1.000), 19: (1.000, 0.600, 0.800),
    20: (1.000, 0.400, 0.400), 21: (0.600, 1.000, 0.400),
    22: (1.000, 0.800, 0.400), 23: (0.400, 0.600, 1.000),
    24: (1.000, 1.000, 1.000), 25: (1.000, 1.000, 0.800),
    26: (0.800, 1.000, 0.800), 27: (0.800, 1.000, 1.000),
    28: (1.000, 0.800, 1.000), 29: (1.000, 0.600, 0.600),
    30: (0.800, 1.000, 0.600), 31: (0.600, 0.800, 1.000),
}


def custom_create_controller(name, shape, radius, axis, pos=None, parent=None, color=6):
    """
    完全自定义的控制器创建函数。
    不依赖 controlUtils.Control.create_ctrl / create_current_ctrl，
    避免其内部的名称解析错误和 add_extra_group 产生的 null 组。

    Args:
        name (str): 控制器名称，例如 "ctrl_l_arm_001"
        shape (str): 形状名称（对应 tools/image 下的 JSON 文件名）
        radius (float): 控制器大小
        axis (str): 轴向，'X+', 'X-', 'Y+', 'Y-', 'Z+', 'Z-'
        pos (str/None): 要吸附的目标物体，None 则留在原点
        parent (str/None): 父物体
        color (int): 颜色索引（0-31），默认 6（蓝色）
    Returns:
        str: 控制器 transform 名称
    """
    if cmds.objExists(name):
        raise ValueError("{} 已存在".format(name))

    # 颜色索引
    color = int(color)
    if color < 0:
        color = 0
    elif color > 31:
        color = 31
    sub_color = color + 1 if color < 31 else 31

    # ---------- 创建主控制器 ----------
    ctrl = controlUtils.Control(n=name, s=shape, r=radius)
    ctrl_transform = ctrl.get_transform().name()
    ctrl.set_color(c=color)

    # ---------- 设置轴向旋转 ----------
    mapping = {
        'X+': (90, 0, 0),
        'X-': (-90, 0, 0),
        'Y+': (0, 90, 0),
        'Y-': (0, -90, 0),
        'Z+': (0, 0, 90),
        'Z-': (0, 0, -90)
    }
    rx = ry = rz = 0
    if axis in mapping:
        rx, ry, rz = mapping[axis]
        ctrl.set_rotateX(rx=rx)
        ctrl.set_rotateY(ry=ry)
        ctrl.set_rotateZ(rz=rz)

    # ---------- 创建次级控制器 (Sub) ----------
    sub_name = name + "Sub"
    sub_ctrl = controlUtils.Control(n=sub_name, s=shape, r=radius * 0.7)
    sub_ctrl.set_parent(ctrl_transform)
    sub_ctrl.set_color(c=sub_color)
    sub_ctrl.set_rotateX(rx=rx)
    sub_ctrl.set_rotateY(ry=ry)
    sub_ctrl.set_rotateZ(rz=rz)

    # ---------- 手动创建层级组 ----------
    def replace_prefix(name, old, new):
        if old in name:
            return name.replace(old, new)
        return name + "_" + new

    offset_name = replace_prefix(name, "ctrl_", "offset_")
    connect_name = replace_prefix(name, "ctrl_", "connect_")
    space_name = replace_prefix(name, "ctrl_", "space_")
    driven_name = replace_prefix(name, "ctrl_", "driven_")
    zero_name = replace_prefix(name, "ctrl_", "zero_")

    offset_grp = cmds.createNode("transform", name=offset_name)
    connect_grp = cmds.createNode("transform", name=connect_name)
    space_grp = cmds.createNode("transform", name=space_name)
    driven_grp = cmds.createNode("transform", name=driven_name)
    zero_grp = cmds.createNode("transform", name=zero_name)

    cmds.parent(ctrl_transform, offset_grp)
    cmds.parent(offset_grp, connect_grp)
    cmds.parent(connect_grp, space_grp)
    cmds.parent(space_grp, driven_grp)
    cmds.parent(driven_grp, zero_grp)

    # ---------- 创建 output 节点 ----------
    output_name = replace_prefix(name, "ctrl_", "output_")
    output = cmds.createNode("transform", name=output_name, parent=ctrl_transform)

    sub_ctrl_transform = sub_ctrl.get_transform().name()
    cmds.connectAttr(sub_ctrl_transform + ".translate", output + ".translate")
    cmds.connectAttr(sub_ctrl_transform + ".rotate", output + ".rotate")
    cmds.connectAttr(sub_ctrl_transform + ".scale", output + ".scale")
    cmds.connectAttr(sub_ctrl_transform + ".rotateOrder", output + ".rotateOrder")

    if not cmds.attributeQuery("subCtrlVis", node=ctrl_transform, exists=True):
        cmds.addAttr(ctrl_transform, longName="subCtrlVis", attributeType="bool")
        cmds.setAttr(ctrl_transform + ".subCtrlVis", channelBox=True)
    cmds.connectAttr(ctrl_transform + ".subCtrlVis", sub_ctrl_transform + ".visibility")

    for attr in ["rotateOrder"]:
        cmds.setAttr(ctrl_transform + "." + attr, lock=True, keyable=False, channelBox=False)

    if pos:
        cmds.matchTransform(zero_grp, pos, position=True, rotation=True, scale=True)
    if parent:
        cmds.parent(zero_grp, parent)

    return ctrl_transform


class ControlButton(QToolButton):
    """形状选择按钮（单选），大图标在上，文字在下"""
    def __init__(self, shape_name, parent=None):
        super(ControlButton, self).__init__(parent)
        self.shape_name = shape_name
        self.setCheckable(True)
        self.setFixedSize(110, 90)
        self.setToolTip(shape_name)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(64, 64))

        self.setStyleSheet("""
            QToolButton {
                background-color: #2b2b2b;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                color: #aaaaaa;
                font-size: 10px;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: #353535;
                border: 2px solid #5a5a5a;
            }
            QToolButton:checked {
                background-color: #3a3a3a;
                border: 2px solid #00a8ff;
                color: #ffffff;
            }
        """)
        self._load_thumbnail()

    def _load_thumbnail(self):
        base_path = os.path.abspath(controlUtils.__file__ + "/../../tools/image")
        jpg_path = os.path.join(base_path, "{}.jpg".format(self.shape_name))
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        if os.path.exists(jpg_path):
            thumb = QPixmap(jpg_path)
            if not thumb.isNull():
                pixmap = thumb.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(pixmap))
        display = self.shape_name if len(self.shape_name) <= 12 else self.shape_name[:11] + "…"
        self.setText(display)


class ColorPreviewLabel(QLabel):
    """颜色预览方块"""
    def __init__(self, parent=None):
        super(ColorPreviewLabel, self).__init__(parent)
        self.setFixedSize(32, 32)
        self.setFrameShape(QFrame.StyledPanel)
        self._apply_color(6)

    def _apply_color(self, idx):
        rgb = MAYA_COLORS.get(idx, (0.5, 0.5, 0.5))
        r, g, b = int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
        self.setStyleSheet(
            "background-color: rgb({}, {}, {}); border: 2px solid #ffffff; border-radius: 4px;".format(r, g, b)
        )
        self.setToolTip("Color Index: {}".format(idx))

    def set_color(self, idx):
        self._apply_color(idx)


class ControlCreatorUI(QDialog):
    axis_list = ["X+", "X-", "Y+", "Y-", "Z+", "Z-"]

    def __init__(self, parent=get_maya_main_window()):
        super(ControlCreatorUI, self).__init__(parent)
        self.setWindowTitle("CONTROL CREATOR")
        self.setMinimumSize(500, 620)
        self.setWindowFlags(Qt.Window)

        self.current_shape = None
        self.shape_buttons = []

        #        # 依次调用三个方法，分别创建界面部件、布局、信号连接
        self.create_widgets ()      # 创建按钮、标签、复选框等 UI 部件
        self._load_shapes()     # 用布局管理器排列这些部件
        self.create_connections ()  # 把按钮的点击事件连接到对应的处理函数


    # -------------------------------------------------------------------------
    def create_widgets(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)


        # 形状滚动区
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; }")

        self.shapes_widget = QWidget()
        self.shapes_layout = QGridLayout(self.shapes_widget)
        self.shapes_layout.setSpacing(8)
        self.shapes_layout.setContentsMargins(4, 4, 4, 4)
        scroll.setWidget(self.shapes_widget)
        main_layout.addWidget(scroll, 1)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #3d3d3d;")
        main_layout.addWidget(line)

        # 参数区域
        params = QGridLayout()
        params.setSpacing(8)

        params.addWidget(QLabel("Scale:"), 0, 0)
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.01, 100.0)
        self.scale_spin.setValue(2.0)
        self.scale_spin.setSingleStep(0.5)
        self.scale_spin.setStyleSheet(self._spin_style())
        params.addWidget(self.scale_spin, 0, 1)

        params.addWidget(QLabel("Up Axis:"), 0, 2)
        self.axis_combo = QComboBox()
        self.axis_combo.addItems(self.axis_list)
        self.axis_combo.setCurrentText("Y+")
        self.axis_combo.setStyleSheet(self._combo_style())
        params.addWidget(self.axis_combo, 0, 3)

        params.addWidget(QLabel("Rotate X:"), 1, 0)
        self.rotate_x_spin = QDoubleSpinBox()
        self.rotate_x_spin.setRange(-360, 360)
        self.rotate_x_spin.setValue(0)
        self.rotate_x_spin.setStyleSheet(self._spin_style())
        params.addWidget(self.rotate_x_spin, 1, 1)

        params.addWidget(QLabel("Match:"), 1, 2)
        self.match_combo = QComboBox()
        self.match_combo.addItems(["Selection Only", "Hierarchy", "None"])
        self.match_combo.setStyleSheet(self._combo_style())
        params.addWidget(self.match_combo, 1, 3)

        main_layout.addLayout(params)

        # 颜色组（仅手动颜色）
        color_grp = QGroupBox("Color Override")
        color_grp.setStyleSheet("""
            QGroupBox {
                color: #aaaaaa;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
        """)
        cl = QHBoxLayout(color_grp)
        cl.setSpacing(10)

        self.color_slider = QSlider(Qt.Horizontal)
        self.color_slider.setRange(0, 31)
        self.color_slider.setValue(6)
        self.color_slider.setTickPosition(QSlider.TicksBelow)
        self.color_slider.setTickInterval(1)
        self.color_slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 6px; background: #3d3d3d; border-radius: 3px; }
            QSlider::handle:horizontal { background: #00a8ff; width: 14px; margin: -4px 0; border-radius: 7px; }
            QSlider::sub-page:horizontal { background: #00a8ff; border-radius: 3px; }
        """)

        self.color_spin = QSpinBox()
        self.color_spin.setRange(0, 31)
        self.color_spin.setValue(6)
        self.color_spin.setFixedWidth(46)
        self.color_spin.setStyleSheet(self._spin_style())

        self.color_preview = ColorPreviewLabel()

        cl.addWidget(QLabel("Index:"))
        cl.addWidget(self.color_slider, 1)
        cl.addWidget(self.color_spin)
        cl.addWidget(self.color_preview)

        main_layout.addWidget(color_grp)

        # 名称
        name_h = QHBoxLayout()
        name_h.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("ctrl_side_name_001 (留空则使用选择物体名)")
        self.name_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #cccccc;
                padding: 4px 8px;
            }""")
        name_h.addWidget(self.name_edit)
        main_layout.addLayout(name_h)

        # 创建按钮
        self.create_btn = QPushButton("Create")
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #00a8ff; color: #ffffff;
                border: none; border-radius: 4px;
                padding: 10px 20px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #0090e0; }
            QPushButton:pressed { background-color: #0078c0; }
        """)
        main_layout.addWidget(self.create_btn)

        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; }
            QLabel { color: #aaaaaa; font-size: 11px; }
        """)

    def _spin_style(self):
        return """
            QDoubleSpinBox, QSpinBox {
                background-color: #2b2b2b; border: 1px solid #3d3d3d;
                color: #cccccc; padding: 2px; border-radius: 3px;
            }
            QDoubleSpinBox::up-button, QSpinBox::up-button { width: 14px; }
            QDoubleSpinBox::down-button, QSpinBox::down-button { width: 14px; }
        """

    def _combo_style(self):
        return """
            QComboBox {
                background-color: #2b2b2b; border: 1px solid #3d3d3d;
                color: #cccccc; padding: 2px 6px; border-radius: 3px;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b; color: #cccccc;
                selection-background-color: #00a8ff; border: 1px solid #3d3d3d;
            }
        """

    # -------------------------------------------------------------------------
    def _load_shapes(self):
        while self.shapes_layout.count():
            item = self.shapes_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.shape_buttons.clear()

        base_path = os.path.abspath(controlUtils.__file__ + "/../../tools/image")
        shapes = []
        if os.path.exists(base_path):
            shapes = [f.replace(".json", "") for f in os.listdir(base_path) if f.endswith(".json")]
        if not shapes:
            shapes = self.DEFAULT_SHAPES

        self.shape_group = QButtonGroup(self)
        self.shape_group.setExclusive(True)

        columns = 4
        for i, name in enumerate(shapes):
            btn = ControlButton(name)
            self.shape_group.addButton(btn)
            self.shapes_layout.addWidget(btn, i // columns, i % columns)
            self.shape_buttons.append(btn)

        self.shape_group.buttonClicked.connect(self._on_shape_selected)

    # -------------------------------------------------------------------------
    def create_connections(self):
        self.create_btn.clicked.connect(self.clicked_create_control_btn)

        self.color_slider.valueChanged.connect(self._on_color_changed)
        self.color_spin.valueChanged.connect(self._on_color_changed)

    def _on_shape_selected(self, btn):
        self.current_shape = btn.shape_name if btn.isChecked() else None

    def _filter_shapes(self, text):
        text = text.lower()
        for btn in self.shape_buttons:
            btn.setVisible(text in btn.shape_name.lower())

    def _on_color_changed(self, value):
        self.color_slider.blockSignals(True)
        self.color_spin.blockSignals(True)
        self.color_slider.setValue(value)
        self.color_spin.setValue(value)
        self.color_slider.blockSignals(False)
        self.color_spin.blockSignals(False)
        self.color_preview.set_color(value)

    # -------------------------------------------------------------------------
    def clicked_create_control_btn(self):
        """
        创建控制器。

        多选时：
        1. 每个选中物体创建一个独立控制器；
        2. 每个控制器吸附到对应物体；
        3. 名称框为空时使用目标物体名；
        4. 名称框有内容且多选时自动追加 001/002/...，避免重名。
        """
        if not self.current_shape:
            cmds.warning("【Control Creator】请先在上方的网格中选择一个控制器形状！")
            return

        selected = cmds.ls(selection=True, type="transform", long=True) or []
        typed_name = self.name_edit.text().strip()

        # 没有选择物体时，在原点创建一个控制器。
        if not selected:
            ctrl_name = typed_name or "ctrl_new_001"
            try:
                created = controlUtils.Control.create_ctrl(
                    name=ctrl_name,
                    shape=self.current_shape,
                    radius=self.scale_spin.value(),
                    axis=self.axis_combo.currentText(),
                    pos=None,
                    parent=None,
                    ctrl_color=self.color_slider.value(),
                    unset_sub_ctrl=True,
                    unset_add_extra_group=True,
                    animation_set=None
                )
                cmds.select(created, replace=True)
            except Exception as exc:
                cmds.warning(u"【Control Creator】创建控制器失败: {}".format(exc))
            return

        created_ctrls = []
        multiple = len(selected) > 1

        for index, sel in enumerate(selected, 1):
            # DAG 路径和 namespace 都不能直接拿来当新节点基础名。
            sel_short = sel.split("|")[-1].replace(":", "_")

            if typed_name:
                # 单选时尊重用户输入；多选时自动编号，杜绝所有循环使用同一个名称。
                ctrl_name = typed_name if not multiple else "{}_{:03d}".format(typed_name, index)
            else:
                # 名称框留空时，每个控制器跟随各自目标物体名称。
                ctrl_name = sel_short

            # Control.create_ctrl 内部会自动补 ctrl_ 前缀。
            final_name = ctrl_name if "ctrl_" in ctrl_name else "ctrl_" + ctrl_name

            # 如果名称已经存在，不中断整个批量任务，自动寻找下一个可用编号。
            if cmds.objExists(final_name):
                base_name = ctrl_name
                suffix = 1
                while True:
                    candidate = "{}_{:03d}".format(base_name, suffix)
                    candidate_final = candidate if "ctrl_" in candidate else "ctrl_" + candidate
                    if not cmds.objExists(candidate_final):
                        ctrl_name = candidate
                        break
                    suffix += 1

            try:
                created = controlUtils.Control.create_ctrl(
                    name=ctrl_name,
                    shape=self.current_shape,
                    radius=self.scale_spin.value(),
                    axis=self.axis_combo.currentText(),
                    pos=sel,                  # 关键：吸附到当前循环对应的物体
                    parent=None,
                    ctrl_color=self.color_slider.value(),
                    unset_sub_ctrl=True,
                    unset_add_extra_group=True,
                    animation_set=None
                )
                created_ctrls.append(created)
            except Exception as exc:
                cmds.warning(u"【Control Creator】{} 创建失败: {}".format(sel_short, exc))

        if created_ctrls:
            cmds.select(created_ctrls, replace=True)
            cmds.warning(u"【Control Creator】已创建 {} 个控制器".format(len(created_ctrls)))


    def _create_at_origin(self):
        """无选择时，在原点创建"""
        try:
            name = self.name_edit.text() or "ctrl_new_001"
            ctrl_name = custom_create_controller(
                name=name,
                shape=self.current_shape,
                radius=self.scale_spin.value(),
                axis=self.axis_combo.currentText(),
                pos=None,
                parent=None,
                color=self.color_slider.value()  # 手动颜色
            )
            if self.rotate_x_spin.value() != 0:
                c = controlUtils.Control(t=ctrl_name)
                c.set_rotateX(rx=self.rotate_x_spin.value())
            cmds.select(ctrl_name)
        except Exception as e:
            cmds.warning("创建控制器失败: {}".format(str(e)))




# ----------------------------------------------------------------------
control_window = None

def main():
    global control_window
    if control_window is not None:
        try:
            control_window.close()
            control_window.deleteLater()
        except:
            pass
    control_window = ControlCreatorUI()
    control_window.show()
    return control_window


if __name__ == "__main__":
    main()