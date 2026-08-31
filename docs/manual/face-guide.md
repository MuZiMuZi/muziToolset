# Face Guide

`FaceGuide` 是 Face Rig 的 **Step 02 定位和 Guide 操作入口**。

进入 Step 02 时，UI 会自动导入或复用 `resources/face/face_guide.ma`。绑定师主要负责摆放 Locator、镜像、修复模板和设置后续 Controller 参数。

## 标准流程

```text
Step 01 Setup 完成
        ↓
进入 Step 02 Guide
        ↓
自动导入 / 复用 face_guide.ma
        ↓
手动调整 Locator
        ↓
需要时 LF ↔ RT Mirror
        ↓
设置 Controller Size / Color
        ↓
点击“下一步”
        ↓
检查模板中的全部 Locator
        ↓
完整 → 保存 Config → 进入 Step 03
缺失 → 阻止继续并列出缺失名称
```

## 当前代码结构

Guide 当前故意保持简单：

```text
systems/face/guide/
├── __init__.py
└── face_guide.py
```

Template、Mirror、Repair 不再分别拆成多个 Python 文件。

固定名称、默认 Controller 参数和 Step Visibility Rule 统一定义在：

```text
systems/face/config.py
```

执行逻辑统一由：

```text
systems/face/guide/face_guide.py
```

负责。

## 名称生成

Guide / Joint / Controller 等标准节点名称不要重复硬编码。

统一使用：

```python
from muziToolset.core import name_utils

name = name_utils.Name.create_name(
    node_type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)
```

结果：

```text
loc_md_upper_teeth_guide_001
```

左右镜像名称统一使用：

```python
mirror_name = name_utils.Name.mirror_name(
    "loc_lf_eye_ball_guide_001"
)
```

结果：

```text
loc_rt_eye_ball_guide_001
```

## Guide 查询

### 查询一个明确 Guide

```python
from muziToolset.core import name_utils
from muziToolset.systems.face import FaceGuide

face_guide = FaceGuide()

guide_name = name_utils.Name.create_name(
    node_type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)

upper_teeth_guide = face_guide.get_guide_node(
    guide_name,
    required=True
)
```

### 查询一个部位

例如 Tongue：

```python
tongue_guides = face_guide.get_part_guides(
    part="tongue"
)
```

例如左侧 Brow：

```python
lf_brow_guides = face_guide.get_part_guides(
    part="brow",
    side="lf"
)
```

不要再额外创建这种没有新增逻辑的方法：

```python
def get_tongue_guides(self):
    return self.get_part_guides(
        part="tongue"
    )
```

只有真正增加固定顺序、结构化结果或特殊校验的方法才值得保留。

## 自动加载 Guide

UI 进入 Step 02 时自动调用：

```python
face_guide.build_guide()
```

如果 Guide 已经存在，就直接复用；不存在时导入：

```text
resources/face/face_guide.ma
```

## 重新导入模板

用于绑定过程中误删 Locator，但又不想丢掉其它已经调整好的位置。

```python
result = face_guide.reimport_guide()
```

流程：

```text
记录当前仍存在 Locator 世界矩阵
        ↓
删除当前模板内容
        ↓
重新导入 face_guide.ma
        ↓
恢复原来仍存在 Locator 的位置
        ↓
被误删 Locator 使用模板默认位置
```

## Guide Mirror

直接调用 `FaceGuide`：

```python
result = face_guide.mirror_guides(
    source_side="lf",
    target_side="rt"
)
```

或者：

```python
result = face_guide.mirror_guides(
    source_side="rt",
    target_side="lf"
)
```

Mirror：

- 只复制当前状态；
- 不建立永久左右连接；
- `md` Guide 不参与；
- 使用 `name_utils.Name.mirror_name()` 获取目标名称；
- 支持 Maya Undo Chunk；
- UI 额外保存最近一次 Mirror Snapshot。

如果目标 Guide 被误删，Mirror 不负责创建新节点，应先使用“重新导入模板”修复。

## 撤销最近一次 Mirror

```python
result = face_guide.undo_mirror(
    snapshot
)
```

UI 会自动保存最近一次 `mirror_guides()` 返回的 `snapshot`。

也可以直接使用 Maya：

```text
Ctrl + Z
```

## 完整性检查

`face_guide.ma` 仍然是 Locator 完整性的最终来源。

```python
validation = face_guide.validate_guides()

print(validation["valid"])
print(validation["missing_guide_names"])
print(validation["guide_count"])
print(validation["template_guide_count"])
```

任意模板 Locator 缺失，Step 02 都不能进入 Step 03。

## Controller Settings

Controller Settings 保存到统一 Face Config，因此重新打开工具、返回 Step 02 或后续重建都能恢复。

默认：

```text
Global Scale = 1.0
LF Color     = 6
RT Color     = 13
MD Color     = 17
Module Size  = 1.0
```

Module Size 使用一位小数：

```text
0.1
0.7
1.0
1.5
...
```

Controller 默认配置统一定义在：

```text
systems/face/config.py
```

## Step Visibility

不再使用单独的 `workflow.py`。

静态显示规则直接定义在：

```text
systems/face/config.py
```

Step 切换时 `ui/workflow_controller.py` 直接执行这些规则。

Step 02 默认：

```text
显示
    原始 Setup Models
    Face Guide

隐藏
    Tweak Work Model
    Stretch Work Model
    Deform Work Model
    Controller Group
    Joint Group
    Rig Nodes
```

## 给 Build Component 使用

简单 Component 直接表达自己需要什么 Guide。

例如 Teeth：

```python
upper_teeth_name = name_utils.Name.create_name(
    node_type="loc",
    side="md",
    part="upper_teeth",
    function="guide",
    index=1
)

upper_teeth_guide = self.get_guide_node(
    upper_teeth_name,
    required=True
)
```

例如 Tongue：

```python
tongue_guides = self.get_part_guides(
    part="tongue",
    required=True
)
```

这种写法是后续 Face Build Component 的推荐模式：

```text
Naming Rule
    ↓
直接 Query
    ↓
Component Build
```

避免为了一个简单查询继续增加中间文件和包装方法。

## 相关文档

- [Face System Architecture](../architecture/face-system.md)
- [UI Design System](../development/ui-design.md)
- [总体架构](../architecture/index.md)

[返回用户手册](index.md){ .md-button }
