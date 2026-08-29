try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QGroupBox
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QGroupBox
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
# 保存窗口实例，避免窗口被 Python 垃圾回收后自动关闭
MyWindow_main = None


# =============================================================================
# 获取 Maya 主窗口
# =============================================================================
def get_maya_main_window():
    u"""获取 Maya 主窗口的 QWidget 对象。"""
    maya_main_window_ptr = omui.MQtUtil.mainWindow()

    if maya_main_window_ptr is None:
        return None

    maya_main_window = wrapInstance(
        int(maya_main_window_ptr),
        QWidget
    )
    return maya_main_window



class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        layout = QVBoxLayout()

        # 按钮1
        btn1 = QPushButton("按钮1")
        layout.addWidget(btn1)

        layout.addStretch(1)

        # 按钮2
        btn2 = QPushButton("按钮2")
        layout.addWidget(btn2)

        layout.addStretch(1)

        # 按钮3
        btn3 = QPushButton("按钮3")
        layout.addWidget(btn3)

        layout.addStretch(2)

        self.setLayout(layout)


def main():
    u"""关闭旧窗口并显示一个新的简单工具面板。"""
    global MyWindow_main

    if MyWindow_main is not None:
        try:
            MyWindow_main.close()
            MyWindow_main.deleteLater()
        except RuntimeError:
            pass

    MyWindow_main = MyWindow()
    MyWindow_main.show()
    MyWindow_main.raise_()
    MyWindow_main.activateWindow()

    return MyWindow_main


# =============================================================================
# 直接运行脚本时自动打开窗口
# =============================================================================
if __name__ == "__main__":
    main()
