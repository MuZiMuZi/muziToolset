# Face PyMEL Migration

Face Rig 正式运行代码已经完成 PyMEL-first 架构迁移。

已迁移：

```text
core/name.py
core/control.py
core/curve.py
core/undo.py
systems/face/config.py
systems/face/face_config.py
systems/face/face_base.py
systems/face/setup/face_setup.py
systems/face/guide/face_guide.py
systems/face/build/face_build.py
systems/face/build/teeth_component.py
systems/face/build/curve_attachment.py
systems/face/build/eyelid/builder.py
systems/face/build/lip/zip_builder.py
systems/face/finalize/face_finalize.py
systems/face/ui/face_rig_ui.py
systems/face/ui/workflow_controller.py
```

规则：正式 Maya Scene 操作使用 PyMEL；正式代码不使用 `maya.cmds`；几何计算需要时允许 `maya.api.OpenMaya`；不恢复旧 `*_utils` Wrapper；Maya Node 在业务层优先保存为 PyNode；Schema 使用 `upper_teeth_model` / `lower_teeth_model` / `mouth_joint_count`；自定义变量统一 snake_case 小写；不维护 cmds 接口兼容。

历史 cmds 架构固定保存在 `cmds-archive-2026-08-31`，其它历史参考代码保存在 `legacy_reference/`。
