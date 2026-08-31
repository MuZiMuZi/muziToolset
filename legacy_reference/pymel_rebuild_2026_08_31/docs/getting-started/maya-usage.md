# Maya 中运行

## 主工具箱

推荐入口：

```python
import muziToolset
muziToolset.show()
```

窗口生命周期统一由 `app/window_manager.py` 管理。

## 运行 Smoke Test

### Core / Pipeline Refactor

```python
import muziToolset
report = muziToolset.pipeline_smoke_test()
```

当前这组测试用于验证 Core 中的重要底层能力，例如：

```text
scene
transform
animation
connection
matrix
constraint
curve
surface
```

### Controller System

```python
report = muziToolset.controller_component_smoke_test()
```

### Face System

```python
report = muziToolset.face_component_smoke_test()
```

## Tool 与 Core 的使用区别

Tool 一般直接面向用户：

```text
用户选择
    ↓
PySide Tool
    ↓
Core / System
    ↓
Maya Scene
```

Core 则应该直接接收明确参数：

```python
from muziToolset.core import transform_utils

position = transform_utils.get_world_translation(
    "ctrl_lf_arm_001"
)
```

不推荐让 Core 自己猜当前 Selection 或弹出 PySide 窗口。
