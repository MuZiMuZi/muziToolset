# 文档维护

MuziTools 的文档目标不是“给代码旁边放一些说明”，而是让整个项目形成一套可以持续维护的 **Project Documentation System**。

文档分成三层：

```text
项目总览 / 用户手册
        ↓
架构与工作流文档
        ↓
自动生成 API Reference
```

三层职责必须分开，避免同一个技术事实被复制到多个 Markdown 后逐渐失真。

---

# 1. 项目总览与用户手册

用于回答：

- 这个项目整体是什么；
- 我想完成什么；
- 推荐操作顺序；
- 什么时候使用哪个 Tool / System；
- 常见错误和修复方式；
- 一个完整 Rig Workflow 怎么走。

主要目录：

```text
docs/index.md
docs/getting-started/
docs/manual/
```

这些页面是人工维护内容。

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

用户手册应该优先回答“怎么做”，而不是逐个解释源码函数。

---

# 2. 架构与开发文档

用于回答：

- 为什么项目要这样分层；
- `core / systems / tools / ui / app` 的边界是什么；
- Rig Module Lifecycle 是什么；
- Face Rig 的阶段如何连接；
- 一个新模块应该放在哪里；
- 测试和文档的维护规则是什么。

主要目录：

```text
docs/architecture/
docs/development/
docs/migration/
```

架构文档描述的是**设计契约**，不是逐行源码说明。

如果某个实现已经退出正式架构，应更新对应架构文档或迁移记录，不要让网站继续把退休实现描述成当前推荐方案。

---

# 3. API Reference

完整 API Reference 由：

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
scripts/refine_generated_reference.py
scripts/refine_generated_callable_layout.py
scripts/extend_docs_summary.py
```

继续统一页面布局、Callable Section 和人工任务页导航。

职责保持为：

```text
Runtime Source Docstring
    技术事实第一来源

API Generator
    根据源码生成动态 API 页面

Reference Refiners
    统一页面展示和可读性

Navigation Extender
    把人工用户手册补回导航

MkDocs
    构建完整网站
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

**不要在 Markdown 里手工复制一份函数签名和参数说明。**

应该先把源码 Docstring 写完整，再让 Generator 同步到网站。

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
        ...     "loc_lf_eye_ball_001"
        ... )

    Notes:
        返回 World Space Position，不是 Local Translate。
    """
```

生成后的 API 页面会自动拆成：

```text
功能摘要
适用场景
Signature
参数
返回值
异常
示例
Notes
```

如果源码暂时没有完整 Docstring，Generator 可以保留 API 骨架和安全的自动说明，但**正式公开 API 最终仍应该补齐源码语义**。

---

# Module Docstring 规范

每个正式 `.py` 文件应该尽量说明：

```text
模块名称
模块解决什么问题
主要职责
设计边界
输入数据
输出数据
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

模块 Docstring 不应该只重复文件名，例如：

```python
u"""Eye Module。"""
```

这种说明无法帮助后续维护者理解模块职责。

---

# Class Docstring 规范

正式公开 Class 至少需要说明：

```text
类负责什么
它处于哪个 Workflow 阶段
主要输入是什么
主要输出是什么
是否修改 Maya Scene
是否支持重复 Build / Rebuild
```

Rig Module 推荐额外说明：

```text
Guide Contract
Naming Contract
Hierarchy Contract
Connection Contract
Rebuild Contract
```

这样网站中的 Class 页面不仅能查方法，还可以直接理解整个模块如何工作。

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
- 会不会修改 Maya Scene；
- 这个参数会影响哪个 Build 阶段。

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

不要只写类型，尽量说明返回结构和返回对象后续用于什么。

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
ctrl_utils.py 有哪些函数？
```

逐函数说明应该交给 API Reference。

---

# 网站首页维护规则

`docs/index.md` 是整个项目的入口，不应该变成 changelog。

首页只保留长期有价值的内容：

```text
项目定位
项目分层
源码结构
主要 Workflow
API 覆盖范围
常用入口
搜索方式
文档同步机制
```

新增一个大系统时，例如 Brow / Lip / Eyelid Rig，应在系统稳定后补充对应入口；普通函数增加不需要修改首页。

---

# 可以清理什么

以下内容可以安全清理或重新生成：

1. 带有 Generator Marker 的过期 `docs/reference/**/*.md`；
2. 已经由新架构替代、且不再承担迁移价值的重复说明；
3. 与源码明显冲突的旧示例；
4. 已经失效的临时审计输出；
5. 空目录和自动生成后的无效占位页面。

自动生成页面由：

```text
<!-- AUTO-GENERATED BY scripts/generate_mkdocs_reference.py -->
```

标记识别。

Generator 在重新生成前会清理旧自动页面，再按当前源码重建。

---

# 不应该直接删除什么

没有确认运行时依赖以前，不要因为“看起来旧”就直接删除：

```text
core/bake/
legacy compatibility code
resources/
迁移记录
仍被 import 的 helper
仍被测试保护的旧入口
```

文档清理和 Runtime 重构必须分开提交。

---

# 小步骤提交规则

文档维护也采用小提交：

```text
1 个主题
    ↓
1 组相关文件
    ↓
1 次检查
    ↓
1 个 Commit
```

推荐提交示例：

```text
docs: expand documentation website overview
docs: improve API reference overview
docs(face): document eye rig API
docs(rig): document rig library API
docs: remove stale generated reference pages
```

不要把大规模 Runtime 重构、文档清理和网站视觉改版塞进同一个 Commit。

---

# 本地完整检查

```bash
python tests/core_import_style_test.py
python tests/jnt_naming_contract_test.py
python tests/rig_architecture_gate_test.py
python tests/rig_base_contract_test.py
python tests/module_base_contract_test.py
python tests/core_single_source_gate_test.py
python tests/core_public_api_gate_test.py
python tests/system_core_reuse_gate_test.py
python tests/maya2023_smoke_contract_test.py
python scripts/normalize_runtime_docstrings.py --check
python scripts/refine_runtime_docstring_semantics.py --check
python tests/docs_reference_generator_test.py
python tests/docs_runtime_api_coverage_test.py
python scripts/generate_mkdocs_reference.py
python scripts/refine_generated_reference.py
python scripts/refine_generated_callable_layout.py --check
python tests/docs_generated_layout_test.py
python scripts/extend_docs_summary.py
python tests/docs_readme_navigation_test.py
mkdocs build --strict
```

只要这些检查通过，GitHub Pages 使用的就是与当前源码一致的文档站点。

---

# 发布流程

`main` 分支发生 Push 后：

```text
GitHub Actions
    ↓
检查 Runtime / Rig Contract
    ↓
检查 Docstring
    ↓
生成完整 API Reference
    ↓
检查导航和页面布局
    ↓
mkdocs build --strict
    ↓
上传 GitHub Pages Artifact
    ↓
部署网站
```

最终网站地址由 `mkdocs.yml` 的 `site_url` 定义。
