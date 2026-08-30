# 基础工具

这页用于日常 Maya 绑定中最常见的基础操作：重命名、属性、连接、约束和吸附。

如果你只是想“完成操作”，优先从这里开始；如果你要修改实现，再进入对应 API 页面。

## 快速入口

| 你想做什么 | Tool | API |
| --- | --- | --- |
| 批量重命名 | `tools/basic/rename_tool.py` | [Rename Tool](../reference/tools/basic/rename_tool.md) |
| 添加 / 编辑属性 | `tools/basic/attr_tool.py` | [Attr Tool](../reference/tools/basic/attr_tool.md) |
| 查看 / 修改连接 | `tools/basic/connections_tool.py` | [Connections Tool](../reference/tools/basic/connections_tool.md) |
| 创建约束 | `tools/basic/constraint_tool.py` | [Constraint Tool](../reference/tools/basic/constraint_tool.md) |
| 快速吸附 | `tools/basic/snap_tool.py` | [Snap Tool](../reference/tools/basic/snap_tool.md) |

## 打开一个 UI Tool

多数基础工具提供 `main()`：

```python
from muziToolset.tools.basic import rename_tool

window = rename_tool.main()
```

如果只是一次性执行操作的 Tool，`main()` 可能直接处理当前 Selection，而不是返回 QWidget。具体行为以对应 API 页面为准。

## 批量重命名

适合这些情况：

- 批量添加 Prefix / Suffix；
- 自动编号；
- 清理错误命名；
- 把临时模型名称整理成 Rig 命名。

推荐步骤：

```text
选择对象
    ↓
打开 Rename Tool
    ↓
选择 Prefix / Suffix / Number 规则
    ↓
Preview 或确认范围
    ↓
执行 Rename
```

底层命名算法主要在：

- [rename_utils.py](../reference/core/rename_utils.md)
- [name_utils.py](../reference/core/name_utils.md)

如果要修改“命名算法”，优先改 Core；如果只是修改按钮、输入框和交互，改 Tool。

## 属性管理

`attr_tool.py` 适合：

- 添加自定义 Attribute；
- 编辑 Min / Max / Default；
- Lock / Hide Channel；
- 调整 Channel Box 中的属性；
- 管理 Message 等绑定配置属性。

底层能力：

- [attr_utils.py](../reference/core/attr_utils.md)

推荐原则：

```text
Tool
    收集用户输入
        ↓
Attr Utils
    真正修改 Maya Attribute
```

## 连接管理

`connections_tool.py` 用于 Maya Plug 连接的查看和处理。

常见用途：

- 查看一个属性的输入；
- 查看一个属性的输出；
- 建立连接；
- 断开连接；
- 排查“为什么这个属性不能改”。

底层 API：

- [connection_utils.py](../reference/core/connection_utils.md)

开发时建议尽量使用完整 Plug：

```text
node.attribute
```

而不是只保存节点名。

## 约束

`constraint_tool.py` 适合快速创建：

- Parent Constraint；
- Point Constraint；
- Orient Constraint；
- Scale Constraint；
- Aim Constraint。

底层 API：

- [constraint_utils.py](../reference/core/constraint_utils.md)

复杂 Rig 如果需要大量稳定空间关系，建议同时评估 Matrix 方案：

- [matrix_utils.py](../reference/core/matrix_utils.md)

## 快速吸附

`snap_tool.py` 适合：

- Position Snap；
- Rotation Snap；
- Transform Match；
- 快速把 Controller / Joint 对齐到目标。

底层 API：

- [snap_utils.py](../reference/core/snap_utils.md)
- [transform_utils.py](../reference/core/transform_utils.md)

## 常见问题

### Tool 能打开，但按钮没有效果

先检查：

1. 当前 Maya Selection 是否符合 Tool 要求；
2. Script Editor 是否有 RuntimeError；
3. 对应节点是否被 Lock；
4. 是否存在同名节点导致查询歧义。

### 我应该改 Tool 还是 Core？

判断方法：

```text
只影响 UI / 选择 / 输入
    → tools/

多个工具都需要同一算法
    → core/

已经是完整 Rig Component
    → systems/
```

## 继续查看

- [常用工具工作流](tools.md)
- [Core API](../reference/core/index.md)
- [Tools API](../reference/tools/index.md)
