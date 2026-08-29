# Systems API

Systems 是 MuziTools 的完整 Rig Builder / Workflow 层。

当前正式分类：

```text
systems/body/
systems/common/
systems/controller/
systems/face/
```

已知主要方向包括：

```text
Controller Builder / Parent Space Blend
Body / Skirt
Face Setup / Guide
Face Curve Attachment
Eyelid / Eye Bag
Lip / Zip Lip
```

运行：

```bash
python scripts/generate_mkdocs_reference.py
```

后，本页会自动扫描 `systems/**/*.py`，并为当前真实模块生成第一版 Reference。

System 文档除了自动 API 页面外，后续还应该继续补充：

- 节点网络；
- Guide → Rig 数据流；
- Builder 输入 / 输出；
- 重建与删除策略；
- 命名规则；
- Maya 真机测试方式。
