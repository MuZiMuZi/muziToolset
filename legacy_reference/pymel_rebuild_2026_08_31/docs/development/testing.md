# 测试

MuziTools 的质量门槛分成两层：

```text
普通 Python / GitHub Actions
    -> 静态架构 + MkDocs 构建

Maya 2023
    -> 真实 Scene / DG / DAG / UI 行为
```

两层测试不能互相替代。

---

# 1. Pipeline / Core Smoke Test

Maya Python Script Editor：

```python
import muziToolset

report = muziToolset.pipeline_smoke_test()
```

这组测试用于验证基础 Core 拆分后的关键底层能力，例如：

```text
Scene
Transform
Animation
Connection
Matrix
Constraint
Curve
Surface
Animation IO
```

测试过程中会创建临时 Maya 节点，完成计算验证后自动清理。

Matrix Case 会重点验证 `offsetParentMatrix` 网络，防止重新出现由 Driven 自身 `parentInverseMatrix` 引起的 Evaluation Cycle。

---

# 2. Extended Core Smoke Test

Maya Python Script Editor：

```python
import muziToolset

report = muziToolset.extended_core_smoke_test()
```

测试范围：

```text
attr_utils
    Attribute / String Config / Message Config

hierarchy_utils
    Extra Group / Parent / World Transform 保持

joint_utils
    Joint Create / Chain / Radius / Joint Label

name_utils + rename_utils
    Standard Name / Parse / Mirror / Maya Rename

model_check_utils
    Model Issue / Issue Schema

scene_clean_utils
    Safe Freeze / Recursive Empty Group Clean
```

当前 Maya 2023 已验证结果：

```text
Total: 6 | Passed: 6 | Failed: 0
```

这组测试是这轮 Core snake_case 整理后的主要真机质量门槛。

---

# 3. Tool Window Smoke Test

所有正式 UI Tool 都要求下面这种调用在 Maya Script Editor 中直接显示窗口：

```python
from muziToolset.tools.controller import create_ctrl_tool

window = create_ctrl_tool.main()
```

完整自动验证入口：

```python
import muziToolset

report = muziToolset.tool_window_smoke_test()
```

测试步骤：

```text
调用 Tool.main()
    ↓
确认返回 QWidget / QDialog
    ↓
确认窗口 Visible
    ↓
再次调用 main()
    ↓
确认还是同一个实例
    ↓
关闭测试窗口
```

测试只检查窗口生命周期，不点击实际 Rig 功能按钮，因此不会创建 Joint、修改 Skin 或执行 Scene Clean。

当前 Maya 2023 已验证结果：

```text
Total: 17 | Passed: 17 | Failed: 0
```

执行型 Tool，例如 Quick Snap 或根据 Selection 直接创建 FK Controller，不属于窗口测试范围。

---

# 4. Core Import Style Gate

Core 已经统一为 snake_case：

```text
attr_utils.py
hierarchy_utils.py
joint_utils.py
name_utils.py
```

以下历史 CamelCase 文件已经删除：

```text
attrUtils.py
hierarchyUtils.py
jointUtils.py
nameUtils.py
```

静态检查：

```bash
python tests/core_import_style_test.py
```

该测试不 Import Maya，使用 Python AST 检查：

1. `core/` 下不能重新出现退休 CamelCase 文件；
2. `app / ui / core / tools / systems / tests` 不能重新 Import 退休模块。

发现问题时脚本返回非零退出码，因此可以作为 GitHub Actions 的硬质量门槛。

---

# 5. Controller Component Test

```python
report = muziToolset.controller_component_smoke_test()
```

用于验证 Controller System，例如 Parent Space Blend。

---

# 6. Face Component Test

```python
report = muziToolset.face_component_smoke_test()
```

用于验证 Face System 中已经正式化的组件。

这组测试与 Core Smoke 分开维护。只有在 Maya 真机运行并得到明确 PASS 输出后，才应该在文档中记录为已验证状态。

---

# 7. 文档 / CI 测试

文档本身不需要 Maya。

本地可以执行：

```bash
python tests/core_import_style_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

GitHub Actions 的正式顺序：

```text
Checkout
    ↓
Install Documentation Dependencies
    ↓
Core Import Style Gate
    ↓
Generate API Reference
    ↓
mkdocs build --strict
    ↓
Upload Pages Artifact
    ↓
Deploy GitHub Pages
```

AST Reference 生成器不会 Import `maya.cmds`，因此 Linux Runner 可以直接构建文档。

---

# 8. 重构 Core 时的推荐顺序

```text
读取现有调用
    ↓
确定正式模块职责
    ↓
保持 API 或准备兼容迁移
    ↓
修改 Core
    ↓
更新 Tool / System 调用
    ↓
更新 Smoke Test
    ↓
运行静态 Import Gate
    ↓
Maya 2023 真机验证
    ↓
删除确认无引用的旧入口
    ↓
更新 MkDocs 文档
    ↓
确认 GitHub Actions 全绿
```

不要在静态引用归零和 Maya 真机测试之前删除仍可能被正式代码引用的旧 API。
