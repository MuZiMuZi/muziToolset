# Core API

Core 是 MuziTools 的 Maya 通用底层能力层。

## 推荐入口

第一次查 Core 时，建议先看：

- [Core API 使用手册](guide.md)：模块选择、使用场景、典型 Maya 示例、设计边界；
- 自动 API Reference：由源码 AST 生成，负责同步真实函数签名、类和方法。

## 当前正式模块

```text
Animation / Scene / File
├─ animation_utils.py
├─ scene_utils.py
└─ file_utils.py

Transform / DG
├─ transform_utils.py
├─ matrix_utils.py
├─ connection_utils.py
└─ constraint_utils.py

DAG / Attribute / Naming
├─ attr_utils.py
├─ hierarchy_utils.py
├─ jnt_utils.py
├─ name_utils.py
├─ rename_utils.py
└─ snap_utils.py

Geometry / Deformer
├─ curve_utils.py
├─ surface_utils.py
├─ mesh_utils.py
├─ skin_utils.py
├─ blendshape_utils.py
└─ control_shape_utils.py

Scene Quality
├─ model_check_utils.py
└─ scene_utils.py
```

## 已完成模块收口

```text
animation_io_utils.py
    -> animation_utils.py

scene_io_utils.py
    -> scene_utils.py

attrUtils.py
    -> attr_utils.py

hierarchyUtils.py
    -> hierarchy_utils.py

jntUtils.py
    -> jnt_utils.py

nameUtils.py
    -> name_utils.py
```

上述旧模块都已经完成迁移并从正式 Core 删除。正式代码、测试、Tools 和文档统一使用 snake_case Import。

## 自动生成 API

运行：

```bash
python scripts/generate_mkdocs_reference.py
```

生成器会扫描当前正式源码：

```text
core/
tools/
systems/
```

并生成：

```text
docs/reference/core/*.md
docs/reference/tools/**/*.md
docs/reference/systems/**/*.md
```

每个模块页面至少包含：

```text
功能
使用场景
API
示例
源码位置
```

GitHub Actions 构建文档时会先执行 Core Import Style Gate，再重新生成 API Reference，最后执行 `mkdocs build --strict`。
因此在线文档中的模块列表、函数签名和类方法会跟随源码更新。

> 注意：本 `index.md` 在 CI 构建阶段会由生成器刷新成最新模块索引；`guide.md` 是人工维护文档，不会被生成器删除。
