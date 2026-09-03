# coding=utf-8
from __future__ import print_function

from pathlib import Path


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError("Expected block not found in {}".format(path))
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


repo_root = Path(__file__).resolve().parents[1]
base_path = repo_root / "systems" / "face" / "modules" / "face_module_base.py"
eyelid_path = repo_root / "systems" / "face" / "modules" / "eyelid.py"
lip_path = repo_root / "systems" / "face" / "modules" / "lip.py"

replace_once(
    base_path,
    "from __future__ import print_function\n\nfrom ....core import scene_utils\n",
    "from __future__ import print_function\n\nimport maya.cmds as cmds\n\nfrom ....core import scene_utils\n"
)

replace_once(
    base_path,
    "        self.module_dict = {\n            \"module\": self,\n        }\n\n    # =========================================================================\n    # Public Build Entry\n",
    "        self.module_dict = {\n            \"module\": self,\n        }\n\n    def _resolve_scene_node(\n            self,\n            node,\n            label=u\"Maya 节点\",\n            node_type=None\n    ):\n        u\"\"\"\n        解析当前 Scene 中真实存在的节点，并返回稳定的 Long Name。\n\n        该 Helper 专门处理 Face Module 跨阶段常见的两种名称变化：\n            1. 当前 Maya Namespace 自动附加到新建节点；\n            2. DAG Reparent 后旧 Long Path 失效。\n\n        Args:\n            node (str):\n                原始节点名、带 Namespace 的节点名，或可能已经过期的 DAG Long Path。\n            label (str):\n                节点不存在或不唯一时用于错误提示的业务标签。\n            node_type (str | None):\n                可选 Maya Node Type，用于进一步限制候选结果。\n\n        Returns:\n            str:\n                当前 Scene 中唯一匹配节点的 Long Name。\n\n        Raises:\n            RuntimeError:\n                节点不存在，或忽略 Namespace 后出现多个同名候选时抛出。\n        \"\"\"\n        # ---------------------------------------------------------------------\n        # Step 01：优先接受仍然有效的原始节点名或 Long Path\n        # ---------------------------------------------------------------------\n        if node is None:\n            raise RuntimeError(\n                u\"{}名称不能为空。\".format(label)\n            )\n\n        node = str(node).strip()\n\n        if not node:\n            raise RuntimeError(\n                u\"{}名称不能为空。\".format(label)\n            )\n\n        if cmds.objExists(node):\n            if node_type is not None and cmds.nodeType(node) != node_type:\n                raise RuntimeError(\n                    u\"{}类型错误：{}，期望 {}。\".format(\n                        label,\n                        cmds.nodeType(node),\n                        node_type\n                    )\n                )\n\n            return scene_utils.get_long_name(node)\n\n        # ---------------------------------------------------------------------\n        # Step 02：提取 DAG Leaf，并忽略 Namespace 比较标准 Rig 名称\n        # ---------------------------------------------------------------------\n        leaf_name = node.rsplit(\"|\", 1)[-1]\n        canonical_name = leaf_name.rsplit(\":\", 1)[-1]\n\n        search_pattern = \"*{}\".format(canonical_name)\n        search_kwargs = {\n            \"long\": True,\n        }\n\n        if node_type is not None:\n            search_kwargs[\"type\"] = node_type\n\n        scene_matches = cmds.ls(\n            search_pattern,\n            **search_kwargs\n        )\n\n        if scene_matches is None:\n            scene_matches = []\n\n        # ---------------------------------------------------------------------\n        # Step 03：只保留 Leaf 去掉 Namespace 后完全相同的候选节点\n        # ---------------------------------------------------------------------\n        resolved_matches = []\n\n        for scene_match in scene_matches:\n            scene_leaf_name = scene_match.rsplit(\"|\", 1)[-1]\n            scene_canonical_name = scene_leaf_name.rsplit(\":\", 1)[-1]\n\n            if scene_canonical_name != canonical_name:\n                continue\n\n            if scene_match in resolved_matches:\n                continue\n\n            resolved_matches.append(scene_match)\n\n        # ---------------------------------------------------------------------\n        # Step 04：要求结果唯一，绝不在同名节点中偷偷选择第一个\n        # ---------------------------------------------------------------------\n        if not resolved_matches:\n            raise RuntimeError(\n                u\"{}不存在：{}\".format(\n                    label,\n                    node\n                )\n            )\n\n        if len(resolved_matches) > 1:\n            raise RuntimeError(\n                u\"{}名称不唯一：{} -> {}\".format(\n                    label,\n                    node,\n                    \", \".join(resolved_matches)\n                )\n            )\n\n        return resolved_matches[0]\n\n    # =========================================================================\n    # Public Build Entry\n"
)

old_eyelid = '''            scene_utils.validate_node(\n                eye_jnt_name,\n                label=u"EyeModule Eye Joint"\n            )\n            scene_utils.validate_node(\n                eye_aim_ctrl_name,\n                label=u"EyeModule Aim Ctrl"\n            )\n            scene_utils.validate_node(\n                eye_output_name,\n                label=u"EyeModule Output"\n            )\n\n            self.eyelid_side_dict[side] = {\n'''
new_eyelid = '''            eye_jnt = self._resolve_scene_node(\n                eye_jnt_name,\n                label=u"EyeModule Eye Joint",\n                node_type="joint"\n            )\n            eye_aim_ctrl = self._resolve_scene_node(\n                eye_aim_ctrl_name,\n                label=u"EyeModule Aim Ctrl",\n                node_type="transform"\n            )\n            eye_output = self._resolve_scene_node(\n                eye_output_name,\n                label=u"EyeModule Output",\n                node_type="transform"\n            )\n\n            self.eyelid_side_dict[side] = {\n'''
replace_once(eyelid_path, old_eyelid, new_eyelid)

replace_once(
    eyelid_path,
    '''                "eye_jnt": eye_jnt_name,\n                "eye_aim_ctrl": eye_aim_ctrl_name,\n                "eye_output": eye_output_name,\n''',
    '''                "eye_jnt": eye_jnt,\n                "eye_aim_ctrl": eye_aim_ctrl,\n                "eye_output": eye_output,\n'''
)

old_lip = '''            for lip_deform_jnt in region_data["deform_jnts"]:\n                scene_utils.validate_node(\n                    lip_deform_jnt,\n                    label=u"Lip Deform Joint"\n                )\n\n        # -------------------------------------------------------------------------\n        # Step 03：整理统一 Module 输出\n'''
new_lip = '''            resolved_deform_jnts = []\n\n            for lip_deform_jnt in region_data["deform_jnts"]:\n                resolved_deform_jnt = self._resolve_scene_node(\n                    lip_deform_jnt,\n                    label=u"Lip Deform Joint",\n                    node_type="joint"\n                )\n                resolved_deform_jnts.append(\n                    resolved_deform_jnt\n                )\n\n            region_data["deform_jnts"] = resolved_deform_jnts\n\n        # -------------------------------------------------------------------------\n        # Step 03：整理统一 Module 输出\n'''
replace_once(lip_path, old_lip, new_lip)

print("Patched Face module scene-node resolution.")
