# coding=utf-8
u"""
Maya Index Color Slider
=======================

可复用的 Maya Index Color 选择控件。

界面结构：
    Slider → Index Label → Color Preview

模块职责：
    1. 使用 0～31 Slider 选择 Maya Index Color；
    2. 实时显示当前颜色 Index；
    3. 使用方块实时预览当前 Maya Index Color；
    4. 对外提供统一 ``value_changed`` Signal 和 ``get_value / set_value`` API；
    5. 视觉样式统一复用 MuziTools Theme Token。

模块边界：
    - 只处理 Qt 交互和 Maya Index Color 的显示；
    - 不负责给 Maya Controller / Shape 真正写入 overrideColor；
    - Controller 颜色写入仍由对应 Core / Tool 负责。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QSlider
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QWidget

from .. import theme


maya_index_colors = {
    0: (0.467, 0.467, 0.467),
    1: (0.000, 0.000, 0.000),
    2: (0.200, 0.200, 0.200),
    3: (0.600, 0.600, 0.600),
    4: (0.800, 0.000, 0.000),
    5: (0.000, 0.000, 0.400),
    6: (0.000, 0.000, 1.000),
    7: (0.000, 0.400, 0.000),
    8: (0.200, 0.000, 0.400),
    9: (0.800, 0.400, 0.000),
    10: (0.600, 0.400, 0.200),
    11: (0.400, 0.200, 0.000),
    12: (1.000, 1.000, 0.000),
    13: (1.000, 0.000, 0.000),
    14: (0.000, 1.000, 0.000),
    15: (0.000, 1.000, 1.000),
    16: (1.000, 1.000, 1.000),
    17: (1.000, 1.000, 0.000),
    18: (0.000, 0.800, 1.000),
    19: (1.000, 0.600, 0.800),
    20: (1.000, 0.400, 0.400),
    21: (0.600, 1.000, 0.400),
    22: (1.000, 0.800, 0.400),
    23: (0.400, 0.600, 1.000),
    24: (1.000, 1.000, 1.000),
    25: (1.000, 1.000, 0.800),
    26: (0.800, 1.000, 0.800),
    27: (0.800, 1.000, 1.000),
    28: (1.000, 0.800, 1.000),
    29: (1.000, 0.600, 0.600),
    30: (0.800, 1.000, 0.600),
    31: (0.600, 0.800, 1.000),
}


class MayaIndexColorSlider(QWidget):
    u"""Maya Index Color 滑条、数值标签和颜色预览组合控件。"""

    value_changed = Signal(int)

    def __init__(
            self,
            value=17,
            parent=None
    ):
        u"""
        初始化 Maya Index Color Slider。

        Args:
            value (int):
                初始 Maya Index Color，最终会限制在 0～31。
            parent (QtWidgets.QWidget | None):
                可选 Qt 父控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：初始化 QWidget，并创建 0～31 的水平颜色索引 Slider
        # -------------------------------------------------------------------------
        super(MayaIndexColorSlider, self).__init__(
            parent
        )

        self.color_slider = QSlider(
            Qt.Horizontal
        )
        self.color_slider.setRange(
            0,
            31
        )
        self.color_slider.setSingleStep(
            1
        )
        self.color_slider.setPageStep(
            1
        )
        self.color_slider.setMinimumWidth(
            160
        )

        # -------------------------------------------------------------------------
        # Step 02：创建当前 Index 数值标签和颜色方块预览控件
        # -------------------------------------------------------------------------
        self.index_label = QLabel()
        self.index_label.setFixedWidth(
            32
        )
        self.index_label.setAlignment(
            Qt.AlignCenter
        )

        self.color_preview = QLabel()
        self.color_preview.setFixedSize(
            28,
            28
        )

        # -------------------------------------------------------------------------
        # Step 03：建立横向布局，按 Slider → Index → Preview 顺序组织控件
        # -------------------------------------------------------------------------
        main_layout = QHBoxLayout(
            self
        )
        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        main_layout.setSpacing(
            9
        )
        main_layout.addWidget(
            self.color_slider,
            1
        )
        main_layout.addWidget(
            self.index_label
        )
        main_layout.addWidget(
            self.color_preview
        )

        # -------------------------------------------------------------------------
        # Step 04：应用 MuziTools 视觉样式并连接 Slider ValueChanged Signal
        # -------------------------------------------------------------------------
        self.style_widgets()

        self.color_slider.valueChanged.connect(
            self._slider_value_changed
        )

        # -------------------------------------------------------------------------
        # Step 05：写入初始 Index，同时刷新数值标签和颜色预览
        # -------------------------------------------------------------------------
        self.set_value(
            value
        )

    # =========================================================================
    # Style
    # =========================================================================

    def style_widgets(self):
        u"""应用高可见度 Slider、Index Label 和 Preview 样式。"""
        # -------------------------------------------------------------------------
        # Step 01：使用 Theme Accent 配置 Slider Groove / Handle 状态
        # -------------------------------------------------------------------------
        self.color_slider.setStyleSheet(
            u"""
            QSlider {
                background: transparent;
            }

            QSlider::groove:horizontal {
                height: 7px;
                background: #D7D3DE;
                border: 1px solid #CBC6D3;
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal {
                background: %(accent)s;
                border: 1px solid %(accent)s;
                border-radius: 3px;
            }

            QSlider::add-page:horizontal {
                background: #E7E3EA;
                border: 1px solid #D7D2DE;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                width: 17px;
                height: 17px;
                margin: -6px 0px;
                background: #FFFFFF;
                border: 2px solid %(accent)s;
                border-radius: 8px;
            }

            QSlider::handle:horizontal:hover {
                background: %(accent_soft)s;
                border-color: %(accent_hover)s;
            }
            """ % {
                "accent": theme.accent,
                "accent_hover": theme.accent_hover,
                "accent_soft": theme.accent_soft,
            }
        )

        # -------------------------------------------------------------------------
        # Step 02：配置 Index Label，使数值与颜色预览在视觉上保持清晰分区
        # -------------------------------------------------------------------------
        self.index_label.setStyleSheet(
            u"""
            QLabel {
                background-color: %(surface)s;
                color: %(text)s;
                border: 1px solid %(border)s;
                border-radius: 7px;
                padding: 3px 4px;
                font-weight: 600;
            }
            """ % {
                "surface": theme.surface,
                "text": theme.text,
                "border": theme.border,
            }
        )

    # =========================================================================
    # Value
    # =========================================================================

    def get_value(self):
        u"""
        返回当前 Maya Index Color。

        Returns:
            int:
                Slider 当前 0～31 的颜色索引。
        """
        return int(
            self.color_slider.value()
        )

    def set_value(self, value):
        u"""
        设置当前 Maya Index Color，并自动限制到 0～31。

        Args:
            value (int):
                需要写入的 Maya Index Color。
        """
        color_index = int(
            value
        )

        if color_index < 0:
            color_index = 0

        if color_index > 31:
            color_index = 31

        self.color_slider.setValue(
            color_index
        )
        self.update_preview(
            color_index
        )

    # =========================================================================
    # Preview
    # =========================================================================

    def _slider_value_changed(self, value):
        u"""Slider 改变时同步 Preview，并向外发送 ``value_changed`` Signal。"""
        color_index = int(
            value
        )

        self.update_preview(
            color_index
        )
        self.value_changed.emit(
            color_index
        )

    def update_preview(self, color_index=None):
        u"""
        根据 Maya Index Color 更新数值标签和颜色方块预览。

        Args:
            color_index (int | None):
                需要显示的 0～31 Maya Index；None 时读取 Slider 当前值。
        """
        # -------------------------------------------------------------------------
        # Step 01：确定需要显示的 Index，并取得对应 0～1 RGB 数据
        # -------------------------------------------------------------------------
        if color_index is None:
            color_index = self.get_value()

        color_index = int(
            color_index
        )
        rgb = maya_index_colors.get(
            color_index,
            maya_index_colors[0]
        )

        # -------------------------------------------------------------------------
        # Step 02：把 Maya 0～1 RGB 转成 Qt Style Sheet 使用的 0～255 RGB
        # -------------------------------------------------------------------------
        red = int(
            rgb[0] * 255
        )
        green = int(
            rgb[1] * 255
        )
        blue = int(
            rgb[2] * 255
        )

        # -------------------------------------------------------------------------
        # Step 03：同步 Index 文本，并使用对应 RGB 刷新 Preview 方块
        # -------------------------------------------------------------------------
        self.index_label.setText(
            u"{}".format(
                color_index
            )
        )

        self.color_preview.setStyleSheet(
            u"""
            QLabel {{
                background-color: rgb({red}, {green}, {blue});
                border: 2px solid #77717E;
                border-radius: 7px;
            }}
            """.format(
                red=red,
                green=green,
                blue=blue
            )
        )


__all__ = [
    "maya_index_colors",
    "MayaIndexColorSlider",
]
