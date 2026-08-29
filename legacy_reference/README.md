# Legacy Reference

这个目录保存 Muzi Toolset 的历史实现，只用于查阅、对比和提取旧算法，不属于正式运行架构。

当前主要目录：

```text
legacy_reference/
├─ bind/           # 早期绑定相关代码
├─ core/           # 已完成的 Core / Pipeline 迁移记录
├─ dev/            # 旧开发辅助脚本
├─ integrations/   # AdvancedSkeleton / MetaHuman 历史集成参考
├─ pyside/         # PySide 学习 / 旧界面代码
├─ res/            # 旧资源与 UI 资源
└─ rigging/        # 旧 Body / IKFK / Ribbon / Controller Rig 参考实现
```

## Core 迁移已完成

`legacy_reference/core/` 现在只保留：

```text
legacy_reference/core/
└─ PIPELINE_MIGRATION.md
```

旧 `pipelineUtils.py` 已在 Maya 2023 真机验证通过后正式删除；空的 `__init__.py` 也一并移除，因此这里不再是可 import 的 Python Package。

最终验证：

```text
muziToolset.pipeline_smoke_test()
9 / 9 PASS

muziToolset.controller_component_smoke_test()
1 / 1 PASS
```

旧 `attrUtils / hierarchyUtils / jointUtils / connectionUtils / vectorUtils / weightsUtils / fileUtils / snapUtils / nameUtils` 等已经由正式 Core 接管或明确淘汰，不再保存第二份实现。

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

旧 `legacy_reference/face/` 已完成审计并删除。正式 Face 开发位于：

```text
systems/face/
├─ config.py
├─ face_base.py
├─ face_setup.py
├─ face_guide.py
├─ curve_attachment.py
├─ eyelid/
├─ lip/
└─ wizard.py
```

## 使用规则

正式代码禁止：

```python
from legacy_reference import ...
```

也不要通过修改 `sys.path` 把历史目录重新加入正式运行路径。

如果历史代码仍有价值，应重新提取算法、去掉旧 UI / PyMel / 硬编码路径 / import-time 副作用，再按职责进入正式的 `core/`、`tools/` 或 `systems/`。

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
