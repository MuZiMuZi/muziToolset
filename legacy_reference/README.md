# Legacy Reference

这个目录保存 Muzi Toolset 的历史实现，只用于查阅、对比和提取旧算法，不属于正式运行架构。

当前主要目录：

```text
legacy_reference/
├─ bind/           # 早期绑定相关代码
├─ core/           # Core 历史实现 / 迁移记录
├─ dev/            # 旧开发辅助脚本
├─ integrations/   # AdvancedSkeleton / MetaHuman 历史集成参考
├─ pyside/         # PySide 学习 / 旧界面代码
├─ res/            # 旧资源与 UI 资源
└─ rigging/        # 旧 Body / IKFK / Ribbon / Controller Rig 参考实现
```

## Core 历史参考

`legacy_reference/core/` 只作为 Core 重构时的历史参考，不属于可 import 的正式 Package。

当前保留：

```text
legacy_reference/core/
├─ PIPELINE_MIGRATION.md
└─ joint_utils_pre_single_joint_refactor.py
```

`joint_utils_pre_single_joint_refactor.py` 是把正式 `core/joint_utils.py`
收口为“单个 Joint 底层对象”之前的完整快照。

这份历史快照中包含旧的：

- Selection / 全场景批量 Joint 操作；
- Component / Curve 到 Joint；
- JointCurve；
- JointChain；
- 旧 Joint Orient / Display 工具接口。

这些接口不再约束新的正式 Core。后续如果仍有价值，应基于新的 `Joint`
底层能力重新设计 Tool / JointChain / Rig Component，而不是把旧实现重新复制回 Core。

旧 `pipelineUtils.py` 已在 Maya 2023 真机验证通过后正式删除；空的 `__init__.py`
也一并移除，因此 `legacy_reference/core/` 不应作为 Python Package 使用。

迁移详情见 `legacy_reference/core/PIPELINE_MIGRATION.md`。

## 第三方集成参考

```text
legacy_reference/integrations/
├─ advanced_skeleton.py
├─ metahuman.py
└─ README.md
```

这些文件只作为第三方 Rig 集成历史参考。未来正式支持时，应在正式架构重新设计独立 Integration。

## Rig 历史参考

旧 `controlUtils.py` 中 Controller Shape / 标准 Controller 层级已经迁入正式代码。剩余 Ribbon、IK Spine、IK Curve Rig 等大型流程保存在：

```text
legacy_reference/rigging/controlUtils.py
```

这些流程如果重新开发，应进入独立 `systems/`，不允许再次塞回 `core/`。

## Face 已完成迁移

旧 `legacy_reference/face/` 已完成审计并删除。正式 Face 开发位于 `systems/face/`。

## 使用规则

正式代码禁止：

```python
from legacy_reference import ...
```

也不要通过修改 `sys.path` 把历史目录重新加入正式运行路径。

如果历史代码仍有价值，应重新提取算法、去掉旧 UI / PyMel / 硬编码路径 /
import-time 副作用，再按职责进入正式的 `core/`、`tools/` 或 `systems/`。

当前正式运行框架始终是仓库根包：

```text
muziToolset/
├─ app/
├─ ui/
├─ core/
├─ tools/
├─ systems/
└─ resources/
```
