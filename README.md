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

也可以执行仓库中的：

```python
start.py
```

第一次使用建议先看：

- [安装与启动](docs/getting-started/installation.md)
- [在 Maya 中运行](docs/getting-started/maya-usage.md)

在线文档：

```text
https://muzimuzi.github.io/muziToolset/
```

---

# 文档导航

MuziTools 文档采用两层结构：

```text
用户手册
    回答“我要完成什么、应该怎么做”

API Reference
    回答“这个 Python 文件 / 类 / 方法怎么调用”
```

## 1. 用户手册

用户手册入口：

- [MuziTools 用户手册](docs/manual/index.md)
- [常用工具工作流](docs/manual/tools.md)
- [完整绑定工作流](docs/manual/rigging.md)

按任务进入：

| 我想做什么 | 文档 |
| --- | --- |
| 重命名、属性、连接、约束、吸附 | [基础工具](docs/manual/basic-tools.md) |
| 创建 / 修改 Controller | [Controller 工作流](docs/manual/controller.md) |
| 创建 / 重采样 Joint | [Joint 工作流](docs/manual/joint.md) |
| SkinCluster、Influence、权重 | [Skin 工作流](docs/manual/skin.md) |
| BlendShape、Corrective、Invert Shape | [BlendShape 工作流](docs/manual/blendshape.md) |
| 模型检查、层级清理、发布前检查 | [场景清理与模型检查](docs/manual/cleanup.md) |
| Face Setup、Guide、左右镜像 | [Face Guide](docs/manual/face-guide.md) |
| 整体角色绑定顺序 | [绑定工作流](docs/manual/rigging.md) |

推荐学习顺序：

```text
安装与启动
    ↓
基础工具
    ↓
Controller / Joint / Skin
    ↓
完整绑定工作流
    ↓
Face Rig
    ↓
架构
    ↓
API Reference
```

## 2. 架构

- [总体架构](docs/architecture/index.md)
- [Core 设计](docs/architecture/core.md)
- [Tools 与 Systems](docs/architecture/tools-systems.md)

如果你准备增加新功能，先确认它应该属于：

```text
core
    Maya 通用底层能力

tools
    用户直接打开的小工具 / UI

systems
    可复用完整 Rig Component / Workflow

ui
    通用 PySide UI 能力

app
    主程序和应用级窗口管理
```

## 3. API Reference

API 总览：

- [API Reference 说明](docs/reference/index.md)

API 页面由：

```text
scripts/generate_mkdocs_reference.py
```

使用 Python AST 自动扫描正式 Runtime 源码生成，并由生成后整理脚本统一控制阅读结构。

正式覆盖范围：

```text
__init__.py
config.py
app/**/*.py
core/**/*.py
systems/**/*.py
tools/**/*.py
ui/**/*.py
```

也就是说，**每一个正式 Python 文件都会拥有独立 API 页面**。

每个模块页面首先只显示简短概览：

```text
用途
模块定位
常用任务
Import
API 一览
```

每个公开 Function / Method 则固定按照下面的顺序展示：

```text
方法名
作用
适用场景（需要时）
Signature
参数
    类型
    必填
    默认值
    说明
返回值
异常
示例
Notes
源码位置
```

其中“作用”直接来自源码 Docstring 的功能摘要；参数的 Maya / Rigging 术语、类型和说明也以源码 Docstring 为第一事实来源。

### 源码与 API 文档路径映射

源码目录与网站 API 目录保持一致：

```text
core/attr_utils.py
    → docs/reference/core/attr_utils.md
    → /reference/core/attr_utils/

systems/face/face_guide.py
    → docs/reference/systems/face/face_guide.md
    → /reference/systems/face/face_guide/

tools/controller/create_ctrl_tool.py
    → docs/reference/tools/controller/create_ctrl_tool.md
    → /reference/tools/controller/create_ctrl_tool/

ui/theme.py
    → docs/reference/ui/theme.md
    → /reference/ui/theme/

app/main.py
    → docs/reference/app/main.md
    → /reference/app/main/

__init__.py
    → docs/reference/package.md

config.py
    → docs/reference/config.md
```

生成页面不需要手工复制函数说明；源码 Docstring 是 API 文档第一事实来源。

## 4. 开发指南

- [文档维护与 Docstring 规范](docs/development/documentation.md)
- [Core 编码规范](docs/development/core-style-guide.md)
- [测试](docs/development/testing.md)

## 5. 迁移记录

- [Pipeline 重构](docs/migration/pipeline.md)

---

# 文档目录与网站导航

当前手写文档目录：

```text
docs/
├── index.md
│
├── getting-started/
│   ├── installation.md
│   └── maya-usage.md
│
├── manual/
│   ├── index.md
│   ├── tools.md
│   ├── basic-tools.md
│   ├── controller.md
│   ├── joint.md
│   ├── skin.md
│   ├── blendshape.md
│   ├── cleanup.md
│   ├── rigging.md
│   └── face-guide.md
│
├── architecture/
│   ├── index.md
│   ├── core.md
│   └── tools-systems.md
│
├── reference/
│   └── index.md
│       └── 其余 API 页面由 AST Generator 自动生成
│
├── development/
│   ├── documentation.md
│   ├── core-style-guide.md
│   └── testing.md
│
├── migration/
│   └── pipeline.md
│
├── stylesheets/
│   └── manual.css
│
└── SUMMARY.md
    └── 由 API Generator 自动生成完整网站导航
```

README、`docs/` 目录和网站导航使用同一套分类，避免出现三套不同的文档结构。
