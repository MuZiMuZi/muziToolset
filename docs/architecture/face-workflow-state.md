# Face / Rig Library Workflow State

当前 Modular Rig UI 的四步导航不是单纯的界面页签，而是由 `RigLibraryService.workflow_state()` 根据 **Maya Scene + Module Config** 动态计算出来的状态机。

这页专门说明：

```text
什么时候某一步算完成
什么时候下一步解锁
为什么顶部只能回退
什么时候 Build
什么时候 Rebuild
什么时候 Final Connect
```

---

# 四个阶段

```text
01 Setup
    ↓
02 Guide
    ↓
03 Ctrl
    ↓
04 Final
```

当前 UI 标题：

| Step | Title | Subtitle |
| --- | --- | --- |
| 01 | Setup | 配置与层级 |
| 02 | Guide | 导入与定位 |
| 03 | Ctrl | 创建与调整 |
| 04 | Final | 检查与完成 |

---

# State 数据结构

`workflow_state()` 返回：

```python
{
    "completed": {
        1: bool,
        2: bool,
        3: bool,
        4: bool,
    },
    "unlocked": {
        1: bool,
        2: bool,
        3: bool,
        4: bool,
    },
    "suggested": int,
}
```

其中：

```text
completed
    当前 Step 的 Scene 条件是否真的完成

unlocked
    用户当前是否允许进入该 Step

suggested
    根据 Scene 实际状态建议显示在哪一步
```

UI 不自己猜流程进度。

---

# Step 01 — Setup Complete

条件：

```text
存在至少一个 Enabled Module
    +
Rig Library Root 有效
    +
Joint Root 有效
    +
Controller Root 有效
```

当前根组：

```text
grp_md_rig_library_001
grp_md_rig_jnt_001
grp_md_rig_ctrl_001
```

并且这些组必须真的属于当前 Rig Library。

Service 会检查：

```text
node exists
node type == transform
存在 muziRigLibraryOwner
Owner == 当前 Config Network
```

如果场景里已经有同名节点，但不是当前绑定库创建的，Setup 不会把它直接“认领”为自己的节点。

---

# Step 02 — Guide Complete

Guide Complete 建立在 Setup Complete 之上。

每个 Enabled Module 都必须满足：

```text
存在 Guide Name
Guide 能唯一解析
同一个 Guide 不重复使用
Guide Node Type 是 transform / joint
```

也就是说，Guide 阶段不是只看“模板导入过没有”，而是看当前模块所需的定位数据是否真正可用。

如果某个 Guide：

```text
不存在
同名不唯一
类型错误
重复使用
```

Step 02 不会被判定完成。

---

# Step 03 — Build Complete

Step 03 Complete 的真实含义是：

> **所有 Enabled Module 的 Joint / Controller / Hierarchy 已经生成且完整。**

判断条件：

```text
record["built"] == True
    +
_check_built(record) 没有错误
```

`_check_built()` 会验证 Catalog 声明的正式输出是否都存在，同时检查模块归属标记。

因此一个 Module 即使 JSON 里写着：

```text
built = True
```

但 Scene 中节点已经被手工删除，也不会继续被当成 Build Complete。

---

# Step 04 — Connection Complete

Step 04 Complete 建立在 Build Complete 之上。

条件：

```text
每个 Enabled Module
    record["connected"] == True
```

Final 时 Service 调用：

```text
builder.connect_outputs()
```

只有成功连接以后，Module 才进入 Connected 状态。

---

# Unlock 规则

当前规则非常明确：

```python
unlocked = {
    1: True,
    2: setup_complete,
    3: guide_complete,
    4: build_complete,
}
```

也就是：

```text
Step 01
    永远可进入

Step 02
    Step 01 完成后解锁

Step 03
    Guide 有效后解锁

Step 04
    Joint / Controller Build 完成后解锁
```

---

# Suggested Step

当前建议步骤：

```text
如果 Build Complete
    -> Step 04

否则如果 Guide Complete
    -> Step 03

否则如果 Setup Complete
    -> Step 02

否则
    -> Step 01
```

这用于窗口刷新或场景状态变化后，让 UI 回到符合真实 Scene 状态的位置。

---

# 为什么顶部只能回退

顶部 Step Button 不是自由 Tab。

当前规则：

```python
if number > self.current_step:
    拒绝
```

用户前进只能通过底部：

```text
下一步
```

原因是前进通常带 Scene 操作：

```text
Setup Root
Import Guide
Build Outputs
Connect Outputs
```

如果允许直接点击未来 Step，会造成：

```text
UI 看起来已经到 Step 04
但 Scene 其实还没有 Joint / Controller
```

因此：

> 顶部负责导航回退，底部负责流程前进。

---

# Step 01 “下一步”行为

当前执行：

```text
service.setup()
```

成功以后：

```text
Step 01 -> Step 02
```

Setup 主要准备：

```text
Config
Rig Root
Joint Root
Controller Root
```

---

# Step 02 “下一步”行为

Step 02 有两种状态。

## Guide 还没准备好

执行：

```text
service.import_guide()
```

然后仍留在 Guide 阶段，让用户调整定位。

## Guide 已经有效

### 当前 Module 尚未 Build

执行：

```text
service.build()
```

生成所有 Enabled 且 Pending 的 Module Outputs：

```text
Joint
Controller
Hierarchy
```

**此时不建立最终 Driver Connection。**

成功后进入 Step 03。

### 当前 Module 已经 Build

如果用户回到 Guide 修改定位，再点击下一步：

