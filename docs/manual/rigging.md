# 绑定工作流

这页按一个典型角色绑定的制作阶段整理 MuziTools 的主要能力。

它回答的是“下一步应该做什么”；具体函数参数请进入对应 API 页面。

## 1. 准备模型与场景

建议先完成：

```text
模型命名
    ↓
模型检查
    ↓
清理历史和无效节点
    ↓
建立绑定工程层级
```

相关入口：

- `tools/basic/rename_tool.py`
- `tools/clean/model_checker.py`
- `tools/clean/hierarchy_cleaner.py`
- `core/scene_clean_utils.py`

## 2. Joint

Joint 层负责正式变形骨架。

常用能力：

- 创建 Joint / Joint Chain；
- 沿 Curve / 现有 Joint 重采样；
- Orient Joint；
- 对齐、镜像和整理层级。

相关文档：

- [Joint Tool](../reference/tools/joint/joint_tool.md)
- [Joint Resample Tool](../reference/tools/joint/joint_resamp_tool.md)
- [Joint Utils](../reference/core/joint_utils.md)

## 3. Controller

标准 Controller 不应该由每一个 Body / Face 模块重复实现。

推荐关系：

```text
Tool UI
    ↓
systems/controller/builder.py
    ↓
core/control_shape_utils.py
```

相关文档：

- [Controller Builder](../reference/systems/controller/builder.md)
- [Parent Space Blend](../reference/systems/controller/space_blend.md)
- [Create Ctrl Tool](../reference/tools/controller/create_ctrl_tool.md)

## 4. Skin 与 Weight

完成 Joint 后进入 Skin。

```text
Joint
    ↓
SkinCluster
    ↓
初始权重
    ↓
Weight 调整
    ↓
变形检查
```

相关文档：

- [Skin Tool](../reference/tools/skin/skin_tool.md)
- [Skin Utils](../reference/core/skin_utils.md)

## 5. BlendShape / Corrective

BlendShape 用于：

- Face Expression；
- Joint Driver Corrective；
- 变形修正；
- 复杂局部形变。

相关文档：

- [BlendShape Utils](../reference/core/blendshape_utils.md)
- [Add BlendShape Tool](../reference/tools/blendshape/add_blendshape_tool.md)
- [Invert Shape Tool](../reference/tools/blendshape/invert_shape_tool.md)

## 6. Matrix 与空间关系

较复杂的 Rig 关系优先考虑 Matrix，而不是堆叠大量 Constraint。

常见用途：

```text
Parent Space
Offset Parent Matrix
Zip Lip
局部跟随
稳定驱动层级
```

相关 API：

- [Matrix Utils](../reference/core/matrix_utils.md)
- [Connection Utils](../reference/core/connection_utils.md)
- [Controller Space Blend](../reference/systems/controller/space_blend.md)

## 7. Face Rig

Face Rig 是独立的多 Step 系统。

当前推荐主流程：

```text
Step 01
FaceSetup.build()
        ↓
Step 02
FaceGuide.build()
        ↓
手动贴合 Guide
        ↓
validate_guides()
        ↓
finalize()
        ↓
Step 03
Lip / Jaw / Eyelid / Brow Builder
        ↓
Step 04
Finalize / Corrective / Picker
```

从 [Face Guide](face-guide.md) 开始。

## 8. Body / Skirt

Body 组件位于：

```text
systems/body/
```

当前 Skirt Builder：

- [Skirt Builder](../reference/systems/body/skirt/builder.md)

UI 辅助工具位于：

- [Skirt Ctrl Tool](../reference/tools/rig/skirt_ctrl_tool.md)

## Tool、Core、System 怎么配合

```text
Core
    Maya 通用原子能力

System
    完整可复用 Rig Component

Tool
    给绑定师使用的 UI / Selection / 参数入口
```

例如创建 Controller：

```text
create_ctrl_tool.py
        ↓
systems/controller/builder.py
        ↓
control_shape_utils.py
```

如果修改的是算法，通常应该改下层；如果修改的是按钮和交互，才改 Tool。
