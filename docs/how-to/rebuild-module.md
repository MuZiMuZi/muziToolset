# 安全重建模块

Guide 位置、模块参数或输出结构变化时，使用 Rebuild 更新结果。单纯修改 Controller 颜色、大小或 Joint Radius 时不需要重建。

## 操作步骤

1. 保存当前 Maya 场景的新版本。
2. 回到 Guide 阶段调整 Locator。
3. 检查左右镜像、命名和父级。
4. 对目标模块执行 Rebuild，不删除整套 Face Guide。
5. 重新检查 Joint 与 Controller 对齐。
6. 重新执行 Step 04 Connect。
7. 测试后保存。

| 内容 | Rebuild 处理方式 |
| --- | --- |
| Guide | 保留，继续作为事实来源 |
| 模块 Joint / Controller | 删除旧输出后重新创建 |
| 模块连接 | 重新建立 |
| Face 总组 | 复用，不创建重名层级 |

!!! warning "不要把输出节点当作 Guide"
    Joint 和 Controller 是构建结果。直接移动它们再重建，修改不会成为新的位置来源。

## 重建后检查

- Outliner 中没有带数字后缀的重复模块组。
- Controller 与 Joint 没有跳回旧位置。
- 连接指向新创建的节点。
- 连续执行两次不会增加重复节点。

