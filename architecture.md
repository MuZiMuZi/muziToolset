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

只负责用户交互、Selection、参数收集和调用 Systems / Core。

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

Systems 可以直接使用 PyMEL。

## 4. PyMEL 使用规则

正式 Maya 代码默认：

```python
import pymel.core as pm
```

优先使用 PyNode / Attribute，而不是频繁在字符串和节点之间转换。

## 5. 不做兼容

本次架构重建不维护任何历史 API。

禁止正式代码：

```python
from legacy_reference import ...
```

旧功能未来根据业务目标使用新架构重新实现。

## 6. Face Rig

`systems/face/` 是当前唯一继续迁移的现有业务系统。

迁移顺序：

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

迁移状态：

```text
systems/face/pymel_migration.md
```

## 7. 命名规范

正式运行区统一：

```text
folder / module / resource file    snake_case
function / method                  snake_case
variable                           snake_case
module config variable             snake_case
class                              PascalCase
```

项目自定义变量全部使用小写 `snake_case`，包括配置变量和逻辑上的常量。
不使用 `UPPER_SNAKE_CASE` 保存项目配置。

示例：

```python
face_side = "md"
guide_version = "1.0"
controller_default_settings = {}

class FaceConfig(object):
    pass
```

`README.md`、`LICENSE` 和平台约定文件保持社区标准名称。
`legacy_reference/` 保持历史路径原样，不参与新架构命名清理。

## 8. 代码风格

优先可读性，不写为了缩短行数的复杂表达式。

```python
for joint in joints:
    joint.radius.set(
        0.1
    )
```

## 9. 当前状态

旧实现保存在：

```text
legacy_reference/
```

正式区从新的 PyMEL-first 架构重新开始。
