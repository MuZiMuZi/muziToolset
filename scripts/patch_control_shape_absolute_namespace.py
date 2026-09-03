# coding=utf-8
from pathlib import Path

path = Path("core/control_shape_utils.py")
source = path.read_text(encoding="utf-8")

old = '''        short_name = transform.split("|")[-1]\n        new_shape_name = "{}Shape".format(short_name)\n\n        if shape_index > 0:\n            new_shape_name = "{}Shape{}".format(\n                short_name,\n                shape_index + 1\n            )\n\n        cmds.rename(\n            parented_shape,\n            new_shape_name\n        )\n'''

new = '''        short_name = transform.rsplit("|", 1)[-1]\n\n        # Maya rename() 的新名称默认相对当前 Namespace。\n        # Controller 位于 Namespace 时，如果再次传入相对的 ns:ctrlShape，\n        # Maya 会把 Namespace 部分视为无效并产生“新名称包含无效字符”警告。\n        # 因此这里始终构造以 ':' 开头的绝对 Namespace 名称。\n        namespace_name = ""\n        transform_name = short_name\n\n        if ":" in short_name:\n            namespace_name, transform_name = short_name.rsplit(\n                ":",\n                1\n            )\n\n        shape_name = "{}Shape".format(\n            transform_name\n        )\n\n        if shape_index > 0:\n            shape_name = "{}Shape{}".format(\n                transform_name,\n                shape_index + 1\n            )\n\n        if namespace_name:\n            new_shape_name = ":{}:{}".format(\n                namespace_name,\n                shape_name\n            )\n        else:\n            new_shape_name = ":{}".format(\n                shape_name\n            )\n\n        cmds.rename(\n            parented_shape,\n            new_shape_name\n        )\n'''

if old not in source:
    raise RuntimeError("Controller Shape rename block not found")

source = source.replace(old, new, 1)
path.write_text(source, encoding="utf-8")
