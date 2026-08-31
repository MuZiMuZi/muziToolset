# Muzi Toolset

Muzi Toolset 是一个 **PyMEL-first Maya Rigging Framework**，当前正式开发重点是程序化 Face Rig。

## 核心原则

```text
Maya Node / Attribute / Connection
                ↓
              PyMEL

项目自己的 Rig Algorithm / Rule
                ↓
              core

完整 Rig Business
                ↓
             systems
```

不再为了对象化重复维护 Joint / Transform / Attribute Wrapper。

```python
import pymel.core as pm

joint = pm.createNode(
    "joint",
    name="jnt_md_test_bind_001"
)
joint.radius.set(0.1)
```

## 项目结构

```text
muziToolset/
├─ core/
├─ systems/
│  ├─ component_base.py
│  └─ face/
├─ tools/
├─ resources/
└─ legacy_reference/
```

## Face Rig Workflow

```text
Step 01  FaceSetup
Step 02  FaceGuide
Step 03  FaceBuild
Step 04  FaceFinalize
```

打开 UI：

```python
import muziToolset.systems.face as face
face.show()
```

使用目标 Maya 的 `mayapy` 安装与该 Maya 版本匹配的 PyMEL。正式运行区不使用 `maya.cmds`；只有低层几何计算需要时使用 `maya.api.OpenMaya`。

## 命名

```text
folder / file          snake_case
function / method      snake_case
variable               snake_case
config variable        snake_case
class                  PascalCase
```

## 历史存档

旧 cmds 架构固定保存在 `cmds-archive-2026-08-31`；其它历史实现保存在 `legacy_reference/`。正式代码不会 import 历史实现。
