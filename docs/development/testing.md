# 测试

MuziTools 的质量门槛分成两层：

```text
普通 Python / GitHub Actions
    -> 静态架构 + 文档构建

Maya 2023
    -> 真实 Scene / DG / DAG / UI 行为
```

两层测试不能互相替代。

---

# 1. Static Architecture Gates

## Core Import Style

```bash
python tests/core_import_style_test.py
```

检查正式 Core 只使用当前 snake_case 模块，不重新引入退休 CamelCase 文件。

## Rig Architecture Gate

```bash
python tests/rig_architecture_gate_test.py
```

阻止以下退休架构重新出现：

```text
core/name_utils.py
systems/component_base.py
systems/controller/
systems/face/build/teeth_component.py
systems/face/build/teeth_builder.py
```

同时检查正式 Python 源码不能重新 Import：

```text
name_utils
component_base
systems.controller
```

并禁止退休类名：

```text
ComponentBase
RigComponentBase
TeethComponent
```

## RigBase Contract

```bash
python tests/rig_base_contract_test.py
```

验证 Rig Naming 的创建、解析、Mirror、Side Normalize 和字段限制。

## ModuleBase Contract

```bash
python tests/module_base_contract_test.py
```

验证：

```text
ModuleBase
    collect_inputs
    prepare_data
    process_data
    finalize_step

RigModuleBase
    collect_inputs
    prepare_data
    create_joint
    create_controller
    create_connection
    finalize_step
```

---

# 2. Maya Non-destructive Smoke

Maya Python Script Editor：

```python
import muziToolset

report = muziToolset.smoke_test()
```

验证：

- Maya / Qt 环境；
- Tool Registry；
- 当前 Core Import；
- `RigBase / ModuleBase / CtrlBase` Import；
- Face Module Import；
- Resources；
- UI Tool `main()`；
- Command Tool `main()` 存在。

不会点击实际 Build / Skin / Clean 操作。

---

# 3. Pipeline / Core Smoke

```python
report = muziToolset.pipeline_smoke_test()
```

验证基础 Core：

```text
Scene
Transform
Animation
Connection
Matrix
Constraint
Curve
Surface
```

测试创建临时节点后自动清理。

---

# 4. Extended Core / RigBase Smoke

```python
report = muziToolset.extended_core_smoke_test()
```

验证：

```text
attr_utils
hierarchy_utils
joint_utils
RigBase + rename_utils
model_check_utils
scene_clean_utils
```

其中 Naming 职责已经拆开：

```text
RigBase
    Standard Rig Name / Parse / Mirror

rename_utils
    Maya Rename
```

不要再把 Rig Naming 写回 Core。

---

# 5. CtrlBase Smoke

```python
report = muziToolset.ctrl_base_smoke_test()
```

验证当前唯一 Controller System：

```text
CtrlBase Create
Follow 0 / 1
```

后续 Space Switch / FK 等专项行为继续扩展此测试。

---

# 6. Face Build Smoke

```python
report = muziToolset.face_build_smoke_test()
```

验证 Face Build Algorithm：

```text
Eyelid Radial Joint
Curve Attachment
Matrix Zip Lip
```

这些是可复用 Builder / Algorithm，不称为 Component。

完整 Teeth / Jaw / Eye 等业务单元统一称为 Module。

---

# 7. Rig Integration Test

```python
report = muziToolset.rig_integration_test()
```

验证跨层构建链：

```text
RigBase Naming
    ↓
Joint
    ↓
CtrlBase
    ↓
Standard Controller Hierarchy
    ↓
offsetParentMatrix
    ↓
Joint Follow
```

需要保留测试结果查看时：

```python
report = muziToolset.rig_integration_test(
    keep_result=True
)
```

---

# 8. Maya 2023 Architecture Smoke

```python
report = muziToolset.maya2023_smoke_test()
```

重点检查当前 0.4 架构：

```text
Core Contract
CtrlBase Contract
Face Module Lifecycle
Face Build Algorithms
```

该测试要求真实 Maya 2023 Runtime。

---

# 9. Functional Smoke Suite

```python
report = muziToolset.functional_smoke_test()
```

当前作为总调度器组合：

```text
Pipeline Core
Extended Core / RigBase
CtrlBase
Face Build
Rig Integration
```

总调度器不再复制各 System 的构建实现。

---

# 10. Tool Window Smoke

```python
report = muziToolset.tool_window_smoke_test()
```

用于检查所有正式 UI Tool：

```text
main()
    ↓
QWidget / QDialog
    ↓
窗口生命周期
```

不执行实际 Rig 场景操作。

---

# 11. 文档 / CI

推荐静态顺序：

```bash
python tests/core_import_style_test.py
python tests/rig_architecture_gate_test.py
python tests/rig_base_contract_test.py
python tests/module_base_contract_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

AST Reference Generator 不 Import Maya，因此可以在 GitHub Actions Linux Runner 运行。

---

# 12. 重构推荐顺序

```text
读取现有调用
    ↓
确定正式职责
    ↓
建立新 API
    ↓
迁移全部调用方
    ↓
迁移 Smoke / Contract Test
    ↓
静态反查退休入口
    ↓
删除旧实现
    ↓
更新文档
    ↓
Maya 2023 真机验证
```

旧 API 已经明确退休时，不保留会让新代码继续误用的 Compatibility Wrapper。
