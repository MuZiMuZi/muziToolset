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
docs/manual/
docs/getting-started/
docs/architecture/
docs/development/
docs/migration/
```

用户手册是人工维护内容。

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
```

以及左侧导航：

```text
docs/SUMMARY.md
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
- Notes。

---

# Docstring 是 API 文档的第一事实来源

不要在 Markdown 里手工复制一份函数签名和参数说明。

应该先把源码 Docstring 写完整，再让生成器同步到网站。

推荐使用下面的格式。

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

生成后的页面会自动拆成：

```text
Signature
参数
返回值
异常
示例
Notes
```

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
    - 不创建最终 Joint；
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

推荐：

```python
Args:
    side (str):
        方向，只允许 "lf" 或 "rt"。

    required (bool):
        Guide 缺失时是否直接抛出异常。
```

不要只写：

```python
Args:
    side: side
```

参数说明应该回答：

- 这个值是什么；
- 有哪些合法值；
- 单位是什么；
- `None` 代表什么；
- 会不会修改 Maya Scene。

## Returns

不要只写类型。

推荐：

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

## Raises

只记录调用者需要知道的公开异常：

```python
Raises:
    ValueError:
        side 不是 lf / rt 时抛出。

    RuntimeError:
        必须的 Guide 节点缺失时抛出。
```

## Example

示例应该尽量是可复制的真实调用。

```python
Example:
    >>> guide = FaceGuide()
    >>> left_lid = guide.get_eyelid_guides(
    ...     side="lf"
    ... )
```

如果源码暂时没有 Example，生成器会根据 Signature 生成一个安全骨架，但正式公开 API 仍建议补真实示例。

## Notes

用于解释容易误用的约束：

```python
Notes:
    返回顺序已经固定，Builder 不应该再次自行排序。
```

---

# 代码书写规范

正式 Maya 代码继续保持当前项目风格：

- `maya.cmds`；
- 不引入 PyMEL；
- 有意义的逻辑使用显式 `for` 循环；
- 不用列表推导式压缩主要业务流程；
- 中文注释解释“为什么”；
- 函数职责尽量单一；
- `core` 不放 UI；
- `tools` 不重复实现底层算法；
- `systems` 不把完整业务塞回 Core。

---

# 为什么继续使用 AST

GitHub Actions 没有 Maya。

如果 API 生成器直接：

```python
import maya.cmds
```

在线文档就无法构建。

当前方案只执行：

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

# 左侧导航

生成器会根据真实源码目录生成：

```text
docs/SUMMARY.md
```

MkDocs 通过 `mkdocs-literate-nav` 读取这份文件。

最终导航会类似：

```text
API 参考
├── Core
│   ├── attr_utils.py
│   ├── curve_utils.py
│   └── ...
├── Tools
│   ├── Basic
│   ├── Controller
│   └── ...
└── Systems
    └── Face
        ├── face_base.py
        ├── face_setup.py
        ├── face_guide.py
        ├── Eyelid
        └── Lip
```

新增正式 Python 文件后，不需要手工维护 `mkdocs.yml` 的几十行导航。

---

# 本地检查顺序

```bash
python tests/core_import_style_test.py
python tests/docs_reference_generator_test.py
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

预览：

```bash
mkdocs serve
```

---

# 提交规范

文档系统修改仍按职责拆 Commit。

推荐：

```text
feat: expand api reference generation
test: cover api reference generator
feat: add generated documentation navigation
docs: reorganize user manual
docs: define api documentation standard
fix: correct generated api links
```

不要把：

```text
Rig 功能修改
文档生成器重构
大量说明页修改
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
7. 运行 API Generator Test；
8. 重新生成 Reference；
9. `mkdocs build --strict`；
10. 再提交。

文档不是代码完成后的附件，而是公开 API 本身的一部分。
