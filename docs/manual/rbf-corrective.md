# 通用 Pose Driver / RBF

工具自动旋转 ADV 控制器，读取最终关节姿态，训练修型权重。大臂、大腿和手腕共用同一套计算与连接流程。此工具创建驱动，不创建或雕刻修型模型，也不改变 ADV 的 FK/IK 绑定结构。

## 打开工具

更新仓库后重启 Maya，打开木子工具箱的 **绑定工具 → 通用 Pose Driver / RBF**。也可直接运行：

```python
from muziToolset.tools.rig import rbf_corrective_tool
window = rbf_corrective_tool.main()
```

窗口使用现有单实例管理，支持最小化。适配 PySide2 / PySide6；目标运行环境是 Maya 2023。

## 自动采样流程

1. 选择部位、侧别和实例序号，点击 **应用 ADV 模板 / 新建配置**。
2. 检查对应的最终关节与采样控制器。可以选择对象，使用拾取按钮覆盖模板名称。
3. 确认绑定处于对应 FK 控制器能够驱动关节的模式。不同 ADV 版本的 FK/IK 切换属性不同，工具不猜测或自动改写它。
4. 点击 **自动采样**。工具逐个旋转控制器，采集中立、上、下、前、后、四个对角，以及正负扭转，总计 11 个姿态。
5. 工具恢复控制器原旋转及自动关键帧状态；点击 **训练并构建**，得到 10 个输出。
6. 选择输出并输入实际 BlendShape 属性，例如 `body_bs.armUp` 或 `body_bs.weight[0]`，点击 **连接输出**。

不用逐个手摆样本。构建时当前控制器姿态定义为中立，工具不会自动把一个正在弯曲的控制器猜测为角色标准中立；如有明确中立姿态，应先将绑定恢复到该状态。采样过程中不改时间、不改控制器旋转顺序，不直接设置关节旋转。

自动采样通道必须可写且无动画、约束或其他输入连接，并且没有启用旋转限制。采样暂时关闭自动关键帧，结束或异常时恢复三个旋转通道及其状态。若当前控制器没有驱动所选关节，采样数据会重复，训练会明确报错。

## ADV 模板

| 部位 | 左侧关节 | 左侧控制器 | 右侧命名 | 默认输入尺度 |
| --- | --- | --- | --- | --- |
| 大臂 arm | Shoulder_L | FKShoulder_L | 对应 `_R` | XYZ 各 90° |
| 大腿 thigh | Hip_L | FKHip_L | 对应 `_R` | XYZ 各 90° |
| 手腕 wrist | Wrist_L | FKWrist_L | 对应 `_R` | XYZ 各 45° |

这些是可编辑的 ADV 名称模板，不能保证所有版本或角色都使用相同名称。`md` 只表示生成网络的中部命名，模板仍先填左侧节点，中心部位需自行覆盖输入和控制器。左右侧不自动推断身体方向符号；可修改采样符号。

## 采样设置与求解设置

| 设置 | 作用 |
| --- | --- |
| 输入属性 | 实际读取的关节或其他标量属性，支持多个关节、多维输入 |
| 输入尺度 | 每个输入的典型变化量；避免某一轴数值过大主导距离 |
| 输入周期 | 0 表示连续值；360 表示角度绕回，周期核平滑跨越 ±180° |
| 采样轴 | 控制器上两个摆动轴、一个扭转轴，默认 `Y,Z,X` |
| 摆动符号 | “上”和“前”在控制器上的旋转符号，默认 `-1,1` |
| 采样角度 | 单轴1、单轴2、对角1、对角2、扭转的角度幅度 |
| 半径 | Gaussian 核在归一化输入空间的宽度 |
| 正则项 | 默认 0，样本点精确插值；增大可缓解病态，但不再严格 one-hot |
| 夹到 0~1 | 限制修型权重范围，默认启用 |
| 输出归一化 | 权重总和超过 1 时缩放，默认关闭 |

大臂与大腿的默认采样角度是 `90,90,45,45,90`，手腕是 `45,45,22.5,22.5,45`。阈值可按角色活动范围调整。控制器采样轴与最终关节输入轴不必相同：RBF 使用采样时实际测得的关节数值，不假定两者一一对应。

