# MuziTools structure

`MuziTools/` 现在只保留主入口、资源和按功能分类后的工具实现。
旧的 `*_Tool_main.py` 已删除，不再作为兼容层维护。

## 目录职责

```text
MuziTools/
├─ __init__.py          # 包入口：MuziTools.show()
├─ main.py              # Maya 脚本入口
├─ rigging_toolbox.py   # 主工具箱 UI
├─ window_manager.py    # 子工具窗口生命周期管理
├─ config.py            # 资源路径配置
├─ tools/               # 实际工具实现
│  ├─ basic/
│  ├─ joint/
│  ├─ ctrl/
│  ├─ rig/
│  ├─ face/
│  ├─ skin/
│  ├─ blendShape/
│  └─ clean/
├─ image/               # Controller Shape JSON / 缩略图
├─ icon/                # UI 图标
├─ qss/                 # Qt 样式表
└─ ui/                  # 仍需要保留的 UI 资源
```

## 新代码调用规则

不要再 import 已删除的 `Attr_Tool_main`、`Joint_Tool_main`、
`Rig_Tool_main` 等旧模块。

需要直接打开某个工具时，从新的分类包导入：

```python
from muziToolset.MuziTools.tools.joint import joint_tool
joint_tool.main()

from muziToolset.MuziTools.tools.ctrl import create_ctrl_tool
create_ctrl_tool.main()

from muziToolset.MuziTools.tools.skin import skin_tool
skin_tool.main()
```

主工具箱推荐入口：

```python
import muziToolset
muziToolset.show()
```

不再需要硬编码 Maya scripts 绝对路径。
