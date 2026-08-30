# muziToolset

面向 **Autodesk Maya 2023** 的 Rigging Toolset 与可扩展绑定框架。

正式 Python Package：

```python
import muziToolset
```

项目显示名称使用 **MuziTools**；源码根包始终使用 `muziToolset`。

---

# 快速开始

把 `muziToolset` 放到 Maya Python 可以访问的位置后，在 Maya Python Script Editor 中运行：

```python
import muziToolset
window = muziToolset.show()
```

第一次使用：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)

在线文档：<https://muzimuzi.github.io/muziToolset/>

---

# 文档导航

文档分为两层：

```text
用户手册      → 我想完成什么、应该怎么做
API Reference → 某个 Python 文件 / 类 / 方法怎么调用
```

## 1. 用户手册

- [MuziTools 用户手册](docs/manual/index.md)
- [常用工具工作流](docs/manual/tools.md)
- [基础工具](docs/manual/basic-tools.md)
- [Controller](docs/manual/controller.md)
- [Joint](docs/manual/joint.md)
- [Skin](docs/manual/skin.md)
- [BlendShape](docs/manual/blendshape.md)
- [场景清理与模型检查](docs/manual/cleanup.md)
- [完整绑定工作流](docs/manual/rigging.md)
- [Face Guide](docs/manual/face-guide.md)

## 2. 架构

- [总体架构](docs/architecture/index.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)

源码职责：

```text
core     Maya 通用底层能力
tools    用户直接操作的工具 / UI
systems  可复用 Rig Component / Workflow
ui       通用 PySide UI
app      主程序和应用级窗口管理
```

## 3. API Reference

- [API Reference 说明](docs/reference/index.md)

AST Generator 会为正式 Runtime Python 文件自动生成独立 API 页面：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

模块页面统一展示：

```text
用途
模块定位
常用任务
Import
API 一览
```

每个公开 Function / Method 统一展示：

```text
方法名
作用
适用场景（需要时）
Signature
参数：类型 / 必填 / 默认值 / 说明
返回值
异常
示例
Notes
源码位置
```

源码与 API 页面路径保持一致，例如：

```text
core/attr_utils.py
→ docs/reference/core/attr_utils.md
→ /reference/core/attr_utils/

systems/face/face_guide.py
→ docs/reference/systems/face/face_guide.md
→ /reference/systems/face/face_guide/
```

源码 Docstring 是 API 文档的第一事实来源。

## 4. 开发指南

- [文档维护与 Docstring 规范](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)

## 5. 迁移记录

- [Pipeline 重构](docs/migration/pipeline.md)

---

# 文档目录

```text
docs/
├── getting-started/
├── manual/
├── architecture/
├── reference/
├── development/
├── migration/
├── stylesheets/
└── SUMMARY.md
```

README、`docs/` 目录和网站导航保持同一套分类。