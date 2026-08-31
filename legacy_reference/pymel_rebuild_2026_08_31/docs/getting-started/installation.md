# 安装与启动

## Maya 版本

当前主要目标环境：

- Autodesk Maya 2023
- Python 3
- PySide2
- Windows

正式 Core 新代码不新增 PyMel 依赖。

## 安装目录

将仓库放入 Maya 可以访问的 Python 路径，例如：

```text
Documents/
└─ maya/
   └─ scripts/
      └─ muziToolset/
```

确保 `muziToolset` 目录本身包含：

```text
__init__.py
app/
core/
tools/
systems/
resources/
```

## 启动

Maya Python Script Editor：

```python
import muziToolset
muziToolset.show()
```

如果刚刚更新了大量 Python 文件，建议完整重启 Maya 后再验证，避免旧模块仍保留在 `sys.modules` 中。

## 更新代码

Git 仓库环境：

```bash
git pull origin main
```

## 文档环境

文档构建不需要 Maya。

```bash
python -m pip install -r requirements-docs.txt
python scripts/generate_mkdocs_reference.py
mkdocs serve
```
