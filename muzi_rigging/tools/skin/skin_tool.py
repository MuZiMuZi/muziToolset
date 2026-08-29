# coding=utf-8
u"""
Skin Tool
=========

Maya 2023+ 蒙皮工具。

功能：
    - Smooth Bind / Detach / Paint / Mirror Skin Weights；
    - 复制 Skin Weight；
    - XML 权重导出 / 导入；
    - 选择 SkinCluster 影响关节；
    - 强制归一化权重。
"""

from __future__ import print_function

import json
import os

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtWidgets import QFileDialog
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QFileDialog
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ... import ui_theme


def _short_name(node):
    """返回适合写文件和 SkinCluster 名称的短名称。"""
    return node.split("|")[-1].replace(":", "_")


def find_skin_cluster(geometry):
    """返回 geometry 关联的第一个 SkinCluster。"""
    if not cmds.objExists(geometry):
        return None

    try:
        skin_cluster = mel.eval(
            'findRelatedSkinCluster("{}")'.format(geometry)
        )
    except Exception:
        skin_cluster = None

    if skin_cluster:
        return skin_cluster

    history = cmds.listHistory(geometry)

    if history is None:
        history = []

    skin_clusters = cmds.ls(
        history,
        type="skinCluster"
    )

    if skin_clusters is None:
        skin_clusters = []

    if skin_clusters:
        return skin_clusters[0]

    return None


def copy_skin_weights(source, targets):
    """把 source 的蒙皮复制到多个 targets。"""
    source_skin = find_skin_cluster(source)

    if not source_skin:
        raise RuntimeError(u"源模型没有 SkinCluster：{}".format(source))

    influences = cmds.skinCluster(
        source_skin,
        query=True,
        influence=True
    )

    if influences is None:
        influences = []

    if not influences:
        raise RuntimeError(u"源 SkinCluster 没有影响关节。")

    results = []

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziCopySkinWeights"
    )

    try:
        for target in targets:
            target_skin = find_skin_cluster(target)

            if target_skin:
                cmds.delete(target_skin)

            target_skin = cmds.skinCluster(
                influences,
                target,
                toSelectedBones=True,
                normalizeWeights=1,
                name="sc_{}".format(_short_name(target))
            )[0]

            cmds.copySkinWeights(
                sourceSkin=source_skin,
                destinationSkin=target_skin,
                noMirror=True,
                surfaceAssociation="closestPoint",
                influenceAssociation=[
                    "label",
                    "oneToOne",
                    "closestJoint",
                ]
            )

            results.append(target_skin)
    finally:
        cmds.undoInfo(closeChunk=True)

    return results


def export_skin_weights(geometry, directory):
    """导出一个模型的 deformerWeights XML 与影响关节 JSON。"""
    skin_cluster = find_skin_cluster(geometry)

    if not skin_cluster:
        raise RuntimeError(u"模型没有 SkinCluster：{}".format(geometry))

    if not os.path.isdir(directory):
        os.makedirs(directory)

    short_name = _short_name(geometry)
    xml_name = "sc_{}.xml".format(short_name)
    influence_name = "sc_{}.infs.json".format(short_name)

    cmds.deformerWeights(
        xml_name,
        path=directory,
        export=True,
        deformer=skin_cluster,
        method="index"
    )

    influences = cmds.skinCluster(
        skin_cluster,
        query=True,
        influence=True
    )

    if influences is None:
        influences = []

    influence_path = os.path.join(
        directory,
        influence_name
    )

    with open(influence_path, "w") as file_object:
        json.dump(
            influences,
            file_object,
            ensure_ascii=False,
            indent=4
        )

    return {
        "geometry": geometry,
        "skin_cluster": skin_cluster,
        "xml": os.path.join(directory, xml_name),
        "influences": influence_path,
    }


def import_skin_weights(geometry, directory):
    """导入一个模型的 XML 权重与影响关节列表。"""
    short_name = _short_name(geometry)
    xml_name = "sc_{}.xml".format(short_name)
    influence_name = "sc_{}.infs.json".format(short_name)

    xml_path = os.path.join(
        directory,
        xml_name
    )
    influence_path = os.path.join(
        directory,
        influence_name
    )

    if not os.path.isfile(xml_path):
        raise RuntimeError(u"找不到权重 XML：{}".format(xml_path))

    if not os.path.isfile(influence_path):
        raise RuntimeError(
            u"找不到影响关节文件：{}".format(influence_path)
        )

    with open(influence_path, "r") as file_object:
        influences = json.load(file_object)

    valid_influences = []
    missing_influences = []

    for influence in influences:
        if cmds.objExists(influence):
            valid_influences.append(influence)
        else:
            missing_influences.append(influence)

    if missing_influences:
        raise RuntimeError(
            u"场景缺少影响关节：{}".format(
                ", ".join(missing_influences)
            )
        )

    if not valid_influences:
        raise RuntimeError(u"没有可用于绑定的影响关节。")

    old_skin = find_skin_cluster(geometry)

    if old_skin:
        cmds.delete(old_skin)

    skin_cluster = cmds.skinCluster(
        valid_influences,
        geometry,
        toSelectedBones=True,
        normalizeWeights=1,
        name="sc_{}".format(short_name)
    )[0]

    cmds.deformerWeights(
        xml_name,
        path=directory,
        im=True,
        deformer=skin_cluster,
        method="index"
    )

    cmds.skinCluster(
        skin_cluster,
        edit=True,
        forceNormalizeWeights=True
    )

    return skin_cluster


