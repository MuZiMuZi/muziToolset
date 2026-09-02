# Rig Architecture 0.4 Migration

0.4 将 MuziTools 的 Rig 基础架构统一到三个正式入口：

```text
systems/rig_base.py
systems/module_base.py
systems/ctrl_base.py
```

这次迁移的目标不是增加兼容层，而是删除重复职责，让后续 Face / Body / Rig Tool 都依赖同一套基础 API。

---

# 1. Name Utility -> RigBase Identity

旧架构：

```text
core/name_utils.py
name_utils.Name.create_name()
name_utils.Name.mirror_name()
```

0.4 最终架构：

```text
systems/rig_base.py
RigBase
```

`RigBase` 不再是 Name Utility，也不是代表某一个 Maya Node 名称的数据对象。

它是所有 Rig Object / Module 共用的**可实例化 Rig Identity 基类**。

一个 Rig Object 的 Identity 只包含：

```text
side
part
index
```

正式使用：

```python
from muziToolset.systems.rig_base import RigBase

rig = RigBase(
    side="lf",
    part="brow",
    index=1
)

joint_name = rig.create_name(
    node_type="jnt",
    function="bind"
)

# jnt_lf_brow_bind_001
```

标准节点格式：

```text
[node_type]_[side]_[part]_[function]_[index]
```

其中：

```text
side / part / index
    属于 Rig Object Identity

node_type / function
    描述本次具体 Maya Node
```

实例能力：

```text
identity
set_identity()
create_name()
mirror_name()
get_next_index()
create_unique_name()
get_opposite_side()
flip_side()
is_left()
is_right()
is_center()
```

纯解析 / 校验能力仍可以直接通过类调用：

```text
RigBase.parse_name()
RigBase.validate_name()
RigBase.normalize_side()
```

0.4 最终收口时同时退休：

```text
RigBase(name=...)
RigBase.create_name(...)
RigBase.mirror_name(...)
name
compose()
decompose()
flip()
type=     # RigBase Naming Keyword
```

正式 Naming Keyword：

```text
node_type=
```

`parse_name()` 只解析输入名称，不会修改 RigBase 实例 Identity。

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

继承关系：

```text
RigBase
   ↓
ModuleBase
   ↓
RigModuleBase
```

因此每个 Module 都拥有自己的 Rig Identity 和 Naming 能力。

完整 Rig 业务单元统一使用 **Module** 术语。

---

# 3. Controller -> CtrlBase

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

`FaceBase` 默认 Rig Identity：

```text
md / face / 001
```

当前 `TeethModule` 的 Rig Identity：

```text
md / teeth / 001
```

后续 Jaw / Tongue / Lip / Eye 等 Module 应遵循同一模式。

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
RigBase.create_name(...)
RigBase(name=...)
create_name(type=...)
```

`tests/rig_base_contract_test.py` 进一步验证：

```text
Rig Identity
Naming Override 不修改 Identity
Parse 不修改 Identity
Side Semantic
001 ~ 999 Index Contract
退休 type= Keyword 不再可用
退休 Name Object API 不再存在
```

历史说明文档可以提及退休名称，但正式 Runtime 不能重新依赖它们。

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
