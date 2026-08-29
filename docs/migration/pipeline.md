# Pipeline 重构

早期 MuziTools 使用 `pipelineUtils.py` 作为综合工具类。

它曾同时承担：

```text
Animation
Scene
Constraint
Curve
Surface
Skin
Controller
Face
Hair
File IO
```

这种结构的问题是：

- 一个文件修改容易影响多个领域；
- Tool / System 不知道应该依赖哪一层；
- 相同逻辑容易在 UI 里再次复制；
- 大型 Rig Workflow 和通用 Core 混在一起；
- Smoke Test 很难只验证某一类能力。

## 当前正式方向

通用能力已经按 Maya 领域进入：

```text
core/animation_utils.py
core/scene_utils.py
core/transform_utils.py
core/connection_utils.py
core/constraint_utils.py
core/matrix_utils.py
core/curve_utils.py
core/surface_utils.py
core/skin_utils.py
...
```

完整 Rig Workflow 进入：

```text
systems/controller/
systems/face/
systems/body/
```

## 第二轮颗粒度优化

第一轮为了拆清职责，曾出现：

```text
animation_utils.py
animation_io_utils.py

scene_utils.py
scene_io_utils.py
```

职责已经稳定后，第二轮重新按“一个 Maya 领域一个模块”收口：

```text
animation_io_utils.py
        ↓
animation_utils.py

scene_io_utils.py
        ↓
scene_utils.py
```

但不会把 Matrix、Constraint、Connection 再合并成一个文件，因为它们已经是明确且会独立增长的领域。

## 验证原则

每次迁移遵循：

```text
提取新 API
    ↓
正式 Tool / System 改用新 API
    ↓
Maya Smoke Test
    ↓
确认 0 正式旧引用
    ↓
删除 Legacy
```

旧 `pipelineUtils.py` 已在真机测试通过后删除，不再作为正式运行依赖。
