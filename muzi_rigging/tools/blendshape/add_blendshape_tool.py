# coding=utf-8
u"""
BlendShape Target Tool
======================

Maya BlendShape Target 管理工具。

功能：
    - 从所选模型获取 BlendShape；
    - 添加新 Target；
    - 同名 Target 使用原 index 替换；
    - 显示真实 weight[index]；
    - 通过逐个激活权重复制所有 Target Mesh。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QListWidget
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ... import ui_theme


def _short_name(node):
    """返回适合 Alias 使用的短名称。"""
    return node.split("|")[-1].replace(":", "_")


def get_mesh_shape(node):
    """返回 Transform 或 Mesh 对应的可见 Mesh Shape。"""
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
    )

    if shapes is None:
        shapes = []

    if shapes:
        return shapes[0]

    return None


def get_transform(node):
    """返回节点对应 Transform。"""
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "transform":
        return node

    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if parents:
        return parents[0]

    return None


def find_blendshape(node):
    """从节点或模型历史中寻找第一个 BlendShape。"""
    if not node or not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "blendShape":
        return node

    history = cmds.listHistory(node)

    if history is None:
        history = []

    blendshape_nodes = cmds.ls(
        history,
        type="blendShape"
    )

    if blendshape_nodes is None:
        blendshape_nodes = []

    if blendshape_nodes:
        return blendshape_nodes[0]

    return None


def get_base_transform(blendshape_node):
    """获取 BlendShape 的 Base Geometry Transform。"""
    geometries = cmds.blendShape(
        blendshape_node,
        query=True,
        geometry=True
    )

    if geometries is None:
        geometries = []

    if not geometries:
        return None

    geometry = geometries[0]
    transform = get_transform(geometry)

    if transform:
        return transform

    return geometry


def sort_targets_by_index(targets):
    """按真实 weight index 从小到大排序。"""
    item_count = len(targets)
    outer_index = 0

    while outer_index < item_count:
        inner_index = 0

        while inner_index < item_count - 1:
            current_index = targets[inner_index]["index"]
            next_index = targets[inner_index + 1]["index"]

            if current_index > next_index:
                temporary_target = targets[inner_index]
                targets[inner_index] = targets[inner_index + 1]
                targets[inner_index + 1] = temporary_target

            inner_index += 1

        outer_index += 1

    return targets


def get_targets(blendshape_node):
    """返回真实 alias -> weight[index] 映射。"""
    if not blendshape_node or not cmds.objExists(blendshape_node):
        return []

    aliases = cmds.aliasAttr(
        blendshape_node,
        query=True
    )

    if aliases is None:
        aliases = []

    targets = []
    index = 0

    while index + 1 < len(aliases):
        alias_name = aliases[index]
        plug_name = aliases[index + 1]

        match = re.search(
            r"weight\[(\d+)\]",
            plug_name
        )

        if match:
            target_index = int(match.group(1))
            target_info = {
                "alias": alias_name,
                "index": target_index,
                "plug": plug_name,
            }
            targets.append(target_info)

        index += 2

    return sort_targets_by_index(targets)


def get_next_target_index(blendshape_node):
    """返回下一个可使用的 weight index。"""
    indices = cmds.getAttr(
        blendshape_node + ".weight",
        multiIndices=True
    )

    if indices is None:
        indices = []

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
            cmds.aliasAttr(
                alias_plug,
                remove=True
            )
        except Exception:
            pass

    input_group = "{}.inputTarget[0].inputTargetGroup[{}]".format(
        blendshape_node,
        target_index
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
        )

        if incoming is None:
            incoming = []

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
        raise RuntimeError(
            u"BlendShape 不存在：{}".format(blendshape_node)
        )

    target_shape = get_mesh_shape(target_transform)

    if not target_shape:
        raise RuntimeError(
            u"目标不是 Mesh：{}".format(target_transform)
        )

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
    """逐个开启 Target 权重，从 Base Mesh 烘焙出所有目标。"""
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

            cmds.delete(
                duplicate,
                constructionHistory=True
            )
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
            cmds.setAttr(
                restore_plug,
                restore_value
            )

    return copies


class AddBlendShapeTool(QWidget):
    """BlendShape Target 管理窗口。"""

    def __init__(self, parent=None):
        super(AddBlendShapeTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"BlendShape Target",
            minimum_width=560
        )
        self.resize(580, 560)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面部件。"""
        self.title_label = ui_theme.make_title(u"BlendShape Target")
        self.subtitle_label = ui_theme.make_subtitle(
            u"管理真实 weight[index]，添加、替换并从 Base Mesh 烘焙 Target。"
        )

        self.bs_node_label = QLabel(u"BlendShape")
        self.bs_node_line = QLineEdit()
        self.bs_node_line.setPlaceholderText(u"BlendShape 节点")
        self.get_bs_button = QPushButton(u"从选择获取")

        self.target_count_label = QLabel(u"0 个 Target")
        ui_theme.set_role(self.target_count_label, "accent")

        self.target_list = QListWidget()
        self.target_list.setMinimumHeight(220)

        self.add_target_button = QPushButton(u"添加 / 同名替换 Target")
        self.add_target_button.setToolTip(
            u"当前选择的 Mesh 会按短名称添加；同名 Alias 复用原 index"
        )
        ui_theme.style_primary(self.add_target_button)

        self.copy_targets_button = QPushButton(u"复制所有 Target Mesh")
        self.refresh_button = QPushButton(u"刷新列表")
        ui_theme.style_ghost(self.refresh_button)

        self.target_info_label = QLabel(
            u"列表显示的是 BlendShape 的真实 weight index，不会因为删除过 Target 而错位。"
        )
        self.target_info_label.setWordWrap(True)
        ui_theme.set_role(self.target_info_label, "muted")

    def create_layouts(self):
        """创建 Silicon Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        node_card, node_layout = ui_theme.make_card(self)
        node_layout.addWidget(
            ui_theme.make_section_title(u"BlendShape Node")
        )

        node_row = QHBoxLayout()
        node_row.setContentsMargins(0, 0, 0, 0)
        node_row.addWidget(self.bs_node_label)
        node_row.addWidget(self.bs_node_line, 1)
        node_row.addWidget(self.get_bs_button)
        node_layout.addLayout(node_row)

        target_card, target_layout = ui_theme.make_card(self)

        target_header = QHBoxLayout()
        target_header.setContentsMargins(0, 0, 0, 0)
        target_header.addWidget(
            ui_theme.make_section_title(u"Targets")
        )
        target_header.addStretch(1)
        target_header.addWidget(self.target_count_label)
        target_layout.addLayout(target_header)
        target_layout.addWidget(self.target_info_label)
        target_layout.addWidget(self.target_list, 1)

        target_action_layout = QHBoxLayout()
        target_action_layout.setContentsMargins(0, 0, 0, 0)
        target_action_layout.addWidget(self.refresh_button)
        target_action_layout.addStretch(1)
        target_action_layout.addWidget(self.copy_targets_button)
        target_layout.addLayout(target_action_layout)

        add_card, add_layout = ui_theme.make_card(self)
        add_layout.addWidget(
            ui_theme.make_section_title(u"添加 Target")
        )

        add_info_label = QLabel(
            u"选择一个或多个 Target Mesh，然后执行添加。"
        )
        ui_theme.set_role(add_info_label, "muted")
        add_layout.addWidget(add_info_label)
        add_layout.addWidget(self.add_target_button)

        main_layout.addWidget(node_card)
        main_layout.addWidget(target_card, 1)
        main_layout.addWidget(add_card)

    def create_connections(self):
        """连接界面信号。"""
        self.get_bs_button.clicked.connect(
            self.get_blendshape_from_selection
        )
        self.add_target_button.clicked.connect(self.add_targets)
        self.copy_targets_button.clicked.connect(self.copy_targets)
        self.refresh_button.clicked.connect(self.refresh_target_list)
        self.bs_node_line.textChanged.connect(self.refresh_target_list)

    def get_blendshape_node(self):
        """读取输入框中的 BlendShape 节点。"""
        return self.bs_node_line.text().strip()

    def get_blendshape_from_selection(self):
        """从选择中查找 BlendShape。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(
                u"请先选择 BlendShape 节点或带 BlendShape 的模型。"
            )
            return

        for node in selections:
            blendshape_node = find_blendshape(node)

            if blendshape_node:
                self.bs_node_line.setText(blendshape_node)
                return

        cmds.warning(u"选择中没有找到 BlendShape。")

    def refresh_target_list(self):
        """刷新真实 Target Index 列表。"""
        self.target_list.clear()
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node or not cmds.objExists(blendshape_node):
            self.target_count_label.setText(u"0 个 Target")
            return

        targets = get_targets(blendshape_node)

        for target_info in targets:
            self.target_list.addItem(
                u"[{0:03d}]  {1}".format(
                    target_info["index"],
                    target_info["alias"]
                )
            )

        self.target_count_label.setText(
            u"{} 个 Target".format(len(targets))
        )

    def add_targets(self):
        """添加或同名替换选择 Target。"""
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node or not cmds.objExists(blendshape_node):
            cmds.warning(u"请先指定有效的 BlendShape 节点。")
            return

        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if not selections:
            cmds.warning(u"请选择一个或多个 Target Mesh。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziAddBlendShapeTargets"
        )

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
        """复制当前 BlendShape 的所有 Target Mesh。"""
        blendshape_node = self.get_blendshape_node()

        if not blendshape_node or not cmds.objExists(blendshape_node):
            cmds.warning(u"请先指定有效的 BlendShape 节点。")
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziDuplicateBlendShapeTargets"
        )

        try:
            copies = duplicate_all_targets(blendshape_node)

            if copies:
                cmds.select(
                    copies,
                    replace=True
                )
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


def main():
    """创建 BlendShape Target 工具。"""
    window = AddBlendShapeTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
