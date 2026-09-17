# 基础工具

`tools/basic/` 收集日常绑定中最高频的五类操作：

```text
Rename
Attribute
Connection
Constraint
Snap
```

这些文件的 UI / 交互设计仍然有价值，但它们多数写于 Core 平铺模块时期，因此当前文档会把“工具功能”和“正式 Core 路径”分开说明。

<div class="grid cards" markdown>

-   :material-rename:{ .lg .middle } **Rename**

    ---

    Prefix、Suffix、Search Replace、Auto Number 和 Pattern Rename。

    [:octicons-code-24: Rename Tool API](../reference/tools/basic/rename_tool.md)

-   :material-tune:{ .lg .middle } **Attribute**

    ---

    Maya Attribute Window、Channel Box、Lock / Hide 和标准 TRSV 状态。

    [:octicons-code-24: Attr Tool API](../reference/tools/basic/attr_tool.md)

-   :material-connection:{ .lg .middle } **Connection**

    ---

    Translate / Rotate / Scale / Matrix 和自定义 Plug Connection。

    [:octicons-code-24: Connections Tool API](../reference/tools/basic/connections_tool.md)

-   :material-vector-link:{ .lg .middle } **Constraint**

    ---

    Parent、Point、Orient、Scale、Aim、Pole Vector 及约束查询 / 删除。

    [:octicons-code-24: Constraint Tool API](../reference/tools/basic/constraint_tool.md)

-   :material-target:{ .lg .middle } **Quick Snap**

    ---

    前面选择作为参考，最后一个对象作为被吸附目标。

    [:octicons-code-24: Snap Tool API](../reference/tools/basic/snap_tool.md)

</div>

## 当前目录

```text
tools/basic/
├── attr_tool.py
├── connections_tool.py
├── constraint_tool.py
├── rename_tool.py
└── snap_tool.py
```

## Tool 与 Core 的边界

Tool 应负责：

```text
Selection
Channel Box
Qt UI
用户输入
多对象批处理意图
Warning / Status
```

Core 应负责：

```text
Naming 规则
Attribute 底层行为
DAG Hierarchy
Transform Match
通用 Rig Primitive
```

当前正式 Core 推荐入口：

```text
core/common/name_utils.py
core/common/attr_utils.py
core/common/hierarchy_utils.py
core/common/transform_utils.py
```

## 当前迁移状态

这批 Tool 源码仍能看到旧式依赖，例如：

```python
from ...core import rename_utils
from ...core import scene_utils
from ...core import connection_utils
from ...core import constraint_utils
from ...core import snap_utils
```

但当前正式 Core 目录已经收敛为：

```text
core/common/
core/rigging/
```

因此：

```text
Tool UI / Workflow
    可以继续参考

旧 Core 平铺 Import
    待迁移
```

!!! warning "不要反向恢复旧 Core"
    修这些 Tool 时，应把它们迁移到当前 Core，或者为确实缺失的新能力建立新的正式 Core 模块；不要为了兼容旧 Tool，把已经清理掉的旧 `core.xxx_utils` 结构重新铺回来。

## Rename Tool

入口：

```python
from muziToolset.tools.basic import rename_tool

window = rename_tool.main()
```

当前 UI 意图包括：

```text
Add Prefix
Add Suffix
Search / Replace
Auto Number
Pattern Rename
```

其中 Pattern Rename 适合把一个模式应用到多个选择对象，例如：

```text
ctrl_lf_arm_*_001
```

真正的新 Rig 标准命名仍应优先复用：

```text
core/common/name_utils.py
```

例如：

```python
from muziToolset.core.common import name_utils

name = name_utils.Name(
    type="ctrl",
    side="lf",
    part="eye",
    function="main",
    index=1
).name
```

## Attribute Tool

当前 UI 设计包括：

```text
Maya Add / Edit Attribute
Connection Editor
Channel Control
Channel Box User Attribute 排序
TRSV Lock / Hide / Keyable 管理
```

新架构底层 Attribute 能力：

```text
core/common/attr_utils.py
```

适合统一处理：

```text
has_attr
add_attr
set_value
get_value
lock / unlock
hide / show
lock + hide
basic connect / disconnect
```

Tool 层应该继续保留：

```text
当前选择是什么
Channel Box 选中了哪个 Attribute
用户点击了什么按钮
```

