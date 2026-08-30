# coding=utf-8
u"""
Step 02 - Face Guide
====================

负责读取 Step 01 保存的模型配置，并为后续 Face Guide 构建准备数据。

当前已实现：
    1. 读取 Step 01 模型和嘴唇 Joint 数量；
    2. 把 zero_lf_* + loc_lf_* Guide 层级镜像为 rt；
    3. 右侧 Locator Transform 属性由对应左侧 Locator 直接驱动；
    4. 右侧 Zero Group 负责 X 轴空间镜像；
    5. 根据部位名称统一设置 Guide Locator 的 Viewport / Outliner 颜色。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import config
from . import face_base


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02。"""

    def __init__(self):
        super(FaceGuide, self).__init__()

        self.step_value = 2

        self.face_head_model = self.get_config_message(
            "face_head_model"
        )
        self.face_lf_eye_model = self.get_config_message(
            "face_lf_eye_model"
        )
        self.face_rt_eye_model = self.get_config_message(
            "face_rt_eye_model"
        )
        self.upper_teech_model = self.get_config_message(
            "upper_teech_model"
        )
        self.lower_teech_model = self.get_config_message(
            "lower_teech_model"
        )
        self.face_tongue_model = self.get_config_message(
            "face_tongue_model"
        )
        self.face_gum_model = self.get_config_message(
            "face_gum_model"
        )

        self.mouth_jnt_number = self.get_config_value(
            "mouth_jnt_number"
        )

    # =========================================================================
    # Validate
    # =========================================================================

    def validate_setup(self):
        u"""检查 Step 01 是否已经提供基本数据。"""
        if not self.face_head_model:
            raise RuntimeError(
                u"没有读取到 Face Head Model，请先完成 Face Setup。"
            )

        if self.mouth_jnt_number is None:
            raise RuntimeError(
                u"没有读取到嘴唇关节数量，请先完成 Face Setup。"
            )

        return True

    # =========================================================================
    # Guide Color
    # =========================================================================

    @staticmethod
    def get_locator_shapes(locator):
        u"""获取 Locator Transform 下全部有效 Locator Shape。"""
        shapes = cmds.listRelatives(
            locator,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="locator"
        )

        if shapes is None:
            shapes = []

        return shapes

    def get_guide_locator_color(self, locator):
        u"""根据 Guide Locator 名称返回对应部位颜色。"""
        short_name = self.get_short_name(locator)
        short_name = short_name.lower()

        for name_token, color in config.guide_locator_color_rules:
            if name_token not in short_name:
                continue

            return color

        return None

    def set_guide_locator_color(self, locator, color):
        u"""
        设置单个 Guide Locator 的颜色。

        Viewport：
            Locator Shape 使用 RGB Drawing Override。

        Outliner：
            Locator Transform 使用 Outliner Color。
        """
        if not cmds.objExists(locator):
            raise RuntimeError(
                u"Guide Locator 不存在: {}".format(
                    locator
                )
            )

        if color is None:
            return False

        red = float(color[0])
        green = float(color[1])
        blue = float(color[2])

        if cmds.attributeQuery(
                "useOutlinerColor",
                node=locator,
                exists=True
        ):
            cmds.setAttr(
                locator + ".useOutlinerColor",
                True
            )

        if cmds.attributeQuery(
                "outlinerColor",
                node=locator,
                exists=True
        ):
            cmds.setAttr(
                locator + ".outlinerColor",
                red,
                green,
                blue,
                type="float3"
            )

        shapes = self.get_locator_shapes(
            locator
        )

        for shape in shapes:
            cmds.setAttr(
                shape + ".overrideEnabled",
                True
            )
            cmds.setAttr(
                shape + ".overrideRGBColors",
                True
            )
            cmds.setAttr(
                shape + ".overrideColorRGB",
                red,
                green,
                blue,
                type="float3"
            )

        return True

    def get_guide_locators(self, parent_group=None):
        u"""获取指定层级下全部 loc_*_guide_* Locator Transform。"""
        locators = []

        if parent_group:
            if not cmds.objExists(parent_group):
                raise RuntimeError(
                    u"Guide Parent Group 不存在: {}".format(
                        parent_group
                    )
                )

            descendants = cmds.listRelatives(
                parent_group,
                allDescendents=True,
                type="transform",
                fullPath=True
            )

            if descendants is None:
                descendants = []

            for node in descendants:
                short_name = self.get_short_name(node)

                if not short_name.startswith("loc_"):
                    continue

                if "_guide_" not in short_name:
                    continue

                shapes = self.get_locator_shapes(
                    node
                )

                if not shapes:
                    continue

                locators.append(node)

        else:
            matches = cmds.ls(
                "loc_*_guide_*",
                type="transform",
                long=True
            )

            if matches is None:
                matches = []

            for node in matches:
                shapes = self.get_locator_shapes(
                    node
                )

                if not shapes:
                    continue

                locators.append(node)

        locators.sort()
        return locators

    def apply_guide_locator_colors(self, parent_group=None):
        u"""根据命名规则批量更新 Face Guide Locator 颜色。"""
        locators = self.get_guide_locators(
            parent_group=parent_group
        )

        colored_locators = []
        skipped_locators = []

        for locator in locators:
            color = self.get_guide_locator_color(
                locator
            )

            if color is None:
                skipped_locators.append(
                    locator
                )
                continue

            self.set_guide_locator_color(
                locator,
                color
            )

            colored_locators.append(
                locator
            )

        return {
            "colored": colored_locators,
            "skipped": skipped_locators,
        }

    # =========================================================================
    # Guide Mirror
    # =========================================================================

    @staticmethod
    def get_short_name(node):
        u"""返回 DAG 节点短名称。"""
        return node.split("|")[-1]

    @staticmethod
    def get_right_name(left_name):
        u"""把 lf 命名转换为对应 rt 命名。"""
        if "_lf_" not in left_name:
            raise ValueError(
                u"节点名称中没有 _lf_，无法生成右侧名称: {}".format(
                    left_name
                )
            )

        return left_name.replace(
            "_lf_",
            "_rt_",
            1
        )

    @staticmethod
    def get_node_under_parent(parent, short_name):
        u"""获取指定 Parent 下的直接子 Transform。"""
        if parent:
            children = cmds.listRelatives(
                parent,
                children=True,
                type="transform",
                fullPath=True
            )

            if children is None:
                children = []

            for child in children:
                child_short_name = child.split("|")[-1]

                if child_short_name == short_name:
                    return child

            return None

        matches = cmds.ls(
            short_name,
            type="transform",
            long=True
        )

        if matches is None:
            matches = []

        if len(matches) == 1:
            return matches[0]

        return None

    @staticmethod
    def get_parent(node):
        u"""返回节点的直接 Parent。"""
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

    def get_left_zero_groups(self, parent_group=None):
        u"""查找需要镜像的 zero_lf_* Guide Group。"""
        left_zero_groups = []

        if parent_group:
            if not cmds.objExists(parent_group):
                raise RuntimeError(
                    u"Guide Parent Group 不存在: {}".format(
                        parent_group
                    )
                )

            descendants = cmds.listRelatives(
                parent_group,
                allDescendents=True,
                type="transform",
                fullPath=True
            )

            if descendants is None:
                descendants = []

            for node in descendants:
                short_name = self.get_short_name(node)

                if not short_name.startswith("zero_lf_"):
                    continue

                left_zero_groups.append(node)

        else:
            matches = cmds.ls(
                "zero_lf_*",
                type="transform",
                long=True
            )

            if matches is None:
                matches = []

            for node in matches:
                left_zero_groups.append(node)

        left_zero_groups.sort()
        return left_zero_groups

    def get_left_locator(self, left_zero_group):
        u"""获取 zero_lf_* 下对应的 loc_lf_* Transform。"""
        children = cmds.listRelatives(
            left_zero_group,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        for child in children:
            short_name = self.get_short_name(child)

            if short_name.startswith("loc_lf_"):
                return child

        return None

    def create_or_update_right_zero(self, left_zero_group):
        u"""创建或更新对应 zero_rt_*，并在 Parent Local X 轴做镜像。"""
        left_zero_name = self.get_short_name(left_zero_group)
        right_zero_name = self.get_right_name(left_zero_name)
        parent_group = self.get_parent(left_zero_group)

        right_zero_group = self.get_node_under_parent(
            parent_group,
            right_zero_name
        )

        if right_zero_group is None:
            right_zero_group = cmds.createNode(
                "transform",
                name=right_zero_name
            )

            if parent_group:
                right_zero_group = cmds.parent(
                    right_zero_group,
                    parent_group
                )[0]

        rotate_order = cmds.getAttr(
            left_zero_group + ".rotateOrder"
        )
        cmds.setAttr(
            right_zero_group + ".rotateOrder",
            rotate_order
        )

        translate_x = cmds.getAttr(
            left_zero_group + ".translateX"
        )
        translate_y = cmds.getAttr(
            left_zero_group + ".translateY"
        )
        translate_z = cmds.getAttr(
            left_zero_group + ".translateZ"
        )

        rotate_x = cmds.getAttr(
            left_zero_group + ".rotateX"
        )
        rotate_y = cmds.getAttr(
            left_zero_group + ".rotateY"
        )
        rotate_z = cmds.getAttr(
            left_zero_group + ".rotateZ"
        )

        scale_x = cmds.getAttr(
            left_zero_group + ".scaleX"
        )
        scale_y = cmds.getAttr(
            left_zero_group + ".scaleY"
        )
        scale_z = cmds.getAttr(
            left_zero_group + ".scaleZ"
        )

        cmds.setAttr(
            right_zero_group + ".translateX",
            -translate_x
        )
        cmds.setAttr(
            right_zero_group + ".translateY",
            translate_y
        )
        cmds.setAttr(
            right_zero_group + ".translateZ",
            translate_z
        )

        cmds.setAttr(
            right_zero_group + ".rotateX",
            rotate_x
        )
        cmds.setAttr(
            right_zero_group + ".rotateY",
            rotate_y
        )
        cmds.setAttr(
            right_zero_group + ".rotateZ",
            rotate_z
        )

        # 右侧 Zero 的负 X Scale 建立镜像 Local Space。
        # 这样右侧 Locator 可以直接连接左侧 Locator 的 Local Transform，
        # 而不需要给每个 Locator 再创建 multiplyDivide。
        cmds.setAttr(
            right_zero_group + ".scaleX",
            -scale_x
        )
        cmds.setAttr(
            right_zero_group + ".scaleY",
            scale_y
        )
        cmds.setAttr(
            right_zero_group + ".scaleZ",
            scale_z
        )

        return right_zero_group

    def create_or_update_right_locator(
            self,
            left_locator,
            right_zero_group
    ):
        u"""创建或复用对应 loc_rt_*。"""
        left_locator_name = self.get_short_name(left_locator)
        right_locator_name = self.get_right_name(left_locator_name)

        right_locator = self.get_node_under_parent(
            right_zero_group,
            right_locator_name
        )

        if right_locator is None:
            right_locator = cmds.spaceLocator(
                name=right_locator_name
            )[0]
            right_locator = cmds.parent(
                right_locator,
                right_zero_group
            )[0]

        return right_locator

    @staticmethod
    def connect_locator_transform(
            left_locator,
            right_locator
    ):
        u"""把左侧 Locator Transform 属性直接连接到右侧。"""
        attributes = [
            "translateX",
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ",
            "scaleX",
            "scaleY",
            "scaleZ",
            "rotateOrder",
            "visibility",
        ]

        for attribute in attributes:
            source_attr = "{}.{}".format(
                left_locator,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_locator,
                attribute
            )

            if not cmds.objExists(source_attr):
                continue

            if not cmds.objExists(destination_attr):
                continue

            if cmds.isConnected(
                    source_attr,
                    destination_attr
            ):
                continue

            cmds.connectAttr(
                source_attr,
                destination_attr,
                force=True
            )

        return True

    @staticmethod
    def connect_locator_shape(
            left_locator,
            right_locator
    ):
        u"""连接 Locator Shape 的 localPosition / localScale。"""
        left_shapes = cmds.listRelatives(
            left_locator,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="locator"
        )
        right_shapes = cmds.listRelatives(
            right_locator,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="locator"
        )

        if left_shapes is None:
            left_shapes = []

        if right_shapes is None:
            right_shapes = []

        if not left_shapes or not right_shapes:
            return False

        left_shape = left_shapes[0]
        right_shape = right_shapes[0]

        shape_attributes = [
            "localPositionX",
            "localPositionY",
            "localPositionZ",
            "localScaleX",
            "localScaleY",
            "localScaleZ",
        ]

        for attribute in shape_attributes:
            source_attr = "{}.{}".format(
                left_shape,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_shape,
                attribute
            )

            if cmds.isConnected(
                    source_attr,
                    destination_attr
            ):
                continue

            cmds.connectAttr(
                source_attr,
                destination_attr,
                force=True
            )

        return True

    def mirror_left_guide(
            self,
            left_zero_group
    ):
        u"""镜像一个 zero_lf_* + loc_lf_* Guide 层级。"""
        left_locator = self.get_left_locator(
            left_zero_group
        )

        if left_locator is None:
            raise RuntimeError(
                u"没有在 {} 下找到 loc_lf_*。".format(
                    left_zero_group
                )
            )

        right_zero_group = self.create_or_update_right_zero(
            left_zero_group
        )
        right_locator = self.create_or_update_right_locator(
            left_locator,
            right_zero_group
        )

        self.connect_locator_transform(
            left_locator,
            right_locator
        )
        self.connect_locator_shape(
            left_locator,
            right_locator
        )

        color = self.get_guide_locator_color(
            left_locator
        )

        if color is not None:
            self.set_guide_locator_color(
                left_locator,
                color
            )
            self.set_guide_locator_color(
                right_locator,
                color
            )

        return {
            "left_zero": left_zero_group,
            "left_locator": left_locator,
            "right_zero": right_zero_group,
            "right_locator": right_locator,
        }

    def mirror_left_guides(self, parent_group=None):
        u"""批量镜像 parent_group 下全部 zero_lf_* Guide。"""
        left_zero_groups = self.get_left_zero_groups(
            parent_group=parent_group
        )

        results = []

        for left_zero_group in left_zero_groups:
            result = self.mirror_left_guide(
                left_zero_group
            )
            results.append(result)

        self.apply_guide_locator_colors(
            parent_group=parent_group
        )

        return results


__all__ = [
    "FaceGuide",
]
