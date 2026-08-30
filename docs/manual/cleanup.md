# 场景清理与模型检查

用于绑定开始前和发布前检查 Maya 场景是否干净、稳定。

<div class="grid cards" markdown>

-   :material-cube-scan:{ .lg .middle } **模型检查**

    ---

    检查模型、Transform、History 和常见发布问题。

    [:octicons-code-24: Model Checker API](../reference/tools/clean/model_checker.md)

-   :material-file-tree-outline:{ .lg .middle } **层级清理**

    ---

    整理 Outliner 和无效层级关系。

    [:octicons-code-24: Hierarchy Cleaner API](../reference/tools/clean/hierarchy_cleaner.md)

-   :material-broom:{ .lg .middle } **场景清理**

    ---

    安全删除明确无用的 Scene Node。

    [:octicons-code-24: Scene Clean API](../reference/core/scene_clean_utils.md)

</div>

## 推荐顺序

```text
模型导入
   ↓
Model Check
   ↓
Hierarchy Check
   ↓
Rig / Animation
   ↓
发布前再次检查
```

1. Rig 开始前先做一次模型检查。
2. 修复命名、Transform、History 和层级问题。
3. 绑定制作过程中只做安全清理。
4. 发布前重新检查整个场景。

!!! warning "不要把清理变成删除一切"
    场景清理应该只处理明确无用的节点。Rig Driver、Constraint、Matrix、Set、Reference 等节点不能因为“不认识”就直接删除。

## 常见问题

**Outliner 很乱**：先整理层级，再删除节点；不要把“看起来多余”和“确实无用”混为一谈。

**删除 History 后 Rig 坏了**：绑定完成后的 Deformer History 往往属于正式 Rig 数据，不应该按建模阶段的规则清除。

## 相关 API

- [model_checker.py](../reference/tools/clean/model_checker.md)
- [hierarchy_cleaner.py](../reference/tools/clean/hierarchy_cleaner.md)
- [model_check_utils.py](../reference/core/model_check_utils.md)
- [scene_clean_utils.py](../reference/core/scene_clean_utils.md)
- [scene_utils.py](../reference/core/scene_utils.md)

[返回常用工具](tools.md){ .md-button }
[打开 Scene Clean API](../reference/core/scene_clean_utils.md){ .md-button .md-button--primary }
