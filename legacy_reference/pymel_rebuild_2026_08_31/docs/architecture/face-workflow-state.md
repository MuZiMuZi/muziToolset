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

Controller Settings 修改后立即写回 Scene Config。

```text
修改 Controller Setting
        ↓
立即保存 Config
        ↓
Step 02 = Dirty
        ↓
face_current_step = Step 02
        ↓
点击“下一步”时再执行 Validation / Completed
```

Guide Locator 的位置已经存在于 Maya Scene Transform 中，因此不重复序列化到 UI Config。

## Scene Visibility 的实现位置

不再单独维护：

```text
systems/face/workflow.py
```

现在分成两个简单职责：

```text
systems/face/config.py
    定义每个 Step 应该显示哪些 Face Group

systems/face/ui/workflow_controller.py
    Step 切换时直接执行 visibility
```

也就是说：

> Config 只定义规则，UI Workflow Controller 直接执行，不再经过第三层管理模块。

## 顶层显示规则

| Step | Model Group | Guide | Ctrl | Joint | Internal Rig Nodes |
| --- | --- | --- | --- | --- | --- |
| 01 Setup | Show | Hide | Hide | Hide | Hide |
| 02 Guide | Show | Show | Hide | Hide | Hide |
| 03 Build | Show | Hide | Show | Show | Hide |
| 04 Finalize | Show | Hide | Show | Hide | Hide |

对应静态配置位于：

```python
config.face_step_visibility_rules
```

## Step 01 / Step 02 Model Display Rule

Step 01 和 Step 02 使用：

```text
setup_sources
```

对应：

```python
config.face_step_model_display_rules
```

Workflow Controller 会读取 Step 01 Config 中保存的模型引用：

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

只显示包含这些输入模型的第一层分支，其它分支隐藏。

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

所以 Step 02 的视图保持为：

```text
Setup 输入模型
+
Face Guide
```

便于选择 Locator。

如果旧场景完全没有可恢复的 Setup Model 信息，则不主动把全部模型隐藏。

## Step 03 / Step 04 Model Display

目前 Step 03 / Step 04 的 Component / Finalize 内容还在继续实现，因此模型内部规则暂时为：

```text
preserve
```

以后明确需要 Deform Model、Final Model 等显示方案时，直接修改：

```python
config.face_step_model_display_rules
```

不需要再增加新的 Workflow 文件。

## Guide Visibility

核心规则：

```text
进入 Step 02
    → grp_md_face_guide_001 显示

离开 Step 02
    → grp_md_face_guide_001 隐藏
```

这个行为由 `workflow_controller.py` 在页面切换时直接执行。

## 正式 UI 入口

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

## 后续 Step 接入规范

Step 03 / 04 新增可编辑参数时：

1. 先定义正式 Config Attribute；
2. Step / Component 保存方法负责持久化；
3. Workflow UI 增加对应 Loader；
4. 进入或回退 Step 自动恢复；
5. 顶层显示规则补到 `config.face_step_visibility_rules`；
6. 模型内部规则补到 `config.face_step_model_display_rules`；
7. 不为简单规则再增加额外管理文件；
8. 不使用仅存在于 QWidget 内存里的状态作为唯一数据源。
