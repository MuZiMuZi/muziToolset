# Core API

Core 是 MuziTools 的 Maya 通用底层能力层。

当前正式模块第一版目录：

```text
animation_utils.py
attrUtils.py
blendshape_utils.py
connection_utils.py
constraint_utils.py
control_shape_utils.py
curve_utils.py
file_utils.py
hierarchyUtils.py
jointUtils.py
matrix_utils.py
mesh_utils.py
model_check_utils.py
nameUtils.py
rename_utils.py
scene_clean_utils.py
scene_utils.py
skin_utils.py
snap_utils.py
surface_utils.py
transform_utils.py
```

其中：

```text
animation_io_utils.py
scene_io_utils.py
```

正在分别合并进：

```text
animation_utils.py
scene_utils.py
```

运行：

```bash
python scripts/generate_mkdocs_reference.py
```

后，本页会被生成器更新为当前源码的完整模块索引，并为每个模块建立独立 API 页面。
