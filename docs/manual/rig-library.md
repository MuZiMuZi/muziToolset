# Rig Library 使用手册

Rig Library 是 MuziTools 当前模块化绑定的主要工作界面。

界面区域和实际截图见 [界面图解](visual-guide.md)。

它不是一个“一键自动绑定”按钮，而是把 Rig 构建拆成四个明确阶段，让你可以在最终连接之前反复调整 Guide、Controller 和 Joint。

当前流程：

```text
01 Setup
    ↓
02 Guide
    ↓
03 Ctrl
    ↓
04 Final
```

---

# 打开 Rig Library

从 MuziTools 主工具箱进入 Rig Library / Modular Rig。

窗口标题：

```text
Muzi · 绑定库 / Rig Library
```

主界面分成三栏：

```text
左侧
    Module Library / Templates

中间
    Rig Structure

右侧
    当前 Module Properties
```

底部：

```text
Validate
下一步
```

---

# 01 Setup — 配置与层级

第一步先决定当前角色要使用哪些模块。

当前正式 Builder 包括：

```text
Ear
Eye
Tongue
FK Chain
```

你可以：

```text
从 Modules 添加单个模块
或者
从 Templates 添加模块组合
```

左右模块会自动尝试分配空闲侧。

例如第一次添加 Eye：

```text
lf / eye
```

再次添加同类 Eye 时会尝试：

```text
rt / eye
```

---

## Setup 阶段可以调整

```text
是否参与构建
模块名称（部分模块）
Side
```

已 Build 的 Module 不允许继续随意修改结构型参数。

---

## 点击“下一步”以后

Rig Library 会准备：

```text
grp_md_rig_library_001
├── grp_md_rig_jnt_001
└── grp_md_rig_ctrl_001
```

并保存 Rig Library 配置。

如果场景里已经有同名节点但不属于当前 Rig Library，系统会停止而不是覆盖。

---

# 02 Guide — 导入与定位

Step 02 用来准备并调整模块定位。

当前支持两种 Guide 来源：

```text
标准 Face Guide Template
手动指定 Guide List
```

对于 Face 模块，第一次进入时可以自动导入仓库里的 Face Guide Template。

---

## 手动指定 Guide

如果 Module 允许自定义 Guide：

1. 在 Maya 中按正确顺序选择 Guide；
2. 点击“读取 Maya 选择”；
3. 检查文本区顺序；
4. 点击“保存 Guide 列表”。

顺序非常重要。

对于链式模块，文本区中的每一行就是最终 Builder 使用的 Guide 顺序。

---

## Guide 检查规则

每个 Guide 必须：

```text
存在
名称能唯一解析
不是重复节点
Node Type 为 transform / joint
```

不符合条件时，Build 会停止并给出错误，而不是猜测正确对象。

---

# Guide 阶段的“下一步”很重要

当前流程中，Joint / Controller 的实际生成发生在 Guide 确认之后。

## 第一次 Build

如果 Guide 已经有效，并且 Module 尚未 Build：

```text
点击“下一步”
    ↓
生成 Joint
    ↓
生成 Controller
    ↓
创建 Module Hierarchy
    ↓
进入 Step 03
```

此时**还没有建立最终 Driver Connection**。

---

## 修改 Guide 后 Rebuild

如果 Module 已经生成过：

1. 从 Step 03 / 04 回到 Guide；
2. 修改 Guide；
3. 再次点击“下一步”。

当前 Module 会按最新 Guide Rebuild。

Rebuild 后：

```text
built = True
connected = False
```

所以之后需要重新 Final。

---

# Mirror

Mirror 可以在前三步使用：

```text
Setup
Guide
Ctrl
```

Final 阶段会要求先返回前面步骤。

操作方式：

1. 在 Rig Structure 里选中模块；
2. 右键；
3. 选择镜像到另一侧。

Guide Position 沿：

```text
World X = 0
```

进行左右镜像。

如果目标侧已经 Build，系统会自动按镜像后的 Guide 重建目标模块，并把连接状态退回未连接。

---

# 03 Ctrl — 创建与调整

Step 03 的名字是 `Ctrl`，但当前职责不仅是 Controller。

这一阶段同时显示：

```text
Controller 设置
Joint 设置
```

因为 Joint / Controller 已经在 Step 02 末尾生成完成。

---

## Controller 设置

可以调整：

```text
Axis
Size
Color
Show Controls
```

对于已经 Build 的模块，这些外观调整会立即应用到场景。

### Size

修改 Controller Curve CV 的显示大小，不需要把 Transform Scale 当成最终视觉大小。

### Color

修改 Controller Shape 显示颜色。