而不是把 Channel Box 状态塞进 Core。

## Connections Tool

当前 UI 意图包括：

```text
Translate
Rotate
Scale
Matrix
Custom Channel Box Plug
```

Selection 会先被整理为：

```text
Driver
Driven List
Attribute Pair
```

再展开成：

```text
sourceNode.sourceAttr
    ↓
destinationNode.destinationAttr
```

这正是 Maya DG 中 Plug Connection 的核心概念。

### Plug 是什么

例如：

```text
ctrl_lf_eye_main_001.rotateX
```

这是一个完整 Plug：

```text
Node.Attribute
```

连接本质：

```text
Source Plug
    ↓
Destination Plug
```

而不是单纯“两个 Object 有关系”。

## Constraint Tool

当前 UI 设计支持：

```text
Parent Constraint
Point Constraint
Orient Constraint
Scale Constraint
Aim Constraint
Pole Vector Constraint
```

并负责：

```text
Selection Workflow
Multi-to-One
One-to-Many
查询 Driven 上真实 Constraint
删除选定 Constraint
```

Tool 负责“谁驱动谁”的选择语义；单个 Constraint 的创建 / 查询算法应该进入正式 Core 能力层。

### Constraint 与 Matrix

Constraint 是一种高层 Maya Driver Node。

未来如果某模块使用 Matrix 驱动替代 Constraint，也应该由具体 System 决定，而不是 Basic Tool 强制统一。

## Quick Snap

`snap_tool.py` 当前交互规则很明确：

```text
选择 1
选择 2
...
最后选择
```

其中：

```text
前面的选择
    = Reference Items

最后一个选择
    = Target Item
```

目标会吸附到参考项的平均位置；Transform / Joint 还会使用有效参考对象的平均旋转。

这是一次性 Action Tool，不需要长驻窗口。

## Transform Match 与 Snap 的区别

### Match Transform

通常是：

```text
一个 Source
    ↓
一个 Target
```

适合 Module 创建时：

```text
Joint -> Guide
Controller -> Guide
```

当前正式入口：

```text
core/common/transform_utils.py
```

### Quick Snap

通常是：

```text
多个 Reference
    ↓
平均结果
    ↓
最后一个 Target
```

是更偏绑定师交互的 Tool Workflow。

## 命名工具和 Rig Naming 的区别

Rename Tool 是通用批量重命名工具。

`name_utils.Name` 是 Rig 标准命名契约。

例如：

```text
把 abc 改成 def
```

适合 Rename Tool。

而：

```text
ctrl_lf_eye_main_001
```

应该由 `Name` 结构化生成。

## Undo

批量 Tool 应尽量把一次用户操作放在同一个 Undo Chunk 中。

这样用户可以：

```text
Ctrl + Z
```

一次撤销整组操作，而不是撤几十次。

这也是后续迁移旧 `scene_utils.open_undo_chunk()` 能力时应该保留的行为契约。

## 常见问题

### Tool 打开时报 ImportError

如果错误类似：

```text
cannot import name scene_utils from core
cannot import name rename_utils from core
```

这通常是旧 Tool 尚未迁移到当前 Core 收敛结构，不应该通过恢复旧架构文档来“解释”为正常。

### Connection 没有效果

检查：

```text
Source Plug 是否存在
Destination Plug 是否存在
Destination 是否已有输入
Attribute 是否 Locked
数据类型是否兼容
```

### Constraint 结果跳动

检查：

```text
Maintain Offset
Driver / Driven 顺序
Parent Space
Initial Transform
```

### Snap 后旋转不对

多参考对象平均 Rotation 需要明确数学语义；不同 Euler Order 下简单平均可能不适合复杂情况。

## 相关 API

- [rename_tool.py](../reference/tools/basic/rename_tool.md)
- [attr_tool.py](../reference/tools/basic/attr_tool.md)
- [connections_tool.py](../reference/tools/basic/connections_tool.md)
- [constraint_tool.py](../reference/tools/basic/constraint_tool.md)
- [snap_tool.py](../reference/tools/basic/snap_tool.md)
- [name_utils.py](../reference/core/common/name_utils.md)
- [attr_utils.py](../reference/core/common/attr_utils.md)
- [transform_utils.py](../reference/core/common/transform_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 Core API](../reference/core/index.md){ .md-button .md-button--primary }
