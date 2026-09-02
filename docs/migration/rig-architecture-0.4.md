# Rig Architecture 0.4 Migration

0.4 将 MuziTools 的 Rig 基础架构统一到三个正式入口：

```text
systems/rig_base.py
systems/module_base.py
systems/ctrl_base.py
```

这次迁移的目标不是增加兼容层，而是删除重复职责，让后续 Face / Body / Rig Tool 都依赖同一套基础 API。

---

# 1. Naming

旧：

```text
core/name_utils.py
name_utils.Name.create_name()
name_utils.Name.mirror_name()
```

新：

```text
systems/rig_base.py
RigBase.create_name()
RigBase.parse_name()
RigBase.validate_name()
RigBase.mirror_name()
```

`core/rename_utils.py` 保留，但职责只包括 Maya Short Name、Rename 和批量 Rename 行为。

---

# 2. Component -> Module

旧：

```text
systems/component_base.py
ComponentBase
RigComponentBase
TeethComponent
```

新：

```text
systems/module_base.py
ModuleBase
RigModuleBase
TeethModule
```

Module 生命周期：

```text
collect_inputs()
prepare_data()
process_data()
finalize_step()
```

RigModuleBase 的 `process_data()` 统一调用：

```text
create_joint()
create_controller()
create_connection()
```

完整 Rig 业务单元统一使用 **Module** 术语。

---

# 3. Controller

旧：

```text
systems/controller/
    builder.py
    space_blend.py
```

新：

```text
systems/ctrl_base.py
```

正式 Controller API 包括：

```text
create_ctrl()
create_fk_ctrl()
create_follow()
create_space_switch()
create_space_blend()
```

Controller Tool、Rig Tool、Body Skirt 和 Face Module 均直接调用 `ctrl_base`。

---

# 4. Face Step 03

完整 Face 业务 Module 从 `build/` 中分离：

```text
systems/face/modules/
    teeth.py
```

`systems/face/build/` 只保存可以被 Module 组合的构建算法，例如：

```text
curve_attachment.py
eyelid/
lip/
```

术语：

```text
Step
    Setup / Guide / Build / Finalize

Module
    Teeth / Jaw / Tongue / Lip / Eye / Brow ...

Builder
    Curve Attachment / Zip Lip / Radial Joint ...
```

---

# 5. 已删除入口

0.4 不保留以下 Compatibility Wrapper：

```text
core/name_utils.py
systems/component_base.py
systems/controller/
systems/face/build/teeth_component.py
systems/face/build/teeth_builder.py
```

旧测试入口也已经替换为：

```text
rig_base_contract_test.py
module_base_contract_test.py
ctrl_base_smoke_test.py
face_build_smoke_test.py
rig_architecture_gate_test.py
```

---

# 6. 架构门禁

`tests/rig_architecture_gate_test.py` 用于阻止退休架构重新进入正式代码。

禁止重新出现：

```text
name_utils
component_base
systems.controller
ComponentBase
RigComponentBase
TeethComponent
```

历史说明文档可以提及这些名称，但正式 Runtime 不能重新依赖它们。

---

# 7. Maya 2023 验证

迁移后的推荐验证顺序：

```python
import muziToolset

muziToolset.smoke_test()
muziToolset.extended_core_smoke_test()
muziToolset.ctrl_base_smoke_test()
muziToolset.rig_integration_test()
muziToolset.face_build_smoke_test()
muziToolset.maya2023_smoke_test()
muziToolset.functional_smoke_test()
```

静态架构迁移完成并不等于 Maya Runtime 已验证；最终仍需要在 Maya 2023 中运行上述 Smoke Test。