一个自动采样控制器也可以同时驱动多个输入关节，只要所有输入对应的尺度、周期数量一致。通过 API 可定义任意 XYZ 偏移列表来采集组合姿态；UI 的 **补充当前姿态** 用于添加额外样本。

## 两种求解模式

**rbf** 是真正的 Gaussian RBF 插值。对归一化距离使用 Gaussian 核，训练时求解 `K × coefficients = targets`，中立样本目标为全零，其他姿态分别对应一个 one-hot 输出。每个输出通过所有样本核值的加权和实时计算。

**smoothstep** 保留旧 V6 的八方向与独立扭转效果，不是 RBF。默认输入索引 `1,2,0` 表示读取输入列表中的 Y、Z、X；默认摆动符号 `-1,1`，阈值 `45,45,90`。固定十输出顺序必须来自标准自动采样集，不能增加自定义输出；需要周期为 0。Smoothstep 固定夹到 0~1，扭转独立，因此不应用 RBF 的总量归一化开关。

RBF 在样本点提供训练目标，样本之间可能共同激活多个修型。它不保证纯单轴时其他输出处处为零，也不保证超过最大采样角度仍保持 1；远离所有样本时 Gaussian 核会衰减。需要原 V6 的严格方向隔离与超限保持时选择 Smoothstep。

## 连接、重建与场景恢复

生成节点统一采用当前仓库的 `Name`：

```text
network_lf_arm_rbf_001
expression_lf_arm_rbf_001
unitConversion_lf_arm_rbfInput_001
```

原有 ADV 关节和控制器不会重命名。输出网络的 `weight0` 等稳定属性通过姿态名设置别名，UI 与 API 均按姿态名访问。

改变半径、样本或尺度后点击 **重建并保留连接**。它先训练并构建候选网络，再迁移同名输出；被删除的输出仍有目标连接时会拒绝重建。重建必须保持侧别、部位与实例序号。构建、采样、连接、删除、重建均纳入 Undo Chunk。

关闭窗口或重开场景后点击 **刷新场景 → 恢复所选网络**。网络通过 message 标记所属节点，删除时不使用通配符，也不会删除 ADV 原绑定和 BlendShape。删除会断开该网络的输出驱动，目标权重不保证保持删除前数值。

训练系数编译到 Maya MEL 表达式，只有数值运算与明确的属性依赖，无 Python 回调、scriptJob 或外部 RBF 插件。计算与窗口是否打开无关。每个角度输入采用显式单位转换，统一为度；采样也将角度转成度。非角度输入只接受无单位标量，不接受平移长度属性。

保存配置会保存关节输入、样本、控制器名称和采样参数。加载配置只产生草稿，不删除当前场景网络。换角色可修改输入映射；UI 更换输入后要求重新采样，API 可在确认数据语义相同时重映射。场景恢复会从实际连接获取已重命名的输入节点，但采样控制器名称仍应检查。

## Python 示例

```python
from muziToolset.systems.rbf.presets import create_adv_model
from muziToolset.systems.rbf.sampling import sample_controller, create_pose_offsets
from muziToolset.systems.rbf.driver import RbfDriver, save_model

model = create_adv_model(part='arm', side='lf', joint='Shoulder_L')
model.sampling = {
    'controller': 'FKShoulder_L',
    'swing_axes': ['Y', 'Z'], 'twist_axis': 'X',
    'swing_signs': [-1, 1], 'swing_angles': [90, 90],
    'diagonal_angles': [45, 45], 'twist_angle': 90,
}
model = sample_controller(model, 'FKShoulder_L', create_pose_offsets())
driver = RbfDriver(model)
output = driver.build()
print(driver.read())
# 使用真实 BlendShape 属性替换示例：
# driver.connect_output('up', 'body_bs.armUp')

restored = RbfDriver.from_scene(output)
# save_model(restored.model, 'D:/rig_data/arm_rbf.json')
```

自定义自动采样偏移：

```python
offsets = [
    ('neutral', [0, 0, 0]),
    ('reachUp', [0, -90, 0]),
    ('reachUpTwist', [45, -90, 0]),
]
model = sample_controller(create_adv_model('arm', 'lf'), 'FKShoulder_L', offsets)
```

