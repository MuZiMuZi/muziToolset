# Core 编码规范

## 模块头规范

所有正式 Core 模块顶部应包含：

```text
模块职责
正式模块路径
当前公开方法 / 类
每个方法功能简介
模块边界
本模块不负责
设计原则
```

打开文件第一屏就应该能知道：

- 这个模块解决什么问题；
- 当前有哪些主要 API；
- 正式 Import 路径是什么；
- 哪些功能不应该继续塞进这个文件。

## 方法注释

建议使用：

```python
def some_function(...):
    """
    功能说明。

    Args:
        ...

    Returns:
        ...
    """

    # -------------------------------------------------------------------------
    # 步骤 1：整理输入。
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # 步骤 2：执行 Maya 场景操作。
    #
    # 为什么：
    # 解释 Maya 特有行为，而不是重复代码字面意思。
    # -------------------------------------------------------------------------
```

步骤注释重点回答：

1. 这一阶段在做什么；
2. 为什么 Maya 需要这样处理；
3. 哪一步会修改 Scene / DG / DAG；
4. 为什么不能直接连接或直接 Parent；
5. 返回结果后准备给哪个 Tool / System 使用。

## 文件与 Python 命名

正式新代码统一：

```text
文件：snake_case.py
函数：snake_case
变量：snake_case
常量：snake_case（项目当前统一风格）
类：PascalCase
```

正式 Core 示例：

```text
attr_utils.py
hierarchy_utils.py
joint_utils.py
name_utils.py
rename_utils.py
matrix_utils.py
curve_utils.py
```

以下早期 CamelCase 模块已经完成迁移并删除：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

不要在新代码中重新创建这些文件，也不要重新 Import 这些名称。

正式写法：

```python
from muziToolset.core import attr_utils
from muziToolset.core import hierarchy_utils
from muziToolset.core import joint_utils
from muziToolset.core import name_utils
```

## Core Import Style Gate

GitHub Actions 会执行：

```bash
python tests/core_import_style_test.py
```

该 Gate 会同时检查：

```text
退休 CamelCase 文件有没有重新出现
              +
正式 Python 源码有没有重新 Import 旧模块
```

所以 snake_case 不只是文档约定，而是 CI 强制规则。

## Maya API

优先：

```python
import maya.cmds as cmds
```

矩阵或高性能查询可以使用：

```python
import maya.api.OpenMaya as om
```

正式新 Core 不新增 PyMel 依赖。

## 循环写法

绑定代码优先可读性：

```python
result = []

for node in nodes:
    value = do_something(node)
    result.append(value)
```

不要为了缩短几行，把场景操作压缩成难调试的列表推导式。

特别是涉及：

```text
cmds.parent
cmds.connectAttr
cmds.setAttr
cmds.createNode
cmds.delete
```

这类会修改 Maya Scene 的操作，保持展开的步骤式写法更容易定位失败节点。

## Core 职责检查

提交新 API 前问自己：

```text
这是可被多个 Tool / System 复用的底层能力吗？
    ↓ Yes
可能属于 Core

这个函数已经知道自己在做 Eyelid / Lip / Arm / Ribbon 吗？
    ↓ Yes
应该进入 System，而不是 Core
```

Core 不应该重新长成新的万能 `pipelineUtils`。
