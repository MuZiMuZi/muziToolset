# 基础工具

用于日常绑定中最高频的五类操作：**重命名、属性、连接、约束、吸附**。

<div class="grid cards" markdown>

-   :material-rename:{ .lg .middle } **重命名**

    ---

    Prefix、Suffix、编号和 Rig 命名整理。

    [:octicons-code-24: Rename API](../reference/tools/basic/rename_tool.md)

-   :material-tune:{ .lg .middle } **属性**

    ---

    添加属性、Lock / Hide、Channel Box 和 Message 配置。

    [:octicons-code-24: Attr API](../reference/tools/basic/attr_tool.md)

-   :material-connection:{ .lg .middle } **连接**

    ---

    查看、建立和断开 Maya Plug 连接。

    [:octicons-code-24: Connections API](../reference/tools/basic/connections_tool.md)

-   :material-vector-link:{ .lg .middle } **约束**

    ---

    Parent、Point、Orient、Scale 和 Aim Constraint。

    [:octicons-code-24: Constraint API](../reference/tools/basic/constraint_tool.md)

-   :material-target:{ .lg .middle } **吸附**

    ---

    快速匹配 Position、Rotation 和 Transform。

    [:octicons-code-24: Snap API](../reference/tools/basic/snap_tool.md)

</div>

## 打开工具

大多数基础工具提供 `main()`：

```python
from muziToolset.tools.basic import rename_tool

window = rename_tool.main()
```

!!! info "Tool 和 Core 的区别"
    Tool 负责 UI、Selection 和用户输入；真正可复用的 Maya 算法应放在 `core/`。

## 推荐用法

1. 在 Maya 中选择需要处理的对象。
2. 打开对应 Tool。
3. 设置参数并执行。
4. 如果结果不符合预期，先看 Script Editor，再进入对应 API 页面检查输入要求。

## 对应底层模块

| 操作 | Core |
| --- | --- |
| 命名规则 | [name_utils.py](../reference/core/name_utils.md) / [rename_utils.py](../reference/core/rename_utils.md) |
| Attribute | [attr_utils.py](../reference/core/attr_utils.md) |
| Plug Connection | [connection_utils.py](../reference/core/connection_utils.md) |
| Constraint | [constraint_utils.py](../reference/core/constraint_utils.md) |
| Snap / Match | [snap_utils.py](../reference/core/snap_utils.md) / [transform_utils.py](../reference/core/transform_utils.md) |

## 常见问题

**按钮没有效果**

先检查 Selection、节点 Lock 状态和 Script Editor 报错。

**应该改 Tool 还是 Core？**

```text
只改界面或选择方式  → tools/
多个功能复用同一算法 → core/
完整 Rig Component   → systems/
```

[返回常用工具](tools.md){ .md-button }
[打开 Core API](../reference/core/index.md){ .md-button .md-button--primary }
