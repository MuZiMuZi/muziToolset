# 绑定工作流

这页按一个典型角色绑定的制作阶段整理 MuziTools 的主要能力。

它回答的是“下一步应该做什么”；具体函数参数请进入对应 API 页面。

## 总览

```text
模型检查 / 清理
    ↓
命名和基础整理
    ↓
Joint
    ↓
Controller
    ↓
Skin / Weight
    ↓
BlendShape / Corrective
    ↓
Face / Body 专项系统
    ↓
发布前检查
```

对应用户手册：

- [场景清理与模型检查](cleanup.md)
- [基础工具](basic-tools.md)
- [Joint 工作流](joint.md)
- [Controller 工作流](controller.md)
- [Skin 工作流](skin.md)
- [BlendShape 工作流](blendshape.md)
- [Face Guide](face-guide.md)

---

# 1. 准备模型与场景

推荐顺序：

```text
模型命名
    ↓
模型检查
    ↓
清理 History / 临时节点
    ↓
整理 Outliner
    ↓
建立 Rig 工作层级
```

先看：

- [基础工具](basic-tools.md)
- [场景清理与模型检查](cleanup.md)

相关 API：

- [model_check_utils.py](../reference/core/model_check_utils.md)
- [scene_clean_utils.py](../reference/core/scene_clean_utils.md)
- [rename_utils.py](../reference/core/rename_utils.md)

---

# 2. Joint

Joint 是正式 Deform Skeleton 的基础。

常用能力：

- 创建 Joint / Joint Chain；
- 沿 Curve / 现有 Joint 重采样；
- Orient Joint；
- 对齐、镜像和整理层级。

先看：[Joint 工作流](joint.md)

相关 API：

- [Joint Tool](../reference/tools/joint/joint_tool.md)
- [Joint Resample Tool](../reference/tools/joint/joint_resamp_tool.md)
- [Joint Utils](../reference/core/joint_utils.md)

---

# 3. Controller

标准 Controller 不应该由每一个 Body / Face 模块重复实现。

推荐关系：

```text
Tool UI
    ↓
systems/controller/builder.py
    ↓
core/control_shape_utils.py
```

先看：[Controller 工作流](controller.md)

相关 API：

- [Controller Builder](../reference/systems/controller/builder.md)
- [Parent Space Blend](../reference/systems/controller/space_blend.md)
- [Create Ctrl Tool](../reference/tools/controller/create_ctrl_tool.md)
- [Control Shape Tool](../reference/tools/controller/control_shape_tool.md)

---

# 4. Skin 与 Weight

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
极限 Pose 检查
```

先看：[Skin 工作流](skin.md)

相关 API：

- [Skin Tool](../reference/tools/skin/skin_tool.md)
- [Skin Utils](../reference/core/skin_utils.md)

---

# 5. BlendShape / Corrective

BlendShape 用于：

- Face Expression；
- Joint Driver Corrective；
- 变形修正；
- 复杂局部形变。

先看：[BlendShape 工作流](blendshape.md)

相关 API：

- [BlendShape Utils](../reference/core/blendshape_utils.md)
- [Add BlendShape Tool](../reference/tools/blendshape/add_blendshape_tool.md)
- [Invert Shape Tool](../reference/tools/blendshape/invert_shape_tool.md)

---

# 6. Matrix 与空间关系

较复杂的 Rig 关系优先评估 Matrix，而不是堆叠大量 Constraint。

常见用途：

```text
Parent Space
Offset Parent Matrix
Zip Lip
局部 Follow
稳定驱动层级
```

相关 API：

- [Matrix Utils](../reference/core/matrix_utils.md)
- [Connection Utils](../reference/core/connection_utils.md)
- [Controller Space Blend](../reference/systems/controller/space_blend.md)

如果只是日常创建 Constraint，则先看 [基础工具](basic-tools.md)。

---

# 7. Face Rig

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

主要 API：

- [face_base.py](../reference/systems/face/face_base.md)
- [face_setup.py](../reference/systems/face/face_setup.md)
- [face_guide.py](../reference/systems/face/face_guide.md)
- [curve_attachment.py](../reference/systems/face/curve_attachment.md)
- [Eyelid Builder](../reference/systems/face/eyelid/builder.md)
- [Zip Lip Builder](../reference/systems/face/lip/zip_builder.md)

---

# 8. Body / Skirt

Body Component 位于：

```text
systems/body/
```

当前 Skirt 相关入口：

- [Skirt Builder](../reference/systems/body/skirt/builder.md)
- [Skirt Ctrl Tool](../reference/tools/rig/skirt_ctrl_tool.md)

完整 Rig 辅助面板：

- [rig_tool.py](../reference/tools/rig/rig_tool.md)

---

# 9. 发布前检查

发布前不要只看“能不能动”。

至少检查：

```text
模型 / Rig 命名
Outliner 层级
临时节点
控制器 Set
Visibility
Joint / Skin
Reference / Namespace
Scene Error
极限 Pose
```

先看：[场景清理与模型检查](cleanup.md)

---

# Tool、Core、System 怎么配合

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

## 下一步

- [用户手册首页](index.md)
- [常用工具工作流](tools.md)
- [API Reference](../reference/index.md)
