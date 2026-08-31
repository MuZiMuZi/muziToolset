# Legacy Reference

`legacy_reference/` 只保存历史实现、迁移快照和第三方集成参考。

正式运行代码禁止从这里 import 任何模块。

## 当前主要快照

```text
legacy_reference/pymel_rebuild_2026_08_31/
```

这是切换到 PyMEL-first 架构前的完整旧运行层快照，包含旧 Core、Tools、App、UI、Tests、Docs、Resources，以及非 Face Systems。

Face Rig 没有移出正式区；它作为当前唯一业务系统继续迁移。

## 使用规则

历史代码只能用于：

- 阅读旧业务流程；
- 对比旧算法；
- 确认工具最终效果；
- 为新的 PyMEL 实现提供参考。

禁止：

```python
from legacy_reference import ...
```

也不要修改 `sys.path` 把这里重新加入正式运行环境。

旧功能需要恢复时，应重新理解需求，并基于当前 `core/`、`systems/`、`tools/` 架构重新实现。
