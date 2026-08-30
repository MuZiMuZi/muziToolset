# BlendShape 工作流

这页说明 MuziTools 中 BlendShape、修型和 Corrective 的推荐使用方式。

## 什么时候看这页

- 添加 BlendShape Target；
- 创建表情目标；
- 处理 Corrective Shape；
- 反算 / Invert Shape；
- 管理 BlendShape 权重；
- 排查 Target 顺序和驱动问题。

## 主要入口

UI Tool：

- [add_blendshape_tool.py](../reference/tools/blendshape/add_blendshape_tool.md)
- [invert_shape_tool.py](../reference/tools/blendshape/invert_shape_tool.md)

底层 API：

- [blendshape_utils.py](../reference/core/blendshape_utils.md)

## 添加 BlendShape Target

常见流程：

```text
准备 Base Mesh
    ↓
准备 Target Mesh
    ↓
检查拓扑一致
    ↓
添加到 BlendShape
    ↓
确认 Target Alias
    ↓
测试 Weight 0 → 1
```

如果是正式 Face Rig，建议统一由 Builder 管理 Target 命名和驱动关系，而不是手动堆大量匿名 Target。

## 打开 Add BlendShape Tool

```python
from muziToolset.tools.blendshape import add_blendshape_tool

window = add_blendshape_tool.main()
```

## Invert Shape

入口：

```text
tools/blendshape/invert_shape_tool.py
```

适合 Corrective 工作流中把最终姿态修型反算回可驱动的 Shape。

打开：

```python
from muziToolset.tools.blendshape import invert_shape_tool

window = invert_shape_tool.main()
```

具体输入对象顺序和参数请查看 API 页面。

## BlendShape 在 Rig 中的位置

推荐理解为：

```text
Joint / Skin
    ↓
基础变形
    ↓
BlendShape / Corrective
    ↓
最终模型输出
```

但实际 Deformer Order 要根据具体系统确认，不能只依赖默认创建顺序。

## Corrective

Corrective 适合解决：

- 肘 / 膝极限弯曲；
- 肩部塌陷；
- 面部嘴角 / 鼻翼 / 眼皮耦合；
- 多轴组合 Pose。

推荐把 Corrective 的“生成方式”和“驱动方式”分开考虑：

```text
Shape 怎么得到
    ↓
谁来驱动 Shape Weight
```

后续可以使用：

- Set Driven Key；
- Matrix / Remap；
- Pose Driver；
- RBF。

## Face Rig

Face 系统里 BlendShape 不应该替代全部 Joint Rig。

推荐：

```text
Joint / Curve
    负责主要结构和连续运动

BlendShape
    负责表情目标和 Corrective
```

这样既保留可程序化结构，也能得到高质量局部修型。

## Target 命名

建议 Target 名称带明确语义：

```text
bs_lf_mouth_smile_001
bs_rt_brow_up_001
bs_md_jaw_open_corrective_001
```

不要长期保留：

```text
target1
target2
pCube23
```

## 常见问题

### Target 加进去了但模型不动

检查：

1. Weight 是否真的变成 1；
2. Target 是否和 Base Mesh 拓扑一致；
3. BlendShape 是否作用在正确 Shape；
4. Deformer Order 是否导致结果被后续节点覆盖。

### Invert 后 Shape 很奇怪

确认输入 Pose、Base、Deformed Mesh 是否是工具要求的对应关系，并检查模型拓扑是否变化。

### Corrective 很多以后难维护

将 Target 命名、驱动来源和用途写入统一 Config / Builder，不要只依赖 Shape 名称猜用途。

## 继续查看

- [Skin 工作流](skin.md)
- [Face Guide](face-guide.md)
- [BlendShape Utils API](../reference/core/blendshape_utils.md)
