# MuziTools 文档

MuziTools 是面向 **Autodesk Maya 2023** 的绑定工具集。

当前正式 Python 包名是：

```python
import muziToolset
```

> `MuziTools` 用作文档站和项目显示名称；正式源码仍以 `muziToolset` 根包为唯一运行架构。

## 文档内容

这套 MkDocs 文档分为五部分：

- **快速开始**：安装、启动、Maya Script Editor 使用方式；
- **架构**：`core / tools / systems / ui / app` 的职责和依赖规则；
- **API 参考**：由源码 AST 自动生成的 Core、Tools、Systems 第一版 API 文档；
- **开发指南**：Core 编码规范、中文注释规范、测试与文档维护方式；
- **迁移记录**：旧 `pipelineUtils` 等历史架构如何迁入当前正式模块。

## 启动 MuziTools

```python
import muziToolset
muziToolset.show()
```

## API 文档自动生成

项目不使用需要 import Maya 模块的 API 生成方案，而是通过 Python AST 静态扫描源码：

```bash
python scripts/generate_mkdocs_reference.py
mkdocs serve
```

生成器会扫描：

```text
core/
tools/
systems/
```

并为现有模块生成第一版：

```text
功能
使用场景
API
示例
源码位置
```

这样 GitHub Actions 在没有 Maya 的 Linux Runner 上也可以正常构建文档。