中立必须是首个零偏移样本，其他样本各生成一个同名修型输出。最大 128 个样本；不是大量姿态数据库的高性能插件替代品。

## 验证与限制

普通 Python 测试覆盖 Gaussian 插值、周期等价、重复样本、范围限制、表达式编译数值一致性、采样成功与失败时的恢复，以及旧 V6 Smoothstep 回归。专用 GitHub Actions 工作流在 Python 3.9 和 3.11 执行这些测试。

本次开发环境没有 Maya，真实 DG 求值、单位转换、界面交互、撤销与 ADV 角色行为尚未在 Maya 验收。已有真实 Maya 验证脚本：

```python
from muziToolset.tests.rbf_maya_smoke_test import run
print(run())
```

脚本创建临时控制器与关节验证自动采样、权重、连接、重建、重命名恢复、单位变化和撤销，并清理自己的对象。它不清空场景；建议先在测试场景运行，再对真实 ADV 角色检查 FK/IK 切换、镜像、旋转顺序与修型效果。

当前输入是局部 Euler 通道，不是四元数空间或几何 Swing/Twist 分解。周期核可以处理单个通道绕回，无法解决所有 Euler 万向节锁或等价旋转表示。jointOrient、父级约束、rotateOrder 与 ADV 切换可能影响关节 Euler 表示；复杂肩部或多轴组合应增加相关采样并实际验收。

