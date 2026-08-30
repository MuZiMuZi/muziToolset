# Joint 工作流

这页说明 MuziTools 中 Joint 的常用操作、推荐顺序以及对应 API。

## 什么时候看这页

- 创建 Joint / Joint Chain；
- 根据选择快速生成骨骼；
- 重采样 Joint 数量；
- 沿 Curve 或已有 Joint 分布骨骼；
- 调整 Joint Orientation；
- 为 Controller / Skin 准备正式 Skeleton。

## 主要入口

UI Tool：

- [joint_tool.py](../reference/tools/joint/joint_tool.md)
- [joint_resamp_tool.py](../reference/tools/joint/joint_resamp_tool.md)

底层 API：

- [joint_utils.py](../reference/core/joint_utils.md)
- [transform_utils.py](../reference/core/transform_utils.md)
- [curve_utils.py](../reference/core/curve_utils.md)

## 打开 Joint Tool

```python
from muziToolset.tools.joint import joint_tool

window = joint_tool.main()
```

具体窗口类和公开方法以 API 页面为准。

## 推荐制作顺序

```text
确定关节数量和位置
    ↓
创建 Joint / Joint Chain
    ↓
检查 Parent Hierarchy
    ↓
处理 Joint Orient
    ↓
统一命名
    ↓
进入 Controller / Skin
```

## 创建 Joint

如果只是一次简单场景操作，可以直接使用 Core API。

复杂工具则应该：

```text
Tool UI
    ↓
joint_utils
    ↓
Maya Joint
```

这样 Joint 算法不会被重复写到多个窗口里。

## Joint Chain

创建 Joint Chain 时重点确认：

- 输入点顺序；
- Parent 顺序；
- Start / End 是否包含；
- Joint Radius；
- Orientation 策略；
- 是否需要自动命名。

不要在后续 Skin 阶段才发现 Joint 顺序反了。

## Joint 重采样

入口：

```text
tools/joint/joint_resamp_tool.py
```

适合：

- 原 Joint 数量太少；
- Ribbon / Tail / Tentacle 需要均匀分布；
- 根据已有 Joint 重新生成更密的链；
- 希望保持 Start / End 位置不变。

打开：

```python
from muziToolset.tools.joint import joint_resamp_tool

window = joint_resamp_tool.main()
```

## 沿 Curve 创建 / 分布 Joint

Curve 驱动类 Rig 建议统一使用：

- [curve_utils.py](../reference/core/curve_utils.md)
- [joint_utils.py](../reference/core/joint_utils.md)

常见流程：

```text
Curve
    ↓
Parameter / Arc Length
    ↓
World Position
    ↓
Joint
```

如果要保证均匀分布，应区分“参数均匀”和“弧长均匀”。

## Joint Orient

Joint Orientation 不是普通 Rotate。

修改前应该明确：

```text
jointOrient
rotate
rotateAxis
parent orientation
```

分别扮演什么角色。

用于正式 Deform Skeleton 时，建议在 Controller 和 Skin 之前把 Orientation 定下来。

## 命名

项目推荐五段式 Rig 命名：

```text
[类型]_[方向]_[部位]_[功能]_[序号]
```

示例：

```text
jnt_lf_arm_bind_001
jnt_rt_brow_bind_003
jnt_md_jaw_bind_001
```

命名 API：

- [name_utils.py](../reference/core/name_utils.md)

## Controller 关系

Joint 完成后再进入 Controller：

```text
Joint
    ↓
Controller Builder
    ↓
Constraint / Matrix
    ↓
Deform Joint
```

标准 Controller 请看：[Controller 工作流](controller.md)。

## Skin 前检查

进入 Skin 之前建议确认：

1. Joint 名称正确；
2. Parent Hierarchy 正确；
3. Joint Orient 正确；
4. 没有意外 Scale；
5. Joint 数量已经确定；
6. 不再需要大规模改骨架结构。

## 常见问题

### 重采样后 Joint 方向乱了

先确认工具是只重建位置，还是同时重建 Orientation。位置采样和 Joint Orient 是两个不同步骤。

### Joint 数量正确但分布不均匀

检查使用的是 Curve Parameter 还是 Arc Length Percentage。

### Skin 后才想改 Joint 数量

可以改，但会增加 Skin 权重迁移成本。正式流程更推荐先定骨架，再 Skin。

## 继续查看

- [Controller 工作流](controller.md)
- [Skin 工作流](skin.md)
- [Joint Utils API](../reference/core/joint_utils.md)
