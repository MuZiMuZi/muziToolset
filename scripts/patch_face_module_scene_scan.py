# coding=utf-8
from pathlib import Path

path = Path("systems/face/modules/face_module_base.py")
source = path.read_text(encoding="utf-8")

old = '''        search_pattern = "*{}".format(canonical_name)\n        search_kwargs = {\n            "long": True,\n        }\n\n        if node_type is not None:\n            search_kwargs["type"] = node_type\n\n        scene_matches = cmds.ls(\n            search_pattern,\n            **search_kwargs\n        )\n\n        if scene_matches is None:\n            scene_matches = []\n'''

new = '''        search_kwargs = {\n            "long": True,\n        }\n\n        if node_type is not None:\n            search_kwargs["type"] = node_type\n\n        # 不依赖 Maya Namespace 通配符匹配。直接枚举候选类型节点，\n        # 再在 Python 层严格比较去 Namespace 后的 DAG Leaf。\n        scene_matches = cmds.ls(\n            **search_kwargs\n        )\n\n        if scene_matches is None:\n            scene_matches = []\n'''

if old not in source:
    raise RuntimeError("FaceModuleBase scene search block not found")

source = source.replace(old, new, 1)
path.write_text(source, encoding="utf-8")
