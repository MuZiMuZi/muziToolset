# 场景清理与模型检查

MuziTools 当前 Cleanup 区包含两个主要 UI：

```text
tools/clean/model_checker.py
tools/clean/hierarchy_cleaner.py
```

它们分别负责“**只读检查 / 安全修复**”和“**明确配置后的场景清理**”。

<div class="grid cards" markdown>

-   :material-cube-scan:{ .lg .middle } **Model Checker**

    ---

    检查非流形、Lamina、DAG 重名、历史、Transform 和锁定法线。

    [:octicons-code-24: Model Checker API](../reference/tools/clean/model_checker.md)

-   :material-file-tree-outline:{ .lg .middle } **Hierarchy Cleaner**

    ---

    删除空组、清理安全范围 History、冻结安全 Transform、处理 Unknown 等。

    [:octicons-code-24: Hierarchy Cleaner API](../reference/tools/clean/hierarchy_cleaner.md)

</div>

## 推荐使用时机

```text
模型进入 Rig 前
    ↓
Model Checker
    ↓
修复明确问题
    ↓
开始 Rig
    ↓
制作过程中谨慎 Cleanup
    ↓
发布前再次 Model Checker
```

“检查”和“删除”不要混成一步。

推荐：

```text
先知道问题是什么
    ↓
再决定要不要修
```

而不是：

```text
看到 Outliner 很多东西
    ↓
全部删掉
```

## Model Checker

入口：

```python
from muziToolset.tools.clean import model_checker

window = model_checker.main()
```

当前 UI 设计可检查：

```text
Non-Manifold
Lamina Face
DAG Duplicate Name
Construction History
Mesh Transform 未冻结
Locked Normals
```

还支持：

```text
Selected Only
Select Issue Nodes
Fix Selected Issues
```

### 为什么拓扑问题默认只报告

像：

```text
Non-Manifold
Lamina
```

并不存在一个对所有模型都安全的“自动修复答案”。

自动删除 Face、合并 Vertex 或重建 Edge 可能直接改变角色拓扑。

因此合理原则是：

```text
高风险拓扑问题
    -> 检查 / 定位
    -> 人工判断
```

## Hierarchy Cleaner

入口：

```python
from muziToolset.tools.clean import hierarchy_cleaner

window = hierarchy_cleaner.main()
```

当前 UI 选项包括：

```text
删除空组
删除安全范围 Construction History
冻结安全范围 Transform
解锁并显示标准 Transform 属性
Geometry Pivot 居中
删除 Unknown 节点
仅处理当前选择
```

默认策略比较保守：

```text
Selected Only = True
Delete Empty = True
Delete Unknown = True
高风险项默认关闭
```

## 全场景模式

如果关闭 `仅处理当前选择`，工具会进入全场景模式。

当前 UI 会再次弹出确认，因为：

```text
全场景 Cleanup
```

风险远高于：

```text
Selected Cleanup
```

即使工具实现了安全过滤，也建议先保存 Maya Scene。

## History 清理

绑定前模型的建模 History 和绑定完成后的 Deformer History 不能用同一规则处理。

### 建模阶段

可能需要清：

```text
polyExtrude
polyBevel
polyMerge
建模临时节点
```

### 绑定阶段

可能必须保留：

```text
skinCluster
blendShape
wire
lattice
cluster
constraint related history
```

因此 Cleanup 不应该简单执行：

```python
cmds.delete(ch=True)
```

作用于整个角色层级。

## Freeze Transform

Freeze 也不是永远安全。

模型在 Rig 前可能适合 Freeze；已经作为 Rig Node 的 Transform 则可能不能 Freeze。

特别需要避免对这些节点做盲目 Freeze：

```text
Controller
Joint
Driven Group
Constraint Target
Deformer Handle
已经有动画的 Transform
```

## Empty Group

“没有 Shape”不等于“空组”。

一个 Rig Group 即使没有 Shape，也可能是：

```text
Zero Group
Driven Group
Space Group
Connect Group
Offset Group
Module Root
Joint Root
Controller Root
```

因此真正的 Empty Group 判断必须考虑：

```text
Children
Connections
Attributes
Rig Ownership
```

不能只判断 `listRelatives(shapes=True)` 为空。

## Unknown Node

Unknown Node 通常来自：

- 缺失 Plugin；
- 旧版本 Maya；
- 第三方节点；
- 文件转换。

删除前应该确认它真的不是 Rig 必需节点。

当前 Cleanup UI 把 Unknown 作为明确选项，而不是后台静默删除，这是正确的交互方向。

## Rig Library 场景尤其要保护什么

Rig Library 会创建和维护：

```text
network_md_rig_library_config_001
grp_md_rig_library_001
grp_md_rig_jnt_001
grp_md_rig_ctrl_001
Module Groups
Ownership Attributes
Constraints
Pose Driver / Driven
```

Cleanup 不能因为这些节点“不是 Mesh”就视为垃圾。

特别是 Network Config 和 Ownership Attribute 是安全 Rebuild 的依据。

## 当前迁移状态

`model_checker.py` 当前源码引用：

```python
from ...core import model_check_utils
```

`hierarchy_cleaner.py` 当前源码引用：

```python
from ...core import scene_utils
```

而当前正式 Core 已收敛为：

```text
core/common/
core/rigging/
```

因此两个 Cleanup UI 的功能设计已经比较明确，但底层 Core 仍需要迁移 / 重新接入。

!!! warning "文档不会伪装成已完成"
    网站会继续展示这些 Tool 的源码 API，但不会把当前不存在的 `core.model_check_utils`、`core.scene_utils` 写成正式 Core。后续应把实际算法迁移到明确的新 Core 模块，再修正 Tool import。

## 发布前检查清单

建议至少确认：

```text
Model
    非流形
    Lamina
    Topology
    Transform
    History
    Normals

Rig
    Naming
    Hierarchy
    Controller Zero Values
    Joint Axis
    Constraint / Driver
    Ownership
    Build State
    Connection State

Scene
    Unknown Node
    Unused Temporary Nodes
    Reference
    Namespace
    Animation / Rig Set
```

## 常见问题

### 删除 History 后 Rig 坏了

说明清理作用到了正式 Deformer History。

Rig 完成后不要用建模阶段的 History 清理规则。

### 删除空组后 Controller 坏了

可能删除了 Zero / Driven / Space / Connect / Offset 等没有 Shape 的正式 Rig Group。

### 全场景 Freeze 后 Joint / Controller 出问题

Freeze 必须有节点类型和 Rig 状态过滤。

### Model Checker 报拓扑问题但不自动修

这是预期设计。拓扑自动修复风险高，先定位再人工决定。

## 相关 API

- [model_checker.py](../reference/tools/clean/model_checker.md)
- [hierarchy_cleaner.py](../reference/tools/clean/hierarchy_cleaner.md)
- [Rig Library](rig-library.md)
- [总体架构](../architecture/index.md)

[返回常用工具](tools.md){ .md-button }
[打开 Model Checker API](../reference/tools/clean/model_checker.md){ .md-button .md-button--primary }
