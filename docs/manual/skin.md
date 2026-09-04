# Skin

用于管理 SkinCluster、Influence 和权重数据。

<div class="grid cards" markdown>

-   :material-link-variant:{ .lg .middle } **绑定模型**

    ---

    创建 SkinCluster，并确认 Jnt Influence。

    [:octicons-code-24: Skin Tool API](../reference/tools/skin/skin_tool.md)

-   :material-account-multiple-outline:{ .lg .middle } **管理 Influence**

    ---

    查询、添加和整理 SkinCluster Influence。

    [:octicons-code-24: Skin Utils API](../reference/core/skin_utils.md)

-   :material-database-arrow-left-outline:{ .lg .middle } **权重数据**

    ---

    查询、导入、导出和恢复权重。

    [:octicons-code-24: Skin Utils API](../reference/core/skin_utils.md)

</div>

## 推荐步骤

1. 确认模型拓扑和 Skeleton 已稳定。
2. 创建 SkinCluster。
3. 检查 Influence 是否完整。
4. 调整和验证权重。
5. 在大改模型或骨骼前先保存权重数据。

```text
Model + Skeleton
       ↓
   SkinCluster
       ↓
   Influence
       ↓
    Weight
       ↓
Deformation Check
```

!!! tip "修改前先保存"
    需要重建 SkinCluster、改 Jnt 层级或调整模型时，先导出权重数据，避免不可逆地丢失当前结果。

## 常见问题

**模型没有正确变形**：先检查 SkinCluster、Influence 和 Jnt 层级，再检查局部权重。

**新增 Jnt 不起作用**：确认它已经进入 SkinCluster Influence，而不是只存在于 Skeleton 中。

**权重导入结果异常**：检查模型拓扑、Vertex 数量和目标 Influence 名称是否与保存时一致。

## 相关 API

- [skin_tool.py](../reference/tools/skin/skin_tool.md)
- [skin_utils.py](../reference/core/skin_utils.md)
- [jnt_utils.py](../reference/core/jnt_utils.md)
- [mesh_utils.py](../reference/core/mesh_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 Skin Utils API](../reference/core/skin_utils.md){ .md-button .md-button--primary }
