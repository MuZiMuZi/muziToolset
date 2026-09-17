# Pipeline / Core Migration — 已退休历史记录

这份页面过去记录过一版“把大型 `pipelineUtils.py` 拆成大量平铺 `core/*_utils.py`”的迁移方案。

其中曾经出现过：

```text
core/animation_utils.py
core/scene_utils.py
core/file_utils.py
core/transform_utils.py
core/matrix_utils.py
core/connection_utils.py
core/constraint_utils.py
core/curve_utils.py
core/surface_utils.py
core/skin_utils.py
...
```

这些平铺路径**已经不是当前正式 Core 结构**。

为了避免旧 README / 外部链接直接 404，本页保留路径，但旧迁移正文已经删除。

## 当前 Core

当前推荐入口：

```text
core/common/
    attr_utils.py
    hierarchy_utils.py
    name_utils.py
    transform_utils.py

core/rigging/
    ctrl_utils.py
    guide_utils.py
    jnt_utils.py
```

历史代码与尚未迁移实现：

```text
core/bake/
legacy_reference/
```

新功能不要默认继续添加到 `core/bake/`。

## 当前原则

```text
明确的通用底层能力
    ↓
进入 current Core

完整 Rig Workflow
    ↓
进入 systems/

用户交互 / Selection / Qt
    ↓
进入 tools/ 或 ui/

历史兼容实现
    ↓
留在 bake / legacy，等待迁移或删除
```

## 为什么网站仍会看到旧 Tool import

部分 `tools/*` 仍然引用早期平铺入口，例如：

```python
from ...core import scene_utils
from ...core import skin_utils
from ...core import constraint_utils
```

这表示：

```text
Tool 仍待迁移
```

而不是：

```text
旧 Core 仍然是正式架构
```

用户手册会明确标注这些迁移状态。

## 当前入口

请继续查看：

- [总体架构](../architecture/index.md)
- [Core 设计](../architecture/core.md)
- [Core 使用手册](../manual/core.md)
- [Tools 总览](../manual/tools.md)
- [文档维护](../development/documentation.md)
- [API Reference](../reference/index.md)

!!! note "保留这个页面的唯一原因"
    旧链接仍然可能存在于 Commit、Issue 或本地笔记中。保留这个文件可以把读者导向当前架构，同时避免继续传播已经退休的旧 Core 目录说明。