Autodesk 技术参考：[expression](https://help.autodesk.com/cloudhelp/2024/ENU/Maya-Tech-Docs/Commands/expression.html)、[unitConversion](https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Tech-Docs/Nodes/unitConversion.html)、[transformLimits](https://help.autodesk.com/cloudhelp/ENU/MayaCRE-Tech-Docs/CommandsPython/transformLimits.html)。

## 通用 Pose Driver 与 Locator 编辑

本轮在已有实现上增加任意关节模板、可编辑样本 Locator 和辅助骨输出。默认模板中 `arm / thigh / wrist` 分别对应 Shoulder / Hip / Wrist；自定义关节可使用 `create_joint_model()`，UI 的部位字段也允许输入自定义命名 token。手腕 Smoothstep 阈值为 `22.5,22.5,45`，大臂和大腿保留 V6 的 `45,45,90`。

构建网络时自动生成一个样本网格和每个姿态的 Locator，包括中立。选择列表中的姿态，再点击 **选择样本 Locator**。Channel Box 的 `poseValue0 / poseValue1 / …` 对应输入列表顺序，角度始终以度记录；`poseInput0` 等锁定文本属性注明原始输入路径。Locator 的平移只是网格显示位置，不是训练输入；旋转 Locator 也不会修改采样值。需要从真实绑定姿态更新时，摆好控制器，点击 **用当前姿态覆盖选中样本**。

编辑 `poseValue` 后点击 **读取 Locator 编辑为草稿 → 重建并保留连接**，训练成功才应用到实时网络。缺失 Locator、重复姿态或非法数值会阻止读取，原驱动仍保留。读取采用全部已构建 Locator；若草稿另外增删过样本，读取会以场景 Locator 集合为准。先重建可将草稿的新增样本生成 Locator。

Smoothstep 的非中立样本值只用于记录，不决定插值曲线；它依照中立值、方向符号和阈值计算。修改 Smoothstep 的方向与过渡范围，应调整输入索引、符号和阈值。Gaussian RBF 使用全部样本值参与训练。两个求解器都禁止配置改变后继续用旧训练结果，Python API 修改模型后需要重新 `train()`；场景驱动则需要 `rebuild()`。

生成名称示例：

```text
transform_lf_arm_rbfPoses_001
transform_lf_arm_rbfPose001_001
transform_lf_arm_rbfPose002_001
animCurveUA_lf_arm_rbfMapping_001
```

Pose Locator 与求解节点通过 `ownedNodes` 标记所有权，辅助骨映射通过 `outputMappings` 标记所有权。重建替换样本 Locator，保留已连接的映射曲线；删除网络同时清理这两类所属节点。旧场景没有 Locator 时仍可恢复网络，点击重建即可补齐。

## 辅助骨端点映射

选定输出，将目标填写为实际辅助骨属性，例如 `jnt_lf_arm_corrective_001.rotateX`。展开 **辅助骨 / 标量端点映射**，设置权重 0 与权重 1 对应的目标数值。默认权重 0 读取目标当前值；取消该选项可以明确指定两个端点。权重 0.5 得到两个端点的中间值；超出 0~1 时保持对应端点。需要多个修型合成到同一个骨骼通道时，应先创建独立的修型 offset 层或外部合成网络；本接口拒绝覆盖已有连接。

| 目标类型 | 映射节点 | 端点单位 |
| --- | --- | --- |
| rotate / doubleAngle | animCurveUA | Maya 当前角度单位 |
| translate / doubleLinear | animCurveUL | Maya 当前距离单位 |
| scale / double / float | animCurveUU | 无单位数值 |

驱动曲线使用无时间的权重输入，不生成时间轴关键帧，也不依赖 UI 回调。Maya 更改角度或距离单位时，曲线输出保留其物理单位。**删除上述目标的当前映射** 只删除当前 Driver 拥有的映射。

## 新增中文 API 示例

```python
from muziToolset.systems.rbf.presets import create_joint_model
from muziToolset.systems.rbf.driver import RbfDriver, capture_pose
from muziToolset.systems.rbf.pose_locator import read_pose_locators
from muziToolset.systems.rbf.output_driver import connect_mapped_output

# 名称可带命名空间；任意部位使用相同核心。
model = create_joint_model('hero:Wrist_L', part='wrist', side='lf')
capture_pose(model, 'neutral', neutral=True)
# 手动将控制器摆到所需姿态，再执行下一行。
# capture_pose(model, 'bend')
# driver = RbfDriver(model)
# driver.build()
# connect_mapped_output(driver, 'bend', 'helperJoint.rotateX', 30, neutral_value=5)

# 修改场景 Locator 的 poseValue 属性后：
# candidate = read_pose_locators(driver)
# driver.rebuild(candidate)
```

| API | 输入与结果 | 使用场景 |
| --- | --- | --- |
| `create_joint_model(joint, …)` | 返回未采样 RbfModel；显式指定摆动、Twist 轴和部位 | 任意肩、髋、腕或自定义关节 |
| `model.update_pose(name, values)` | 按名称更新样本；验证失败保留原数据 | 修改草稿，保留输出名称 |
| `model.remove_pose(name)` | 删除非中立样本 | 移除不再使用的修型 |
| `get_pose_locators(driver)` | 返回姿态名到 Locator 的映射 | 选择、查询所属样本 |
| `write_pose_locator(driver, name, values)` | 写入采样值，支持撤销 | 当前姿态覆盖既有记录 |
| `read_pose_locators(driver)` | 返回独立模型并检查可训练性 | 编辑后生成重建草稿 |
| `connect_mapped_output(driver, name, destination, full_value, neutral_value=None)` | 返回所属 Driven 曲线 | 权重映射到辅助骨 |
| `disconnect_mapped_output(driver, destination)` | 删除指定目标的所属映射 | 解除辅助骨驱动 |

## 本轮验证

普通 Python 回归覆盖训练失效、编辑原子性、三种轴顺序、非零中立、V6 超限与 Twist、Locator 编辑、辅助骨映射类型、连续两次重建、迁移失败回滚、已有驱动保护与所属节点清理。Qt 使用真实 PySide6 窗口和 Maya 查询替身测试；Maya 2023 的 PySide2 与真实 DG 仍需执行 Maya smoke 验收。

```bash
python -m unittest discover -s tests -p 'rbf_*_test.py' -v
QT_QPA_PLATFORM=offscreen python tests/tool_ui_qt_smoke_test.py
```

`rbf_maya_smoke_test.run()` 已增加 Locator、辅助骨端点、重建后映射保留和 radians 单位切换检查；普通 Python 的发现过程不会导入 Maya。上述 Maya smoke 脚本是待执行的验收入口，不能将命令替身测试视为真实 DG 验证。

Autodesk 参考：[animCurve 节点类型与单位](https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Nodes/animCurve.html)、[无时间输入的 setKeyframe](https://help.autodesk.com/cloudhelp/2026/ENU/Maya-Tech-Docs/Commands/setKeyframe.html)。
