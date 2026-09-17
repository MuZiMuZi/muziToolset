# coding=utf-8
u"""
批量统一 Controller Shape Library 的标准尺寸。

标准：
    1. Controller Shape Library 继续统一使用 X+ 作为标准轴向。
    2. 一个 JSON 文件中所有 Curve Shape 共用同一个缩放比例。
    3. 从控制器原点到最远 CV 的距离统一归一化为 1.0。
    4. 只修改 points，不修改 degree / periodic / knot，因此不会改变曲线拓扑。

这个脚本同时会把相同的归一化规则写入 Ctrl.save_ctrl_shape()，
保证以后新保存到 Shape Library 的控制器也会自动使用半径 1.0 的标准尺寸。
"""

from __future__ import print_function

import json
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHAPE_LIBRARY_DIR = os.path.join(PROJECT_ROOT, "resources", "controller_shapes")
CTRL_UTILS_FILE = os.path.join(PROJECT_ROOT, "core", "rigging", "ctrl_utils.py")


SAVE_NORMALIZE_MARKER = u"# Shape Library 保存前统一归一化到标准半径 1.0。"


def get_max_radius(shape_data):
    u"""计算一个 Controller JSON 中距离原点最远的 CV 距离。"""

    max_radius = 0.0

    # 一个 Controller JSON 可能保存多个 NurbsCurve Shape。
    # 所有 Shape 必须使用同一个缩放比例，才能保持组合控制器原有的相对关系。
    for shape_info in shape_data:
        point_values = shape_info.get("points", [])

        # points 使用 [x0, y0, z0, x1, y1, z1, ...] 的一维格式保存。
        for index in range(0, len(point_values), 3):
            point_x = float(point_values[index])
            point_y = float(point_values[index + 1])
            point_z = float(point_values[index + 2])

            radius = (
                point_x * point_x +
                point_y * point_y +
                point_z * point_z
            ) ** 0.5

            if radius > max_radius:
                max_radius = radius

    return max_radius


def normalize_shape_data(shape_data):
    u"""把一个完整 Controller Shape 数据等比归一化到最大半径 1.0。"""

    max_radius = get_max_radius(shape_data)

    # 没有有效尺寸的数据不能进行归一化。
    # 这种情况下直接返回 False，避免除以 0 并破坏原始 JSON。
    if max_radius <= 0.0:
        return False

    scale_value = 1.0 / max_radius

    # 所有 CV 使用同一个 scale_value，保持 Shape 原有比例和轮廓不变。
    for shape_info in shape_data:
        point_values = shape_info.get("points", [])

        for index in range(len(point_values)):
            point_values[index] = float(point_values[index]) * scale_value

    return True


def normalize_shape_file(shape_file):
    u"""归一化一个 Shape JSON，并直接覆盖原文件。"""

    with open(shape_file, "r", encoding="utf-8") as file_object:
        shape_data = json.load(file_object)

    if not normalize_shape_data(shape_data):
        print(u"[SKIP] 没有有效 CV：{}".format(shape_file))
        return False

    # 统一使用可读的 4 空格 JSON，方便后续人工检查和版本对比。
    with open(shape_file, "w", encoding="utf-8") as file_object:
        json.dump(
            shape_data,
            file_object,
            indent=4,
            ensure_ascii=False
        )
        file_object.write("\n")

    # 写入后重新检查，确保最远 CV 已经是标准半径 1.0。
    normalized_radius = get_max_radius(shape_data)

    if abs(normalized_radius - 1.0) > 0.000001:
        raise RuntimeError(
            u"Controller Shape 归一化失败：{} -> {}".format(
                shape_file,
                normalized_radius
            )
        )

    print(u"[OK] {} -> radius 1.0".format(os.path.basename(shape_file)))
    return True


