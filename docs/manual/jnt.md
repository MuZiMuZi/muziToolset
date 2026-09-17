# Jnt

MuziTools 当前正式 Joint 基础能力集中在：

```text
core/rigging/jnt_utils.py
```

Rig Module 不应该重复实现单个 Joint 的创建、匹配和显示半径逻辑，而是通过 `Jnt` 或 `RigModule.create_joint()` 复用这一层。

<div class="grid cards" markdown>

-   :material-bone:{ .lg .middle } **单 Joint 基础能力**

    ---

    创建或读取 Joint、匹配 Guide、设置 Radius、清理 Joint Orient。

    [:octicons-code-24: Jnt Utils API](../reference/core/rigging/jnt_utils.md)

-   :material-sitemap-outline:{ .lg .middle } **Rig Module Joint**

    ---

    由具体 Module 决定 Joint 数量、命名、Guide 对应关系和层级。

    [:octicons-code-24: RigModule API](../reference/systems/rig_module.md)

-   :material-tune-variant:{ .lg .middle } **Rig Library Step 03**

    ---

    构建后实时调整 Joint Radius、Local Axis 和可见性。

    [:octicons-code-24: Rig Library Service](../reference/systems/rig/library_service.md)

-   :material-tools:{ .lg .middle } **独立 Jnt Tool**

    ---

    提供创建、重采样、Orient、IK、Curve / Edge Chain 和 Skin 辅助入口。

    [:octicons-code-24: Jnt Tool API](../reference/tools/jnt/jnt_tool.md)

</div>

## 当前正式分层

```text
core/rigging/jnt_utils.py
    ↓
单 Joint 基础能力

systems/rig_module.py
    ↓
Module Joint 调度

systems/face/* / systems/components/*
    ↓
具体 Joint System

systems/rig/library_service.py
    ↓
绑定库阶段、重建、显示参数和安全检查
```

Core 只处理一个 Joint 的基础行为。

具体业务 Module 决定：

- Joint 数量；
- Guide 对应关系；
- 命名；
- 父子拓扑；
- Driver / Bind 用途；
- 与 Controller 的最终连接。

## `Jnt` 的基本使用

```python
from muziToolset.core.rigging import jnt_utils

jnt = jnt_utils.Jnt(
    "jnt_lf_eye_bind_001"
)
```

实例化时：

```text
同名 Joint 已存在
    ↓
直接复用

同名节点不存在
    ↓
创建新 Joint

同名对象存在但不是 Joint
    ↓
抛出 TypeError
```

这样 Module 在重复查询节点时不会无条件创建第二套 Joint。

## 匹配 Guide

```python
jnt.set_match_transform(
    "loc_lf_eye_ball_001"
)
```

当前实现通过 `core/common/transform_utils.py` 完成 Transform Match。

在 Module 中通常不直接手写：

```python
jnt = jnt_utils.Jnt(name)
jnt.set_match_transform(guide)
```

而是使用：

```python
self.create_joint(
    name="jnt_lf_eye_bind_001",
    guide="loc_lf_eye_ball_001"
)
```

这让具体 Module 只负责表达 Joint 的语义，而不是重复底层代码。

## 设置 Joint Radius

```python
jnt.set_radius(0.5)
```

`radius` 只影响 Maya Viewport 中 Joint 的显示大小，不改变骨骼长度、世界空间位置或 Skin 权重。

在 Rig Library Step 03 中，`jnt_radius` 就是通过这一能力应用到已经生成的 Joint。

## 清理 Joint Orient

```python
jnt.reset_joint_orient()
```

当前方法会把：

```text
jointOrientX
jointOrientY
jointOrientZ
```

统一归零。

!!! warning "不是通用 Orient 求解器"
    `reset_joint_orient()` 只是清零已有 `jointOrient`，并不会自动计算一条 Joint Chain 应该朝向哪里。真正的 Joint Orientation 仍然需要根据链条主轴、Up Axis、镜像规则和后续 Rig 需求设计。

## Module 中的 Joint 创建

`RigModule.create_joint()` 只负责**单个 Joint**。

例如 Eye：

```text
Ball Guide
    ↓
jnt_lf_eye_bind_001
```

Ear / Tongue / FK Chain 则可以创建多个 Joint。

因此：

```text
RigModule.create_joint()
```

不决定：

```text
Joint Count
Joint Chain Topology
Branch
Driver Joint
Bind Joint
```

这些都由具体 Module 的 `create_joints()` 决定。

## Build 生命周期中的 Joint

当前 Module 生命周期：

```text
get_guides()
    ↓
create_joints()
    ↓
create_ctrls()
    ↓
setup_hierarchy()
    ↓
connect_rig()
```

Rig Library 为了允许 Step 03 调整和 Step 04 延迟连接，会拆成：

```text
build_outputs()
    ├── Joint
    ├── Controller
    └── Hierarchy

connect_outputs()
    └── Connection
```

这意味着 Joint 在 Final 之前就已经存在，可以检查位置、Radius 和 Local Axis。

## Rig Library Step 03

当前 Step 03 同时显示 Controller 和 Joint 设置。

