# coding=utf-8
u"""
Maya Index Color Slider
=======================

可复用的 Maya Index Color 选择控件。

界面结构：
    Slider -> Index -> Color Preview

职责：
    1. 使用 0～31 Slider 选择 Maya Index Color；
    2. 实时显示当前颜色 Index；
    3. 使用方块实时预览当前 Maya 颜色；
    4. 对外提供统一 value_changed Signal 和 get_value / set_value API。

重要边界：
    - 本模块只负责 UI，不直接修改 Maya Controller；
    - 真正的 Controller Shape Color 仍然由 core.control_shape_utils 负责；
    - Maya Index Color 数据统一保存在本 Widget，不依赖 tools 层。
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
    u"""Maya Index Color 滑条 + 数值 + 方块预览控件。"""

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
                初始 Maya Index Color，范围 0～31。
            parent (QWidget | None):
                Qt 父窗口。
        """
        super(MayaIndexColorSlider, self).__init__(parent)

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
            150
        )
        self.style_color_slider()

        self.index_label = QLabel()
        self.index_label.setMinimumWidth(
            30
        )
        self.index_label.setAlignment(
            Qt.AlignCenter
        )
        self.index_label.setStyleSheet(
            u"""
            QLabel {
                background-color: #F3F3F5;
                color: #3A3C42;
                border: 1px solid #D9DBE0;
                border-radius: 5px;
                padding: 2px 4px;
                font-weight: 600;
            }
            """
        )

        self.color_preview = QLabel()
        self.color_preview.setFixedSize(
            28,
            28
        )

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
            8
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

        self.color_slider.valueChanged.connect(
            self._slider_value_changed
        )

        self.set_value(
            value
        )

    # =========================================================================
    # Style
    # =========================================================================

    def style_color_slider(self):
        u"""增强 Slider Track 和 Handle 对比度，保证浅色主题下仍然清晰。"""
        self.color_slider.setStyleSheet(
            u"""
            QSlider {
                background: transparent;
            }

            QSlider::groove:horizontal {
                height: 8px;
                background: #D8DADE;
                border: 1px solid #C9CBD0;
                border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
                background: #EC4141;
                border: 1px solid #EC4141;
                border-radius: 4px;
            }

            QSlider::add-page:horizontal {
                background: #E5E6E9;
                border: 1px solid #D4D6DA;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                width: 18px;
                height: 18px;
                margin: -6px 0px;
                background: #FFFFFF;
                border: 3px solid #EC4141;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #FFF0F0;
                border-color: #F05252;
            }

            QSlider::handle:horizontal:pressed {
                background: #FFE4E4;
                border-color: #D93636;
            }
            """
        )

    # =========================================================================
    # Value
    # =========================================================================

    def get_value(self):
        u"""
        返回当前 Maya Index Color。

        Returns:
            int:
            当前颜色 Index。
        """
        return int(
            self.color_slider.value()
        )

    def set_value(self, value):
        u"""
        设置当前 Maya Index Color。

        Args:
            value (int):
                Maya Index Color，自动限制到 0～31。
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

        # setValue 在数值没有变化时不会触发 Signal，仍然主动刷新一次显示。
        self.update_preview(
            color_index
        )

    # =========================================================================
    # Preview
    # =========================================================================

    def _slider_value_changed(self, value):
        u"""Slider 改变时同步数值和颜色预览。"""
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
        更新 Index Label 和方块颜色预览。

        Args:
            color_index (int | None):
                不传时使用当前 Slider Value。
        """
        if color_index is None:
            color_index = self.get_value()

        color_index = int(
            color_index
        )

        rgb = maya_index_colors.get(
            color_index,
            maya_index_colors[0]
        )

        red = int(
            rgb[0] * 255
        )
        green = int(
            rgb[1] * 255
        )
        blue = int(
            rgb[2] * 255
        )

        self.index_label.setText(
            u"{}".format(
                color_index
            )
        )

        self.color_preview.setStyleSheet(
            u"""
            QLabel {{
                background-color: rgb({red}, {green}, {blue});
                border: 2px solid #7C7F86;
                border-radius: 5px;
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