def normalize_shape_library():
    u"""批量归一化 resources/controller_shapes 下的全部 JSON Shape。"""

    json_files = []

    for file_name in os.listdir(SHAPE_LIBRARY_DIR):
        if not file_name.lower().endswith(".json"):
            continue

        json_files.append(file_name)

    json_files.sort()

    normalized_count = 0

    for file_name in json_files:
        shape_file = os.path.join(SHAPE_LIBRARY_DIR, file_name)

        if normalize_shape_file(shape_file):
            normalized_count += 1

    return normalized_count


def patch_save_ctrl_shape():
    u"""把半径 1.0 的归一化规则写入 Ctrl.save_ctrl_shape()。"""

    with open(CTRL_UTILS_FILE, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    # 已经存在新规则时不重复插入，保证脚本可以安全重复执行。
    if SAVE_NORMALIZE_MARKER in source:
        return False

    old_text = '''        if not shape_data:\n            pm.warning(u"当前控制器没有可以保存的 NurbsCurve Shape。")\n            return None\n\n        # 获取 muziToolset 项目根目录。\n'''

    new_text = '''        if not shape_data:\n            pm.warning(u"当前控制器没有可以保存的 NurbsCurve Shape。")\n            return None\n\n        # ---------------------------------------------------------------------\n        # Shape Library 保存前统一归一化到标准半径 1.0。\n        #\n        # 不同 Controller Shape 在 Maya 中制作时可能使用完全不同的尺寸。\n        # 如果把这些原始 CV 数值直接保存进 Shape Library，后续相同的 ctrl_size\n        # 会得到不同的视觉尺寸。这里统一计算所有 Shape 中距离原点最远的 CV，\n        # 再使用同一个缩放比例处理全部 CV，让最远 CV 的距离固定为 1.0。\n        #\n        # 一个 Controller 可能由多个 NurbsCurve Shape 组成，所以必须先遍历\n        # 全部 Shape 找到共同的最大半径，再整体等比缩放，不能逐个 Shape 单独归一化。\n        # ---------------------------------------------------------------------\n        max_radius = 0.0\n\n        for shape_info in shape_data:\n            point_values = shape_info["points"]\n\n            for index in range(0, len(point_values), 3):\n                point_x = point_values[index]\n                point_y = point_values[index + 1]\n                point_z = point_values[index + 2]\n\n                radius = (\n                    point_x * point_x +\n                    point_y * point_y +\n                    point_z * point_z\n                ) ** 0.5\n\n                if radius > max_radius:\n                    max_radius = radius\n\n        # 没有有效半径时不写入 Shape Library，避免除以 0。\n        if max_radius <= 0.0:\n            pm.warning(u"当前控制器 Shape 没有有效尺寸，无法保存。")\n            return None\n\n        normalize_scale = 1.0 / max_radius\n\n        # 所有 Curve Shape 使用同一个比例进行缩放。\n        # 这里只修改即将写入 JSON 的 point_values，不修改 Maya 场景中的控制器。\n        for shape_info in shape_data:\n            point_values = shape_info["points"]\n\n            for index in range(len(point_values)):\n                point_values[index] = point_values[index] * normalize_scale\n\n        # 获取 muziToolset 项目根目录。\n'''

    if old_text not in source:
        raise RuntimeError(
            u"没有找到 Ctrl.save_ctrl_shape() 的目标插入位置，请检查 ctrl_utils.py。"
        )

    source = source.replace(old_text, new_text, 1)

    with open(CTRL_UTILS_FILE, "w", encoding="utf-8") as file_object:
        file_object.write(source)

    return True


def main():
    u"""执行 Shape Library 批量归一化，并更新未来保存规则。"""

    normalized_count = normalize_shape_library()
    patched = patch_save_ctrl_shape()

    print(u"Controller Shape Library 已归一化 {} 个 JSON。".format(normalized_count))

    if patched:
        print(u"Ctrl.save_ctrl_shape() 已加入自动半径归一化。")
    else:
        print(u"Ctrl.save_ctrl_shape() 已经包含自动归一化规则。")


if __name__ == "__main__":
    main()
