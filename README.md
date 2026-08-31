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
├─ core/                 # 真正可复用的算法和项目规则
├─ systems/
│  ├─ component_base.py # Component 生命周期
│  └─ face/             # 当前唯一继续开发的业务系统
├─ tools/                # 新工具层，目前为空
└─ legacy_reference/     # 历史实现，只允许查阅
```

## 架构原则

- PyMEL 是默认 Maya Node 操作层；
- `core/` 不重复包装 PyMEL 已经清晰提供的基础能力；
- `systems/` 负责完整 Rig Component；
- `tools/` 负责用户交互和工作流入口；
- 历史接口不兼容、不恢复；
- 旧工具未来根据新架构重新实现；
- `legacy_reference/` 永远不能被正式代码 import。

## Maya 依赖

在目标 Maya 的 Python 环境中安装与该 Maya 版本兼容的 PyMEL：

```bash
mayapy -m pip install pymel
```

当前 Face Rig 正在逐步从旧实现迁移到新的 PyMEL 架构，迁移状态见：

```text
systems/face/PYMEL_MIGRATION.md
```
