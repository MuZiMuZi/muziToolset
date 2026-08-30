# coding=utf-8
u"""
Step 01 - Face Setup
====================

负责：
    1. 指定头部模型；
    2. 指定左右眼模型；
    3. 指定上下牙模型；
    4. 指定舌头模型；
    5. 指定牙龈模型；
    6. 设置嘴唇 Joint 数量；
    7. 更新 Face Rig 工作模型；
    8. 更新 Config Network Node；
    9. 更新 Face UI Step 状态。

设计：
    Config Node 只创建一次。
    Step 01 可以重复执行。
    用户修改 Step 01 后，会把最新配置写回同一个 Config Node。
    后续 Step 统一从 FaceBase 读取最新数据。

模型名称规则：
    FaceSetup 内部统一保存 Maya 节点短名称，不保存 Long DAG Path。

    原因是 Step 01 会重新整理输入模型 Parent。如果保存：
        |grp_model|grp_head|model_md_head_001
    这样的 Long DAG Path，reparent 后原路径会立即失效。

    因此统一转换成：
        model_md_head_001

    同时要求短名称在场景中唯一，避免同名 DAG 节点产生歧义。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import hierarchy_utils
from ...core import mesh_utils
from ...core import name_utils
from . import face_base


class FaceSetup(face_base.FaceBase):
    u"""Face Rig Step 01。"""

    def __init__(
            self,
            face_head_model=None,
            face_lf_eye_model=None,
            face_rt_eye_model=None,
            upper_teech_model=None,
            lower_teech_model=None,
            face_tongue_model=None,
            face_gum_model=None,
            mouth_jnt_number=32
    ):
        u"""
        初始化 Face Setup。

        Args:
            face_head_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            face_lf_eye_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            face_rt_eye_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            upper_teech_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            lower_teech_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            face_tongue_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            face_gum_model (str):
                当前检查、绑定、复制或变形使用的模型 Transform。
            mouth_jnt_number (int):
                嘴唇分布系统需要创建的 Joint 总数量。
        """
        super(FaceSetup, self).__init__()

        # ------------------------------------------------------------
        # Face UI Step
        # ------------------------------------------------------------
        self.step_value = 1

        # ------------------------------------------------------------
        # 用户输入模型
        # ------------------------------------------------------------
        # UI Picker 正常已经返回短名称。
        # 这里仍然再次规范化，保证直接调用 FaceSetup API 时也安全。
        self.face_head_model = self.normalize_model_name(
            face_head_model
        )
        self.face_lf_eye_model = self.normalize_model_name(
            face_lf_eye_model
        )
        self.face_rt_eye_model = self.normalize_model_name(
            face_rt_eye_model
        )
        self.upper_teech_model = self.normalize_model_name(
            upper_teech_model
        )
        self.lower_teech_model = self.normalize_model_name(
            lower_teech_model
        )
        self.face_tongue_model = self.normalize_model_name(
            face_tongue_model
        )
        self.face_gum_model = self.normalize_model_name(
            face_gum_model
        )

        self.face_model_list = [
            self.face_head_model,
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model,
        ]

        # ------------------------------------------------------------
        # 构建参数
        # ------------------------------------------------------------
        self.mouth_jnt_number = mouth_jnt_number

        # ------------------------------------------------------------
        # Step 01 创建的工作模型
        # ------------------------------------------------------------
        self.face_head_tweak_model = None
        self.face_head_stretch_model = None
        self.face_head_deform_model = None

    # =========================================================================
    # Name
    # =========================================================================

    @staticmethod
    def normalize_model_name(model):
        u"""
        把输入模型名称统一转换成 Maya DAG 短名称。

        Args:
            model (str | None):
                Maya 节点名称或 Long DAG Path。

        Returns:
            str | None:
                短名称；None 输入保持 None。
        """
        if model is None:
            return None

        model = str(model).strip()

        if not model:
            return ""

        return model.split("|")[-1]

    # =========================================================================
    # Check
    # =========================================================================

    def check_model_exists(self):
        u"""
        检查 Step 01 指定的模型是否存在，并确认短名称唯一。

        Returns:
            bool:
                检查通过返回 True。

        Raises:
            RuntimeError:
                模型不存在、名称不唯一或不是 Transform 时抛出。
        """
        if self.face_head_model is None or self.face_head_model == "":
            raise RuntimeError(
                u"Face Setup 必须指定头部模型。"
            )

        for face_model in self.face_model_list:
            if face_model is None:
                continue

            if face_model == "":
                continue

            matches = cmds.ls(
                face_model,
                long=True
            )

            if matches is None:
                matches = []

            if not matches:
                raise RuntimeError(
                    u"给定名称的模型不存在于当前 Maya 场景中: {}".format(
                        face_model
                    )
                )

            if len(matches) > 1:
                raise RuntimeError(
                    u"模型短名称不唯一，Face Setup 无法安全确定目标: {}\n"
                    u"请先把场景中的同名节点重命名。".format(
                        face_model
                    )
                )

            node = matches[0]
            node_type = cmds.nodeType(
                node
            )

            if node_type != "transform":
                raise RuntimeError(
                    u"Face Setup 输入必须是 Transform，当前节点: {} | 类型: {}".format(
                        face_model,
                        node_type
                    )
                )

        return True

    def check_mouth_jnt_number(self):
        u"""
        检查嘴唇 Joint 数量。

        Returns:
            bool:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if self.mouth_jnt_number is None:
            raise RuntimeError(
                u"没有设置嘴唇 Joint 数量。"
            )

        if not isinstance(self.mouth_jnt_number, int):
            raise TypeError(
                u"嘴唇 Joint 数量必须是整数。"
            )

        if self.mouth_jnt_number < 4:
            raise ValueError(
                u"嘴唇 Joint 数量不能小于 4。"
            )

        if self.mouth_jnt_number % 4 != 0:
            raise ValueError(
                u"嘴唇 Joint 数量必须是 4 的倍数，当前值为: {}".format(
                    self.mouth_jnt_number
                )
            )

        return True

    # =========================================================================
    # Model
    # =========================================================================

    def parent_input_models(self):
        u"""
        把 Step 01 指定的模型整理到 Face Model Group。

        输入模型使用短名称，因此节点 reparent 后名称引用仍然有效。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        for face_model in self.face_model_list:
            if face_model is None:
                continue

            if face_model == "":
                continue

            hierarchy_utils.Hierarchy.parent(
                face_model,
                self.face_model_grp
            )

        return True

    def get_work_model_names(self):
        u"""
        生成 Step 01 三个头部工作模型名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        face_head_tweak_name = name_utils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="tweak",
            index=1
        )

        face_head_stretch_name = name_utils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="stretch",
            index=1
        )

        face_head_deform_name = name_utils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="deform",
            index=1
        )

        work_model_name_dict = {
            "tweak": face_head_tweak_name,
            "stretch": face_head_stretch_name,
            "deform": face_head_deform_name,
        }

        return work_model_name_dict

    def delete_old_work_models(self, work_model_name_dict):
        u"""
        删除 Step 01 之前生成的旧工作模型。

        Args:
            work_model_name_dict (dict):
                Step 01 三个 Head Work Model（tweak / stretch / deform）的名称映射。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        for key in work_model_name_dict:
            model = work_model_name_dict.get(
                key
            )

            if not model:
                continue

            if not cmds.objExists(model):
                continue

            cmds.delete(
                model
            )

        return True

    def create_work_models(self, work_model_name_dict):
        u"""
        根据最新 Head Model 创建三个独立工作模型。

        Args:
            work_model_name_dict (dict):
                Step 01 三个 Head Work Model（tweak / stretch / deform）的名称映射。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        face_head_tweak_name = work_model_name_dict.get(
            "tweak"
        )
        face_head_stretch_name = work_model_name_dict.get(
            "stretch"
        )
        face_head_deform_name = work_model_name_dict.get(
            "deform"
        )

        self.face_head_tweak_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_tweak_name,
            parent=self.face_tweak_grp
        )

        self.face_head_stretch_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_stretch_name,
            parent=self.face_stretch_grp
        )

        self.face_head_deform_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_deform_name,
            parent=self.face_deform_grp
        )

        return True

    def update_work_models(self):
        u"""
        根据最新输入更新 Step 01 工作模型。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        self.parent_input_models()

        work_model_name_dict = self.get_work_model_names()

        self.delete_old_work_models(
            work_model_name_dict
        )

        self.create_work_models(
            work_model_name_dict
        )

        return True

    # =========================================================================
    # Config
    # =========================================================================

    def save_config(self):
        u"""
        把 Step 01 最新设置更新到 Face Config。

        Config 的具体读写动作统一交给 FaceBase，
        FaceSetup 只负责组织 Step 01 自己的数据。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        model_config_dict = {
            "face_head_model": self.face_head_model,
            "face_lf_eye_model": self.face_lf_eye_model,
            "face_rt_eye_model": self.face_rt_eye_model,
            "upper_teech_model": self.upper_teech_model,
            "lower_teech_model": self.lower_teech_model,
            "face_tongue_model": self.face_tongue_model,
            "face_gum_model": self.face_gum_model,
        }

        self.set_config_messages(
            attrs_dict=model_config_dict,
            force=True,
            clear_empty=True
        )

        value_config_dict = {
            "mouth_jnt_number": self.mouth_jnt_number,
        }

        value_type_dict = {
            "mouth_jnt_number": "long",
        }

        self.set_config_values(
            attrs_dict=value_config_dict,
            attr_types=value_type_dict,
            lock=False,
            hide=False
        )

        return True

    # =========================================================================
    # Build
    # =========================================================================

    def build(self):
        u"""
        执行可以重复运行的 Face Rig Step 01。

        重新 Build Step 01 后：
            1. Step 01 标记为完成；
            2. Step 02～04 标记为未完成。
        原因：
            模型输入或嘴唇 Joint 数量改变后，
            后续旧 Guide / Rig 结果不能继续被视为最新结果。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        self.check_model_exists()
        self.check_mouth_jnt_number()

        self.ensure_hierarchy()
        self.update_work_models()
        self.save_config()

        self.set_step_completed(
            completed=True
        )
        self.invalidate_later_steps()

        return True


__all__ = [
    "FaceSetup",
]
