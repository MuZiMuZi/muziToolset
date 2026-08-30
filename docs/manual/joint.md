# Joint

用于创建、整理和重采样绑定骨骼。

<div class="grid cards" markdown>

-   :material-bone:{ .lg .middle } **创建 Joint**

    ---

    创建单个 Joint、Joint Chain 和基础骨骼结构。

    [:octicons-code-24: Joint Tool API](../reference/tools/joint/joint_tool.md)

-   :material-ruler-square:{ .lg .middle } **重采样 Joint**

    ---

    调整骨骼数量，并重新分布位置。

    [:octicons-code-24: Resample Tool API](../reference/tools/joint/joint_resamp_tool.md)

-   :material-vector-line:{ .lg .middle } **沿 Curve 分布**

    ---

    根据 Curve / Position 数据创建稳定 Joint Chain。

    [:octicons-code-24: Joint Utils API](../reference/core/joint_utils.md)

</div>

## 打开工具

```python
from muziToolset.tools.joint import joint_tool

window = joint_tool.main()
```

## 推荐步骤

1. 先确认骨骼用途和数量。
2. 创建或重采样 Joint。
3. 检查父子层级和 Joint Orient。
4. 确认骨骼名称符合 Rig 命名规则。
5. 再进入 Controller 和 Skin 阶段。

```text
位置
  ↓
Joint Chain
  ↓
Orient
  ↓
Naming
  ↓
Controller / Skin
```

!!! warning "Joint Orient"
    不要只看 Rotate 是否为 0。正式 Skeleton 更应该检查 Joint Orient、局部轴方向和父子空间是否符合后续 Rig 计算。

## 常见问题

**Joint 数量改了但间距不均匀**：使用重采样工具或 Curve 参数化方法，不要只在世界空间里平均 Translate。

**左右骨骼方向不一致**：检查镜像方式、主轴和 Joint Orient，而不是只修 Rotate 数值。

## 相关 API

- [joint_tool.py](../reference/tools/joint/joint_tool.md)
- [joint_resamp_tool.py](../reference/tools/joint/joint_resamp_tool.md)
- [joint_utils.py](../reference/core/joint_utils.md)
- [transform_utils.py](../reference/core/transform_utils.md)
- [curve_utils.py](../reference/core/curve_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 Joint Utils API](../reference/core/joint_utils.md){ .md-button .md-button--primary }