Joint 相关设置包括：

```text
Joint Radius
Show Local Axis
Show Joints
```

修改流程：

```text
UI
    ↓
RigLibraryService.update_module()
    ↓
_apply_display()
    ↓
Jnt(name).set_radius()
    ↓
displayLocalAxis / group visibility
```

这些操作只修改显示和 Joint Radius，不改变 Guide，也不重建驱动连接。

## Guide 改动后的 Joint Rebuild

如果 Joint 的位置本身需要改变，不应该在 Step 03 直接拖 Joint。

推荐：

```text
返回 Step 02
    ↓
修改 Guide
    ↓
Rebuild Module
    ↓
重新生成 Joint / Controller
    ↓
connected = False
    ↓
Step 03 检查
    ↓
Step 04 Final
```

这样 Guide 继续保持为构建位置的事实来源。

## Mirror 与 Joint

当前 Rig Library 的 Mirror 不是简单对 Joint 做负 Scale。

流程为：

```text
Source Guide Position
    ↓
World X = 0 镜像
    ↓
Target Guide Position
    ↓
目标已 Build？
    ├── 否：只更新 Guide
    └── 是：重建 Target Module
             ↓
             新 Joint 按镜像 Guide 生成
```

这样 Joint 的最终位置由目标侧 Guide 决定，而不是对已经生成的 Skeleton 强行做负缩放。

## Eye Joint 特殊规则

Eye Joint 的位置来自：

```text
loc_<side>_eye_ball_001
```

最终正式连接：

```text
Pose Driven
    ↓
Orient Constraint
    ↓
Eye Joint
```

Eye Joint 只接收 Orientation，不接收 Controller Translate。

这是为了保证眼球围绕真实 Ball Center 旋转，而不是被 Iris / Aim Controller 的位置带走。

## Joint Master Group

每个 Module 统一拥有自己的 Joint 根组：

```text
grp_<side>_<module>_jnt_001
```

Rig Library 再把这些 Module Joint Group 挂到：

```text
grp_md_rig_jnt_001
```

因此层级大致为：

```text
grp_md_rig_library_001
└── grp_md_rig_jnt_001
    ├── grp_lf_eye_jnt_001
    ├── grp_rt_eye_jnt_001
    ├── grp_lf_ear_jnt_001
    └── ...
```

## 独立 Jnt Tool

入口：

```python
from muziToolset.tools.jnt import jnt_tool

window = jnt_tool.main()
```

当前源码意图提供：

- Joint Radius；
- Local Rotation Axis 显示；
- Maya Orient Joint Options；
- Mirror Joint Options；
- IK Handle / IK Spline Options；
- 按选择创建 Joint；
- 创建 Child Joint；
- Joint Resample；
- 组成 Joint Chain；
- Curve CV → Joint Chain；
- Polygon Edge → Joint Chain；
- Segment Scale Compensate；
- Joint Orient 显示 / 清理；
- Joint Chain → Curve；
- 批量 Parent Constraint；
- 常用 Skin 入口。

!!! warning "当前迁移状态"
    `tools/jnt/jnt_tool.py` 仍引用一批旧的 Core 平铺入口，例如 `core.jnt_chain_utils`、`core.scene_utils`、`core.constraint_utils` 等，而当前正式 Core 已收敛为 `core/common/`、`core/rigging/` 与兼容区 `core/bake/`。因此这个独立 Tool 目前属于**待迁移 UI**，不应拿它的旧依赖关系定义当前 Core 架构。Rig Library / RigModule 的正式 Joint 主路径仍是 `core/rigging/jnt_utils.py`。

## 常见问题

### Joint 创建在错误父节点下

创建新 Joint 前必须注意 Maya 当前选择。

`Jnt._get_or_create_jnt()` 创建新 Joint 时会清空选择，避免新 Joint 自动成为当前选择 Joint 的子节点。

### Joint 位置改了，但重新 Build 又回去了

这是预期行为。

Module 的构建位置来自 Guide。应该修改 Guide，然后 Rebuild，而不是把生成结果当作新的构建源。

### 左右 Joint 不对称

优先检查：

```text
左右 Guide 是否对称
Guide Naming 是否正确
Mirror 是否真的作用于 Target Guide
Target Module 是否重新 Build
```

不要只修改 Joint Translate。

### Joint Radius 不一致

使用 Step 03 的 `jnt_radius` 或 `Jnt.set_radius()` 统一处理。

## 相关 API

- [jnt_utils.py](../reference/core/rigging/jnt_utils.md)
- [rig_module.py](../reference/systems/rig_module.md)
- [library_service.py](../reference/systems/rig/library_service.md)
- [jnt_tool.py](../reference/tools/jnt/jnt_tool.md)
- [jnt_resamp_tool.py](../reference/tools/jnt/jnt_resamp_tool.md)
- [transform_utils.py](../reference/core/common/transform_utils.md)
- [Rig Library](rig-library.md)

[返回常用工具](tools.md){ .md-button }
[打开 Jnt Utils API](../reference/core/rigging/jnt_utils.md){ .md-button .md-button--primary }
