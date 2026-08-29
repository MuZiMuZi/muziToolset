# MuziTools structure

`MuziTools/` 已完成旧入口收敛：

- 旧 `*_Tool_main.py` 已删除；
- 旧顶层转发文件已删除；
- 旧 `ui/` 和 `qss/` 资源已删除；
- 实际工具实现统一放在 `tools/<category>/`；
- 主工具箱只做工具发现、启动和窗口管理。

## 当前目录

```text
MuziTools/
├─ __init__.py          # 包入口：MuziTools.show()
├─ main.py              # Maya Python 脚本入口
├─ config.py            # tools / image / icon 资源路径
├─ rigging_toolbox.py   # 主工具箱 UI
├─ window_manager.py    # PySide 子工具窗口生命周期管理
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
└─ icon/                # 当前工具需要的 UI 图标
```

## 调用规则

不要再 import 已删除的 `Attr_Tool_main`、`Joint_Tool_main`、
`Rig_Tool_main`、`Control_Tool_main` 等旧模块。

直接打开具体工具时，从对应分类包导入：

```python
from muziToolset.MuziTools.tools.joint import joint_tool
joint_tool.main()

from muziToolset.MuziTools.tools.ctrl import create_ctrl_tool
create_ctrl_tool.main()

from muziToolset.MuziTools.tools.skin import skin_tool
skin_tool.main()
```

推荐的主入口：

```python
import muziToolset
muziToolset.show()
```

工具注册表采用懒加载：打开主工具箱不会一次性 import 所有子工具，只有点击某个工具时才加载对应模块。
