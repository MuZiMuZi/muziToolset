# coding=utf-8
u"""绑定库应用服务：配置持久化、场景检查和正式 Module 构建调度。"""

import copy
import json
import os

from . import library_catalog as catalog
from ... import config


class RigLibraryService(object):
    u"""管理当前场景的一套绑定库配置；Maya 依赖只在创建服务时加载。"""

    config_node = "network_md_rig_library_config_001"
    config_attr = "muziRigLibraryJson"
    owner_attr = "muziRigLibraryOwner"
    module_attr = "muziRigLibraryModule"
    root = "grp_md_rig_library_001"
    joint_root = "grp_md_rig_jnt_001"
    control_root = "grp_md_rig_ctrl_001"

    def __init__(self, commands=None):
        u"""可注入命令对象用于检查调度行为；正常运行直接使用 maya.cmds。"""
        if commands is None:
            import maya.cmds as commands
        self.cmds = commands
        self.document = catalog.new_document()
        self.reload()

    def _config_exists(self):
        u"""只接受本工具写入的 Network，避免覆盖同名用户节点。"""
        if not self.cmds.objExists(self.config_node):
            return False
        if self.cmds.nodeType(self.config_node) != "network":
            raise RuntimeError(u"绑定库配置名称被其他节点占用。")
        if not self.cmds.attributeQuery(self.config_attr, node=self.config_node, exists=True):
            raise RuntimeError(u"同名 Network 不属于绑定库。")
        return True

    def reload(self):
        u"""从场景恢复配置；不在打开窗口时创建或更改场景节点。"""
        document = catalog.new_document()
        if self._config_exists():
            raw = self.cmds.getAttr(self.config_node + "." + self.config_attr)
            document = catalog.validate_document(json.loads(raw))
        self.document = document
        return self.document

    def _commit(self, document, action=None, label="Muzi Rig Library"):
        u"""配置和对应场景操作放在同一个 Undo Chunk；失败时整体回滚。"""
        candidate = catalog.validate_document(document)
        if self.cmds.namespaceInfo(currentNamespace=True) not in (":", ""):
            raise RuntimeError(u"当前版本请在根命名空间中操作绑定库。")
        if not self.cmds.undoInfo(query=True, state=True):
            raise RuntimeError(u"请先开启 Maya Undo，再执行绑定库操作。")
        exists = self._config_exists()
        changed = False
        failure = None
        self.cmds.undoInfo(openChunk=True, chunkName=label)
        try:
            if not exists:
                self.cmds.createNode("network", name=self.config_node, skipSelect=True)
                changed = True
                self.cmds.addAttr(self.config_node, longName=self.config_attr, dataType="string")
            # 首次写入保证这个 Chunk 拥有自己的可撤销操作，避免失败时撤销用户上一步。
            self.cmds.setAttr(self.config_node + "." + self.config_attr,
                              json.dumps(candidate, ensure_ascii=False), type="string")
            changed = True
            if action is not None:
                action(candidate)
            candidate = catalog.validate_document(candidate)
            self.cmds.setAttr(self.config_node + "." + self.config_attr,
                              json.dumps(candidate, ensure_ascii=False), type="string")
        except Exception as error:
            failure = error
        finally:
            self.cmds.undoInfo(closeChunk=True)
        if failure is not None:
            if changed:
                self.cmds.undo()
            raise failure
        self.document = candidate
        return candidate

    def add_module(self, kind):
        u"""添加模块配置；耳朵自动选择空闲侧，通用 FK 自动分配可读名称。"""
        document = copy.deepcopy(self.document)
        record = catalog.new_module(kind)
        used = set()
        for item in document["modules"]:
            used.add((item["side"], item["name"]))
        if kind == "ear" and ("lf", "ear") in used:
            record = catalog.new_module(kind, "rt")
        if kind == "fk_chain":
            index = 1
            while (record["side"], record["name"]) in used:
                record["name"] = "chain_{:02d}".format(index)
                index += 1
        document["modules"].append(record)
        self._commit(document)
        return record["id"]

    def add_template(self, key):
        u"""添加已实现模块的组合，不重复插入相同模块。"""
        candidate = catalog.add_template(self.document, key)
        if candidate != self.document:
            self._commit(candidate)

    def remove_module(self, identity):
        u"""移除尚未构建的配置；已构建绑定不会通过列表删除。"""
        document = copy.deepcopy(self.document)
        for record in document["modules"]:
            if record["id"] == identity:
                if record["built"]:
                    raise RuntimeError(u"已构建模块不能从配置中移除；可使用 Maya Undo 撤销构建。")
                document["modules"].remove(record)
                break
        self._commit(document)

    def update_module(self, identity, values):
        u"""更新参数；已构建模块仅允许显示与控制器外观调整。"""
        document = copy.deepcopy(self.document)
        previous = None
        updated = None
        for record in document["modules"]:
            if record["id"] == identity:
                previous = copy.deepcopy(record)
                allowed = {"enabled", "name", "side", "guides", "ctrl_size", "ctrl_color",
                           "ctrl_axis", "jnt_radius", "show_axis", "show_joints", "show_controls"}
                if record["built"]:
                    allowed = {"ctrl_size", "ctrl_color", "ctrl_axis", "jnt_radius",
                               "show_axis", "show_joints", "show_controls"}
                if not set(values).issubset(allowed):
                    raise ValueError(u"当前模块状态不允许修改这些参数。")
                record.update(values)
                updated = record
                break
        if previous is None:
            raise ValueError(u"没有找到当前模块。")
        if updated == previous:
            return
        catalog.validate_document(document)
        if previous["built"]:
            errors = self._check_built(previous)
            if errors:
                raise RuntimeError("\n".join(errors))

        def apply(candidate):
            if previous["built"]:
                self._apply_display(updated, previous)

        self._commit(document, apply, "Muzi Module Properties")

    def _owned_group(self, name):
        u"""检查场景中的固定根组是否属于当前绑定库。"""
        if not self.cmds.objExists(name):
            return False
        if self.cmds.nodeType(name) != "transform":
            raise RuntimeError(u"{} 已被非 Transform 节点占用。".format(name))
        if not self.cmds.attributeQuery(self.owner_attr, node=name, exists=True):
            raise RuntimeError(u"{} 已存在且不属于绑定库。".format(name))
        if self.cmds.getAttr(name + "." + self.owner_attr) != self.config_node:
            raise RuntimeError(u"{} 属于另一套绑定。".format(name))
        return True

    def _prepare_roots(self):
        u"""创建本工具拥有的根组，不自动认领场景中已有同名对象。"""
        for name in (self.root, self.joint_root, self.control_root):
            if self._owned_group(name):
                continue
            if name == self.root:
                self.cmds.createNode("transform", name=name, skipSelect=True)
            else:
                self.cmds.createNode("transform", name=name, parent=self.root, skipSelect=True)
            self.cmds.addAttr(name, longName=self.owner_attr, dataType="string")
            self.cmds.setAttr(name + "." + self.owner_attr, self.config_node, type="string")

    def setup(self):
        u"""Step 01：保存配置并准备独立的 Rig / Joint / Controller 根组。"""
        self._commit(self.document, lambda document: self._prepare_roots(), "Muzi Rig Setup")

    def import_guide(self):
        u"""Step 02：复用仓库现有 Face Guide 模板导入入口。"""
        from ...core.rigging.guide_utils import Guide

        def apply(document):
            Guide("face").import_template()

        self._commit(self.document, apply, "Muzi Import Face Guide")

    def _check_built(self, record):
        u"""检查已构建模块是否完整，缺失节点时不尝试重建或覆盖剩余绑定。"""
        errors = []
        for nodes in catalog.output_names(record).values():
            for name in nodes:
                if not self.cmds.objExists(name):
                    errors.append(u"已构建节点缺失：{}".format(name))
                elif record["built"]:
                    if not self.cmds.attributeQuery(self.module_attr, node=name, exists=True):
                        errors.append(u"节点归属信息缺失：{}".format(name))
                    elif self.cmds.getAttr(name + "." + self.module_attr) != record["id"]:
                        errors.append(u"节点不属于当前模块：{}".format(name))
        return errors

    def validate(self):
        u"""只读预检查：验证 Guide 数量、节点类型、重复路径和输出名称冲突。"""
        catalog.validate_document(self.document)
        errors = []
        active = 0
        for record in self.document["modules"]:
            if not record["enabled"]:
                continue
            active += 1
            if record["built"]:
                errors.extend(self._check_built(record))
                continue
            names = catalog.guide_names(record)
            if not names:
                errors.append(u"{}：请按链条顺序指定 Guide。".format(record["name"]))
            resolved = set()
            for name in names:
                found = self.cmds.ls(name, long=True) or []
                if len(found) != 1:
                    errors.append(u"Guide 不存在或名称不唯一：{}".format(name))
                    continue
                if found[0] in resolved:
                    errors.append(u"同一个 Guide 被重复使用：{}".format(name))
                resolved.add(found[0])
                if self.cmds.nodeType(found[0]) not in ("transform", "joint"):
                    errors.append(u"Guide 必须为 Transform 或 Joint：{}".format(name))
            for nodes in catalog.output_names(record).values():
                for name in nodes:
                    if self.cmds.objExists(name):
                        errors.append(u"输出名称已存在，停止构建：{}".format(name))
        if not active:
            errors.append(u"请先添加并启用至少一个模块。")
        for name in (self.root, self.joint_root, self.control_root):
            try:
                self._owned_group(name)
            except RuntimeError as error:
                errors.append(str(error))
        return errors

    def _make_builder(self, record):
        u"""仅调度正式实现；具体 FK 绑定算法仍由原 Module 负责。"""
        from ..face.ear_module import EarModule
        from ..face.tongue_module import TongueModule
        from ..components.fk_chain import FKChain

        builders = {"ear": EarModule, "tongue": TongueModule, "fk_chain": FKChain}
        builder = builders[record["kind"]](
            module=record["name"], side=record["side"], guide=catalog.guide_names(record),
            jnt_parent=self.joint_root, ctrl_parent=self.control_root,
            ctrl_axis=record["ctrl_axis"])
        builder.ctrl_size = record["ctrl_size"]
        builder.ctrl_color = record["ctrl_color"]
        return builder

    def build(self):
        u"""Step 03：一次构建所有启用的待建模块；已有绑定不会再次运行 build。"""
        errors = self.validate()
        if errors:
            raise RuntimeError("\n".join(errors))
        pending = []
        for record in self.document["modules"]:
            if record["enabled"] and not record["built"]:
                pending.append(record)
        if not pending:
            return 0

        def apply(document):
            self._prepare_roots()
            for record in document["modules"]:
                if not record["enabled"] or record["built"]:
                    continue
                builder = self._make_builder(record)
                builder.build()
                errors = self._check_built(record)
                if errors:
                    raise RuntimeError("\n".join(errors))
                for nodes in catalog.output_names(record).values():
                    for name in nodes:
                        self.cmds.addAttr(name, longName=self.module_attr, dataType="string")
                        self.cmds.setAttr(name + "." + self.module_attr, record["id"], type="string")
                self._apply_display(record)
                record["built"] = True

        self._commit(self.document, apply, "Muzi Build Modules")
        return len(pending)

    def _apply_display(self, record, previous=None):
        u"""只修改本模块的显示属性和 Curve CV，保留控制器位置与连接。"""
        from ...core.rigging.ctrl_utils import Ctrl
        from ...core.rigging.jnt_utils import Jnt

        outputs = catalog.output_names(record)
        if previous is not None:
            scale_ratio = record["ctrl_size"] / previous["ctrl_size"]
            for name in outputs["controls"] + outputs["subcontrols"]:
                ctrl = Ctrl(name)
                if scale_ratio != 1.0:
                    ctrl.set_ctrl_size(scale_ratio)
                if record["ctrl_color"] != previous["ctrl_color"]:
                    ctrl.set_ctrl_color(record["ctrl_color"])
                if record["ctrl_axis"] != previous["ctrl_axis"]:
                    ctrl.set_ctrl_axis(record["ctrl_axis"])
        for name in outputs["joints"]:
            Jnt(name).set_radius(record["jnt_radius"])
            self.cmds.setAttr(name + ".displayLocalAxis", record["show_axis"])
        self.cmds.setAttr(outputs["groups"][0] + ".visibility", record["show_joints"])
        self.cmds.setAttr(outputs["groups"][1] + ".visibility", record["show_controls"])

    def selected_guides(self):
        u"""读取 Maya 当前选择顺序；UI 允许按行修正最终链条顺序。"""
        return self.cmds.ls(orderedSelection=True, long=True, transforms=True) or []

    def node_exists(self, name):
        u"""查询结构项是否已存在于场景，不创建占位节点。"""
        return self.cmds.objExists(name)

    def select_nodes(self, names):
        u"""从结构树选择对应场景节点，不清空用户选择来表示不存在的节点。"""
        existing = []
        for name in names:
            if self.cmds.objExists(name):
                existing.append(name)
        if existing:
            self.cmds.select(existing, replace=True)

    def export_recipe(self, path):
        u"""导出可复用配置；剥离构建状态，不伪装成包含场景绑定的备份。"""
        document = copy.deepcopy(self.document)
        for record in document["modules"]:
            record["built"] = False
        with open(path, "w", encoding="utf-8") as stream:
            json.dump(document, stream, ensure_ascii=False, indent=2)

    def import_recipe(self, path):
        u"""完整校验 JSON 后追加配置，冲突时整次导入不生效。"""
        if os.path.getsize(path) > 2 * 1024 * 1024:
            raise ValueError(u"配置文件过大。")
        with open(path, "r", encoding="utf-8") as stream:
            incoming = catalog.validate_document(json.load(stream))
        document = copy.deepcopy(self.document)
        for record in incoming["modules"]:
            record["built"] = False
            document["modules"].append(record)
        self._commit(document)
