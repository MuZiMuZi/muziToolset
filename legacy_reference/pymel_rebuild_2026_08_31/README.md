# PyMEL Rebuild Snapshot — 2026-08-31

这个目录保存 PyMEL-first 架构重建前的正式代码快照。

用途只有两个：

1. 查阅旧工具的业务效果；
2. 未来用新架构重新实现时参考旧算法。

这里不是兼容层，正式代码禁止 import 本目录。

归档内容：

```text
.github/          旧 CI / Docs Workflow
app/              旧应用入口和 ToolBox
core/             旧 cmds-first Core
resources/        旧工具资源
docs/             旧文档
scripts/          旧辅助脚本
tests/            旧测试
tools/            全部旧用户工具，包括旧 Face Tool 外壳
ui/               旧公共 UI 框架
systems/
├─ body/           旧 Body System
├─ controller/     旧 Controller System
├─ component_base.py
└─ __init__.py
root/              重建前的根包文件和文档配置
```

`systems/face/` 没有从正式区移走，因为 Face Rig 是当前唯一继续开发的业务系统。
它会直接迁移到新的 PyMEL-first 架构。
