# 林雄《Rig Build Description》中文译文与架构参考

> 原作者：Xiong Lin（林雄）  
> 原文标题：Rig Build Description  
> 文档用途：MuziTools Component Based Procedural Rig 架构研究参考  
> 翻译说明：正文部分按原 PDF 内容翻译；最后的“MuziTools 架构参考”是项目自身的研究结论，不属于原文。

---

## 参考资料

- PDF：Rig Build Description - Xiong Lin
- Bilibili：Component Based Procedure Auto Rig  
  https://www.bilibili.com/video/BV1e4411G7Hq/
- Bilibili：Maya绑定和动画工具展示  
  https://www.bilibili.com/video/BV1fK4y1T7uw/

这两段视频和 PDF 后续统一作为 MuziTools 绑定系统的架构参考资料。

---

# 一、PDF 中文翻译

## 第 1 页 - Rig Build Description

### Rig 构建说明

你好！感谢你查看我的 Auto Rig。

在这份文档中，我会介绍我是如何设计 Rig Building Workflow（绑定构建工作流）的。

下面的图片展示了 Auto Rig 在 UI 部分的一些主要功能。

整个界面使用 PySide 实现。

从整体结构上来说，我的 Auto Rig 是一个 **Module Based Procedure Auto Rig（基于模块的程序化自动绑定系统）**。

同时，它也具备 **Asset Manager（资产管理器）** 的功能。

---

### 为什么叫 Jigsaw

因为整个系统是基于模块构建的，所以我把这套 Auto Rig 称为：

**Jigsaw**

它有点像拼图。

我可以把不同的 Rig Module 组合在一起，从而构建各种不同类型的生物角色。

例如，一个基础的人类角色可以由下面这些模块组成：

- 2 个 Arm Rig
- 2 个 Leg Rig
- 2 个 Hand Rig
- 1 个 Torso Rig
- 1 个 Neck Rig

如果再加入：

- 2 个 Wing Rig

就可以构建一个 Angel Character（天使角色）。

系统中预先准备了一些 Rig Module 的组合模板，包括：

- Angel
- Bat
- Bird
- Dog
- Human
- Dragon
- Tiger Hawk

---

### UI 中展示的主要区域

原图中的界面包含以下概念：

**Rig Module Library**

Rig 模块库。

用于浏览当前系统中已经存在的各种 Rig Module。

**Building Workflow**

绑定构建工作流。

用于按照制作流程逐步完成 Rig。

**Rig Module Setting**

当前 Rig Module 的设置区域。

**Rig Module Current In Use**

当前角色正在使用的 Rig Module。

**Rig Module Preset**

Rig Module 的预设组合。

**Version Control**

版本控制。

**Asset Management**

资产管理。

---

## 第 2 页 - Rig Module Preset

这一页主要展示系统中已经预设好的不同角色模板。

包括：

- Human Template
- Angel Template
- Bat Template
- Bird Template
- Dog Template
- Quad Dragon Template
- Face Template

这些模板本质上并不是完全独立的 Rig 系统。

它们是由不同 Rig Module 组合出来的预设方案。

因此，同一个 Rig Module 可以被多个角色 Template 重复使用。

---

## 第 3 页 - Base Rig 与模块继承

整个系统一共有 **21 个可以用于实际制作的 Rig Module**。

所有模块使用：

- Python
- Object-Oriented Programming（面向对象编程）

进行开发。

---

### Base Rig

首先，我创建了一个基础 Rig Class：

**Base Rig**

Base Rig 只包含一些最基础、所有 Rig Module 都需要的信息和功能，例如：

- Naming Convention（命名规范）
- Connection Method（连接方式）

之后，其余的 Rig Module 都从 Base Rig 继承。

然后在 Base Rig 的基础上继续扩展，逐渐形成更加复杂的 Rig Module。

原文中的图展示了各个 Rig Module 之间的继承关系。

这意味着：

```text
Base Rig
    ↓
Basic Rig Module
    ↓
More Specialized Rig Module
    ↓
Final Production Rig Module
```

公共逻辑由基础层提供。

具体角色模块只增加自己真正需要的绑定功能。

---

### Limb Rig 已开发功能

作者列出的 Limb Rig 功能包括：

1. IK / FK Switch  
   IK / FK 切换。

2. IK Control Auto Stretch  
   IK 控制器自动拉伸。

3. Soft IK  
   Soft IK。

4. Elbow Offset / Lock  
   手肘偏移 / 锁定。

5. Limb Squeeze and Squash  
   肢体挤压与拉伸变形。

6. Local Scale  
   局部缩放。

7. IK Control Space Switch  
   IK 控制器空间切换。

8. FK Control Rotation Space Switch  
   FK 控制器旋转空间切换。

9. Limb Length Adjust in Both FK and IK Mode  
   FK / IK 两种模式下都可以调整肢体长度。

10. Bendy Control  
    Bendy 控制。

