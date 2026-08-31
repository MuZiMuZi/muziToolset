# Face PyMEL Migration

当前 Face Rig 正式迁移到 PyMEL-first 架构。

已完成：

- `core/name.py`
- `systems/face/config.py`
- `systems/face/face_config.py`
- `systems/face/face_base.py`
- `systems/face/setup/face_setup.py`
- `resources/face/face_guide.ma`

正在迁移：

1. `guide/face_guide.py`
2. `build/curve_attachment.py`
3. `build/eyelid/builder.py`
4. `build/lip/zip_builder.py`
5. `build/teeth_component.py`
6. `ui/`

规则：

- Maya Node / Attribute / Connection / Parent / Selection 优先直接使用 PyMEL；
- 不恢复旧 `*_utils` Wrapper；
- `core` 只保存项目规则和通用算法；
- 不维护 cmds 架构接口兼容；
- 新代码使用 `upper_teeth` / `lower_teeth` 和 `mouth_joint_count`；
- 正式目录、模块和资源文件统一使用 `snake_case`；
- 函数、方法、普通变量、配置变量全部使用小写 `snake_case`；
- 类名使用 `PascalCase`；
- 项目自定义配置不使用 `UPPER_SNAKE_CASE`。
