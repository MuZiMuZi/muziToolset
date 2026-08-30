# Skin 工作流

这页说明 MuziTools 中 SkinCluster 和权重相关功能的推荐使用方式。

## 什么时候看这页

- 把模型绑定到 Joint；
- 查找 SkinCluster；
- 增加 / 删除 Influence；
- 导出 / 导入权重；
- 调整初始权重；
- 排查模型变形异常。

## 主要入口

UI Tool：

- [skin_tool.py](../reference/tools/skin/skin_tool.md)

底层 API：

- [skin_utils.py](../reference/core/skin_utils.md)
- [mesh_utils.py](../reference/core/mesh_utils.md)
- [transform_utils.py](../reference/core/transform_utils.md)

## 打开 Skin Tool

```python
from muziToolset.tools.skin import skin_tool

window = skin_tool.main()
```

## 推荐流程

```text
完成 Joint
    ↓
检查 Joint Orient / Hierarchy
    ↓
选择模型 + Influence
    ↓
创建 SkinCluster
    ↓
检查初始权重
    ↓
调整 / 镜像 / 导入导出权重
    ↓
做极限 Pose 检查
```

## 创建 SkinCluster 前

建议确认：

1. Joint 数量已经稳定；
2. Joint 名称已经稳定；
3. 模型拓扑不会再大改；
4. 模型 Transform 状态合理；
5. Influence 列表没有漏项；
6. 不需要的临时 Joint 没有混入。

## Tool 与 Core 的边界

```text
skin_tool.py
    选择模型 / Joint
    收集 UI 参数
        ↓
skin_utils.py
    创建 / 查询 / 修改 SkinCluster
```

如果多个工具都需要同一种权重逻辑，应下沉到 `core/skin_utils.py`。

## 查找 SkinCluster

开发时不要仅靠固定节点名猜 SkinCluster。

推荐通过模型历史或 Core API 查询真实 SkinCluster，再继续操作。

具体接口查看：

- [Skin Utils API](../reference/core/skin_utils.md)

## Influence 管理

常见操作：

- 添加 Influence；
- 删除未使用 Influence；
- 查询 Influence；
- 检查锁定权重；
- 保持 Influence 顺序稳定。

修改 Influence 后，应重新检查受影响区域的权重。

## 权重导入导出

权重数据适合用于：

- 角色版本迭代；
- 模型替换；
- 同拓扑模型恢复；
- 自动化测试；
- Rig 发布前备份。

导入前要确认：

```text
模型拓扑是否匹配
Joint / Influence 名称是否匹配
命名空间是否变化
SkinCluster 是否已经存在
```

## 权重镜像

左右角色权重镜像时重点确认：

- 左右 Joint 命名；
- Mirror Plane；
- Influence Association；
- 模型是否处于对称状态。

Face Rig 的局部权重不一定适合简单左右镜像，尤其是非对称扫描模型。

## 变形检查

建议至少测试：

```text
大幅旋转
极限弯曲
肩 / 胯
肘 / 膝
手腕 / 脚腕
面部张嘴 / 闭眼
```

发现问题时先判断属于：

```text
Joint 位置问题
Joint Orient 问题
Skin Weight 问题
Corrective / BlendShape 问题
```

不要把所有问题都通过刷权重硬修。

## Skin 与 Corrective

基础 Skin 无法解决的极限形变，可以进入 BlendShape / Corrective：

- [BlendShape 工作流](blendshape.md)
- [blendshape_utils.py](../reference/core/blendshape_utils.md)

## 常见问题

### 找不到 SkinCluster

先检查模型是否真正绑定，以及查询的是 Transform 还是 Shape。

### 导入权重后完全不对

优先检查拓扑、Influence 名称和 Joint Namespace，而不是立即重新刷一遍。

### 一个 Joint 没有效果

检查：

1. 是否真的属于 SkinCluster Influence；
2. 权重是否全为 0；
3. Influence 是否被锁定；
4. Joint 是否被错误替换或重命名。

## 继续查看

- [Joint 工作流](joint.md)
- [BlendShape 工作流](blendshape.md)
- [Skin Utils API](../reference/core/skin_utils.md)