这些功能会继续被继承到：

- Arm Rig
- Bird Wing Rig
- Bat Wing Rig
- Leg Rig
- Hind Leg Rig
- Fore Leg Rig

也就是说，通用 Limb 能力只开发一次，再由更具体的角色模块继承使用。

---

## 第 4 页 - Procedure Workflow 与 Skin Weight

作者的 Auto Rig 使用的是：

**Procedure Workflow（程序化制作流程）**

这意味着系统保存的不只是最终完成的 Rig 文件。

同时还会保存：

**Rig Building Progress（绑定制作过程中的数据）**

在作者的工作流中，主要保存两类重要制作数据：

- Skin Weights
- Pose Space Deformer（PSD）

---

### Skin Weight Tool

原图展示的是 Skin Weight Tool 的 UI。

这个工具可以把 Skin Weight 数据导出。

工具使用：

- Python
- PySide

开发。

Auto Rig 在重新构建 Rig 时，会自动读取这些已经保存的 Skin Data。

---

### Skin Weight Tool 功能

作者列出的功能：

1. High Speed Data Transfer  
   高速数据传输。

2. Export / Import Each Skin Weight in Separate File  
   每一个 Skin Weight 可以单独导出 / 导入文件。

3. Export / Import Skin Weights in One Single File  
   也可以把 Skin Weight 统一导出 / 导入到一个文件中。

4. Works for Polygon, NURBS and Curves  
   支持 Polygon、NURBS 和 Curve。

UI 中还会显示：

- 当前场景中的 Skin Cluster
- 当前场景中的 Polygon / NURBS / Curve

---

## 第 5 页 - Pose Space Deformer

这一页展示的是 Pose Space Deformer Tool。

作者使用这个工具：

1. 在角色 Pose 状态下以更符合艺术制作的方式进行 Sculpt；
2. 导出已经完成的 Sculpt Data；
3. 在 Auto Rig 重新构建时自动读取这些 PSD Data。

工具使用：

- Python
- PySide
- Maya API

开发。

---

### PSD Tool 功能

1. Create Pose Reader and Connect with Corrective BlendShape  
   创建 Pose Reader，并连接 Corrective BlendShape。

2. Direct Sculpt on Posed Mesh and Bake Difference  
   直接在 Pose 状态的 Mesh 上 Sculpt，然后 Bake Difference。

3. Mirror Pose Space Deformer from One Side to Another  
   把一侧 PSD 镜像到另一侧。

4. Pose Management  
   Pose 管理，包括：

   - 快速访问任意 Pose
   - PSD 创建以后继续调整 Pose
   - 调整 PSD Influence Range
   - Rename PSD
   - 根据关键字过滤 PSD
   - Delete PSD

5. Copy PSD Influence from One Mesh to Another  
   把 PSD Influence 从一个 Mesh 复制到另一个 Mesh。

6. Restore Corrective BlendShape after Target BlendShape is Deleted  
   即使 Target BlendShape 被删除，也可以恢复 Corrective BlendShape。

7. Export and Import PSD Setup  
   导出 / 导入整个 PSD Setup。

---

### UI 中展示的信息

- 当前场景中已经创建的所有 Pose Sculpt
- Keyword Search
- Pose Information and Setting
- Pose Geometry Information and Tool Set

---

## 第 6 页 - Procedure Workflow 最大优势

作者认为 Procedure Method 最大的优势是：

**可以返回到之前的 Rig Building Stage，对 Rig 进行修改或修复，同时不会丢失之前已经完成的工作。**

例如：

可以重新调整 Joint 的位置，然后只需要一次点击，就重新构建整个 Rig。

因为 Skin Weight、PSD 等制作数据已经被保存，所以重新构建 Rig 并不意味着重新做一遍所有艺术数据。

---

### Character Data Sharing

如果两个角色比较相似，还可以在两个角色之间共享数据。

例如：

可以让两个相似角色使用相同的 Skin Weight。

这会节省大量制作时间。

原文最后展示了完整的 Rig Building Workflow。

作者最后再次感谢读者查看他的工作。

---

# 二、从 PDF 中提炼出的核心架构思想

下面开始不再是原文翻译，而是 MuziTools 对资料的架构分析。

## 1. Rig 不应该只保存最终结果

传统思路：

```text
Guide
    ↓
Build
    ↓
Final Rig.ma
```

Procedure Rig 更接近：

```text
Input
    ↓
Guide Data
    ↓
Build Data
    ↓
Skin Data
    ↓
PSD Data
    ↓
Final Rig
```

这里真正重要的是：

**制作过程中的数据也是资产。**

因此 MuziTools 后续不应该把 Skin Weight、Corrective Data、Guide、Controller Custom Data 当成一次 Build 的临时副产品。

---

## 2. Template 应该是 Component 的组合

Human / Angel / Bird / Dog 不应该分别复制一套完整代码。

更合理的是：