### Axis

修改 Controller Shape 的朝向。

Eye Aim Controller 有自己的固定 Aim Axis 逻辑，因此不是所有 Eye Controller 都跟随同一 Axis 设置。

---

## Joint 设置

可以调整：

```text
Joint Radius
Show Local Axis
Show Joints
```

Joint Radius 直接用于当前 Module 的 Joint Display。

---

# 为什么 Step 03 不重新 Build

Step 03 只负责调整已经存在的输出。

如果需要改变：

```text
Guide
Side
Module Structure
```

应该回退到前面阶段，通过正式 Rebuild 处理。

这样 Scene 与配置不会因为随意修改结构参数而失去同步。

---

# 04 Final — 检查与完成

Final 才建立最终驱动连接。

点击“下一步”时：

```text
每个 Enabled + Built + 未连接 Module
    ↓
connect_outputs()
    ↓
connected = True
```

完成后会选择当前 Rig 的主 Controller。

---

# 为什么 Connection 放最后

这使你在前面阶段可以安全完成：

```text
Guide 调整
Mirror
Controller Size
Controller Color
Controller Axis
Joint Radius
Joint Axis Display
Module Rebuild
```

而不会被已经建立的 Constraint / Driver Network 干扰。

---

# 顶部步骤不能向前跳

这是当前 UI 的正式规则。

假如你在 Step 02：

```text
可以点击 Step 01
不能直接点击 Step 03 / Step 04
```

顶部按钮只负责**回退**。

向前只能点击底部：

```text
下一步
```

这样每一个阶段都会先实际完成 Scene 操作，再解锁后续阶段。

---

# Validate

底部 `检查 / Validate` 是只读预检查。

它会检查：

```text
是否至少有一个启用模块
Guide 是否有效
输出名称是否冲突
已 Build 模块输出是否完整
Root Ownership 是否正确
```

建议在 Build / Final 前遇到异常时先点 Validate。

---

# Eye Module 当前行为

Eye 是当前 Rig Library 中最完整的 Face Module 示例。

标准 Guide：

```text
loc_lf_eye_ball_001
loc_lf_eye_iris_001
loc_lf_eye_aim_001
```

右侧对应 `rt`。

其中：

```text
Ball
    真实眼球旋转中心

Iris
    Main Controller 可见位置

Aim
    Aim Controller 位置
```

最终主要结构：

```text
Aim Ctrl
    ↓
Main Driven
    ↓
Main Ctrl
    ↓
Main Output
    ↓
Pose Driver
    ↓
Pose Driven
    ↓
Eye Joint
```

Main Controller 保持在 Iris，可见旋转轴心位于 Ball。

---

# 配置保存在哪里

当前 Rig Library 配置保存在 Maya Network：

```text
network_md_rig_library_config_001
```

JSON 属性：

```text
muziRigLibraryJson
```

窗口重新打开时会读取已有配置，但不会因为“打开窗口”就自动创建 Scene 节点。

---

# 导入 / 导出配置

顶部支持：

```text
导入配置
导出配置
```

导出的是 **Recipe / 参数配置**，不是 Maya Scene Rig Backup。

导出时：

```text
built = False
connected = False
```

因此导出的 JSON 可以用于重新创建 Module 配置，但不包含当前场景里已经生成的 Joint / Controller / Constraint 数据。

---

# Undo

Rig Library 的重要 Scene 操作会放进 Maya Undo Chunk。

如果 Maya Undo 被关闭，Service 会拒绝执行需要修改场景的操作。

这可以避免 Build 失败时只回滚一半。

---

# 常见问题

## 为什么下一步是灰的？

检查：

```text
有没有 Module
当前 Step 是否已经解锁
Root / Guide / Build 状态是否完整
```

先点击 Validate 查看具体错误。

## 为什么 Step 03 里不能改 Guide？

因为 Guide 是结构型输入。请回到 Step 02 修改，然后 Rebuild。

## 为什么 Final 后不能 Mirror？

Mirror 会改变 Guide / Module Output。请先回到前三步处理镜像，然后重新 Final。

## 为什么 Build 后 Side 不能改？

Side 会影响命名和输出结构，不能只改 JSON。需要在 Build 前确定，或通过正式镜像 / 重建流程处理。

## 为什么 JSON 导出后没有绑定节点？

因为它是 Recipe，不是 Maya Scene Backup。

---

# 相关文档

- [Face System Architecture](../architecture/face-system.md)
- [Workflow State](../architecture/face-workflow-state.md)
- [Rig Library API](../reference/systems/rig/package.md)
- [Face API](../reference/systems/face/package.md)
