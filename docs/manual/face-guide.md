# Face Guide 使用手册

Face Guide 是当前 Face Rig 的定位输入层。

它的职责是告诉各个 Module：

```text
Joint 应该在哪里
Controller 应该在哪里
旋转中心在哪里
Aim 目标在哪里
链条顺序是什么
```

Guide 不是最终 Joint，也不是最终 Controller。

---

# 当前 Guide 命名规则

标准 Locator：

```text
loc_<side>_<part>_<function>_<index>
```

方向：

```text
lf = Left
rt = Right
md = Middle
```

普通 Face Locator 默认：

```text
function = bind
```

例如：

```text
loc_lf_ear_bind_001
loc_md_nose_center_bind_001
loc_lf_upper_lid_bind_001
```

---

# Eye Guide 是特殊语义

Eye 不通过 Locator 列表顺序猜测 Ball / Iris / Aim。

当前使用固定语义名称：

```text
loc_lf_eye_ball_001
loc_lf_eye_iris_001
loc_lf_eye_aim_001

loc_rt_eye_ball_001
loc_rt_eye_iris_001
loc_rt_eye_aim_001
```

其中：

## Ball

```text
loc_<side>_eye_ball_001
```

用途：

- 真实眼球旋转中心；
- Eye Bind Joint 创建位置；
- Main Controller 旋转 Pivot 的目标位置。

## Iris

```text
loc_<side>_eye_iris_001
```

用途：

- Main Controller 的可见位置。

Main Ctrl Transform 保持在 Iris，而 Rotate Pivot 放在 Ball。

## Aim

```text
loc_<side>_eye_aim_001
```

用途：

- Eye Aim Controller 的位置。

---

# Guide Template

Rig Library Step 02 会复用：

```text
core/rigging/guide_utils.py
```

中的 Guide Template 导入能力。

Face Template 名称和 Root 由：

```text
systems/face/face_guide_config.py
```

统一维护。

因此不要在多个 Module 里重复硬编码 Guide Template 路径。

---

# Rig Library 中如何使用

## 第一次进入 Guide

1. 完成 Step 01 Setup；
2. 进入 Step 02 Guide；
3. 如果 Face Guide 尚未导入，点击底部“下一步”；
4. 系统导入 Face Guide Template；
5. 调整 Locator 位置；
6. 再点击“下一步”生成 Joint / Controller。

---

# 手动 Guide List

某些模块支持手动指定 Guide 顺序。

操作：

1. 在 Maya 中按正确顺序选择 Transform / Joint；
2. 点击“读取 Maya 选择”；
3. Guide Edit 中每行显示一个节点；
4. 手工检查顺序；
5. 点击“保存 Guide 列表”。

Guide Edit 的最终文本顺序就是 Builder 使用顺序。

---

# Guide 必须满足什么

Build 前会检查：

```text
节点存在
名称唯一
节点不重复
类型是 transform / joint
```

如果一个名字匹配多个 DAG 节点，会被视为无效。

这样做是为了避免 Builder 在复杂 Scene 中“猜一个节点”然后生成错误 Rig。

---

# Mirror Guide

Rig Library 可以把左右 Module 的 Guide 沿：

```text
World X = 0
```

镜像。

例如：

```text
[x, y, z]
    ↓
[-x, y, z]
```

Mirror 适用于：

```text
Step 01
Step 02
Step 03
```

Final 阶段需要先回退。

---

# 已 Build 后还能改 Guide 吗？

可以。

推荐流程：

```text
Step 03 / Final
    ↓
回退 Step 02
    ↓
修改 Guide
    ↓
点击“下一步”
    ↓
Rebuild 当前 Module
    ↓
进入 Step 03
    ↓
重新 Final
```

Rebuild 后：

```text
connected = False
```

因为旧的最终连接不应该继续指向被重新生成的输出。

---

# 旧 Guide 名称兼容

旧版本曾使用：

```text
loc_*_*_guide_*
```

当前标准已经迁移。

普通 Locator：

```text
loc_lf_ear_guide_001
    ↓
loc_lf_ear_bind_001
```

复合 Part：

```text
loc_lf_upper_lid_guide_001
    ↓
loc_lf_upper_lid_bind_001
```

Eye 特殊 Locator：

```text
loc_lf_eye_ball_guide_001
    ↓
loc_lf_eye_ball_001
```

兼容转换由：

```text
face_guide_config.normalize_legacy_locator_name()
```

集中处理。

---

# 批量迁移旧 Locator

`face_guide_config.py` 还提供当前 Scene 的旧 Locator 重命名能力。

它只处理真正带 Locator Shape 的 Transform，不会把：

```text
zero_*_guide_*
grp_*_guide_*
crv_*_guide_*
```

这类 Guide 层级节点误当成 Locator。

迁移前会先检查目标名称冲突。

---

# 为什么普通 Guide 统一用 `bind`

旧名称里的 `guide` 更像“这个节点属于 Guide 系统”，并没有说明它在 Rig 里的业务用途。

当前普通 Locator 使用：

```text
function = bind
```

使名字更接近后续输出语义。

只有确实需要区分功能的 Eye Locator 使用：

```text
ball
iris
aim
```

---

# Guide Config 与 Module 的关系

推荐：

```text
face_guide_config.py
    定义稳定命名
        ↓
EyeModule / EarModule / TongueModule
    获取自己需要的 Guide
        ↓
RigModule / Core
    创建 Joint / Controller
```

不要在 UI 里硬编码大量 Locator 名称。

---

# 常见问题

## Eye 为什么不能只给三个 Locator 然后按顺序判断？

因为顺序非常容易在 Scene Selection、JSON 或 UI 中被改变。

Eye Ball / Iris / Aim 属于强语义数据，所以通过名称直接匹配语义更安全。

## Guide 可以是 Joint 吗？

当前 Rig Library 校验允许：

```text
transform
joint
```

但具体 Module 是否适合使用 Joint Guide，仍取决于 Builder 实现。

## Guide 改完为什么 Final 要重新做？

因为 Rebuild 会重新生成 Module Outputs，旧 Connection 不再被视为可靠。

## 镜像后右侧为什么重新生成了？

如果右侧已经 Build，Mirror 会按新的 Guide Position 安全 Rebuild，避免右侧 Joint / Controller 继续停留在旧位置。

---

# 对应 API

- [Face Guide Config](../reference/systems/face/face_guide_config.md)
- [Guide Utils](../reference/core/rigging/guide_utils.md)
- [Eye Module](../reference/systems/face/eye_module.md)
- [Rig Library Service](../reference/systems/rig/library_service.md)
