# Face System Architecture

MuziTools 当前 Face Rig 不再采用“一个大脚本一次性创建全部面部绑定”的思路，而是拆成**独立 Module + Rig Library Workflow**。

当前目标：

```text
Guide 负责定位
Module 负责生成 Joint / Controller
Step 03 负责外观与 Joint 调整
Final 负责最终驱动连接
```

用户可以在 Final 前回退修改前面阶段，再重新生成对应模块。

---

# 当前 Face Runtime 结构

```text
systems/face/
├── __init__.py
├── face_guide_config.py
├── eye_module.py
├── ear_module.py
└── tongue_module.py
```

配套 Modular Rig 位于：

```text
systems/rig/
├── library_catalog.py
├── library_service.py
└── ui/
    ├── library_style.py
    ├── library_widgets.py
    └── modular_rig_ui.py
```

Face Tool 用户入口位于：

```text
tools/face/
tools/rig/
```

---

# 四步工作流

当前 UI 顶部四步为：

```text
01 Setup
02 Guide
03 Ctrl
04 Final
```

副标题分别是：

```text
Setup  -> 配置与层级
Guide  -> 导入与定位
Ctrl   -> 创建与调整
Final  -> 检查与完成
```

具体行为不是简单切换页面，而是与 Scene State 绑定。

---

## Step 01 — Setup

职责：

```text
添加模块 / 模板
保存模块配置
创建 Rig Library Root
创建 Joint Root
创建 Controller Root
```

当前根组：

```text
grp_md_rig_library_001
├── grp_md_rig_jnt_001
└── grp_md_rig_ctrl_001
```

这些根组带 Owner 标记，不会自动认领场景里碰巧同名但不属于绑定库的节点。

Step 01 完成条件：

```text
至少存在一个 Enabled Module
+ 三个根组存在
+ 根组归属当前 Rig Library
```

---

## Step 02 — Guide

职责：

```text
导入 Face Guide
读取 / 保存 Module Guide 列表
调整 Guide
左右镜像 Guide
根据最新 Guide 生成或重建 Joint / Controller
```

这是当前流程里非常关键的一步：

> **Joint / Controller 的实际生成发生在 Guide 阶段确认之后。**

第一次进入 Step 02，如果标准 Face Guide 还没有准备好，会通过：

```text
core/rigging/guide_utils.py
```

导入 Face Guide Template。

Guide 完成条件：

- 每个启用模块都有 Guide；
- Guide 名称可以唯一解析；
- 同一模块不会重复使用同一个 Guide；
- Guide 节点必须是 Transform 或 Joint。

当 Guide 已经有效时，点击底部“下一步”会：

```text
未 Build 模块
    -> 生成 Joint / Controller

已 Build 当前模块
    -> 删除当前模块正式输出
    -> 按最新 Guide Rebuild
    -> Connection 状态退回未连接
```

因此用户可以回到 Guide 修改位置，再重新生成模块。

---

## Step 03 — Ctrl

Step 03 当前不是“第一次创建 Controller”的阶段。

它的定位是：

> **Joint / Controller 已经生成后，对显示和外观进行实时调整。**

当前 UI 同时显示：

```text
Controller 设置
Joint 设置
```

Controller 可调：

```text
ctrl_size
ctrl_color
ctrl_axis
show_controls
```

Joint 可调：

```text
jnt_radius
show_axis
show_joints
```

这些修改由 `RigLibraryService.update_module()` 处理。

对于已经 Build 的 Module，只允许修改显示与 Controller 外观相关字段，不允许直接改：

```text
module name
side
guide list
enabled
```

这可以避免生成以后因为结构型参数被随意修改，导致 Scene 与配置失去一致性。

---

## Step 04 — Final

Final 才建立最终驱动连接。

当前 Service 行为：

```text
for each enabled + built + not connected module:
    builder.connect_outputs()
    record["connected"] = True
```

因此：

```text
Step 02/03
    主要得到 Joint / Controller / Hierarchy

Step 04
    才生成最终 Driver Connection
```

这样做的好处是，在最终连接前用户可以自由调整 Controller 大小、颜色、轴向、Joint 显示和 Guide 定位，不需要每次都拆完整驱动网络。

Final 完成后会选择主 Controller，方便继续动画或检查。

---

# 顶部导航规则

当前 UI 明确禁止通过顶部 Step Button 跳到未来步骤。

规则：

```text
顶部 Step Button
    只能回退

底部“下一步”
    唯一正式前进入口
```

例如当前在 Step 02：

```text
可以点击 Step 01
不能直接点击 Step 03 / 04
```

前进必须让当前阶段操作成功，避免 UI 状态与 Scene State 脱节。

---

# Mirror 规则

Mirror 在前三步都可以使用，但 Final 阶段禁止直接镜像。

当前逻辑：

```text
Step 01 / 02 / 03
    可以 Mirror

Step 04
    提示返回前三步后再镜像
```

Mirror 会复制左右模块设置，并把 Guide 世界位置沿：

```text
X = 0
```

镜像到另一侧。

如果目标模块已经 Build：

