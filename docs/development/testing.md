# 测试

MuziTools 的正式测试重点是 **Maya 2023 真机场景验证**。

## Pipeline / Core Smoke Test

Maya Python Script Editor：

```python
import muziToolset

report = muziToolset.pipeline_smoke_test()
```

这组测试用于验证 Core 的关键底层能力，例如：

```text
Scene
Transform
Animation
Connection
Matrix
Constraint
Curve
Surface
```

测试过程中会创建临时 Maya 节点，完成计算验证后自动清理。

## Controller Component Test

```python
report = muziToolset.controller_component_smoke_test()
```

用于验证 Controller System，例如 Parent Space Blend。

## Face Component Test

```python
report = muziToolset.face_component_smoke_test()
```

用于验证 Face System 中已经正式化的组件。

## 文档测试

文档不需要 Maya：

```bash
python scripts/generate_mkdocs_reference.py
mkdocs build --strict
```

GitHub Actions 会在 Push / Pull Request 时执行同样的文档生成和构建检查。

## 重构 Core 时的推荐顺序

```text
读取现有调用
    ↓
保持 API 或准备兼容迁移
    ↓
修改 Core
    ↓
更新 Tool / System 调用
    ↓
更新 Smoke Test
    ↓
Maya 2023 真机验证
    ↓
更新 MkDocs 文档
```

不要在 Maya 真机测试之前删除仍可能被正式代码引用的旧 API。
