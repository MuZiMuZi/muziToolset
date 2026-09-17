# 检查与发布

## 场景

- [ ] 删除测试模型、临时节点和未知节点。
- [ ] 模型、Guide、Joint、Controller 分层清楚。
- [ ] 没有意外重名或自动数字后缀。
- [ ] 保存、关闭并重新打开无报错。

## 绑定

- [ ] 左右模块位置和轴向正确。
- [ ] Controller 只开放动画需要的属性。
- [ ] Joint Local Axis 和父子关系正确。
- [ ] Eye Aim、Main Controller 与最终 Joint 响应正确。
- [ ] 重复 Build / Connect 不会生成额外节点。

## 发布

1. 保存最后一个可编辑工作版本。
2. 运行 Model Check 与 Hierarchy Clean。
3. 创建新的发布文件。
4. 记录 MuziTools、Maya 版本和已构建模块。
5. 用简单动画片段验证发布文件。

