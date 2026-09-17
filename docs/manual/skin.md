# Skin

MuziTools 的 Skin 相关代码目前处于**新架构迁移中**。

当前仓库同时存在：

```text
tools/skin/skin_tool.py
    新 UI / 新交互设计
```

但当前正式 `core/common/`、`core/rigging/` 中还没有完成新的 Skin Core。因此网站会如实区分“当前 UI 意图”和“历史可用实现”，不会把旧 `weightsUtils.py` 写成新架构标准。

<div class="grid cards" markdown>

-   :material-human-handsup:{ .lg .middle } **Skin Tool UI**

    ---

    Smooth Bind、Detach、Paint、Mirror、Copy、Influence、Normalize、Import / Export。

    [:octicons-code-24: Skin Tool API](../reference/tools/skin/skin_tool.md)

-   :material-bone:{ .lg .middle } **Joint**

    ---

    Skin 前先确认 Skeleton / Joint 已稳定。

    [:octicons-arrow-right-24: Jnt 手册](jnt.md)

</div>

## 推荐 Skin 工作流

```text
Skeleton 稳定
    ↓
确认模型拓扑
    ↓
Smooth Bind
    ↓
检查 Influences
    ↓
Paint / Copy / Mirror
    ↓
Normalize
    ↓
保存权重
    ↓
Deformation Check
```

Skin 应该放在 Joint 结构稳定之后。

如果你还在频繁修改：

```text
Joint Count
Joint Naming
Joint Parent
Guide Position
Module Rebuild
```

先不要进入最终 Skin 阶段。

## 当前 Skin Tool 设计

入口：

```python
from muziToolset.tools.skin import skin_tool

window = skin_tool.main()
```

当前 UI 源码设计了这些功能：

```text
Maya Skin
    Smooth Bind
    Detach Skin
    Paint Skin Weights
    Mirror Skin Weights

Weight Tools
    Copy Weights
    Select Influences
    Normalize

Weight Files
    Export
    Import
```

### Copy Weight 选择规则

当前 UI 约定：

```text
第一个选择
    = Source

其余选择
    = Targets
```

概念上：

```text
Source SkinCluster
    ↓
Source Influences
    ↓
Targets
    ↓
Copy Skin Weights
```

## 当前迁移状态

`tools/skin/skin_tool.py` 当前仍引用：

```python
from ...core import skin_utils
from ...core import scene_utils
```

而当前正式 Core 已收敛为：

```text
core/common/
core/rigging/
```

因此这两个平铺 Core 入口并不是当前正式结构。

!!! warning "当前状态"
    Skin Tool 的 UI 和工作流设计可以作为新 Skin 模块目标，但底层 `core.skin_utils / core.scene_utils` 仍需要迁移或重新接入。当前网站不会把它描述成已经完成的新 Core Skin 实现。

## 历史 `Weights` 实现

旧兼容代码已经从正式 Runtime 与 API Reference 退休，不应继续作为新功能依赖：

```text
core/bake/weightsUtils.py
```

核心类：

```python
from muziToolset.core.bake import weightsUtils

weights = weightsUtils.Weights(
    "body_geo"
)
```

当前历史实现包括：

- `save_skinWeights()`；
- `load_skinWeights()`；
- `copy_weight()`；
- `get_skin_node()`；
- `get_skin_node_jnt()`；
- `rename_skin_node()`；
- 一些旧的自动权重 / Deformer 辅助逻辑。

这些名称只用于理解旧场景或迁移记录，不再出现在正式 API Reference 中：

```text
Compatibility / Historical Implementation
```

不是新功能默认扩展位置。

## 权重文件

历史 `Weights` 使用 Maya `deformerWeights` 导出 XML，同时保存 Influence 信息。

历史目录逻辑大致为：

```text
<maya file folder>/
└── <maya file name>_skin/
    ├── sc_<geo>.xml
    └── sc_<geo>.infs
```