class SkinTool(QWidget):
    """蒙皮工具窗口。"""

    def __init__(self, parent=None):
        super(SkinTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"Skin Tool",
            minimum_width=560
        )
        self.resize(580, 500)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面部件。"""
        self.title_label = ui_theme.make_title(u"Skin Tool")
        self.subtitle_label = ui_theme.make_subtitle(
            u"绑定、刷权重、权重复制以及 XML 权重文件管理。"
        )

        self.bind_button = QPushButton(u"Smooth Bind")
        self.detach_button = QPushButton(u"Detach Skin")
        self.paint_button = QPushButton(u"Paint Weights")
        self.mirror_button = QPushButton(u"Mirror Weights")

        self.copy_button = QPushButton(u"复制权重")
        self.copy_button.setToolTip(
            u"第一个选择模型作为源，其余选择模型作为目标"
        )
        ui_theme.style_primary(self.copy_button)

        self.export_button = QPushButton(u"导出权重")
        self.import_button = QPushButton(u"导入权重")
        self.select_influences_button = QPushButton(u"选择影响关节")
        self.normalize_button = QPushButton(u"强制归一化")

        self.copy_info_label = QLabel(
            u"复制权重：先选源模型，再选择一个或多个目标模型。"
        )
        self.copy_info_label.setWordWrap(True)
        ui_theme.set_role(self.copy_info_label, "muted")

        self.file_info_label = QLabel(
            u"权重文件使用 sc_<模型名>.xml + sc_<模型名>.infs.json。"
        )
        self.file_info_label.setWordWrap(True)
        ui_theme.set_role(self.file_info_label, "muted")

    def create_layouts(self):
        """创建 Silicon Card 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        maya_card, maya_layout = ui_theme.make_card(self)
        maya_layout.addWidget(
            ui_theme.make_section_title(u"Maya Skin")
        )

        maya_description = QLabel(
            u"快速打开 Maya 自带蒙皮工具和选项。"
        )
        ui_theme.set_role(maya_description, "muted")
        maya_layout.addWidget(maya_description)

        maya_grid = QGridLayout()
        maya_grid.setHorizontalSpacing(8)
        maya_grid.setVerticalSpacing(8)
        maya_grid.addWidget(self.bind_button, 0, 0)
        maya_grid.addWidget(self.detach_button, 0, 1)
        maya_grid.addWidget(self.paint_button, 1, 0)
        maya_grid.addWidget(self.mirror_button, 1, 1)
        maya_layout.addLayout(maya_grid)

        weight_card, weight_layout = ui_theme.make_card(self)
        weight_layout.addWidget(
            ui_theme.make_section_title(u"权重工具")
        )
        weight_layout.addWidget(self.copy_info_label)
        weight_layout.addWidget(self.copy_button)

        utility_layout = QGridLayout()
        utility_layout.setHorizontalSpacing(8)
        utility_layout.setVerticalSpacing(8)
        utility_layout.addWidget(self.select_influences_button, 0, 0)
        utility_layout.addWidget(self.normalize_button, 0, 1)
        weight_layout.addLayout(utility_layout)

        file_card, file_layout = ui_theme.make_card(self)
        file_layout.addWidget(
            ui_theme.make_section_title(u"权重文件")
        )
        file_layout.addWidget(self.file_info_label)

        file_button_layout = QHBoxLayout()
        file_button_layout.setContentsMargins(0, 0, 0, 0)
        file_button_layout.addWidget(self.export_button)
        file_button_layout.addWidget(self.import_button)
        file_layout.addLayout(file_button_layout)

        main_layout.addWidget(maya_card)
        main_layout.addWidget(weight_card)
        main_layout.addWidget(file_card)
        main_layout.addStretch(1)

    def create_connections(self):
        """连接界面信号。"""
        self.bind_button.clicked.connect(
            self.open_smooth_bind_options
        )
        self.detach_button.clicked.connect(
            self.open_detach_skin_options
        )
        self.paint_button.clicked.connect(
            self.open_paint_skin_weights
        )
        self.mirror_button.clicked.connect(
            self.open_mirror_skin_weights_options
        )

        self.copy_button.clicked.connect(self.copy_selected)
        self.export_button.clicked.connect(self.export_selected)
        self.import_button.clicked.connect(self.import_selected)
        self.select_influences_button.clicked.connect(
            self.select_influences
        )
        self.normalize_button.clicked.connect(
            self.normalize_selected
        )

    # -------------------------------------------------------------------------
    # Maya Skin 入口
    # -------------------------------------------------------------------------

    def open_smooth_bind_options(self):
        mel.eval("SmoothBindSkinOptions;")

    def open_detach_skin_options(self):
        mel.eval("DetachSkinOptions;")

    def open_paint_skin_weights(self):
        mel.eval("ArtPaintSkinWeightsToolOptions;")

    def open_mirror_skin_weights_options(self):
        mel.eval("MirrorSkinWeightsOptions;")

    # -------------------------------------------------------------------------
    # 权重操作
    # -------------------------------------------------------------------------

    def copy_selected(self):
        """第一个选择作为源，其余选择作为目标复制权重。"""
        selections = cmds.ls(
            selection=True,
            long=True
        )

        if selections is None:
            selections = []

        if len(selections) < 2:
            cmds.warning(
                u"请先选择源模型，再选择一个或多个目标模型。"
            )
            return

        source = selections[0]
        targets = selections[1:]

        try:
            copy_skin_weights(
                source=source,
                targets=targets
            )
        except Exception as error:
            cmds.warning(str(error))

    def choose_directory(self, title):
        """选择权重目录。"""
        scene_path = cmds.file(
            query=True,
            sceneName=True
        )

        if scene_path is None:
            scene_path = ""

        start_directory = os.path.dirname(scene_path)

        return QFileDialog.getExistingDirectory(
            self,
            title,
            start_directory
        )

    def export_selected(self):
        """导出选择模型权重。"""
        geometries = cmds.ls(
            selection=True,
            long=True
        )

        if geometries is None:
            geometries = []

        if not geometries:
            cmds.warning(u"请选择需要导出权重的模型。")
            return

        directory = self.choose_directory(u"选择权重导出目录")

        if not directory:
            return

        success_count = 0

        for geometry in geometries:
            try:
                export_skin_weights(
                    geometry,
                    directory
                )
                success_count += 1
            except Exception as error:
                cmds.warning(str(error))

        print(
            u"[Skin Tool] 已导出 {} 个模型的权重。".format(
                success_count
            )
        )

    def import_selected(self):
        """从选择目录导入权重到选择模型。"""
        geometries = cmds.ls(
            selection=True,
            long=True
        )

        if geometries is None:
            geometries = []

        if not geometries:
            cmds.warning(u"请选择需要导入权重的模型。")
            return

        directory = self.choose_directory(u"选择权重目录")

        if not directory:
            return

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziImportSkinWeights"
        )

        try:
            for geometry in geometries:
                try:
                    import_skin_weights(
                        geometry,
                        directory
                    )
                except Exception as error:
                    cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    def select_influences(self):
        """选择当前模型 SkinCluster 的影响 Joint。"""
        geometries = cmds.ls(
            selection=True,
            long=True
        )

        if geometries is None:
            geometries = []

        if not geometries:
            cmds.warning(u"请先选择蒙皮模型。")
            return

        influences = []

        for geometry in geometries:
            skin_cluster = find_skin_cluster(geometry)

            if not skin_cluster:
                continue

            skin_influences = cmds.skinCluster(
                skin_cluster,
                query=True,
                influence=True
            )

            if skin_influences is None:
                skin_influences = []

            for influence in skin_influences:
                if influence not in influences:
                    influences.append(influence)

        if influences:
            cmds.select(
                influences,
                replace=True
            )
        else:
            cmds.warning(u"选择的模型没有找到影响关节。")

    def normalize_selected(self):
        """强制归一化选择模型的 Skin 权重。"""
        geometries = cmds.ls(
            selection=True,
            long=True
        )

        if geometries is None:
            geometries = []

        if not geometries:
            cmds.warning(u"请先选择蒙皮模型。")
            return

        for geometry in geometries:
            skin_cluster = find_skin_cluster(geometry)

            if not skin_cluster:
                continue

            cmds.skinCluster(
                skin_cluster,
                edit=True,
                forceNormalizeWeights=True
            )


def main():
    """创建 Skin Tool 窗口。"""
    window = SkinTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
