# BlendShape

入口：主工具箱 → **BlendShape 工具 → BlendShape Target**。

```python
from muziToolset.tools.blendshape import add_blendshape_tool
window = add_blendshape_tool.main()
```

底层实现位于 `core/deformation/`，使用 `maya.cmds`，不需要 PyMEL。

## 添加与管理普通 Target

1. 选中 BS 节点或带 BS 的模型，点击“从选择获取”。
2. 选择一个或多个 Target Mesh，点击“添加 / 同名替换 Target”。
3. 使用“刷新”查看真实 Weight Index，或使用“复制所有 Target Mesh”烘焙目标。

普通添加的同名替换行为与反算添加不同：反算添加只创建新 Target，名称冲突时停止。

## 添加反算修型 Target

1. 把控制器摆到需要修型的姿势，用拓扑一致的模型完成雕刻修型。
2. 在窗口顶部载入已有 BS 节点；在“反算修型 → 添加 BS Target”区域载入驱动控制器。
3. 可填写新 Target 名称。留空时自动生成不冲突的名称。
4. 在场景中先选择**修型 Mesh**，再选择**基础 Mesh**，共两个模型。
5. 点击“添加反算 Target”。

处理顺序：保存姿态和 envelope → 冻结雕刻快照 → 暂时关闭该 BS → invertShape → 烘焙反算模型 → 控制器 TR 归零 → 添加新 Target → 恢复原姿态和 envelope → 清理临时模型。

成功后，新 Target 的权重为 **0**。工具不自动建立控制器到 Weight 的驱动关系；请根据绑定方案自行连接或设置 Driven Key。

输入要求：

- 基础和修型是不同的 Mesh，且各自只有一个可见 Mesh Shape。
- 顶点、边、面数量，以及面的顶点索引必须一致。
- BS 当前只作用于指定的基础模型。
- 控制器六个 Translate / Rotate 通道、BS envelope 未锁定且没有输入连接。
- Maya Undo 已启用；失败会尝试撤销本次操作。

恢复使用原 envelope 数值，不会固定设为 1。控制器 Scale 不会归零。变形器堆栈对 invertShape 的支持需在实际 Maya 场景中验证。

## 整理左右复制 Target 名称

载入 BS 后点击“重命名 lf_*_Copy → rt_*”。

| 原 Alias | 新 Alias |
|---|---|
| `lf_smile_Copy` | `rt_smile` |
| `lf_brow_lf_detail_Copy` | `rt_brow_lf_detail` |
| `lf_smile` | 不变 |
| `md_smile_Copy` | 不变 |

只替换名称开头 `lf_` 和结尾 `_Copy`；中间文本保留。按真实 `weight[index]` 修改 Alias，不依赖列表位置，支持删除 Target 后的稀疏索引。新名称冲突时，整批停止。

此按钮只改名称，不镜像几何、不更改权重值，也不改变驱动连接。

## 独立反算窗口

原有独立 Invert Shape 工具仍可用于批量生成反算模型，不会自动添加到 BS：

```python
from muziToolset.tools.blendshape import invert_shape_tool
window = invert_shape_tool.main()
```

## 验证范围

自动测试验证索引、冲突、状态恢复、失败回滚以及真实 Qt 按钮调用。测试使用 Maya 命令桩，不验证 invertShape 的数学结果；最终需要在 Maya 2023 中用真实模型测试。

命令参考：[BlendShape](https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/blendShape.html)、[aliasAttr](https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/CommandsPython/aliasAttr.html)。
