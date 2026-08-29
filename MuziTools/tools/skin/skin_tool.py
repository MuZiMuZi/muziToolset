# coding=utf-8
u"""
Skin Tool
=========

Maya 2023 / PySide2 蒙皮工具。

功能：
    - Maya Smooth Bind / Detach / Paint / Mirror 选项入口；
    - 复制 Skin Weight；
    - XML 权重导出 / 导入；
    - 选择 SkinCluster 影响关节；
    - 强制归一化权重。

不依赖 PyMel。
"""

from __future__ import print_function

import json
import os

import maya.cmds as cmds
import maya.mel as mel

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget

from ....core import qtUtils


_window = None


def _short_name(node):
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

    history = cmds.listHistory(geometry) or []
    skin_clusters = cmds.ls(history, type="skinCluster") or []

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
    ) or []

    if not influences:
        raise RuntimeError(u"源 SkinCluster 没有影响关节。")

    results = []

    cmds.undoInfo(openChunk=True, chunkName="MuziCopySkinWeights")
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
    ) or []

    influence_path = os.path.join(directory, influence_name)
    with open(influence_path, "w") as file_obj:
        json.dump(
            influences,
            file_obj,
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

    xml_path = os.path.join(directory, xml_name)
    influence_path = os.path.join(directory, influence_name)

    if not os.path.isfile(xml_path):
        raise RuntimeError(u"找不到权重 XML：{}".format(xml_path))

    if not os.path.isfile(influence_path):
        raise RuntimeError(u"找不到影响关节文件：{}".format(influence_path))

    with open(influence_path, "r") as file_obj:
        influences = json.load(file_obj)

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
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(SkinTool, self).__init__(parent)
        self.setWindowTitle(u"Skin Tool")
        self.setMinimumWidth(420)

        self.bind_btn = QPushButton(u"Smooth Bind 选项")
        self.detach_btn = QPushButton(u"Detach Skin 选项")
        self.paint_btn = QPushButton(u"Paint Skin Weights")
        self.mirror_btn = QPushButton(u"Mirror Skin Weights 选项")

        self.copy_btn = QPushButton(u"复制权重：源 -> 多目标")
        self.export_btn = QPushButton(u"导出选择模型权重")
        self.import_btn = QPushButton(u"导入选择模型权重")
        self.select_influences_btn = QPushButton(u"选择影响关节")
        self.normalize_btn = QPushButton(u"强制归一化权重")

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        maya_group = QGroupBox(u"Maya Skin")
        maya_layout = QGridLayout(maya_group)
        maya_layout.addWidget(self.bind_btn, 0, 0)
        maya_layout.addWidget(self.detach_btn, 0, 1)
        maya_layout.addWidget(self.paint_btn, 1, 0)
        maya_layout.addWidget(self.mirror_btn, 1, 1)
        main_layout.addWidget(maya_group)

        utility_group = QGroupBox(u"权重工具")
        utility_layout = QVBoxLayout(utility_group)
        utility_layout.addWidget(self.copy_btn)
        utility_layout.addWidget(self.export_btn)
        utility_layout.addWidget(self.import_btn)
        utility_layout.addWidget(self.select_influences_btn)
        utility_layout.addWidget(self.normalize_btn)
        main_layout.addWidget(utility_group)

    def _create_connections(self):
        self.bind_btn.clicked.connect(
            lambda: mel.eval("SmoothBindSkinOptions;")
        )
        self.detach_btn.clicked.connect(
            lambda: mel.eval("DetachSkinOptions;")
        )
        self.paint_btn.clicked.connect(
            lambda: mel.eval("ArtPaintSkinWeightsToolOptions;")
        )
        self.mirror_btn.clicked.connect(
            lambda: mel.eval("MirrorSkinWeightsOptions;")
        )

        self.copy_btn.clicked.connect(self.copy_selected)
        self.export_btn.clicked.connect(self.export_selected)
        self.import_btn.clicked.connect(self.import_selected)
        self.select_influences_btn.clicked.connect(self.select_influences)
        self.normalize_btn.clicked.connect(self.normalize_selected)

    @staticmethod
    def copy_selected():
        selections = cmds.ls(selection=True, long=True) or []
        if len(selections) < 2:
            cmds.warning(u"请先选择源模型，再选择一个或多个目标模型。")
            return

        try:
            copy_skin_weights(
                source=selections[0],
                targets=selections[1:]
            )
        except Exception as error:
            cmds.warning(str(error))

    def _choose_directory(self, title):
        scene_path = cmds.file(query=True, sceneName=True) or ""
        start_directory = os.path.dirname(scene_path)

        return QFileDialog.getExistingDirectory(
            self,
            title,
            start_directory
        )

    def export_selected(self):
        geometries = cmds.ls(selection=True, long=True) or []
        if not geometries:
            cmds.warning(u"请选择需要导出权重的模型。")
            return

        directory = self._choose_directory(u"选择权重导出目录")
        if not directory:
            return

        success_count = 0
        for geometry in geometries:
            try:
                export_skin_weights(geometry, directory)
                success_count += 1
            except Exception as error:
                cmds.warning(str(error))

        print(
            u"[Skin Tool] 已导出 {} 个模型的权重。".format(
                success_count
            )
        )

    def import_selected(self):
        geometries = cmds.ls(selection=True, long=True) or []
        if not geometries:
            cmds.warning(u"请选择需要导入权重的模型。")
            return

        directory = self._choose_directory(u"选择权重目录")
        if not directory:
            return

        cmds.undoInfo(openChunk=True, chunkName="MuziImportSkinWeights")
        try:
            for geometry in geometries:
                try:
                    import_skin_weights(geometry, directory)
                except Exception as error:
                    cmds.warning(str(error))
        finally:
            cmds.undoInfo(closeChunk=True)

    @staticmethod
    def select_influences():
        geometries = cmds.ls(selection=True, long=True) or []
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
            ) or []

            for influence in skin_influences:
                if influence not in influences:
                    influences.append(influence)

        if influences:
            cmds.select(influences, replace=True)
        else:
            cmds.warning(u"选择的模型没有找到影响关节。")

    @staticmethod
    def normalize_selected():
        geometries = cmds.ls(selection=True, long=True) or []
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
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = SkinTool()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window
