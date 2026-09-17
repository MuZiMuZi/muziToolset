# 源码文件职责边界

MuziTools 采用“一个职责一个文件”，但不会机械地把每个方法拆成独立文件。拆分的目标是让文件名能够直接回答：这段代码负责什么、依赖谁、由谁调用。

## 分层方向

```text
app / ui
    ↓
tools
    ↓
systems
    ↓
core
```

`core` 不允许反向导入 Tool、UI 或具体 Rig System。Maya 界面只负责收集输入和展示状态，绑定构建规则保留在 System，通用 Maya 能力下沉到 Core。

## 文件拆分标准

| 文件职责 | 应包含 | 不应包含 |
| --- | --- | --- |
| `*_catalog.py` | 名称、说明、静态注册信息 | Qt Widget、Maya 场景修改 |
| `*_widgets.py` | 可复用小型 Widget | 完整业务工作流 |
| `*_window.py` | 主窗口布局与信号编排 | Joint、Controller 构建算法 |
| `*_service.py` | 用例编排、状态转换 | 具体 Qt 绘制 |
| `*_builder.py` | Maya 节点创建与连接 | 文档展示数据 |
| `*_config.py` | 可序列化配置与 Schema | UI 临时状态 |
| `*_utils.py` | 单一 Maya 领域的通用能力 | 完整绑定流程 |

## 兼容策略

旧文件保留公开导入入口，通过显式 Import 转发到新模块。调用方可以逐步迁移，不需要在一次提交中同时修改全部 Maya Shelf、用户脚本和历史场景工具。

例如主工具箱的展示目录已经从 `app/toolbox.py` 拆到：

```python
from muziToolset.app.toolbox_catalog import get_tool_display_name
```

旧入口仍然可以继续使用：

```python
from muziToolset.app.toolbox import get_tool_display_name
```

## 文档映射

每个正式 Runtime Python 文件必须生成一个独立 API Reference 页面。生成器使用 AST 读取源码，不会 Import Maya，因此 GitHub Actions 和普通 Python 环境也能完成文档构建。

新增或拆分文件后必须依次执行：

```bash
python scripts/normalize_runtime_docstrings.py --check
python tests/docs_runtime_api_coverage_test.py
python scripts/generate_mkdocs_reference.py
python scripts/refine_generated_reference.py
python tests/docs_generated_layout_test.py
mkdocs build --strict
```

## Maya 2023 约束

- Runtime 继续使用 `maya.cmds`，不新增 PyMEL 依赖。
- Maya 2023 使用 PySide2；PySide6 只作为 Maya 2025+ 兼容分支。
- 拆分只改变模块边界，不改变节点命名、DAG 层级、Guide 位置或连接顺序。
- 复杂函数继续采用中文 `Step 01 → Step 02 → …` 注释。
- 旧 Import Path 删除前必须先经过 Maya 2023 场景回归。
