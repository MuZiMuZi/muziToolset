from __future__ import print_function, unicode_literals

import os
from importlib import reload

from PySide2 import QtWidgets, QtCore

import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

Cesardsasa
# -----------------------------
# Maya 主窗口获取
# -----------------------------
def get_maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QtWidgets.QWidget)
    return None


# -----------------------------
# Rigging Toolbox 主窗口
# -----------------------------
class RiggingToolbox(QtWidgets.QMainWindow):

    WINDOW_NAME = "RiggingToolbox_Muzi"

    def __init__(self, parent=get_maya_main_window()):
        super(RiggingToolbox, self).__init__(parent)

        self.setObjectName(self.WINDOW_NAME)
        self.setWindowTitle("Rigging Toolbox")
        self.setMinimumSize(520, 650)

        self.build_ui()

    # -------------------------
    # UI 主结构
    # -------------------------
    def build_ui(self):

        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # ===== Tabs =====
        self.tab_widget.addTab(self.build_rig_tab(), "Rig")
        self.tab_widget.addTab(self.build_joint_tab(), "Joint")
        self.tab_widget.addTab(self.build_control_tab(), "Control")
        self.tab_widget.addTab(self.build_attr_tab(), "Attr")
        self.tab_widget.addTab(self.build_util_tab(), "Utils")

    # -------------------------
    # Rig Tab
    # -------------------------
    def build_rig_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)

        layout.addWidget(self.make_button("Create Joint Chain", self.create_joint_chain))
        layout.addWidget(self.make_button("Create IK Handle", self.create_ik_handle))
        layout.addWidget(self.make_button("Simple FK Setup", self.simple_fk_setup))

        layout.addStretch()
        return w

    # -------------------------
    # Joint Tab
    # -------------------------
    def build_joint_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)

        layout.addWidget(self.make_button("Orient Joint", self.orient_joint))
        layout.addWidget(self.make_button("Freeze Joints", self.freeze))

        layout.addStretch()
        return w

    # -------------------------
    # Control Tab
    # -------------------------
    def build_control_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)

        layout.addWidget(self.make_button("Create Controller", self.create_controller))
        layout.addWidget(self.make_button("Align Objects", self.align_objects))

        layout.addStretch()
        return w

    # -------------------------
    # Attr Tab
    # -------------------------
    def build_attr_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)

        layout.addWidget(self.make_button("Add Custom Attr", self.add_attr))

        layout.addStretch()
        return w

    # -------------------------
    # Utils Tab
    # -------------------------
    def build_util_tab(self):
        w = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(w)

        layout.addWidget(self.make_button("Freeze Transforms", self.freeze))
        layout.addWidget(self.make_button("Delete History", self.delete_history))

        layout.addStretch()
        return w

    # -------------------------
    # UI helper
    # -------------------------
    def make_button(self, name, func):
        btn = QtWidgets.QPushButton(name)
        btn.clicked.connect(func)
        return btn

    # =========================================================
    # Rig Functions
    # =========================================================

    def create_joint_chain(self, *args):
        import maya.cmds as cmds

        sel = cmds.ls(sl=True)
        if len(sel) < 2:
            cmds.warning("Select at least 2 objects")
            return

        cmds.select(clear=True)

        cmds.joint(p=cmds.xform(sel[0], q=True, ws=True, t=True))

        for obj in sel[1:]:
            cmds.joint(p=cmds.xform(obj, q=True, ws=True, t=True))

    def create_ik_handle(self, *args):
        import maya.cmds as cmds

        sel = cmds.ls(sl=True)
        if len(sel) != 2:
            cmds.warning("Select start and end joint")
            return

        cmds.ikHandle(sj=sel[0], ee=sel[1], sol="ikRPsolver")

    def simple_fk_setup(self, *args):
        import maya.cmds as cmds

        sel = cmds.ls(sl=True)
        if not sel:
            cmds.warning("Select joints")
            return

        for j in sel:
            ctrl = cmds.circle(n=j + "_CTRL")[0]
            grp = cmds.group(ctrl, n=j + "_GRP")

            pos = cmds.xform(j, q=True, ws=True, t=True)
            cmds.xform(grp, ws=True, t=pos)

            cmds.parentConstraint(ctrl, j, mo=True)

    # =========================================================
    # Control
    # =========================================================

    def create_controller(self, *args):
        import maya.cmds as cmds

        ctrl = cmds.circle(n="CTRL")[0]
        cmds.group(ctrl, n="CTRL_GRP")

    def align_objects(self, *args):
        import maya.cmds as cmds

        sel = cmds.ls(sl=True)
        if len(sel) != 2:
            cmds.warning("Select target + object")
            return

        t, obj = sel

        pos = cmds.xform(t, q=True, ws=True, t=True)
        rot = cmds.xform(t, q=True, ws=True, ro=True)

        cmds.xform(obj, ws=True, t=pos)
        cmds.xform(obj, ws=True, ro=rot)

    # =========================================================
    # Attr
    # =========================================================

    def add_attr(self, *args):
        import maya.cmds as cmds

        sel = cmds.ls(sl=True)
        if not sel:
            return

        cmds.addAttr(sel[0], ln="customAttr", at="double")
        cmds.setAttr(sel[0] + ".customAttr", e=True, keyable=True)

    # =========================================================
    # Utils
    # =========================================================

    def freeze(self, *args):
        import maya.cmds as cmds
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    def delete_history(self, *args):
        import maya.cmds as cmds
        cmds.delete(ch=True)

    def orient_joint(self, *args):
        import maya.cmds as cmds
        cmds.joint(e=True, oj="xyz", sao="yup", ch=True)


# -----------------------------
# 启动器（Maya safe）
# -----------------------------
def show():
    global rig_toolbox

    try:
        rig_toolbox.close()
        rig_toolbox.deleteLater()
    except:
        pass

    rig_toolbox = RiggingToolbox()
    rig_toolbox.show()


if __name__ == "__main__":
    show()