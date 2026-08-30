# Face Guide

`FaceGuide` 是 Face Rig 的 **Step 02 定位数据管理层**。

进入 Step 02 时，UI 会自动导入或复用 `resources/face/face_guide.ma`。绑定师主要负责摆放定位器、镜像、修复模板和设置后续 Controller 参数。

## 标准流程

```text
Step 01 Setup 完成
        ↓
进入 Step 02
        ↓
自动导入 / 复用 face_guide.ma
        ↓
手动贴合 Locator
        ↓
需要时 LF ↔ RT Mirror
        ↓
设置 Controller Size / Color
        ↓
点击“下一步”
        ↓
检查模板中的全部 Locator
        ↓
全部存在 → 保存 Config → Step 03
任意缺失 → 阻止继续并列出缺失名称
```

## 自动加载 Guide

正常流程不需要手动点击 Build Guide。

```python
from muziToolset.systems.face import FaceGuide

guide = FaceGuide()
guide.build_guide()
```

`build_guide()` 是系统层公开入口，UI 会在进入 Step 02 时自动调用。

## Guide Template Contract

`resources/face/face_guide.ma` 是标准 Locator 完整性的唯一来源。

`guide_data.py` 会读取模板中的全部：

```text
loc_*_guide_###
```

点击“下一步”时逐个验证。

这意味着：

- 绑定师误删任意标准 Locator 都会被发现；
- 不只检查几个核心嘴唇 / 眼睛 Guide；
- Template 以后新增 Locator 后，Validation 会自动跟随模板。

## 重新导入模板

Step 02 提供 **重新导入模板**。

用途：绑定过程中误删了某个 Locator，但不希望丢失已经摆好的其它定位结果。

流程：

```text
当前 Guide
    ↓
记录仍然存在 Locator 的世界矩阵
    ↓
重新导入完整 face_guide.ma
    ↓
按标准名称匹配 Locator
    ↓
恢复已有 Locator 的原位置
    ↓
缺失 Locator 使用模板默认位置补回
```

因此这个功能是 Repair / Reimport，不等同于完全 Reset。

## Guide Mirror

Step 02 支持：

```text
LF → RT
RT → LF
```

Mirror 只复制当前 Guide 状态，不建立永久左右 Transform Connection。

镜像后：

- LF / RT 可以继续独立调整；
- `md` 中线 Guide 不参与镜像；
- 非对称角色仍然可以继续手工修改。

## 撤销镜像

每次 Guide Mirror 都作为一个 Maya Undo Chunk 执行，因此可以直接使用：

```text
Ctrl + Z
```

UI 同时提供：

```text
撤销上次镜像
```

按钮会恢复 Mirror 前记录的 Target Side Snapshot。

## Controller Settings

### Global Scale

控制整个 Face Controller 的整体大小倍率。

默认：

```text
1.0
```

### Side Color

默认 Maya Index Color：

```text
LF = 6   蓝色
RT = 13  红色
MD = 17  黄色
```

UI 使用 Slider + Index + Color Preview。

### Module Size

全部默认：

```text
1.0
```

使用 `QDoubleSpinBox`：

```text
最小 0.1
最大 100.0
步进 0.1
小数 1 位
```

按面部从上到下排列：

```text
Brow
Eye
Eyelid
Nose
Cheek
Lip
Jaw
```

## 完整性检查

可以在代码中主动查询：

```python
validation = guide.validate_guides()

print(validation["valid"])
print(validation["missing_guide_names"])
print(validation["guide_count"])
print(validation["template_guide_count"])
```

如果 `valid == False`，Step 02 不应该进入 Step 03。

## Guide 数据给 Builder 使用

后续 Builder 不应该使用 `cmds.ls()` 猜 Locator 顺序。

直接使用稳定 API：

```python
lip_data = guide.get_lip_guides()
lid_data = guide.get_eyelid_guides("lf")
brow_data = guide.get_brow_guides("lf")
```

固定顺序和名称由 `guide/guide_data.py` 管理。

## 目录

```text
systems/face/guide/
├── face_guide.py       Step 02 调度 / Query / Validation / Config
├── guide_data.py       Template Contract / 固定数据 / Controller Default
├── guide_template.py   Import / Reset / Repair / Reimport
└── guide_mirror.py     LF ↔ RT / Undo
```

## 相关文档

- [Face System Architecture](../architecture/face-system.md)
- [UI Design System](../development/ui-design.md)
- [总体架构](../architecture/index.md)

[返回用户手册](index.md){ .md-button }
