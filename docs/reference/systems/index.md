# Systems API

Systems 是 MuziTools 的完整 Rig Builder / Workflow / Component 层。

当前正式结构：

```text
systems/
├─ component_base.py       # 所有 Component 的统一生命周期与 Rig 构建规范
├─ body/
├─ controller/
└─ face/
```

## Component 构建规范

所有具有明确构建过程的 Component，统一继承：

```python
from muziToolset.systems import ComponentBase
```

并按照四阶段生命周期组织：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

真正涉及 Jnt、Controller、Connection 的 Rig Component 统一继承：

```python
from muziToolset.systems import RigComponentBase
```

它会把核心 `process_data()` 固定拆成：

```text
create_jnt()
      ↓
create_controller()
      ↓
create_connection()
```

因此 FK、IK、Single Control、Face、Jaw、Teeth、Tongue、Eye、Brow、Body、Spine、Ribbon 等 Rig 都可以使用同一套构建规范。

## 当前主要方向

```text
ComponentBase / RigComponentBase
Controller Builder / Parent Space Blend
Body / Skirt
Face Setup / Guide
Face Curve Attachment
Eyelid / Eye Bag
Lip / Zip Lip
```

## Face Rig

Face Guide 的职责划分、标准 Build / Finalize 流程、Guide 查询 API、左右镜像修复以及 Maya 测试方法，参见：

- [Face Guide 工作流](face-guide.md)

运行：

```bash
python scripts/generate_mkdocs_reference.py
```

后，本页会自动扫描 `systems/**/*.py`，并为当前真实模块生成第一版 Reference。

System 文档除了自动 API 页面外，后续还应该继续补充：

- 节点网络；
- Guide → Rig 数据流；
- Builder 输入 / 输出；
- 重建与删除策略；
- 命名规则；
- Maya 真机测试方式。
