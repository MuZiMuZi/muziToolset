# Muzi Toolset Architecture

## 1. 技术路线

Muzi Toolset 正式采用 **PyMEL-first** 架构。

PyMEL 负责 Maya 场景对象层：

```text
PyNode
Joint
Transform
Attribute
Matrix Plug
Parent / Child
Connection
```

因此正式架构不再为这些基础能力重复创建包装类。

例如：

```python
joint.radius.set(0.1)
joint.rename("jnt_md_test_bind_001")
parent = joint.getParent()
controller.translate >> joint.translate
```

优先于再次包装成：

```python
Joint.set_radius()
Joint.rename()
Joint.get_parent()
Connection.connect()
```

## 2. 正式分层

```text
muziToolset/
│
├─ core/
│   └─ 通用算法、项目规则、数据处理
│
├─ systems/
│   ├─ component_base.py
│   └─ face/
│
├─ tools/
│   └─ 用户工具与工作流入口
│
└─ legacy_reference/
    └─ 历史实现，只允许查阅
```

### core

只保存真正增加项目语义的能力，例如：

- Rig Naming；
- Matrix / Math 算法；
- Geometry 采样；
- Rig 数据序列化；
- 与具体 Face / Body Component 无关的可复用计算。

不应该因为某个 PyMEL API 有三四行代码，就自动创建一个 Utils 包装函数。

### systems

负责完整 Rig 业务。

Component 可以直接持有 PyNode：

```python
self.joint = pm.PyNode("jnt_md_test_bind_001")
```

而不是强制把 Maya Node 转成字符串保存。

标准生命周期：

```text
collect_inputs()
prepare_data()
process_data()
finalize_step()
```

统一入口：

```text
run_step()
```

标准 Rig Component 的 `process_data()` 继续分成：

```text
create_joint()
create_controller()
create_connection()
```

### tools

只负责：

- Selection；
- UI；
- 用户参数收集；
- 调用 Core / Systems；
- 工作流组织。

Tool 不应该反向定义底层 Rig 规则。

## 3. 依赖方向

```text
Tools
  ↓
Systems
  ↓
Core
  ↓
PyMEL / Maya API
```

允许 Systems 直接使用 PyMEL。

Core 也可以在需要时使用：

```python
import pymel.core as pm
import maya.api.OpenMaya as om
```

但 Core 不应该 import Systems 或 Tools。

## 4. PyMEL 使用规则

正式 Maya 代码默认：

```python
import pymel.core as pm
```

优先使用 PyNode / Attribute，而不是频繁在字符串和节点之间转换。

推荐：

```python
joint = pm.PyNode("jnt_md_test_bind_001")
joint.radius.set(0.1)
```

避免：

```python
joint = "jnt_md_test_bind_001"
pm.setAttr(joint + ".radius", 0.1)
```

字符串主要用于：

- Naming 构建；
- Config 序列化；
- UI 输入输出；
- 日志；
- 外部文件数据。

## 5. 不做兼容

本次架构重建不维护任何历史 API。

禁止：

```python
from legacy_reference import ...
```

也禁止为了旧 Tool 恢复已经淘汰的 Core Wrapper。

旧功能如果未来需要，先理解它的业务目标，再使用新架构重新实现。

## 6. Face Rig

`systems/face/` 是当前唯一保留的现有业务系统。

旧 Face 实现不会反过来限制新底层设计。迁移时按以下顺序处理：

```text
FaceBase / Config
        ↓
FaceSetup
        ↓
FaceGuide
        ↓
Build Components
        ↓
UI / Workflow
```

迁移规则见：

```text
systems/face/PYMEL_MIGRATION.md
```

## 7. 代码风格

优先可读性，不写为了缩短行数的复杂表达式。

推荐：

```python
for joint in joints:
    joint.radius.set(
        0.1
    )
```

而不是把 Rig 构建流程压成难以调试的一行代码。

## 8. 当前状态

旧 Core、Tools、App、UI、Tests、Docs 和非 Face Systems 已归档到：

```text
legacy_reference/pymel_rebuild_2026_08_31/
```

正式区从新的 PyMEL-first 架构重新开始。
