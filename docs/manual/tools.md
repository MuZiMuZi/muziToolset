# 常用工具工作流

`tools/` 是绑定师可以直接打开的小工具层。

这里按“我要做什么”来找工具，不要求你先记住文件路径。

## 命名与基础操作

### 批量重命名

入口：`tools/basic/rename_tool.py`

适合：

- 批量 Prefix / Suffix；
- 自动编号；
- 统一 Rig 命名。

API：[打开 `rename_tool.py`](../reference/tools/basic/rename_tool.md)

### 属性管理

入口：`tools/basic/attr_tool.py`

适合：

- 打开 Add / Edit Attribute；
- 调整 Channel Box 属性顺序；
- 批量 Lock / Hide Transform 属性。

API：[打开 `attr_tool.py`](../reference/tools/basic/attr_tool.md)

### 连接管理

入口：`tools/basic/connections_tool.py`

适合检查和处理 Maya Plug 连接。

API：[打开 `connections_tool.py`](../reference/tools/basic/connections_tool.md)

### 约束与吸附

- `tools/basic/constraint_tool.py`
- `tools/basic/snap_tool.py`

API：

- [Constraint Tool](../reference/tools/basic/constraint_tool.md)
- [Snap Tool](../reference/tools/basic/snap_tool.md)

## Controller

### 创建标准控制器

入口：`tools/controller/create_ctrl_tool.py`

Tool 负责 UI；真正的标准 Controller 构建逻辑在：

```text
systems/controller/builder.py
```

因此修改 Controller 核心结构时，不要只改 Tool。

相关 API：

- [Create Ctrl Tool](../reference/tools/controller/create_ctrl_tool.md)
- [Controller Builder](../reference/systems/controller/builder.md)
- [Control Shape Utils](../reference/core/control_shape_utils.md)

### 控制器 Shape

入口：`tools/controller/control_shape_tool.py`

用于浏览、应用和编辑控制器 Shape。

API：[Control Shape Tool](../reference/tools/controller/control_shape_tool.md)

## Joint

### Joint 常用操作

入口：`tools/joint/joint_tool.py`

API：[Joint Tool](../reference/tools/joint/joint_tool.md)

### Joint 重采样

入口：`tools/joint/joint_resamp_tool.py`

适合重新分布 Joint 数量或沿现有结构重建 Joint。

API：[Joint Resample Tool](../reference/tools/joint/joint_resamp_tool.md)

## Skin

入口：`tools/skin/skin_tool.py`

Tool 负责选择和 UI；底层 SkinCluster / Weight 能力在 `core/skin_utils.py`。

相关 API：

- [Skin Tool](../reference/tools/skin/skin_tool.md)
- [Skin Utils](../reference/core/skin_utils.md)

## BlendShape

常用入口：

- `tools/blendshape/add_blendshape_tool.py`
- `tools/blendshape/invert_shape_tool.py`

底层能力：`core/blendshape_utils.py`

相关 API：

- [Add BlendShape Tool](../reference/tools/blendshape/add_blendshape_tool.md)
- [Invert Shape Tool](../reference/tools/blendshape/invert_shape_tool.md)
- [BlendShape Utils](../reference/core/blendshape_utils.md)

## 清理与检查

### 模型检查

入口：`tools/clean/model_checker.py`

底层：`core/model_check_utils.py`

### 层级清理

入口：`tools/clean/hierarchy_cleaner.py`

底层通用 Scene 清理能力位于 `core/scene_clean_utils.py`。

## Face

当前 Face UI 入口位于：

```text
tools/face/
```

完整 Face Rig 生命周期则放在：

```text
systems/face/
```

如果你要修改 Face Setup / Guide / Eyelid / Lip 的算法，优先看 [Face Guide](face-guide.md) 和 Systems API，而不是只改 UI Tool。

## Rig 辅助工具

`tools/rig/` 放直接给绑定师使用的 Rig 辅助面板。

如果一个功能开始拥有稳定输入、输出、可重复 Build 和完整节点网络，应该考虑把核心逻辑下沉到 `systems/`。

## 如何打开 Tool

多数 Tool 都提供 `main()`：

```python
from muziToolset.tools.basic import attr_tool

window = attr_tool.main()
```

如果某个文件没有公开 `main()`，API 页面会显示实际公开入口。
