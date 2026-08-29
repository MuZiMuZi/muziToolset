# coding=utf-8
u"""
BlendShape Target Tool
======================

Maya 2023 / PySide2 BlendShape Target 管理工具。

功能：
    - 从所选模型获取 BlendShape；
    - 添加新 Target；
    - 同名 Target 使用原 index 替换；
    - 显示真实 ``weight[index]``；
    - 即使原始 Target 模型已经删除，也能通过逐个激活权重复制出所有目标体。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QListWidget
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget

from ....core import qtUtils


_window = None


def _short_name(node):
    return node.split("|")[-1].replace(":", "_")


def get_mesh_shape(node):
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "mesh":
        return node

    shapes = cmds.listRelatives(
        node,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="mesh"
    ) or []

    if shapes:
        return shapes[0]

    return None


def get_transform(node):
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "transform":
        return node

    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=True
    ) or []

    if parents:
        return parents[0]

    return None


def find_blendshape(node):
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "blendShape":
        return node

    history = cmds.listHistory(node) or []
    blendshape_nodes = cmds.ls(history, type="blendShape") or []

    if blendshape_nodes:
        return blendshape_nodes[0]

    return None


def get_base_transform(blendshape_node):
    geometries = cmds.blendShape(
        blendshape_node,
        query=True,
        geometry=True
    ) or []

    if not geometries:
        return None

    geometry = geometries[0]
    transform = get_transform(geometry)

    if transform:
        return transform

    return geometry


def get_targets(blendshape_node):
    """
    返回真实 alias -> weight[index] 映射。

    Returns:
        list[dict]:
            [{"alias": "smile", "index": 3, "plug": "weight[3]"}, ...]
    """
    if not blendshape_node or not cmds.objExists(blendshape_node):
        return []

    aliases = cmds.aliasAttr(
        blendshape_node,
        query=True
    ) or []

    targets = []
    index = 0

    while index + 1 < len(aliases):
        alias_name = aliases[index]
        plug_name = aliases[index + 1]

        match = re.search(r"weight\[(\d+)\]", plug_name)
        if match:
            target_index = int(match.group(1))
            targets.append({
                "alias": alias_name,
                "index": target_index,
                "plug": plug_name,
            })

        index += 2

    targets.sort(key=lambda item: item["index"])
    return targets


def get_next_target_index(blendshape_node):
    indices = cmds.getAttr(
        blendshape_node + ".weight",
        multiIndices=True
    ) or []

    if not indices:
        return 0

    return max(indices) + 1


def remove_target(blendshape_node, target_index, alias_name=None):
    """删除一个 Target 的 inputTargetGroup，并尽量清理 weight alias。"""
    if alias_name:
        alias_plug = "{}.{}".format(
            blendshape_node,
            alias_name
        )
        try:
            cmds.aliasAttr(alias_plug, remove=True)
        except Exception:
            pass

    input_group = (
        "{}.inputTarget[0].inputTargetGroup[{}]".format(
            blendshape_node,
            target_index
        )
    )

    if cmds.objExists(input_group):
        try:
            cmds.removeMultiInstance(
                input_group,
                b=True
            )
        except Exception:
            pass

    weight_plug = "{}.weight[{}]".format(
        blendshape_node,
        target_index
    )

    if cmds.objExists(weight_plug):
        incoming = cmds.listConnections(
            weight_plug,
            source=True,
            destination=False,
            plugs=True
        ) or []

        if not incoming:
            try:
                cmds.removeMultiInstance(
                    weight_plug,
                    b=True
                )
            except Exception:
                pass


def add_or_replace_target(blendshape_node, target_transform):
    """按目标 Transform 短名称添加或替换 BlendShape Target。"""
    if not cmds.objExists(blendshape_node):
        raise RuntimeError(u"BlendShape 不存在：{}".format(blendshape_node))

    target_shape = get_mesh_shape(target_transform)
    if not target_shape:
        raise RuntimeError(u"目标不是 Mesh：{}".format(target_transform))

    base_transform = get_base_transform(blendshape_node)
    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    alias_name = _short_name(target_transform)
    existing_targets = get_targets(blendshape_node)
    target_index = None

    for target_info in existing_targets:
        if target_info["alias"] == alias_name:
            target_index = target_info["index"]
            break

    if target_index is not None:
        remove_target(
            blendshape_node,
            target_index,
            alias_name=alias_name
        )
    else:
        target_index = get_next_target_index(blendshape_node)

    cmds.blendShape(
        blendshape_node,
        edit=True,
        target=(
            base_transform,
            target_index,
            target_transform,
            1.0
        )
    )

    cmds.aliasAttr(
        alias_name,
        "{}.weight[{}]".format(
            blendshape_node,
            target_index
        )
    )

    return {
        "alias": alias_name,
        "index": target_index,
    }


def duplicate_all_targets(blendshape_node):
    """
    通过逐个开启 target 权重，从 Base Mesh 烘焙出所有目标。

    这种方式不要求 inputGeomTarget 仍连接着原始 Target Mesh。
    """
    base_transform = get_base_transform(blendshape_node)
    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    targets = get_targets(blendshape_node)
    if not targets:
        return []

    original_values = {}

    for target_info in targets:
        weight_plug = "{}.weight[{}]".format(
            blendshape_node,
            target_info["index"]
        )
        original_values[target_info["index"]] = cmds.getAttr(weight_plug)

    copies = []

    try:
        for target_info in targets:
            for zero_target in targets:
                zero_plug = "{}.weight[{}]".format(
                    blendshape_node,
                    zero_target["index"]
                )
                cmds.setAttr(zero_plug, 0.0)

            active_plug = "{}.weight[{}]".format(
                blendshape_node,
                target_info["index"]
            )
            cmds.setAttr(active_plug, 1.0)

            duplicate_name = target_info["alias"]
            if cmds.objExists(duplicate_name):
                duplicate_name = "{}_copy".format(duplicate_name)

            duplicate = cmds.duplicate(
                base_transform,
                name=duplicate_name,
                returnRootsOnly=True
            )[0]
            cmds.delete(duplicate, constructionHistory=True)
            copies.append(duplicate)

    finally:
        for target_info in targets:
            restore_plug = "{}.weight[{}]".format(
                blendshape_node,
                target_info["index"]
            )
            restore_value = original_values.get(
                target_info["index"],
                0.0
            )
            cmds.setAttr(restore_plug, restore_value)

    return copies


class AddBlendShapeTool(QWidget):
    """BlendShape Target 管理窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(AddBlendShapeTool, self).__init__(parent)
        self.setWindowTitle(u"BlendShape Target Tool")
        self.setMinimumWidth(380)

        self.bs_node_line = QLineEdit()
        self.bs_node_line.setPlaceholderText(u"BlendShape 节点")
        self.get_bs_btn = QPushButton(u"从选择获取")

        self.target_list = QListWidget()
        self.target_list.setMinimumHeight(180)

        self.add_target_btn = QPushButton(u"添加 / 同名替换 Target")
        self.copy_targets_btn = QPushButton(u"复制所有 Target Mesh")
        self.refresh_btn = QPushButton(u"刷新")

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel(u"BS:"))
        input_layout.addWidget(self.bs_node_line, 1)
        input_layout.addWidget(self.get_bs_btn)
        main_layout.addLayout(input_layout)

        main_layout.addWidget(self.target_list)
        main_layout.addWidget(self.add_target_btn)
        main_layout.addWidget(self.copy_targets_btn)
        main_layout.addWidget(self.refresh_btn)

    def _create_connections(self):
        self.get_bs_btn.clicked.connect(self.get_blendshape_from_selection)
        self.add_target_btn.clicked.connect(self.add_targets)
        self.copy_targets_btn.clicked.connect(self.copy_targets)
        self.refresh_btn.clicked.connect(self.refresh_target_list)
        self.bs_node_line.textChanged.connect(self.refresh_target_list)

    def _blendshape_node(self):
        return self.bs_node_line.text().strip()

    def get_blendshape_from_selection(self):
        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请先选择 BlendShape 节点或带 BlendShape 的模型。")
            return

        for node in selections:
            blendshape_node = find_blendshape(node)
            if blendshape_node:
                self.bs_node_line.setText(blendshape_node)
                return

        cmds.warning(u"选择中没有找到 BlendShape。")

    def refresh_target_list(self):
        self.target_list.clear()
        blendshape_node = self._blendshape_node()

        if not blendshape_node or not cmds.objExists(blendshape_node):
            return

        targets = get_targets(blendshape_node)
        for target_info in targets:
            self.target_list.addItem(
                u"[{0:03d}] {1}".format(
                    target_info["index"],
                    target_info["alias"]
                )
            )

    def add_targets(self):
        blendshape_node = self._blendshape_node()
        if not blendshape_node or not cmds.objExists(blendshape_node):
            cmds.warning(u"请先指定有效的 BlendShape 节点。")
            return

        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            cmds.warning(u"请选择一个或多个 Target Mesh。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziAddBlendShapeTargets")
        try:
            for target in selections:
                try:
                    result = add_or_replace_target(
                        blendshape_node,
                        target
                    )
                    print(
                        u"[BlendShape] {} -> weight[{}]".format(
                            result["alias"],
                            result["index"]
                        )
                    )
                except Exception as error:
                    cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        self.refresh_target_list()

    def copy_targets(self):
        blendshape_node = self._blendshape_node()
        if not blendshape_node or not cmds.objExists(blendshape_node):
            cmds.warning(u"请先指定有效的 BlendShape 节点。")
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziDuplicateBlendShapeTargets")
        try:
            copies = duplicate_all_targets(blendshape_node)
            if copies:
                cmds.select(copies, replace=True)
                print(
                    u"[BlendShape] 已复制 {} 个 Target。".format(
                        len(copies)
                    )
                )
            else:
                cmds.warning(u"当前 BlendShape 没有 Target。")
        except Exception as error:
            cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)


# 旧类名兼容。
Add_BS_Tool = AddBlendShapeTool


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = AddBlendShapeTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
