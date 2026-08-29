# 总体架构

MuziTools 当前唯一正式运行框架是仓库根包 `muziToolset`。

```text
muziToolset/
├─ app/         # 应用入口、工具箱、窗口生命周期
├─ ui/          # Theme 与通用 UI Widget
├─ core/        # Maya 通用底层能力
├─ tools/       # 用户直接使用的小工具
├─ systems/     # 可复用 Rig Builder / Workflow
├─ resources/   # 图标、Controller Shape 等静态资源
└─ tests/       # Maya Smoke / Functional Smoke
```

## 依赖方向

推荐依赖方向：

```text
app / tools
    ↓
systems
    ↓
core
```

`core` 不能反向依赖 `tools / systems / app / ui`。

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

同时也避免拆得过细：例如 Animation JSON 已回收进 `animation_utils.py`，Scene IO 回收进 `scene_utils.py`。
