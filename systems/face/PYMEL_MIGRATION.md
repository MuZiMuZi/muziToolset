# Face PyMEL Migration

`systems/face/` 是 PyMEL 架构重建后唯一继续保留的现有业务系统。

当前规则：

1. 不为了兼容旧 Face 代码恢复已经归档的 Core / Tool API。
2. Face 代码逐文件迁移到 PyMEL；迁移后的 Maya Node 应优先保存为 PyNode，而不是字符串名称。
3. Joint、Transform、Attribute、Parent、Connection 等基础 Maya 操作直接使用 PyMEL，不再额外制造包装类。
4. 只有真正可复用的项目算法才进入 `core/`。
5. Face Component 继续使用 `ComponentBase / RigComponentBase` 生命周期。
6. 尚未迁移的 Face 文件可能仍包含 `maya.cmds` 或旧 Core Import；这些文件不是兼容目标，而是接下来要替换的迁移对象。

推荐迁移顺序：

```text
FaceBase / Config
        ↓
FaceSetup
        ↓
FaceGuide
        ↓
Build Components
        ↓
Face UI / Workflow
```

迁移期间不要从 `legacy_reference/` import 任何实现。
