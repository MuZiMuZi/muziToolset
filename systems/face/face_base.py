# coding=utf-8
u"""
Face Rig 公共基础类
==================

负责：
    1. Face Rig 公共配置；
    2. Face Rig 公共层级名称；
    3. 确保基础层级存在；
    4. 确保 Config Network Node 存在；
    5. 读取 Config Node 中保存的数据。

说明：
    正式系统代码不在模块 import 时主动 reload 依赖。
    热重载由开发阶段的专用入口负责，避免 Maya 中出现旧类实例和新模块混用。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import attrUtils
from ...core import hierarchyUtils
from . import config


class FaceBase(object):
    u"""所有 Face Rig Step 共用的基础类。"""

    def __init__(self):
        # ------------------------------------------------------------
        # Face Rig 基础配置
        # ------------------------------------------------------------
        self.face_side = config.face_side
        self.face_center_axis = config.face_center_axis

        # ------------------------------------------------------------
        # Config Node
        # ------------------------------------------------------------
        self.config_node = config.config_node

        # ------------------------------------------------------------
        # Face Rig 主层级
        # ------------------------------------------------------------
        self.face_master_grp = config.face_master_grp
        self.face_model_grp = config.face_model_grp

        # ------------------------------------------------------------
        # Face Rig 功能组
        # ------------------------------------------------------------
        self.face_guide_grp = config.face_guide_grp
        self.face_ctrl_grp = config.face_ctrl_grp
        self.face_jnt_grp = config.face_jnt_grp
        self.face_rig_nodes_grp = config.face_rig_nodes_grp
        self.face_pos_driver_grp = config.face_pos_driver_grp

        # ------------------------------------------------------------
        # 模型工作层
        # ------------------------------------------------------------
        self.face_tweak_grp = config.face_tweak_grp
        self.face_stretch_grp = config.face_stretch_grp
        self.face_deform_grp = config.face_deform_grp

        # ------------------------------------------------------------
        # 层级列表
        # ------------------------------------------------------------
        self.type_groups = config.type_grp_list
        self.model_groups = config.model_grp_list

    # =========================================================================
    # Hierarchy
    # =========================================================================

    def ensure_hierarchy(self):
        u"""确保 Face Rig 基础层级存在。"""
        if not cmds.objExists(self.face_master_grp):
            hierarchyUtils.Hierarchy.create_grp(
                self.face_master_grp
            )

        if not cmds.objExists(self.face_model_grp):
            hierarchyUtils.Hierarchy.create_grp(
                self.face_model_grp,
                parent=self.face_master_grp
            )

        for group_name in self.type_groups:
            if cmds.objExists(group_name):
                continue

            hierarchyUtils.Hierarchy.create_grp(
                group_name,
                parent=self.face_master_grp
            )

        for group_name in self.model_groups:
            if cmds.objExists(group_name):
                continue

            hierarchyUtils.Hierarchy.create_grp(
                group_name,
                parent=self.face_model_grp
            )

        return True

    # =========================================================================
    # Config Node
    # =========================================================================

    def ensure_config_node(self):
        u"""确保 Face Rig Config Network Node 存在。"""
        if cmds.objExists(self.config_node):
            node_type = cmds.nodeType(self.config_node)

            if node_type != "network":
                raise RuntimeError(
                    u"Config 节点名称已经被其他类型节点占用: {0}，"
                    u"当前节点类型为: {1}".format(
                        self.config_node,
                        node_type
                    )
                )

            return self.config_node

        config_node = cmds.createNode(
            "network",
            name=self.config_node
        )

        self.config_node = config_node
        return config_node

    def config_node_exists(self):
        u"""检查 Face Rig Config Node 是否存在。"""
        if not cmds.objExists(self.config_node):
            return False

        if cmds.nodeType(self.config_node) != "network":
            return False

        return True

    # =========================================================================
    # Config Attr
    # =========================================================================

    def get_config_attr(self):
        u"""获取 Face Rig Config 节点的 Attr 操作对象。"""
        config_attr = attrUtils.Attr(self.config_node)
        return config_attr

    def get_config_message(self, attr_name):
        u"""读取 Config Node 中保存的 Maya 节点消息连接。"""
        if not self.config_node_exists():
            return None

        config_attr = self.get_config_attr()
        node = config_attr.get_message(attr_name)
        return node

    def get_config_value(self, attr_name):
        u"""读取 Config Node 中保存的普通属性值。"""
        if not self.config_node_exists():
            return None

        config_attr = self.get_config_attr()
        value = config_attr.get_attr_value(attr_name)
        return value
