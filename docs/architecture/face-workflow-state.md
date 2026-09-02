# Face Workflow State

Face Rig 的 UI 恢复和场景显示统一遵守 **Scene Config Driven Workflow**。

## 核心原则

```text
Scene Config
    ↓
Workflow Progress
    ↓
进入 / 回退 Step
    ↓
Load Config
    ↓
Restore UI
    ↓
Apply Scene Visibility
```

`network_md_face_config_001` 是可恢复 UI 参数的主要持久化来源。

UI Widget 自身不承担长期数据保存。

## Workflow Progress 与 Current View

```text
Workflow Progress
    当前真正制作到哪一步
    保存到 face_current_step

Current View Step
    当前用户正在查看哪个页面
    可以临时回退查看旧 Step
```

回看旧页面不会自动降低 Workflow Progress；只有旧 Step 数据被真正修改并失效时才回退正式进度。

---

# Step 01 UI Restore

从 Config Message / Value 恢复：

```text
Face Head Model
Face LF Eye Model
Face RT Eye Model
Upper Teeth Model
Lower Teeth Model
Tongue Model
Gum Model
Mouth Joint Number
```

模型节点使用 Message Connection 保存，因此 Maya Rename 后仍可以恢复。

---

# Step 02 UI Restore

从 Config 恢复：

```text
Global Scale
LF Controller Color
RT Controller Color
MD Controller Color
Brow Size
Eye Size
Eyelid Size
Nose Size
Cheek Size
Lip Size
Jaw Size
Teeth Size
Tongue Size
```

Controller Settings 使用 `systems/face/config.py` 中的正式 Attribute Schema。

修改 Controller Setting：

```text
修改 UI
    ↓
立即保存 Config
    ↓
Step 02 = Dirty
    ↓
Step 03 / 04 Invalid
    ↓
face_current_step = Step 02
```

Guide Locator 的 Transform 已存在 Maya Scene，不重复序列化到 UI Config。

---

# Scene Visibility

静态规则：

```text
systems/face/config.py
```

执行位置：

```text
systems/face/ui/workflow_controller.py
```

顶层显示规则：

| Step | Model Group | Guide | Ctrl | Joint | Internal Rig Nodes |
| --- | --- | --- | --- | --- | --- |
| 01 Setup | Show | Hide | Hide | Hide | Hide |
| 02 Guide | Show | Show | Hide | Hide | Hide |
| 03 Build | Show | Hide | Show | Show | Hide |
| 04 Finalize | Show | Hide | Show | Hide | Hide |

对应：

```python
config.face_step_visibility_rules
```

Step 01 / 02 使用 `setup_sources` 模型显示策略，只显示 Setup Config 保存的原始输入模型。

Step 03 / 04 当前模型内部规则为：

```text
preserve
```

后续需要 Deform / Final Model 专用显示规则时，直接扩展 `config.face_step_model_display_rules`。

---

# Step 03 Module Build State

Step 03 的完整业务单元统一称为 **Module**。

当前已经接入：

```text
TeethModule
```

UI 入口：

```text
ui/build_controller.py
```

当前 Teeth Button 的“构建完成”状态主要反映当前 UI Session 的构建结果；Rig 节点本身会真实存在于 Maya Scene。

在 Step 03 完整产品化之前，Module 完成状态应继续迁移到以下两种方案之一：

```text
Scene Config 持久化 Module Completed State
```

或：

```text
从确定性的 Maya Rig Nodes 推导 Module Build State
```

不能长期只依赖 QWidget 内存状态。

TeethModule 完成也**不会**直接把整个 Step 03 标记 Completed，因为 Jaw / Tongue / Lip / Eye / Brow 等 Module 尚未全部接入。

---

# Guide Visibility

```text
进入 Step 02
    → grp_md_face_guide_001 显示

离开 Step 02
    → grp_md_face_guide_001 隐藏
```

由 `workflow_controller.py` 在页面切换时直接执行。

---

# 正式 UI 入口

当前真实调用链：

```text
systems.face.show()
    ↓
systems.face.ui.show()
    ↓
ui/build_controller.py
    ↓
ui/workflow_controller.py
    ↓
ui/face_rig_ui.py
```

职责：

```text
face_rig_ui.py
    基础 Widget / Layout / Step 01-02 视图

workflow_controller.py
    Config -> UI Restore
    Step Scene Visibility
    Workflow Progress

build_controller.py
    当前正式 UI 扩展层
    Controller Schema 补全
    Step 03 Module Build 页面
```

---

# 后续 Step 接入规范

Step 03 / 04 新增可编辑参数时：

1. 先定义正式 Config Attribute；
2. Module / Step 保存方法负责持久化；
3. Workflow UI 增加 Loader；
4. 进入或回退 Step 自动恢复；
5. 显示规则补到 `config.face_step_visibility_rules`；
6. 模型规则补到 `config.face_step_model_display_rules`；
7. 不为简单规则额外增加管理文件；
8. 不使用仅存在于 QWidget 内存里的状态作为唯一数据源。