```text
Human
├── Spine
├── Neck
├── Arm L
├── Arm R
├── Leg L
├── Leg R
└── ...

Angel
├── Human Components
├── Wing L
└── Wing R
```

因此：

**Template = Component Combination**

而不是：

**Template = 一套独立 Rig Code**

---

## 3. Step 与 Component 不是同一个概念

MuziTools 当前 Face Workflow：

```text
Step 01 Setup
Step 02 Guide
Step 03 Build
Step 04 Finalize
```

这个结构可以继续保留。

但是 Step 03 内部应该由 Component 组成：

```text
Step 03 Build
├── Jaw Component
├── Teeth Component
├── Tongue Component
├── Lip Component
├── Eye Component
├── Eyelid Component
└── Brow Component
```

因此：

```text
Step
    = 用户制作流程

Component
    = 独立绑定模块
```

---

## 4. Component 必须支持 Non-destructive Rebuild

以后每一个正式 Component 都应该围绕：

```text
Collect Input
    ↓
Prepare Data
    ↓
Save Rebuild Data
    ↓
Delete Previous Build Result
    ↓
Build
    ↓
Restore Data
    ↓
Validate
```

设计。

Rebuild 时：

### 保留

```text
config_node
Guide
Model Input
Skin Weight
PSD / Corrective Data
Artist Custom Attribute
External Connection
```

### 可以删除

```text
Component Ctrl
Component Jnt
Component Rig Helper
Matrix / Constraint / Utility DG Node
Component SkinCluster（保存权重成功以后）
```

---

## 5. 每个 Component 应该有明确 Build Ownership

例如 Teeth：

```text
grp_md_teeth_ctrl_001
grp_md_teeth_jnt_001
grp_md_teeth_rig_001
```

Jaw：

```text
grp_md_jaw_ctrl_001
grp_md_jaw_jnt_001
grp_md_jaw_rig_001
```

DAG Build Result 可以通过 Component Group 一次清理。

不能 Parent 到 Group 的 DG Node，则使用 Build Manifest / Message Ownership 管理。

因此删除 Rig 时不应该再使用：

```python
cmds.ls("*teeth*")
```

去猜哪些节点属于 Teeth。

---

## 6. Component 之间通过 Input / Output 连接

模块化不能只是“文件拆开”。

真正的模块化应该做到：

```text
Jaw Component
    ↓
Published Output
    ↓
jaw_ctrl_node
    ↓
Teeth Component Input
```

Teeth 不需要知道 Jaw 内部到底用了：

- parentConstraint
- multMatrix
- blendMatrix
- offsetParentMatrix

它只需要消费 Jaw 发布的 Output。

因此后续 Component 设计应该逐渐形成：

```text
Input
Component
Output
```

边界。

---

## 7. Ctrl Base 对应 Base Rig 中的公共 Controller 能力

当前 MuziTools 的 `systems/ctrl_base.py` 可以被理解为控制器领域的基础层：

```text
Ctrl Creation
Follow
Space Switch
Rebuild Cache
```

而具体 Component：

```text
Jaw
Teeth
Lip
Arm
Leg
```

只负责调用这些基础能力。

这符合“公共能力只实现一次，具体模块组合使用”的方向。

---

# 三、MuziTools 当前建议目标

```text
MuziTools
│
├── Core
│   ├── Joint
│   ├── Matrix
│   ├── Connection
│   ├── Constraint
│   ├── Skin
│   ├── Curve
│   └── ...
│
├── System Base
│   ├── Component Base
│   └── Ctrl Base
│
├── Body Components
│   ├── Spine
│   ├── Neck
│   ├── Arm
│   ├── Leg
│   └── ...
│
├── Face Components
│   ├── Jaw
│   ├── Teeth
│   ├── Tongue
│   ├── Lip
│   ├── Eye
│   ├── Eyelid
│   └── Brow
│
└── Character Template
    ├── Human
    ├── Quadruped
    ├── Winged Human
    └── ...
```

最终目标不是“把很多 Maya 小工具放到一个 Toolbox 中”。

而是建立：

**Component Based Procedural Rigging System**

核心关键词：

```text
Module Based
+
Procedure Build
+
Editable Guide
+
Persistent Config
+
Data Persistence
+
Non-destructive Rebuild
+
Reusable Component
+
Template Composition
```

---

## 结论

林雄这份资料最值得 MuziTools 学习的并不是某个具体 IK、Constraint 或 UI 实现。

真正重要的是：

> Rig 的最终节点只是可重新生成的结果；真正需要长期保存的是制作过程中的数据、模块定义以及模块之间的关系。

因此 MuziTools 后续的设计目标应该是：

```text
Rig Result 可以删除重建
制作数据不能丢
Component 可以独立重建
Component 可以重新组合
角色可以共享制作数据
```

这份原则后续作为 Face Rig、Body Rig、Component Rebuild、Weight System 和 Controller System 的长期架构参考。
