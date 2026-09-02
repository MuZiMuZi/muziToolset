# Core 编码规范

## 模块头规范

所有正式 Core 模块顶部应说明：

```text
模块职责
正式模块路径
主要公开 API
模块边界
本模块不负责什么
```

打开文件第一屏就应该知道：

- 这个模块解决什么问题；
- 当前主要 API 是什么；
- 正式 Import 路径是什么；
- 哪些功能不应该继续塞进这个文件。

## 方法注释

建议使用清晰 Docstring 和阶段注释：

```python
def some_function(...):
    u"""功能说明。"""

    # 步骤 1：整理输入。

    # 步骤 2：执行 Maya 场景操作。
```

注释重点解释 Maya 特有行为和设计原因，不重复代码字面意思。

---

# 文件与 Python 命名

正式代码统一：

```text
文件      snake_case.py
函数      snake_case
变量      snake_case
类        PascalCase
```

当前 Core 示例：

```text
attr_utils.py
hierarchy_utils.py
joint_utils.py
rename_utils.py
matrix_utils.py
curve_utils.py
```

以下早期 CamelCase 模块已经删除：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

不要重新创建或 Import 这些名称。

---

# Rig Identity / Naming 已经移出 Core

旧：

```text
core/name_utils.py
```

已删除。

正式入口：

```text
systems/rig_base.py
```

`RigBase` 是可实例化的 Rig Object Identity 基类，不是 Name Utility。

Rig Object Identity：

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
    part="upper_arm",
    index=1
)

name = rig.create_name(
    node_type="jnt",
    function="bind"
)
```

不要写：

```python
RigBase.create_name(...)
```

也不要在 RigBase Naming API 中使用退休参数：

```python
type="jnt"
```

正式参数始终是：

```python
node_type="jnt"
```

需要解析已有 Rig Name 时，可以使用纯 Class Method：

```python
fields = RigBase.parse_name(
    "jnt_lf_upper_arm_bind_001"
)

valid = RigBase.validate_name(
    "jnt_lf_upper_arm_bind_001"
)
```

Core 中的：

```python
from muziToolset.core import rename_utils
```

只负责：

```text
get_short_name()
rename_node()
批量 Rename 行为
```

职责规则：

```text
RigBase
    一个 Rig 对象是谁：side / part / index
    并基于这个 Identity 创建正式 Rig Node 名称

rename_utils
    对 Maya 节点执行 Rename / Short Name
```

Core 不允许重新建立第二套 Rig Identity 或 Rig Naming Convention。

---

# Core Import Style Gate

```bash
python tests/core_import_style_test.py
```

检查退休 CamelCase Core 文件和 Import。

Rig 架构额外由：

```bash
python tests/rig_architecture_gate_test.py
```

阻止：

```text
core/name_utils.py
systems/component_base.py
systems/controller/
RigBase.create_name(...)
RigBase(name=...)
create_name(type=...)
```

重新出现。

---

# Maya API

优先：

```python
import maya.cmds as cmds
```

矩阵或高性能查询可以使用：

```python
import maya.api.OpenMaya as om
```

正式新代码不新增 PyMel。

---

# 循环写法

绑定代码优先可读性：

```python
result = []

for node in nodes:
    value = do_something(node)
    result.append(value)
```

不要为了缩短几行，把场景修改压成难调试的列表推导式。

尤其是：

```text
cmds.parent
cmds.connectAttr
cmds.setAttr
cmds.createNode
cmds.delete
```

这类 Scene 操作应保持展开步骤。

---

# Core 职责检查

提交新 API 前判断：

```text
可被多个 Tool / System 复用的 Maya 底层能力？
    → Core

已经知道自己在做 Teeth / Eyelid / Lip / Arm？
    → System / Module / Builder

正在描述一个 Rig Object 的 Identity 或基于 Identity 创建正式节点名？
    → RigBase

正在创建完整 Controller Hierarchy？
    → CtrlBase
```

Core 不应该重新长成万能 `pipelineUtils`，也不应该承载 Rig 业务基类。