```text
service.rebuild_module(record_id)
```

Rebuild 会：

```text
验证旧输出归属
    ↓
删除当前 Module 旧输出
    ↓
按最新 Guide build_outputs()
    ↓
重新写 Ownership Tag
    ↓
恢复显示设置
    ↓
built = True
connected = False
```

这样 Final 必须重新执行，避免旧连接指向已经删除的输出。

---

# Step 03 “下一步”行为

Step 03 本身主要用于调整。

如果 Build Complete：

```text
直接进入 Step 04
```

如果 Build 不完整：

```text
提示返回 Guide 步骤生成关节和控制器
```

Step 03 不重新创建结构，也不建立最终 Connection。

---

# Step 03 可以修改什么

已 Build Module 允许修改：

```text
ctrl_size
ctrl_color
ctrl_axis
jnt_radius
show_axis
show_joints
show_controls
```

这些修改会直接作用于已经存在的输出。

不允许修改：

```text
name
side
guides
enabled
```

原因是这些属于结构型数据，一旦输出已经 Build，直接修改会破坏 Scene 与配置的一致性。

如果需要修改 Guide / Side，应回退到前面阶段走正式 Rebuild / Mirror 流程。

---

# Step 04 “下一步”行为

执行：

```text
service.finalize()
```

对于：

```text
enabled == True
built == True
connected == False
```

的 Module，调用：

```text
builder.connect_outputs()
```

成功后：

```text
record["connected"] = True
```

最后选择当前所有主 Controller。

---

# Build 与 Connect 为什么分离

这是当前架构最重要的变化之一。

旧的一次性流程：

```text
Guide
 ↓
一次 Build 完全部节点和连接
```

当前流程：

```text
Guide
 ↓
Build Outputs
 ↓
调整 Joint / Controller
 ↓
Final Connect
```

优势：

- Controller 大小可以实时调整；
- Controller 颜色 / Axis 可以调整；
- Joint Radius 可以调整；
- Guide 可以回退修改后 Rebuild；
- Mirror 可以在 Final 前安全处理；
- 最终 Connection 不会过早干扰中间编辑。

---

# Mirror State

Mirror 在：

```text
Step 01
Step 02
Step 03
```

可用。

Step 04 会禁用并提示：

```text
请返回前三步后再镜像
```

Mirror 对 Built Target 的行为不是只更新数据，而是：

```text
Mirror Guide
 ↓
Delete Target Outputs
 ↓
Rebuild Target Outputs
 ↓
connected = False
```

因此镜像后需要重新 Final。

---

# Scene Ownership 与 State 安全

当前 Module Output 使用：

```text
muziRigLibraryModule
```

记录所属 Module ID。

Root 使用：

```text
muziRigLibraryOwner
```

记录所属 Config Network。

Rebuild / Check 不只看名字，还看 Ownership。

如果节点：

```text
名称正确
但 Ownership 缺失 / 错误
```

Service 会停止操作，而不是直接删除。

这使自动 Rebuild 更安全。

---

# Config 状态

Rig Library 配置保存在 Maya Network：

```text
network_md_rig_library_config_001
```

JSON 属性：

```text
muziRigLibraryJson
```

Module Record 里与 Workflow 直接相关的字段：

```text
id
enabled
kind
name
side
guides
built
connected
ctrl_size
ctrl_color
ctrl_axis
jnt_radius
show_axis
show_joints
show_controls
```

配置只是 Workflow Metadata，不等于 Maya Scene Backup。

Export Recipe 会主动把：

```text
built = False
connected = False
```

写入导出文件，避免让 JSON 假装包含已经生成的 Scene Rig。

---

# 常见状态例子

## 新场景

```text
completed: 1=False 2=False 3=False 4=False
unlocked:  1=True  2=False 3=False 4=False
suggested: 1
```

## Setup 完成

```text
completed: 1=True 2=False 3=False 4=False
unlocked:  1=True 2=True  3=False 4=False
suggested: 2
```

## Guide 有效，但还没 Build

```text
completed: 1=True 2=True 3=False 4=False
unlocked:  1=True 2=True 3=True  4=False
suggested: 3
```

注意：用户通常仍会在 Step 02 点击“下一步”执行实际 Build，然后进入 Step 03。

## Joint / Controller 已 Build

```text
completed: 1=True 2=True 3=True 4=False
unlocked:  1=True 2=True 3=True 4=True
suggested: 4
```

## Final 完成

```text
completed: 1=True 2=True 3=True 4=True
unlocked:  1=True 2=True 3=True 4=True
suggested: 4
```

---

# 排查 Step 无法前进

按这个顺序检查：

```text
Step 01 锁住？
    -> 是否有 Enabled Module
    -> Root Ownership 是否正确

Step 02 不完成？
    -> Guide 是否存在且唯一
    -> Guide Type 是否正确
    -> Guide 是否重复

Step 03 不完成？
    -> record.built 是否为 True
    -> Catalog 声明的输出是否都存在
    -> Output Ownership 是否正确

Step 04 不完成？
    -> record.connected 是否为 True
    -> Final 是否真正成功执行
```

不要只看 UI 颜色判断 Scene 状态，`workflow_state()` 才是最终依据。

---

# 相关源码

- [`systems/rig/library_service.py`](../reference/systems/rig/library_service.md)
- [`systems/rig/ui/modular_rig_ui.py`](../reference/systems/rig/ui/modular_rig_ui.md)
- [`systems/rig/library_catalog.py`](../reference/systems/rig/library_catalog.md)
- [Face System Architecture](face-system.md)
