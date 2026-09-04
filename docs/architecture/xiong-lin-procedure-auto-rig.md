# 林雄《Rig Build Description》中文译文与架构参考

> 原作者：Xiong Lin（林雄）  
> 原文标题：Rig Build Description  
> 文档用途：MuziTools Module Based Procedural Rig 架构研究参考  
> 翻译说明：第一部分按原 PDF 内容翻译；第二部分开始是 MuziTools 自身的架构结论，不属于原文。

!!! note "术语说明"
    外部资料和视频原名中的 **Component Based** 保留原始标题，不做改写。MuziTools 0.4 正式代码和项目架构统一使用 **Module**，不再使用 Component 表示完整 Rig 业务单元。

---

## 参考资料

- PDF：Rig Build Description - Xiong Lin
- Bilibili：Component Based Procedure Auto Rig  
  __MUZI_MAYA_JNT_PROTECTED_00000__
- Bilibili：Maya绑定和动画工具展示  
  __MUZI_MAYA_JNT_PROTECTED_00001__

这两段视频和 PDF 作为 MuziTools 程序化绑定系统的架构参考资料。

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

### 为什么叫 Jigsaw

因为整个系统是基于模块构建的，所以我把这套 Auto Rig 称为 **Jigsaw**。

它有点像拼图。不同的 Rig Module 可以组合成不同类型的生物角色。

例如，一个基础人类角色可以由：

- 2 个 Arm Rig
- 2 个 Leg Rig
- 2 个 Hand Rig
- 1 个 Torso Rig
- 1 个 Neck Rig

组成；再加入 2 个 Wing Rig，就可以构建 Angel Character。

系统预先准备了不同 Rig Module 组合模板，例如：

- Angel
- Bat
- Bird
- Dog
- Human
- Dragon
- Tiger Hawk

### UI 中展示的主要区域

原图中的界面包含：

- **Rig Module Library**：Rig 模块库；
- **Building Workflow**：绑定构建工作流；
- **Rig Module Setting**：当前 Module 设置；
- **Rig Module Current In Use**：当前角色正在使用的 Module；
- **Rig Module Preset**：Module 预设组合；
- **Version Control**：版本控制；
- **Asset Management**：资产管理。

---

## 第 2 页 - Rig Module Preset

这一页展示系统预设的角色模板，包括：

- Human Template
- Angel Template
- Bat Template
- Bird Template
- Dog Template
- Quad Dragon Template
- Face Template

这些模板不是彼此完全独立的 Rig 系统，而是不同 Rig Module 的组合方案，因此同一个 Rig Module 可以被多个角色 Template 重复使用。

---

## 第 3 页 - Base Rig 与模块继承

整个系统一共有 **21 个可以用于实际制作的 Rig Module**。

所有模块使用 Python 和 Object-Oriented Programming 开发。

作者首先创建基础 Rig Class：**Base Rig**。

Base Rig 保存所有 Rig Module 都需要的公共信息和功能，例如：

- Naming Convention
- Connection Method

之后其它 Rig Module 从 Base Rig 继承，并逐渐扩展为更复杂的生产模块。

```text
Base Rig
    ↓
Basic Rig Module
    ↓
More Specialized Rig Module
    ↓
Final Production Rig Module
```

公共逻辑只实现一次，具体角色 Module 只增加自己真正需要的绑定能力。

### Limb Rig 已开发功能

作者列出的 Limb Rig 功能包括：

1. IK / FK Switch；
2. IK Control Auto Stretch；
3. Soft IK；
4. Elbow Offset / Lock；
5. Limb Squeeze and Squash；
6. Local Scale；
7. IK Control Space Switch；
8. FK Control Rotation Space Switch；
9. FK / IK 两种模式下的 Limb Length Adjust；
10. Bendy Control。

这些能力继续被 Arm、Bird Wing、Bat Wing、Leg、Hind Leg、Fore Leg 等具体 Module 继承。

---

## 第 4 页 - Procedure Workflow 与 Skin Weight

作者的 Auto Rig 使用 **Procedure Workflow（程序化制作流程）**。

系统保存的不只是最终 Rig 文件，还保存 **Rig Building Progress**。

主要保存的制作数据包括：

- Skin Weights
- Pose Space Deformer（PSD）

### Skin Weight Tool

Skin Weight Tool 可以导出和导入权重数据，并在 Auto Rig 重建时自动恢复。

主要能力包括：

1. High Speed Data Transfer；
2. 每个 Skin Weight 独立导出 / 导入；
3. 多个 Skin Weight 合并到单一文件；
4. 支持 Polygon、NURBS 和 Curve。

---

## 第 5 页 - Pose Space Deformer

作者使用 Pose Space Deformer Tool：

1. 在角色 Pose 状态下 Sculpt；
2. 导出 Sculpt Data；
3. Auto Rig 重建时恢复 PSD Data。

工具使用 Python、PySide 和 Maya API 开发。

主要能力包括：

- Pose Reader + Corrective BlendShape；
- Pose Mesh 直接 Sculpt + Bake Difference；
- PSD Mirror；
- Pose Management；
- PSD Influence Copy；
- Corrective 恢复；
- PSD Setup Export / Import。

---

## 第 6 页 - Procedure Workflow 最大优势

作者认为 Procedure Method 最大的优势是：

**可以返回之前的 Rig Building Stage 修改或修复，同时不丢失已经完成的制作数据。**

