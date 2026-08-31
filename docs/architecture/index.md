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

Face System 按四步 Workflow 分包：

```text
systems/face/
├── face_base.py
├── config.py
├── setup/
├── guide/
├── build/
├── finalize/
├── data/
└── ui/
```

其中：

```text
config      Face 静态名称、默认参数和 Step 显示规则

setup       Step 01 输入和基础场景

guide       Step 02 Template / Query / Mirror / Repair / Validation

build       Step 03 Component / Builder

finalize    Step 04 Final Check / Cleanup / Publish

data        跨 Step 的 Face 公共数据

ui          Face Wizard View / Config Restore / Step Visibility
```

Guide 当前保持单文件实现：

```text
systems/face/guide/
└── face_guide.py
```

不再为了 Guide Data、Template、Mirror 或 Workflow Visibility 单独增加中间管理文件。

详见：[Face System Architecture](face-system.md)。

Face Rig 的 Config 恢复、UI 回填、Current Step 和 Scene Visibility 规则详见：[Face Workflow State](face-workflow-state.md)。

## Step 与 Component

不要把 Step 和 Component 当成同一个概念。

```text
Step
    用户工作流阶段

Component
    Teeth / Tongue / Jaw / Lip / Eyelid / Brow 等面部绑定模块

Builder
    Curve Attachment / Zip / Radial Joint 等可组合算法

Core
    Matrix / Curve / Joint / DAG / Attribute / Naming 等通用 Maya 能力
```

所有可重新提交的 Step 统一使用：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

简单 Component 也可以复用这套四阶段构建思路，但 Component 本身不等于整个 Workflow Step。

## 为什么不再使用万能 Utils，也不做无意义拆分

早期项目存在 `pipelineUtils.py` 一类综合模块，把动画、Curve、Surface、Constraint、Face、Controller、文件 IO 等内容放在同一个类中。

现在 Core 改成“一个 Maya 领域一个模块”：

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

但是 System 层不为了形式继续拆小文件。

如果一个文件只是：

- 转发固定参数；
- 保存已经可以通过 Naming API 动态生成的完整名称；
- 把一个很短的业务流程再包装一层；

则优先合回所属 Step / Component。

目标是：

```text
职责清楚
+
调用路径短
+
容易查询
+
容易重建
```
