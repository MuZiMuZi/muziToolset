# 文档维护

MuziTools 文档分成两层，而且职责不能混在一起。

## 1. 用户手册

用于解释：

- 我想完成什么；
- 推荐操作顺序；
- 什么时候使用哪个 Tool / System；
- 常见错误和修复方式；
- 一个完整 Rig Workflow 怎么走。

目录：

```text
docs/getting-started/
docs/manual/
docs/architecture/
docs/development/
docs/migration/
```

用户手册是人工维护内容。

当前主要任务页：

```text
docs/manual/basic-tools.md
docs/manual/controller.md
docs/manual/jnt.md
docs/manual/skin.md
docs/manual/blendshape.md
docs/manual/cleanup.md
docs/manual/rigging.md
docs/manual/face-guide.md
```

## 2. API Reference

由：

```text
scripts/generate_mkdocs_reference.py
```

使用 Python AST 自动扫描正式 Runtime 源码：

```text
__init__.py
config.py
app/
core/
systems/
tools/
ui/
```

生成：

```text
docs/reference/
docs/SUMMARY.md
```

然后：

```text
scripts/extend_docs_summary.py
```

只负责把人工维护的任务型用户手册页面补进 `SUMMARY.md`。

这样职责保持清楚：

```text
API Generator
    维护动态源码树

Navigation Extender
    维护人工任务页导航
```

API Reference 负责解释：

- 模块做什么；
- Function / Class / Method 有哪些；
- Signature；
- 参数类型；
- 参数是否必填；
- 默认值；
- 返回值；
- 异常；
- 示例；
- Notes；
- 源码位置。

---

# Docstring 是 API 文档第一事实来源

不要在 Markdown 里手工复制一份函数签名和参数说明。

应该先把源码 Docstring 写完整，再让生成器同步到网站。

推荐：

```python
def get_world_position(self, guide):
    u"""
    获取 Guide Transform 的世界坐标。

    Args:
        guide (str):
            Maya Guide Transform 名称。
            节点必须存在于当前场景中。

    Returns:
        list:
            世界空间坐标。

            格式::

                [x, y, z]

    Raises:
        ValueError:
            guide 为空时抛出。

        RuntimeError:
            Guide 节点不存在时抛出。

    Example:
        >>> guide_system = FaceGuide()
        >>> position = guide_system.get_world_position(
        ...     "loc_lf_eye_ball_guide_001"
        ... )

    Notes:
        返回 World Space Position，不是 Local Translate。
    """
```

生成后的 API 页面会自动拆成：

```text
功能摘要
Signature
参数
返回值
异常
示例
Notes
```

如果源码暂时没有完整 Docstring，Generator 会保留 API 骨架和自动调用示例，但正式公开 API 仍应该继续补全源码说明。

---

# Module Docstring 规范

每个正式 `.py` 文件建议说明：

```text
模块名称
模块解决什么问题
主要职责
设计边界
典型使用方式
兼容环境
```

示例：

```python
u"""
Face Guide
==========

Face Rig Step 02 Guide Manager。

职责：
    1. 加载 Guide 模板；
    2. 查询定位数据；
    3. 验证 Guide；
    4. 修复镜像关系。

设计边界：
    - 不创建最终 Jnt；
    - 不创建最终 Controller；
    - 模板视觉属性保存在 face_guide.ma。
"""
```

---

# Function / Method Docstring 规范

公开 API 至少应该有一句明确摘要：

```python
def validate_guides(self, check_symmetry=True):
    u"""检查 Step 02 Guide 是否可以交给后续 Builder。"""
```

复杂公开 API 推荐补齐：

```text
Args
Returns
Raises
Example
Notes
```

## Args

```python
Args:
    side (str):
        方向，只允许 "lf" 或 "rt"。

    required (bool):
        Guide 缺失时是否直接抛出异常。
```

参数说明应该回答：

- 这个值是什么；
- 有哪些合法值；
- 单位是什么；
- `None` 代表什么；
- 会不会修改 Maya Scene。

## Returns

```python
Returns:
    dict:
        Eyelid Guide 数据。

        格式::

            {
                "upper": [...],
                "lower": [...],
            }
```

不要只写类型，尽量说明返回结构。

## Raises

```python
Raises:
    ValueError:
        side 不是 lf / rt 时抛出。

    RuntimeError:
        必须的 Guide 节点缺失时抛出。
```

## Example

```python
Example:
    >>> guide = FaceGuide()
    >>> left_lid = guide.get_eyelid_guides(
    ...     side="lf"
    ... )
```

示例应该尽量可以直接复制到 Maya Python Script Editor。

## Notes

```python
Notes:
    返回顺序已经固定，Builder 不应该再次自行排序。
```

Notes 用于记录容易误用的约束，而不是重复摘要。

