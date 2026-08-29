# Legacy Integrations

这个目录保存第三方 Rig 系统的历史集成参考。

当前包含：

```text
advanced_skeleton.py
metahuman.py
```

这些文件 **不是正式运行模块**，也不保证可以直接 import 或执行。

它们保留的主要价值是：

- AdvancedSkeleton 特定控制器 / Joint 命名和二次扩展思路；
- MetaHuman Driver Joint 分区、动画导出和控制器重置思路。

旧实现依赖早期 `pipelineUtils / controlUtils / fileUtils` 等架构，因此未来如果重新支持 AdvancedSkeleton 或 MetaHuman，应按当前正式架构重新实现：

```text
systems/
└─ integrations/
   ├─ advanced_skeleton/
   └─ metahuman/
```

正式实现应遵守：

1. 不依赖 `legacy_reference`；
2. 不使用 PyMel；
3. 通用节点、连接、动画、文件能力调用正式 `core/`；
4. 第三方命名和专用 Workflow 留在对应 Integration System；
5. 添加 Maya Functional Smoke Test 后再接入主工具箱。
