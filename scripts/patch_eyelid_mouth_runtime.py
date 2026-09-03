# coding=utf-8
from pathlib import Path


# =============================================================================
# Eyelid: avoid parenting a curve that is already under the target group
# =============================================================================
eyelid_path = Path("systems/face/modules/eyelid.py")
eyelid_source = eyelid_path.read_text(encoding="utf-8")

eyelid_old = '''            blink_curve = cmds.duplicate(\n                eyelid_dict["skin_curve_dict"]["upper"],\n                name=blink_curve_name\n            )[0]\n            blink_curve = cmds.parent(\n                blink_curve,\n                self.face_rig_nodes_grp\n            )[0]\n'''

eyelid_new = '''            blink_curve = cmds.duplicate(\n                eyelid_dict["skin_curve_dict"]["upper"],\n                name=blink_curve_name\n            )[0]\n\n            blink_curve_parent = cmds.listRelatives(\n                blink_curve,\n                parent=True,\n                fullPath=True\n            )\n\n            if blink_curve_parent is None:\n                blink_curve_parent = []\n\n            if not blink_curve_parent or blink_curve_parent[0] != self.face_rig_nodes_grp:\n                blink_curve = cmds.parent(\n                    blink_curve,\n                    self.face_rig_nodes_grp\n                )[0]\n            else:\n                blink_curve = scene_utils.get_long_name(\n                    blink_curve\n                )\n'''

if eyelid_old not in eyelid_source:
    raise RuntimeError("Eyelid blink curve parent block not found")

eyelid_source = eyelid_source.replace(
    eyelid_old,
    eyelid_new,
    1
)
eyelid_path.write_text(eyelid_source, encoding="utf-8")


# =============================================================================
# Mouth: resolve dependencies created by JawModule / LipModule in namespaces
# =============================================================================
mouth_path = Path("systems/face/modules/mouth.py")
mouth_source = mouth_path.read_text(encoding="utf-8")

mouth_setup_old = '''        self.jaw_ctrl = self.create_name(\n            type="ctrl",\n            side="md",\n            part="jaw",\n            function="bind",\n            index=1\n        )\n        self.jaw_output = ctrl_base.get_ctrl_hierarchy_names(\n            self.jaw_ctrl,\n            create_sub_ctrl=True\n        )["output"]\n        # -------------------------------------------------------------------------\n        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象\n        # -------------------------------------------------------------------------\n        self.left_corner_ctrl = self.create_name(\n            type="ctrl",\n            side="lf",\n            part="mouth_corner",\n            function="bind",\n            index=1\n        )\n        self.right_corner_ctrl = self.create_name(\n            type="ctrl",\n            side="rt",\n            part="mouth_corner",\n            function="bind",\n            index=1\n        )\n\n        for node in [\n                self.jaw_ctrl,\n                self.jaw_output,\n                self.left_corner_ctrl,\n                self.right_corner_ctrl\n        ]:\n            scene_utils.validate_node(\n                node,\n                label=u"Mouth Dependency"\n            )\n'''

mouth_setup_new = '''        jaw_ctrl_name = self.create_name(\n            type="ctrl",\n            side="md",\n            part="jaw",\n            function="bind",\n            index=1\n        )\n        jaw_output_name = self.create_name(\n            type="output",\n            side="md",\n            part="jaw",\n            function="bind",\n            index=1\n        )\n\n        # -------------------------------------------------------------------------\n        # Step 04：解析 Jaw / Lip Module 已创建的真实 Namespace / DAG 节点\n        # -------------------------------------------------------------------------\n        left_corner_ctrl_name = self.create_name(\n            type="ctrl",\n            side="lf",\n            part="mouth_corner",\n            function="bind",\n            index=1\n        )\n        right_corner_ctrl_name = self.create_name(\n            type="ctrl",\n            side="rt",\n            part="mouth_corner",\n            function="bind",\n            index=1\n        )\n\n        self.jaw_ctrl = self._resolve_scene_node(\n            jaw_ctrl_name,\n            label=u"Mouth Jaw Ctrl Dependency",\n            node_type="transform"\n        )\n        self.jaw_output = self._resolve_scene_node(\n            jaw_output_name,\n            label=u"Mouth Jaw Output Dependency",\n            node_type="transform"\n        )\n        self.left_corner_ctrl = self._resolve_scene_node(\n            left_corner_ctrl_name,\n            label=u"Mouth Left Corner Ctrl Dependency",\n            node_type="transform"\n        )\n        self.right_corner_ctrl = self._resolve_scene_node(\n            right_corner_ctrl_name,\n            label=u"Mouth Right Corner Ctrl Dependency",\n            node_type="transform"\n        )\n'''

