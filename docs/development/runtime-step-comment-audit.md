# Runtime 中文步骤注释审计

> 本文件由 `scripts/audit_runtime_step_comments.py` 自动生成。

扫描 Runtime Python 文件：**104**

需要补充步骤注释的复杂函数：**18**

## `systems/face/modules/brow.py`

- `BrowModule.load_setup` — L64，51 行，控制流 2，Call 9
- `BrowModule.create_ctrl` — L191，79 行，控制流 2，Call 9
- `BrowModule.create_connect` — L275，54 行，控制流 3，Call 9
- `BrowModule.create_deform` — L334，152 行，控制流 3，Call 23
## `systems/face/modules/cheek.py`

- `CheekModule.create_finalize` — L220，29 行，控制流 5，Call 3
## `systems/face/modules/eye.py`

- `EyeModule.create_ctrl` — L147，86 行，控制流 3，Call 10
## `systems/face/modules/eyelid.py`

- `EyelidModule.load_setup` — L58，83 行，控制流 2，Call 15
- `EyelidModule.create_jnt` — L164，114 行，控制流 3，Call 22
- `EyelidModule.create_deform` — L357，201 行，控制流 5，Call 29
## `systems/face/modules/jaw.py`

- `JawModule.__init__` — L63，54 行，控制流 0，Call 3
## `systems/face/modules/lip.py`

- `LipModule.create_jnt` — L116，157 行，控制流 4，Call 29
- `LipModule.create_deform` — L336，47 行，控制流 3，Call 7
## `systems/face/modules/nose.py`

- `NoseModule.load_guide` — L88，35 行，控制流 6，Call 8
- `NoseModule.create_jnt` — L124，67 行，控制流 4，Call 13
- `NoseModule.create_ctrl` — L192，69 行，控制流 4，Call 11
## `systems/face/modules/teeth.py`

- `TeethModule.__init__` — L60，49 行，控制流 0，Call 3
- `TeethModule._validate_build_nodes_available` — L552，44 行，控制流 5，Call 5
- `TeethModule._create_rigid_skin_cluster` — L618，54 行，控制流 3，Call 6
