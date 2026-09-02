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

# Rig Naming

旧：

```text
core/name_utils.py
```

已删除。

正式入口：

```text
systems/rig_base.py
```

标准命名统一为：

```text
[type]_[side]_[part]_[function]_[index]
```

正式字段统一使用：

```text
type
side
part
function
index
```

不要再使用 `node_type` 作为 Rig Naming 字段。

## 直接创建名称

```python
from muziToolset.systems.rig_base import RigBase

jaw_ctrl = RigBase(
    type="ctrl",
    side="md",
    part="jaw",
    function="bind",
    index=1
)

print(jaw_ctrl.name)
# ctrl_md_jaw_bind_001
```

## 从已有名称快速拆分

```python
jaw_ctrl = RigBase(
    name="ctrl_md_jaw_bind_001"
)

print(jaw_ctrl.type)
print(jaw_ctrl.side)
print(jaw_ctrl.part)
print(jaw_ctrl.function)
print(jaw_ctrl.index)
```

也可以单独读取字段：

```python
name_data = RigBase.parse_name(
    "jnt_lf_upper_teeth_bind_003"
)
```

返回：

```python
{
    "type": "jnt",
    "side": "lf",
    "part": "upper_teeth",
    "function": "bind",
    "index": 3,
}
```

Module 可以只继承和保存自己需要的 `side / part / index`，需要具体节点名称时再补充 `type / function`。

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

Core 不允许重新建立第二套 Rig Naming Convention。

---

# 内部 Naming 默认可信

绑定库内部创建的名称全部来自统一 Rig Naming API，因此**不要在每一层重复判断名称是否符合规范**。

不推荐：

```python
if not isinstance(ctrl_name, str):
    ...

if not ctrl_name.startswith("ctrl_"):
    ...

if ":" in ctrl_name:
    ...

if "|" in ctrl_name:
    ...
```

也不需要在每次创建名称时重复做：

```text
normalize_side
normalize_type
normalize_part
normalize_function
validate_index
validate_name
```

项目约定：

```text
内部 Rig 数据
    → 默认符合统一规范
    → 直接组合 / 拆分 / 使用

已有 Maya 场景数据
    → 可能来自上一次 Build / Rebuild
    → 判断目标节点、属性、连接是否真实存在
```

因此真正应该重点检查的是 Scene State，例如：

```python
if cmds.objExists(node_name):
    # 已存在节点：进入 Rebuild / Cleanup / Update 逻辑
```

以及：

```python
if cmds.attributeQuery(
        attr_name,
        node=node_name,
        exists=True
):
    # 已有属性：复用或恢复
```

这类存在性判断主要用于：

```text
Rebuild
Restore
Cleanup
重复执行 Build
恢复 Attribute / Connection
查找上一次创建的节点
```

不要把“名称格式防御”与“场景状态判断”混在一起。

---

# 复用优先

新增代码前，先检查 Core 是否已经提供同类能力。**能调用现有 Core API 时，不在 System / Tool 中重新创建同功能 Helper。**

推荐顺序：

```text
1. 先查现有 core/*_utils.py
2. 已有能力 → 直接调用
3. 多个 System / Tool 出现相同 Maya 底层逻辑 → 提取到对应 Core 模块
4. 只有明确 Rig 业务语义的代码 → 留在 System / Module / Builder
5. 只有 UI / Selection 交互语义的代码 → 留在 Tool / UI
```

例如：

```text
节点存在、Scene Query       → scene_utils
Parent / Child / Descendant → hierarchy_utils
Transform / Matrix Space    → transform_utils / matrix_utils
Attribute                   → attr_utils
Plug Connection             → connection_utils
Short Name / Maya Rename    → rename_utils
Joint                       → joint_utils
Curve                        → curve_utils
Controller Shape             → control_shape_utils
```

不推荐在业务模块中重新包装：

```python
def get_parent(node):
    return cmds.listRelatives(node, parent=True)
```

如果已有：

```python
hierarchy_utils.get_parent(node)
```

就直接调用现有 Core。

只有满足下面条件时才新增 Core API：

```text
- 与具体 Face / Teeth / Lip / Jaw 等业务无关；
- 至少有多个调用场景，或明显会成为通用底层能力；
- 现有 Core 中没有等价 API；
- 能明确归属到一个 Core 领域模块，而不是建立万能 Utils。
```

代码 Review 时，新增私有 Helper 也必须先判断是否已经有 Core 等价能力。

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
退休 Component 类名
RigBase 重新加入多余 Normalize / Validate Naming 层
Rig Naming 重新使用 node_type 字段
```

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
现有 Core 已经能做？
    → 直接复用，不新增 Helper

可被多个 Tool / System 复用的 Maya 底层能力？
    → Core

已经知道自己在做 Teeth / Eyelid / Lip / Arm？
    → System / Module / Builder

正在创建、组合或拆分正式 Rig Name？
    → RigBase

正在创建完整 Controller Hierarchy？
    → CtrlBase

正在确认上一次 Build 的节点是否还存在？
    → Scene / Rebuild 逻辑
```

Core 不应该重新长成万能 `pipelineUtils`，也不应该承载 Rig 业务基类。