新的 `SkinTool` UI 文案则使用：

```text
sc_<模型名>.xml
sc_<模型名>.infs.json
```

这两套命名目前并不完全一致，也是后续 Skin Core 收敛时需要统一的地方。

## 为什么权重文件要同时保存 Influence

只保存 Vertex Weight 数值不够。

导入时还必须知道：

```text
这些数值属于哪些 Joint
```

因此完整 Skin Data 通常至少包含：

```text
Geometry Identity
SkinCluster
Influence Names
Weights
Topology / Vertex Assumption
```

否则同一份 Weight 数据在不同 Skeleton 上没有稳定含义。

## Copy Skin Weight 注意事项

复制前检查：

```text
Source 有有效 SkinCluster
Target Mesh 可绑定
Influence Joint 存在
拓扑 / 空间关系满足复制策略
```

Maya `copySkinWeights` 常见 Association：

```text
Surface Association
Influence Association
```

不同角色、LOD 或拓扑复制时，不要默认认为同一种 Association 一定正确。

## Normalize

Normalize 负责保证一个 Vertex 上的 Influence Weight 满足期望总和。

典型目标：

```text
Σ influenceWeight = 1.0
```

但不同 SkinCluster 的 Normalize Mode 可能不同。

因此“强制归一化”是一个明确操作，不应该在所有 Skin 修改后无条件偷偷执行。

## Influence 管理

Influence 是 Skin 数据的一部分，不只是场景中“存在一些 Joint”。

如果新增 Joint 后没有加入 SkinCluster：

```text
Joint 存在
≠
Joint 是 Skin Influence
```

排查变形问题时先检查：

```text
findRelatedSkinCluster
    ↓
Influence List
    ↓
Weight
```

## Rig Library 与 Skin

当前 Rig Library 的职责主要到：

```text
Guide
Joint
Controller
Hierarchy
Connection
```

Skin 还没有并入四步 Rig Library 生命周期。

因此当前建议：

```text
Rig Library Final 完成
    ↓
Skeleton / Module 稳定
    ↓
再进入 Skin Workflow
```

未来如果 Skin 被纳入 Module Lifecycle，应单独设计：

```text
Skin Ownership
Rebuild Preservation
Weight Export / Restore
Influence Remap
Topology Contract
```

不能只在 `finalize()` 后面直接塞一个 `skinCluster()`。

## 常见问题

### 模型没有正确变形

排查顺序：

```text
是否有 SkinCluster
    ↓
Influence 是否正确
    ↓
Joint 是否在正确位置
    ↓
Weight 是否正常
    ↓
Joint / Rig Connection 是否正常
```

### 新 Joint 不起作用

确认它是否已经成为 SkinCluster Influence。

### 导入权重异常

检查：

```text
Geometry 名称
Vertex 数量 / 拓扑
Influence 名称
Weight 文件版本
SkinCluster 是否被重新创建
```

### 修改 Rig 后权重丢失

在 Rebuild Skeleton 或删除 SkinCluster 前先保存权重。

当前 Rig Library Rebuild 只针对 Module 输出，并没有自动负责 Skin Weight Preserve。

## 后续新 Skin Core 建议

新架构最终应该收敛成类似：

```text
core/skin/
或
core/rigging/skin_utils.py
```

并至少提供：

```text
find_skin_cluster
get_influences
copy_skin_weights
export_skin_weights
import_skin_weights
normalize
add_influence
remove_influence
```

到那时再把 `tools/skin/skin_tool.py` 从旧平铺依赖迁移过去。

## 相关 API

- [skin_tool.py](../reference/tools/skin/skin_tool.md)
- [jnt_utils.py](../reference/core/rigging/jnt_utils.md)
- [Rig Library](rig-library.md)

[返回常用工具](tools.md){ .md-button }
[打开 Skin Tool API](../reference/tools/skin/skin_tool.md){ .md-button .md-button--primary }
