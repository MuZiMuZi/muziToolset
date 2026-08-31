# Muzi Toolset

Muzi Toolset 正在重建为 **PyMEL-first Maya Rigging Framework**。

## 当前方向

Maya Node 的创建、属性、连接、父子关系等基础操作直接使用 PyMEL：

```python
import pymel.core as pm

joint = pm.joint(
    name="jnt_md_test_bind_001",
    position=(0, 0, 0),
    radius=0.1
)

joint.radius.set(0.2)
```

不再为了对象化而额外维护 Joint / Transform / Attribute 包装类。

## 正式结构

```text
muziToolset/
├─ core/
├─ systems/
│  ├─ component_base.py
│  └─ face/
├─ tools/
└─ legacy_reference/
```

## 命名规范

正式运行区统一使用：

```text
folder / module / resource file    snake_case
function / method                  snake_case
variable                           snake_case
module config variable             snake_case
class                              PascalCase
```

项目自定义变量全部小写，包括 `config.py` 顶层配置变量。

示例：

```python
face_side = "md"
guide_version = "1.0"
controller_default_settings = {}

class FaceConfig(object):
    pass
```

`README.md`、`LICENSE` 和平台约定文件保持标准名称；历史归档内部不重命名。

## 架构原则

- PyMEL 是默认 Maya Node 操作层；
- `core/` 不重复包装 PyMEL 已经清晰提供的基础能力；
- `systems/` 负责完整 Rig Component；
- `tools/` 负责用户交互和工作流入口；
- 历史接口不兼容、不恢复；
- `legacy_reference/` 永远不能被正式代码 import。

## Maya 依赖

在目标 Maya 的 Python 环境中安装与该 Maya 版本兼容的 PyMEL：

```bash
mayapy -m pip install pymel
```

依赖文件：

```text
requirements_maya.txt
```

当前 Face Rig 迁移状态：

```text
systems/face/pymel_migration.md
```
