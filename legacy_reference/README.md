# Legacy Reference

这个目录保存 Muzi Toolset 的历史实现，只用于查阅和提取旧算法。

当前包含：

```text
legacy_reference/
├─ bind/
├─ pyside/
├─ res/
└─ rigging/
```

## 使用规则

这些目录 **不属于当前正式运行架构**。

正式代码禁止：

```python
from legacy_reference import ...
```

如果历史代码中有仍然有价值的功能，应按下面流程处理：

1. 阅读旧实现；
2. 找出需要保留的算法；
3. 去掉旧 UI、旧路径、PyMel 等不再需要的依赖；
4. 按职责迁入 `muzi_rigging/core`、`muzi_rigging/tools` 或 `muzi_rigging/systems`；
5. 为新实现增加清晰的中文注释和 Maya 使用边界。

不要直接让新系统依赖历史包，否则项目会重新产生两套运行架构。