if mouth_setup_old not in mouth_source:
    raise RuntimeError("Mouth dependency setup block not found")

mouth_source = mouth_source.replace(
    mouth_setup_old,
    mouth_setup_new,
    1
)

mouth_jnt_old = '''            scene_utils.validate_node(\n                upper_lip_jnt,\n                label=u"Upper Lip Deform Joint"\n            )\n            scene_utils.validate_node(\n                lower_lip_jnt,\n                label=u"Lower Lip Deform Joint"\n            )\n            self.upper_lip_jnts.append(upper_lip_jnt)\n            self.lower_lip_jnts.append(lower_lip_jnt)\n'''

mouth_jnt_new = '''            upper_lip_jnt = self._resolve_scene_node(\n                upper_lip_jnt,\n                label=u"Upper Lip Deform Joint",\n                node_type="joint"\n            )\n            lower_lip_jnt = self._resolve_scene_node(\n                lower_lip_jnt,\n                label=u"Lower Lip Deform Joint",\n                node_type="joint"\n            )\n            self.upper_lip_jnts.append(upper_lip_jnt)\n            self.lower_lip_jnts.append(lower_lip_jnt)\n'''

if mouth_jnt_old not in mouth_source:
    raise RuntimeError("Mouth Lip Joint validation block not found")

mouth_source = mouth_source.replace(
    mouth_jnt_old,
    mouth_jnt_new,
    1
)

mouth_ctrl_dict_old = '''    @staticmethod\n    def _get_existing_ctrl_dict(ctrl_name):\n        u"""根据 CtrlBase 确定性层级恢复 create_follow() 所需的最小 Ctrl Dict。"""\n        hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(\n            ctrl_name\n        )\n        ctrl_node = scene_utils.get_long_name(\n            ctrl_name\n        )\n        zero_grp = scene_utils.get_long_name(\n            hierarchy_names["zero"]\n        )\n        driven_grp = scene_utils.get_long_name(\n            hierarchy_names["driven"]\n        )\n\n        return {\n            "ctrl_node": ctrl_node,\n            "grp_dict": {\n                "zero": zero_grp,\n                "driven": driven_grp,\n            },\n        }\n'''

mouth_ctrl_dict_new = '''    def _get_existing_ctrl_dict(self, ctrl_name):\n        u"""根据 CtrlBase 确定性层级恢复 create_follow() 所需的最小 Ctrl Dict。"""\n        ctrl_leaf_name = str(ctrl_name).rsplit("|", 1)[-1]\n        ctrl_canonical_name = ctrl_leaf_name.rsplit(":", 1)[-1]\n        hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(\n            ctrl_canonical_name\n        )\n        ctrl_node = self._resolve_scene_node(\n            ctrl_name,\n            label=u"Mouth Existing Ctrl",\n            node_type="transform"\n        )\n        zero_grp = self._resolve_scene_node(\n            hierarchy_names["zero"],\n            label=u"Mouth Existing Ctrl Zero",\n            node_type="transform"\n        )\n        driven_grp = self._resolve_scene_node(\n            hierarchy_names["driven"],\n            label=u"Mouth Existing Ctrl Driven",\n            node_type="transform"\n        )\n\n        return {\n            "ctrl_node": ctrl_node,\n            "grp_dict": {\n                "zero": zero_grp,\n                "driven": driven_grp,\n            },\n        }\n'''

if mouth_ctrl_dict_old not in mouth_source:
    raise RuntimeError("Mouth existing ctrl dict block not found")

mouth_source = mouth_source.replace(
    mouth_ctrl_dict_old,
    mouth_ctrl_dict_new,
    1
)

mouth_path.write_text(mouth_source, encoding="utf-8")
