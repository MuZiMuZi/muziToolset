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

`network_md_face_config_001` 是可恢复 UI 参数的唯一持久化来源。

UI Widget 自身不承担长期数据保存。

## Workflow Progress 与当前查看页面

这两个概念必须区分：

```text
Workflow Progress
    当前真正制作到哪一步
    保存到 face_current_step

Current View Step
    当前用户正在查看哪个页面
    可以临时回退查看旧 Step
```

例如已经制作到 Step 03 时，可以返回 Step 01 查看 Setup 数据，但不会因此把 `face_current_step` 改回 Step 01。

如果旧 Step 被真正修改并失效，例如 Step 02 修改 Controller Settings、Mirror 或 Reimport Guide，则 Workflow Progress 会退回 Step 02。

## Step 01 UI Restore

返回 Step 01 时，从 Config Message / Value 恢复：

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

模型节点使用 Message Connection 保存，因此 Maya Rename 后仍可以恢复到 UI。

Step 01 数据仍然在正式提交 Setup 时保存，因为这些输入和 Work Model 构建结果必须保持一致。

## Step 02 UI Restore

返回 Step 02 时，从 Config 恢复：

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
```

Controller Settings 与 Build Result 不同，它们是纯配置数据，因此修改后立即写回 Scene Config。

```text
修改 Controller Setting
        ↓
立即保存 Config
        ↓
Step 02 = Dirty
        ↓
face_current_step = Step 02
        ↓
点击“下一步”时再执行 Guide Validation / Completed
```

这样即使关闭 Face Rig、保存 Maya、重新打开工具，参数也不会丢失。

## Guide Position

Guide Locator 的位置已经存在于 Maya Scene Transform 中，因此不重复把矩阵复制进 UI Config。

Config 只保存 Guide Root / Move Ctrl / Version 等稳定引用和参数。

## Step Scene Visibility

`systems/face/workflow.py` 统一负责当前查看 Step 的场景显示状态。

场景显示分成两层：

```text
Top Level Face Group Visibility
        +
Face Model Group Internal Visibility
```

顶层规则：

| Step | Model Group | Guide | Ctrl | Joint | Internal Rig Nodes |
| --- | --- | --- | --- | --- | --- |
| 01 Setup | Show | Hide | Hide | Hide | Hide |
| 02 Guide | Show | Show | Hide | Hide | Hide |
| 03 Build | Show | Hide | Show | Show | Hide |
| 04 Finalize | Show | Hide | Show | Hide | Hide |

其中 `Model Group = Show` 只表示 `grp_md_face_model_001` 这个容器允许显示，里面具体哪些模型可见还要继续执行 Model Display Rule。

## Step 01 / Step 02 Model Display Rule

Step 01 和 Step 02 使用：

```text
setup_sources
```

系统会读取 Step 01 Config 中保存的模型引用：

```text
Head
LF Eye
RT Eye
Upper Teeth
Lower Teeth
Tongue
Gum
```

然后扫描：

```text
grp_md_face_model_001
```

只显示包含这些输入模型的第一层分支，其它分支全部隐藏。

例如：

```text
grp_md_face_model_001
├── grp_md_face_tweak_001       Hide
├── grp_md_face_stretch_001     Hide
├── grp_md_face_deform_001      Hide
├── model_md_head_001           Show
├── model_lf_eyeball_001        Show
├── model_rt_eyeball_001        Show
├── model_md_upper_teeth_001    Show
├── model_md_lower_teeth_001    Show
├── model_md_tongue_001         Show
└── model_md_lower_gum_001      Show
```

所以进入 Step 02 后，绑定师看到的是：

```text
Setup 输入模型
+
Face Guide
```

而不会同时看到 Tweak / Stretch / Deform 工作副本，减少视图遮挡和误选择。

如果某个可选模型在 Step 01 没有指定，系统不会因为它不存在而报错。

旧场景如果完全没有可恢复的 Setup Model 信息，Model Display Rule 会保持当前内部显示状态，避免误把全部模型隐藏。

## Step 03 / Step 04 Model Display Contract

目前 Step 03 / Step 04 的正式 Component / Finalize 内容尚未完全定义，因此模型内部规则暂时使用：

```text
preserve
```

也就是保留当前内部模型显示状态，不提前猜测 Build / Finalize 到底应该显示哪一份 Work Model。

以后正式实现 Step 03 / Step 04 时，继续在同一份：

```python
step_model_display_rules
```

中增加明确规则，例如只显示 Deform Model、Final Model 等，而不是在各个 UI 页面单独写 Visibility。

## Guide Visibility

最重要的 Guide 规则是：

```text
进入 Step 02
    → grp_md_face_guide_001 显示

离开 Step 02
    → grp_md_face_guide_001 隐藏
```

后续 Step 03 / Step 04 增加正式 Component 和 Finalize 内容后，继续扩展同一份 Visibility Contract，不在各 UI 页面散落 `cmds.setAttr(...visibility)`。

## UI Controller

正式入口通过：

```text
systems.face.show()
    ↓
systems.face.ui.show()
    ↓
ui/workflow_controller.py
    ↓
ui/face_rig_ui.py
```

其中：

```text
face_rig_ui.py
    Widget / Layout / 用户交互视图

workflow_controller.py
    Config -> UI Restore
    Step Scene Visibility
    Controller Settings 实时持久化
```

这样系统业务仍然在 `setup / guide / build / finalize`，UI Controller 不复制 Rig Algorithm。

## 后续 Step 接入规范

Step 03 / 04 新增可编辑参数时，应遵守：

1. 数据先定义正式 Config Attribute；
2. Step 保存方法负责持久化；
3. Workflow UI 增加对应 Loader；
4. 进入或回退 Step 自动恢复；
5. 当前 Step 的顶层场景显示加入 `workflow.step_visibility_rules`；
6. 当前 Step 的模型内部显示加入 `workflow.step_model_display_rules`；
7. 不使用仅存在于 QWidget 内存里的状态作为唯一数据源。
