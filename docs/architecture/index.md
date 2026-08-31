# 总体架构

MuziTools 当前唯一正式运行框架是仓库根包 `muziToolset`。

```text
muziToolset/
├─ app/         # 应用入口、主工具箱、窗口生命周期
├─ ui/          # Theme 与通用 UI Widget
├─ core/        # Maya 通用底层能力
├─ tools/       # 用户直接使用的小工具
├─ systems/     # 可复用 Rig Builder / Workflow
├─ resources/   # Guide Template、Controller Shape 等静态资源
└─ tests/       # Maya Smoke / Functional Smoke
```

## 依赖方向

```text
app / ui / tools
        ↓
      systems
        ↓
       core
```

`core` 不能反向依赖 `tools / systems / app / ui`。

## UI / App

`ui` 维护整个项目的统一视觉和复合 Widget：

```text
ui/
├── theme.py
├── window_utils.py
└── widgets/
```

当前正式视觉方向采用 Arc-inspired 的 clean / calm / sidebar-first 信息组织，所有业务窗口优先复用 Theme Token 和 Role，不在 Tool 中维护第二套完整 QSS。

详见：[UI Design System](../development/ui-design.md)。

`app` 负责主工具箱、分类 Sidebar、Tool Discovery、Window Manager 和应用生命周期。

## Systems

`systems` 实现完整且可复用的 Rig Workflow / Component / Builder。

Face System 已经按四步 Workflow 分包：

```text
systems/face/
├── face_base.py
├── config.py
├── workflow.py
├── setup/
├── guide/
├── build/
├── finalize/
├── data/
└── ui/
```

其中：

```text
setup       Step 01 输入和基础场景

guide       Step 02 Template / Query / Mirror / Repair / Validation

build       Step 03 Component / Builder

finalize    Step 04 Final Check / Cleanup / Publish

data        跨 Step 的 Face 公共数据

workflow    跨 Step 的场景显示状态

ui          Face Wizard View / Workflow UI Controller
```

详见：[Face System Architecture](face-system.md)。

Face Rig 的 Config 恢复、UI 回填、Current Step 和 Scene Visibility 规则详见：[Face Workflow State](face-workflow-state.md)。

## Step 与 Component

不要把 Step 和 Component 当成同一个概念。

```text
Step
    用户工作流阶段

Component
    Jaw / Lip / Eyelid / Brow 等面部绑定模块

Builder
    Curve Attachment / Zip / Radial Joint 等可组合算法

Core
    Matrix / Curve / Joint / DAG / Attribute 等通用 Maya 能力
```

所有可重新提交的 Step 统一继承 `systems.common.StepBase`：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

## 为什么不再使用万能 Utils

早期项目存在 `pipelineUtils.py` 一类综合模块，把动画、Curve、Surface、Constraint、Face、Controller、文件 IO 等内容放在同一个类中。

现在改成“一个 Maya 领域一个模块”：

```text
animation_utils.py
scene_utils.py
transform_utils.py
matrix_utils.py
connection_utils.py
constraint_utils.py
curve_utils.py
surface_utils.py
skin_utils.py
...
```

同时避免拆得过细：如果两个文件只是同一个业务生命周期中的少量辅助能力，应优先在所属 Package 内收敛，而不是让根目录无限增加小模块。
