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

`systems/face/workflow.py` 统一负责当前查看 Step 的 Face 顶层功能组显示状态。

当前规则：

| Step | Model | Guide | Ctrl | Joint | Internal Rig Nodes |
| --- | --- | --- | --- | --- | --- |
| 01 Setup | Show | Hide | Hide | Hide | Hide |
| 02 Guide | Show | Show | Hide | Hide | Hide |
| 03 Build | Show | Hide | Show | Show | Hide |
| 04 Finalize | Show | Hide | Show | Hide | Hide |

最重要的规则是：

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
5. 当前 Step 的场景显示组加入 `workflow.step_visibility_rules`；
6. 不使用仅存在于 QWidget 内存里的状态作为唯一数据源。
