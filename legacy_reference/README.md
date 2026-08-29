# Legacy Reference

这个目录保存 Muzi Toolset 的历史实现，只用于查阅、对比和提取旧算法。

当前包含：

```text
legacy_reference/
├─ bind/           # 早期绑定相关代码
├─ core/           # Pipeline 最终迁移台账与待验证历史实现
├─ dev/            # 旧开发辅助脚本，例如 MayaSender
├─ integrations/   # AdvancedSkeleton / MetaHuman 历史集成参考
├─ pyside/         # PySide 学习 / 旧界面代码
├─ res/            # 旧资源与 UI 资源
└─ rigging/        # 旧 Body / IKFK / Ribbon / Controller Rig 参考实现
```

这些目录全部属于历史资料区，不是正式运行架构。

## Core 迁移状态

`legacy_reference/core/` 已完成大部分审计和迁移，目前只保留：

```text
legacy_reference/core/
├─ PIPELINE_MIGRATION.md
├─ __init__.py
└─ pipelineUtils.py
```

旧 `attrUtils / hierarchyUtils / jointUtils / connectionUtils / vectorUtils / weightsUtils / fileUtils / snapUtils / nameUtils` 等已经由正式 Core 接管或明确淘汰，不再保存第二份实现。

`pipelineUtils.py` 目前只作为最后的历史算法参考。新版 Pipeline / Controller Smoke Test 在 Maya 2023 真机验证通过后即可删除。

迁移详情见：

```text
legacy_reference/core/PIPELINE_MIGRATION.md
```

## 第三方集成参考

AdvancedSkeleton 和 MetaHuman 的旧专用代码已经从 `legacy_reference/core/` 移出：

```text
legacy_reference/integrations/
├─ advanced_skeleton.py
└─ metahuman.py
```

它们是第三方 Rig 集成历史参考，不属于通用 Core。未来如果正式支持对应系统，应在正式架构中重新设计独立 Integration，而不是直接 import 这些 Legacy 文件。

## Rig 历史参考

旧 `controlUtils.py` 中 Controller Shape / 标准控制器层级等通用能力已经迁入正式代码。

剩余 Ribbon、IK Spine、IK Curve Rig 等大型工作流参考移动到：

```text
legacy_reference/rigging/controlUtils.py
```

这些大型流程以后如果重新开发，应拆成独立 Rig System，不允许再次塞回 `core/`。

其中 `rigging/line_rig_v02.py` 等实验脚本也统一保存在历史区，不再占用项目根目录。

## Face 已完成迁移

旧 `legacy_reference/face/` 已完成审计并移除。

对应正式开发位置：

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

旧 Face Setup / Config / Base / Guide 已由正式系统版本接管；旧 Face UI 已由 `systems/face/wizard.py` 重写；旧 Maya 测试则由根包 `tests/` 下的 Smoke Test 接管。

## 使用规则

正式代码禁止：

```python
from legacy_reference import ...
```

也不要通过修改 `sys.path` 的方式把历史目录重新加入正式运行路径。

如果历史代码中有仍然有价值的功能，应按下面流程处理：

1. 阅读旧实现；
2. 找出真正需要保留的算法；
3. 去掉旧 UI、旧路径、PyMel、主动 reload 等不再需要的依赖；
4. 根据职责迁入根包中的 `core/`、`tools/` 或 `systems/`；
5. 把场景算法与 PySide UI 分开；
6. 使用正式 `ui/` Theme、`app/window_manager.py` 和公共 Widget；
7. 在 Maya 中验证新实现后，再让正式工具调用新的 API。

## 正式代码位置

当前正式运行框架就是仓库根包：

```text
muziToolset/
├─ app/
├─ ui/
├─ core/
├─ tools/
├─ systems/
└─ resources/
```

历史区只作为代码资料库，不应该重新变成第二套运行架构。