---

# 用户手册写法

用户手册不要按源码文件顺序写。

推荐结构：

```text
标题
    ↓
什么时候使用
    ↓
快速入口
    ↓
推荐步骤
    ↓
常见操作
    ↓
常见问题
    ↓
对应 API
    ↓
继续查看
```

例如 Controller 用户手册先回答：

```text
我要怎么创建 Controller？
```

而不是一上来解释：

```text
systems/controller/builder.py 有哪些函数？
```

后者属于 API Reference。

---

# 左侧导航

第一阶段由 API Generator 生成：

```bash
python scripts/generate_mkdocs_reference.py
```

会得到：

```text
docs/SUMMARY.md
```

然后执行：

```bash
python scripts/extend_docs_summary.py
```

把人工任务页加入用户手册区域。

MkDocs 使用：

```text
mkdocs-literate-nav
```

读取最终 `SUMMARY.md`。

最终结构类似：

```text
用户手册
├── 基础工具
├── Controller
├── Jnt
├── Skin
├── BlendShape
├── 场景清理
├── 绑定工作流
└── Face Guide

API 参考
├── App
├── Core
├── Tools
├── Systems
├── UI
└── Package
```

API 下的文件树保持与源码目录一致。

---

# README 同步规则

`README.md` 是 GitHub 仓库首页，也是文档站入口地图。

当下面任意内容变化时必须同步 README：

- 新增 / 删除主要用户手册页面；
- 调整文档一级分类；
- 修改 API 覆盖范围；
- 修改源码顶层架构；
- 修改 Docs CI；
- 修改在线文档入口。

README 中的文档路径必须和 `docs/` 实际结构对应。

当前要求：

```text
README 文档导航
        ↓
docs/ 真实路径
        ↓
SUMMARY.md 网站导航
```

三者使用同一套分类和命名。

不要出现：

```text
README 叫“Core 手册”
网站叫“开发参考”
docs 目录又叫别的名字
```

---

# 为什么继续使用 AST

GitHub Actions 没有 Maya。

如果文档生成器直接：

```python
import maya.cmds
```

在线文档就无法构建。

当前方案：

```text
read source
    ↓
ast.parse
    ↓
Docstring / Signature
    ↓
Markdown
```

因此：

- 不需要 Maya；
- 不需要 PySide；
- 不执行 Scene 修改；
- 可以在 Linux Runner 构建。

---

# 文档覆盖 Gate

两个静态测试负责文档质量底线。

## Generator Smoke Test

```bash
python tests/docs_reference_generator_test.py
```

检查：

- Package 页面；
- Function / Class / Method；
- 参数表；
- Returns；
- Raises；
- Example；
- SUMMARY 基础导航。

## Runtime API Coverage Test

```bash
python tests/docs_runtime_api_coverage_test.py
```

检查正式 Runtime 文件：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

全部都能映射到唯一 API Markdown 页面。

这样以后新增 `.py` 文件时，不会静默漏掉文档。

---

# 本地检查顺序

```bash
python tests/core_import_style_test.py
python tests/docs_reference_generator_test.py
python tests/docs_runtime_api_coverage_test.py
python scripts/generate_mkdocs_reference.py
python scripts/extend_docs_summary.py
mkdocs build --strict
```

本地预览：

```bash
mkdocs serve
```

---

# 代码书写规范

正式 Maya 代码继续保持项目现有风格：

- `maya.cmds`；
- 不新增 PyMEL；
- 有意义的逻辑使用显式 `for` 循环；
- 不用列表推导式压缩主要业务流程；
- 中文注释解释“步骤”和“为什么”；
- 函数职责尽量单一；
- `core` 不放 UI；
- `tools` 不重复实现底层算法；
- `systems` 不把完整业务塞回 Core。

---

# 提交规范

文档系统仍按职责拆 Commit。

推荐：

```text
feat: expand api reference generation
test: cover api reference generator
test: verify runtime api documentation coverage
feat: expand task manual navigation
docs: add controller user guide
docs: sync readme with documentation navigation
fix: correct generated api links
```

不要把：

```text
Rig 功能修改
文档生成器重构
用户手册重写
README 重写
```

全部混到一个提交。

---

# 修改一个公开 API 时

推荐完整步骤：

1. 修改实现；
2. 更新对应 Docstring；
3. 参数变更时更新 `Args`；
4. 返回结构变更时更新 `Returns`；
5. 增加或更新 Example；
6. 更新 Smoke Test；
7. 运行 Generator Test；
8. 运行 Runtime API Coverage Test；
9. 重新生成 Reference；
10. 扩展用户手册导航；
11. `mkdocs build --strict`；
12. 如果文档结构变化，同步 README；
13. 再提交。

文档不是代码完成后的附件，而是公开 API 本身的一部分。
