# Face Bind Legacy Reference — 2026-09-03

这是 Face Rig Step 03 绑定系统的只读参考快照。

## 来源

- Source commit: `03eaf19455fb5f59994451ba34c7d8ae4e3ba117`
- 状态：Controller / Guide 对齐修复完成之后、Controller Appearance Workflow 重构之前。
- 目的：保留此前 Brow / Eye / Eyelid / Nose / Cheek / Ear / Jaw / Teeth / Tongue / Lip / Mouth 的绑定实现，方便后续查看算法、节点结构和构建思路。

## 重要说明

这里的文件 **不属于当前 Runtime**，正式代码不得从 `legacy_reference` Import。

当前生产版本继续以 `systems/face/` 为唯一正式实现；本目录只用于阅读、对照和恢复历史实现思路。

## 目录

- `build/`：旧版 Step 03 Workflow、Curve Attachment、Eyelid Builder、Zip Lip Builder。
- `modules/`：旧版 11 个 Face Module 与 FaceRig Orchestrator。
- `config.py` / `face_base.py`：该快照对应的 Face 基础配置和公共基类。
