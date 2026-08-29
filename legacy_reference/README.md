# Legacy Reference

这个目录保存 Muzi Toolset 的历史实现，只用于查阅、对比和提取旧算法。

当前包含：

```text
legacy_reference/
├─ MuziTools/      # 旧工具箱与旧 UI 结构
├─ bind/           # 早期绑定相关代码
├─ core/           # 旧 Core 全量备份
├─ dev/            # 旧开发辅助脚本，例如 MayaSender
├─ face/           # 旧 Face Rig 与旧 Face UI
├─ pyside/         # PySide 学习 / 旧界面代码
├─ res/            # 旧资源与 UI 资源
└─ rigging/        # 旧 Body / IKFK / Rig 参考实现
```

其中 `rigging/line_rig_v02.py` 等实验脚本也统一保存在历史区，不再占用项目根目录。

## 使用规则

这些目录 **不属于当前正式运行架构**。

正式代码禁止：

```python
from legacy_reference import ...
```

也不要通过修改 `sys.path` 的方式把历史目录重新加入正式运行路径。

如果历史代码中有仍然有价值的功能，应按下面流程处理：

1. 阅读旧实现；
2. 找出真正需要保留的算法；
3. 去掉旧 UI、旧路径、PyMel、主动 reload 等不再需要的依赖；
4. 根据职责迁入根包中的 `core/`、`tools/` 或 `systems/`；
5. 把场景算法与 PySide UI 分开；
6. 使用正式 `ui/` Theme、`app/window_manager.py` 和公共 Widget；
7. 在 Maya 中验证新实现后，再让正式工具调用新的 API。

## 正式代码位置

当前正式运行框架就是仓库根包：

```text
muziToolset/
├─ app/
├─ ui/
├─ core/
├─ tools/
├─ systems/
└─ resources/
```

历史区只作为代码资料库，不应该重新变成第二套运行架构。
