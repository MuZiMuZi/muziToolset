# Controller Shape Library

`resources/controller_shapes/` 是 muziToolset 的 Controller Shape 资源库。

这个目录只保存控制器形状数据和可选预览图，不负责 Controller 的创建、层级、属性或 Transform 逻辑。新版 `core/rigging/ctrl_utils.py` 后续只需要从这里读取 Shape 数据并创建 NurbsCurve Shape。

## 目录职责

```text
resources/
└── controller_shapes/
    ├── README.md
    ├── __init__.py
    ├── circle.json
    ├── circle.jpg
    ├── cube.json
    ├── cube.jpg
    ├── ...
    └── shape_XX.json / shape_XX.jpg
```

- `.json`：真正参与 Controller Shape 重建的数据文件。
- `.jpg`：可选的 Shape 预览图，只用于 UI 浏览，不参与绑定计算。
- 同名 `.json` 与 `.jpg` 代表同一个 Shape 资源。
- 某些旧资源只有 `.json`，没有 `.jpg`，这种情况仍然是有效 Shape。

当前资源库同时保留了有意义名称的旧资源，例如 `circle`、`cube`、`ball`、`jaw`、`eyeBallCtrl` 等，以及原来的 `shape_XX` 编号资源。

为了兼容旧绑定代码，现阶段不主动重命名、删除或合并这些资源。即使两个资源看起来相似，也可能已经被旧模块通过文件名引用。

---

# JSON 数据结构

每一个 Controller Shape JSON 文件的最外层都是一个 `list`：

```json
[
    {
        "points": [],
        "degree": 3,
        "periodic": false,
        "knot": []
    }
]
```

最外层使用列表，是因为一个 Controller Transform 理论上可以同时拥有多个 NurbsCurve Shape。

因此：

```text
JSON 文件
    ↓
list
    ↓
第 1 个 dict → 第 1 个 NurbsCurve Shape
第 2 个 dict → 第 2 个 NurbsCurve Shape
第 3 个 dict → 第 3 个 NurbsCurve Shape
...
```

即使一个控制器只有一个 Shape，最外层仍然保持列表结构。

## points

```json
"points": [
    x0, y0, z0,
    x1, y1, z1,
    x2, y2, z2
]
```

`points` 保存 NurbsCurve 的 CV 坐标。

为了让 JSON 数据更简单，旧 Shape Library 没有把每个点保存成嵌套列表，而是把所有 XYZ 数值连续保存成一个一维列表。

例如：

```json
"points": [
    0.0, 1.0, 0.0,
    1.0, 0.0, 0.0,
    0.0, -1.0, 0.0
]
```

读取后需要重新组合成：

```python
points = []

for index in range(0, len(point_values), 3):
    point = [
        point_values[index],
        point_values[index + 1],
        point_values[index + 2]
    ]
    points.append(point)
```

最终得到：

```text
[
    [x0, y0, z0],
    [x1, y1, z1],
    [x2, y2, z2]
]
```

注意：`points` 数组长度应该能够被 3 整除。

## degree

```json
"degree": 3
```

`degree` 是 NurbsCurve 的曲线 Degree。

常见值：

```text
1 → Linear Curve
2 → Quadratic Curve
3 → Cubic Curve
```

Controller Shape 最常见的是 Degree 1 和 Degree 3。

重建曲线时直接传给：

```python
pm.curve(degree=degree, ...)
```

## periodic

```json
"periodic": false
```

`periodic` 表示曲线是否为周期闭合曲线。

```text
False → 非周期曲线
True  → 周期闭合曲线
```

旧 Shape Library 在重建周期曲线时，会把开头的 `degree` 个 CV 再追加到点列表末尾：

```python
if periodic:
    points = points + points[:degree]
```

然后创建：

```python
pm.curve(periodic=periodic, ...)
```

因此新版读取器在兼容旧 JSON 数据时，需要继续保留这个处理逻辑。

## knot

```json
"knot": [
    0.0,
    1.0,
    2.0,
    3.0
]
```

`knot` 保存 NurbsCurve 的 Knot Vector。

它决定 CV 参数在曲线上的分布方式，需要和 `degree`、CV 数量以及 `periodic` 状态一起使用。

加载旧 Shape 时不要重新自动计算 Knot，应该直接使用 JSON 中保存的原始 Knot 数据，避免控制器曲线外形发生变化。

重建时：

```python
pm.curve(
    degree=degree,
    knot=knot,
    periodic=periodic,
    point=points
)
```

---

# 完整读取流程

新版 Controller Shape Loader 推荐保持下面的简单流程：

```text
shape_name
    ↓
resources/controller_shapes/<shape_name>.json
    ↓
json.load()
    ↓
遍历最外层 Shape list
    ↓
读取 points / degree / periodic / knot
    ↓
把 points 一维数组恢复成 XYZ 点列表
    ↓
如果 periodic=True，补充开头 degree 个点
    ↓
pm.curve()
    ↓
将创建出的 NurbsCurve Shape parent 到 Controller Transform
    ↓
删除临时 Transform
```

这个流程与旧 Shape Library 的数据格式保持兼容，但新版代码应只负责 Shape 本身，不再把 Controller 层级、属性、动画集等逻辑混进 Shape Loader。

---

# 资源管理约定

1. `resources/controller_shapes/` 作为新版 Controller Shape Library 的唯一标准目录。
2. 旧资源文件名暂时全部保留，避免破坏已有引用。
3. 不因为预览图相同就删除 JSON，JSON 才是 Shape 的真实数据。
4. 不补齐缺失的 `shape_XX` 编号；编号不是资源完整性的判断标准。
5. 新增 Shape 时，推荐使用可读名称，例如 `eye_aim.json`、`jaw_main.json`，不要继续依赖无语义编号。
6. 新资源最好同时提供同名 `.jpg` 预览图，但 `.jpg` 不是必须文件。
7. Controller 大小修改仍然操作 Curve CV，不修改 Controller Transform Scale。
8. 后续 `ctrl_utils.py` 只读取这个目录，不再兼容多个历史 Shape 路径。

---

# 后续代码接口建议

`core/rigging/ctrl_utils.py` 后续可以逐步增加：

```text
Ctrl
├── get_ctrl_shape()
├── set_ctrl_shape(shape_name)
├── set_ctrl_color(ctrl_color)
└── set_ctrl_size(ctrl_size)
```

其中 `set_ctrl_shape(shape_name)` 负责从本目录读取 JSON 并替换 Controller 的 Curve Shape。

Shape Library 的保存、预览图生成和 UI 浏览功能可以等基础读取流程稳定后再增加，不需要一次全部迁移旧 `controlUtils.py` 的功能。
