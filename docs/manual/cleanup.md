# 场景清理与模型检查

这页说明 MuziTools 中模型检查、层级清理和场景安全整理的推荐方式。

## 什么时候看这页

- Rig 开始前检查模型；
- 发布前清理场景；
- 检查异常 Transform；
- 清理无效 History / Node；
- 整理 Outliner 层级；
- 排查模型或绑定层级里多余节点。

## 主要入口

UI Tool：

- [model_checker.py](../reference/tools/clean/model_checker.md)
- [hierarchy_cleaner.py](../reference/tools/clean/hierarchy_cleaner.md)

底层 API：

- [model_check_utils.py](../reference/core/model_check_utils.md)
- [scene_clean_utils.py](../reference/core/scene_clean_utils.md)
- [scene_utils.py](../reference/core/scene_utils.md)

## 推荐顺序

```text
模型导入
    ↓
Model Check
    ↓
修复模型问题
    ↓
整理命名
    ↓
Hierarchy Clean
    ↓
开始 Rig
```

发布前再执行一次：

```text
Rig 完成
    ↓
Scene Check
    ↓
删除临时节点
    ↓
确认 Display / Visibility / Sets
    ↓
保存发布版本
```

## Model Checker

打开：

```python
from muziToolset.tools.clean import model_checker

window = model_checker.main()
```

适合检查：

- Transform 是否异常；
- 模型命名；
- Shape / Transform 结构；
- 可能影响绑定的模型问题。

底层规则位于：

- [model_check_utils.py](../reference/core/model_check_utils.md)

如果新增一种“模型质量检查规则”，优先放到 Core；Tool 只负责展示结果和用户交互。

## Hierarchy Cleaner

打开：

```python
from muziToolset.tools.clean import hierarchy_cleaner

window = hierarchy_cleaner.main()
```

适合：

- 整理指定层级；
- 删除明显临时节点；
- 清理空 Group；
- 检查不符合规则的节点。

## 安全清理原则

场景清理不能简单理解成“能删的都删”。

正式工具应区分：

```text
安全删除
    明确无引用、无输出、无业务用途

需要确认
    可能被 Rig / Animation / Reference 使用

禁止自动删除
    无法证明安全的节点
```

特别是 Face Rig、Matrix Network、Message Config Node，很多节点在 Outliner 看起来“没用”，但实际上参与计算或配置。

## History

删除 History 前先判断模型处于哪个阶段：

```text
建模阶段
    通常可以清理大量 Construction History

Rig 阶段
    Skin / BlendShape / Wrap / Wire 等都是 History
    不能一键全删
```

不要在已经 Skin / BlendShape 的模型上使用普通 Delete History 作为“场景清理”。

## Namespace 与 Reference

如果场景使用 Reference：

- 不要随意 Rename Reference 内部节点；
- 不要把 Namespace 当作普通字符串直接删除；
- 清理前确认节点是否来自 Reference。

相关 API：

- [scene_utils.py](../reference/core/scene_utils.md)

## Outliner 层级

建议正式 Rig 保持明确顶层：

```text
model
rig
ctrl
joint
system / nodes
```

具体 Face Rig 会由 `FaceBase` 管理自己的正式层级，不应通过通用 Cleaner 随意重排。

## 常见问题

### Cleaner 把我想保留的节点删了

自动清理规则应该只删除“可以证明安全”的节点。若遇到误删，应把该节点类型加入保护规则，而不是要求用户每次手动恢复。

### 空 Group 为什么不能直接全删

有些空 Transform 是 Zero / Space / Offset / Output 层，本身没有 Shape，但具有重要的坐标空间意义。

### Model Check 报 Transform 非零，但这是故意的

检查结果应该区分 Error 和 Warning。角色建模、扫描数据或特定 Rig 输入可能允许非零 Transform。

## 继续查看

- [基础工具](basic-tools.md)
- [绑定工作流](rigging.md)
- [Scene Clean Utils API](../reference/core/scene_clean_utils.md)