例如重新调整 Jnt 位置后，可以重新 Build Rig，而 Skin Weight、PSD 等艺术数据会被恢复。

相似角色之间还可以共享 Skin Weight 等 Character Data，从而节省大量制作时间。

---

# 二、MuziTools 从资料中提炼的架构原则

以下内容是 MuziTools 自身结论，不属于原文。

## 1. Rig Result 是可重建结果，制作数据才是长期资产

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

需要长期保存的是：

- Guide；
- Config；
- Skin Weight；
- PSD / Corrective；
- Artist Custom Data；
- Module 之间的关系。

最终 Maya Rig Nodes 应尽量做到可以删除并重建。

---

## 2. Template 应该是 Module 的组合

```text
Human
├── SpineModule
├── NeckModule
├── ArmModule L
├── ArmModule R
├── LegModule L
└── LegModule R

Angel
├── Human Modules
├── WingModule L
└── WingModule R
```

因此：

```text
Template = Module Combination
```

而不是每一种角色复制一套独立 Rig Code。

---

## 3. Step 与 Module 不是同一个概念

MuziTools Face Workflow：

```text
Step 01 Setup
Step 02 Guide
Step 03 Build
Step 04 Finalize
```

Step 03 内部由完整 Rig Module 组成：

```text
Step 03 Build
├── JawModule
├── TeethModule
├── TongueModule
├── LipModule
├── EyeModule
├── EyelidModule
└── BrowModule
```

定义：

```text
Step
    用户制作流程阶段

Module
    可独立构建、验证和重新构建的完整 Rig 业务单元
```

---

## 4. Module Lifecycle

MuziTools 0.4 使用：

```text
systems/module_base.py
```

标准生命周期：

```text
collect_inputs()
      ↓
prepare_data()
      ↓
process_data()
      ↓
finalize_step()
```

真正的 Rig Module 使用 `RigModuleBase`：

```text
create_jnt()
      ↓
create_controller()
      ↓
create_connection()
```

未来 Non-destructive Rebuild 可以继续在这个生命周期上增加 Build Manifest、Data Cache 和 Restore 机制，而不是重新创造第二套 Module Protocol。

---

## 5. 每个 Module 应该有明确 Build Ownership

Module 创建的 DAG / DG Node 应可被明确识别和清理。

不要使用：

```python
cmds.ls("*teeth*")
```

猜测节点归属。

更合理的是：

```text
Module Public Result
+
Config Message
+
Build Manifest / Ownership
```

后续用它支持安全 Rebuild。

---

## 6. Module 之间通过 Public Input / Output 协作

```text
JawModule
    ↓
Published Output
    ↓
TeethModule Input
```

TeethModule 不需要知道 JawModule 内部用了：

- parentConstraint；
- multMatrix；
- blendMatrix；
- offsetParentMatrix。

它只消费 JawModule 发布的稳定 Output。

因此模块化的重点不是“多几个 Python 文件”，而是清晰的：

```text
Input
Module
Output
```

边界。

---

## 7. RigBase / ModuleBase / CtrlBase 对应公共 Rig 基础层

MuziTools 0.4 当前基础结构：

```text
systems/
├── rig_base.py
├── module_base.py
└── ctrl_base.py
```

职责：

```text
RigBase
    Rig Naming

ModuleBase / RigModuleBase
    Module Lifecycle

CtrlBase
    Controller Creation / FK / Follow / Space
```

具体 Module：

```text
JawModule
TeethModule
LipModule
ArmModule
LegModule
```

只组合这些基础能力，不重复实现公共规则。

---

# 三、MuziTools 当前目标结构

```text
MuziTools
│
├── Core
│   ├── Jnt
│   ├── Matrix
│   ├── Connection
│   ├── Constraint
│   ├── Skin
│   ├── Curve
│   └── ...
│
├── System Base
│   ├── RigBase
│   ├── ModuleBase / RigModuleBase
│   └── CtrlBase
│
├── Body Modules
│   ├── SpineModule
│   ├── NeckModule
│   ├── ArmModule
│   ├── LegModule
│   └── ...
│
├── Face Modules
│   ├── JawModule
│   ├── TeethModule
│   ├── TongueModule
│   ├── LipModule
│   ├── EyeModule
│   ├── EyelidModule
│   └── BrowModule
│
└── Character Template
    ├── Human
    ├── Quadruped
    ├── Winged Human
    └── ...
```

最终目标不是“把很多 Maya 小工具放到一个 Toolbox 中”，而是建立可维护的 **Module Based Procedural Rigging System**。

核心关键词：

```text
Module Based
+
Procedural Build
+
Editable Guide
+
Persistent Config
+
Data Persistence
+
Non-destructive Rebuild
+
Reusable Module
+
Template Composition
```

---

# 结论

这份资料最值得 MuziTools 学习的不是某个具体 IK、Constraint 或 UI 实现，而是：

> Rig 的最终节点只是可重新生成的结果；真正需要长期保存的是制作过程数据、Module 定义以及 Module 之间的关系。

因此后续设计目标是：

```text
Rig Result 可以删除重建
制作数据不能丢
Module 可以独立重建
Module 可以重新组合
角色可以共享制作数据
```

这套原则作为 Face Rig、Body Rig、Module Rebuild、Weight System 和 Controller System 的长期架构参考。
