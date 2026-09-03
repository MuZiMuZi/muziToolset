# coding=utf-8
from pathlib import Path

path = Path("systems/face/modules/mouth.py")
source = path.read_text(encoding="utf-8")

old = '''        if not self.zip_lip_dict:\n            raise RuntimeError(u"Mouth Zip Lip 没有完成构建。")\n\n        for upper_lip_jnt in self.upper_lip_jnts:\n            scene_utils.validate_node(\n                upper_lip_jnt,\n                label=u"Upper Lip Joint"\n            )\n\n        for lower_lip_jnt in self.lower_lip_jnts:\n            scene_utils.validate_node(\n                lower_lip_jnt,\n                label=u"Lower Lip Joint"\n            )\n'''

new = '''        if not self.zip_lip_dict:\n            raise RuntimeError(u"Mouth Zip Lip 没有完成构建。")\n\n        # -------------------------------------------------------------------------\n        # Step 01：Zip Lip Builder 可能重新组织 Joint DAG，先刷新真实 Long Path\n        # -------------------------------------------------------------------------\n        resolved_upper_lip_jnts = []\n\n        for upper_lip_jnt in self.upper_lip_jnts:\n            resolved_upper_lip_jnt = self._resolve_scene_node(\n                upper_lip_jnt,\n                label=u"Upper Lip Joint",\n                node_type="joint"\n            )\n            resolved_upper_lip_jnts.append(\n                resolved_upper_lip_jnt\n            )\n\n        resolved_lower_lip_jnts = []\n\n        for lower_lip_jnt in self.lower_lip_jnts:\n            resolved_lower_lip_jnt = self._resolve_scene_node(\n                lower_lip_jnt,\n                label=u"Lower Lip Joint",\n                node_type="joint"\n            )\n            resolved_lower_lip_jnts.append(\n                resolved_lower_lip_jnt\n            )\n\n        self.upper_lip_jnts = resolved_upper_lip_jnts\n        self.lower_lip_jnts = resolved_lower_lip_jnts\n\n        # -------------------------------------------------------------------------\n        # Step 02：使用刷新后的 Scene Node 验证最终 Mouth / Zip Lip 输出\n        # -------------------------------------------------------------------------\n        for upper_lip_jnt in self.upper_lip_jnts:\n            scene_utils.validate_node(\n                upper_lip_jnt,\n                label=u"Upper Lip Joint"\n            )\n\n        for lower_lip_jnt in self.lower_lip_jnts:\n            scene_utils.validate_node(\n                lower_lip_jnt,\n                label=u"Lower Lip Joint"\n            )\n'''

if old not in source:
    raise RuntimeError("Mouth finalize validation block not found")

source = source.replace(old, new, 1)
path.write_text(source, encoding="utf-8")