```text
镜像 Guide
    ↓
删除目标模块旧输出
    ↓
重新 Build Joint / Controller
    ↓
connected = False
```

也就是说，Mirror 不是单纯复制 UI 参数，而是正式 Workflow 能力。

---

# Module Lifecycle

一个 Face Module 推荐统一遵循：

```text
get_guides()
    ↓
create_joints()
    ↓
create_ctrls()
    ↓
setup_hierarchy()
    ↓
build_outputs()
    ↓
用户调整
    ↓
connect_outputs()
```

如果需要修改：

```text
Guide Change
    ↓
Rebuild Module Outputs
    ↓
connected = False
    ↓
Final Reconnect
```

这样所有模块都能接入同一个 Rig Library Service。

---

# Eye Module

当前 Eye 是最完整的 Face Module 示例。

Guide Contract：

```text
loc_<side>_eye_ball_001
loc_<side>_eye_iris_001
loc_<side>_eye_aim_001
```

语义：

```text
Ball
    真实眼球旋转中心
    Eye Joint 创建位置

Iris
    Eye Main Controller 可见位置

Aim
    Eye Aim Controller 位置
```

关键设计：

```text
Main Ctrl Transform 保持在 Iris
Main Ctrl Rotate Pivot 位于 Ball
Aim 只驱动旋转
Eye Joint 只接收旋转
Pose Driver / Pose Driven 作为后续 Eyelid / RBF / Corrective 接口
```

正式驱动链：

```text
ctrl_<side>_eye_aim_001
    ↓
output_<side>_eye_aim_001
    ↓
Aim Constraint
    ↓
driven_<side>_eye_main_001
    ↓
ctrl_<side>_eye_main_001
    ↓
output_<side>_eye_main_001
    ↓
driver_<side>_eye_pose_001
    ↓
driven_<side>_eye_pose_001
    ↓
Orient Constraint
    ↓
jnt_<side>_eye_bind_001
```

这套 Pose Driver / Driven 层是未来接入：

```text
Eyelid Follow
RBF Pose Reader
Corrective BlendShape
```

的重要扩展点。

API：[Eye Module](../reference/systems/face/eye_module.md)

---

# Ear / Tongue Module

当前正式 Module 还包括：

```text
EarModule
TongueModule
```

它们已经进入 Rig Library Builder Dispatch。

后续继续扩展时，应统一向 Eye Module 的 Lifecycle 靠拢：

```text
稳定 Guide Contract
稳定 Output Naming
Build Outputs
Connect Outputs
Safe Rebuild
Validate
```

而不是为每个部位写独立 UI Callback 构建流程。

---

# Guide Contract

Face Guide 的稳定命名与兼容逻辑集中在：

```text
systems/face/face_guide_config.py
```

Module 不应该把大量 Locator 字符串散落在各处。

推荐：

```text
Guide Config
    定义标准语义与名字
        ↓
Module
    按语义获取 Guide
        ↓
Builder
    创建输出
```

如果需要兼容旧 Guide 名称，应在 Guide Config 中集中处理 Normalize，而不是每个模块各写一份兼容表。

---

# Rig Library 与 Face Module 的关系

Rig Library 不负责具体算法。

它负责：

```text
Catalog
Config
Workflow State
Validation
Build Dispatch
Mirror
Rebuild
Finalize
Scene Ownership
```

真正的 Eye / Ear / Tongue 构建算法仍由 Module 自己负责。

调用关系：

```text
ModularRigWindow
    ↓
RigLibraryService
    ↓
_make_builder(record)
    ↓
EyeModule / EarModule / TongueModule / FKChain
    ↓
Core
```

---

# Scene Ownership

Rig Library 会给正式输出写入模块归属信息：

```text
muziRigLibraryModule
```

Root 使用：

```text
muziRigLibraryOwner
```

这使 Rebuild 可以做到：

```text
只删除属于当前 Module 的输出
不误删场景里其他同名或相邻节点
```

如果归属信息缺失或不一致，Service 会停止自动重建，而不是猜测节点归属。

---

# 当前支持的正式 Builder

`RigLibraryService._make_builder()` 当前调度：

```text
ear      -> EarModule
eye      -> EyeModule
tongue   -> TongueModule
fk_chain -> FKChain
```

Rig Library UI 只应该展示仓库中已经有正式构建入口的 Module。

---

# 后续 Face Module 推荐方向

眉毛、眼睑、嘴唇等后续模块建议继续遵循：

```text
1. 先定义 Guide Contract
2. 再实现 Joint / Controller Output
3. Build 和 Connect 分离
4. 支持 Safe Rebuild
5. 支持 Mirror
6. 用稳定 Driver Output 给 RBF / BlendShape / Corrective 使用
```

特别是 Eyelid / Brow / Lip，不建议只用 UI 脚本直接生成节点，而应做成正式 `systems/face/` Module。

---

# 对应文档

- [Face Workflow State](face-workflow-state.md)
- [总体架构](index.md)
- [Tools 与 Systems](tools-systems.md)
- [Face API](../reference/systems/face/package.md)
- [Rig Library API](../reference/systems/rig/package.md)
