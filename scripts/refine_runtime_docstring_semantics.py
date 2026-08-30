# coding=utf-8
u"""
Runtime Docstring Semantic Refiner
==================================

把第一轮自动补齐的 Runtime Docstring 从“字段完整”继续提升到“绑定师可直接阅读”。

只替换 Normalizer 生成的通用占位说明，不覆盖已经人工编写的参数文档。
术语优先采用 Maya / Rigging 常用表达，例如 Driver、Driven、Constraint、Joint Orient、
Influence、SkinCluster、BlendShape Target、Guide、Controller、Offset Parent Matrix 等。

使用：
    python scripts/refine_runtime_docstring_semantics.py --check
    python scripts/refine_runtime_docstring_semantics.py --write
"""

from __future__ import print_function

import argparse
import os
import re
import sys


SOURCE_ROOTS = [
    "app",
    "core",
    "systems",
    "tools",
    "ui",
]

ROOT_MODULE_FILES = [
    "__init__.py",
    "config.py",
]

GENERIC_DESCRIPTION_PATTERNS = [
    re.compile(r"^`([^`]+)` 对应的输入数据。$"),
    re.compile(r"^`([^`]+)` 对应的名称、标记或字符串参数。$"),
    re.compile(r"^`([^`]+)` 对应的整数参数。$"),
    re.compile(r"^`([^`]+)` 对应的数值参数。$"),
    re.compile(r"^`([^`]+)` 对应的数据列表。$"),
    re.compile(r"^`([^`]+)` 对应的配置或映射字典。$"),
    re.compile(r"^是否启用 `([^`]+)` 对应的处理。$"),
]


# =============================================================================
# Project
# =============================================================================

def get_project_root():
    u"""返回 MuziTools 仓库根目录。"""
    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        script_directory
    )


def iter_runtime_source_files(project_root):
    u"""扫描正式 Runtime Python 文件。"""
    source_files = []

    for root_name in SOURCE_ROOTS:
        source_root = os.path.join(
            project_root,
            root_name
        )

        if not os.path.isdir(source_root):
            continue

        for current_root, folder_names, file_names in os.walk(source_root):
            if "__pycache__" in folder_names:
                folder_names.remove(
                    "__pycache__"
                )

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                if file_name.startswith("_") and file_name != "__init__.py":
                    continue

                source_files.append(
                    os.path.join(
                        current_root,
                        file_name
                    )
                )

    for file_name in ROOT_MODULE_FILES:
        source_path = os.path.join(
            project_root,
            file_name
        )

        if os.path.isfile(source_path):
            source_files.append(
                source_path
            )

    source_files.sort()
    return source_files


def read_text(file_path):
    u"""读取 UTF-8 文本。"""
    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as file_object:
        return file_object.read()


def write_text(file_path, text):
    u"""写入 UTF-8 文本。"""
    with open(
            file_path,
            "w",
            encoding="utf-8",
            newline="\n"
    ) as file_object:
        file_object.write(
            text
        )


# =============================================================================
# Semantic Rules
# =============================================================================

def infer_semantic_info(parameter_name):
    u"""根据常见 Maya / Rigging 参数名返回类型和清晰说明。"""
    name = parameter_name.lower()

    exact_rules = {
        "node": ("str", u"需要查询或处理的 Maya 节点名称。"),
        "nodes": ("str | list[str]", u"需要批量查询或处理的 Maya 节点名称或节点列表。"),
        "object": ("str", u"需要处理的 Maya 场景对象名称。"),
        "objects": ("str | list[str]", u"需要批量处理的 Maya 场景对象名称或对象列表。"),
        "child": ("str", u"需要挂接到新 Parent 下的 Child DAG 节点。"),
        "parent": ("str", u"Child DAG 节点需要挂接到的 Parent 节点。"),
        "child_node": ("str", u"需要重新挂接父级的 Child DAG 节点名称。"),
        "parent_node": ("str", u"Child 最终需要挂接到的 Parent DAG 节点名称。"),
        "driver": ("str", u"驱动关系中的 Driver 节点。"),
        "driven": ("str", u"驱动关系中接收结果的 Driven 节点。"),
        "driver_object": ("str", u"作为 Constraint、Matrix 或属性关系 Driver 的 Maya 节点。"),
        "driver_objects": ("str | list[str]", u"一个或多个 Driver Maya 节点；输入顺序会保留。"),
        "driven_object": ("str", u"接收 Constraint、Matrix 或属性驱动结果的 Driven 节点。"),
        "driven_objects": ("str | list[str]", u"需要批量接收驱动结果的 Driven 节点或节点列表。"),
        "constraint_type": ("str", u"Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。"),
        "maintain_offset": ("bool", u"是否保持建立 Constraint / Matrix 关系前 Driver 与 Driven 的当前空间偏移。"),
        "search_types": ("str | list[str] | None", u"需要查询的 Maya 节点类型；None 表示使用方法默认的类型集合。"),
        "node_type": ("str", u"需要创建、查询或过滤的 Maya 节点类型。"),
        "source": ("str", u"数据、连接或复制关系的 Source 节点。"),
        "target": ("str", u"接收数据、连接或匹配结果的 Target 节点。"),
        "source_node": ("str", u"作为数据来源、复制来源或驱动来源的 Maya 节点。"),
        "target_node": ("str", u"接收数据、匹配结果或操作结果的 Target Maya 节点。"),
        "source_attr": ("str", u"驱动端完整 Maya Plug，例如 `ctrl.translateX`。"),
        "destination_attr": ("str", u"接收连接的完整 Maya Plug，例如 `jnt.rotateY`。"),
        "attr": ("str", u"Maya Attribute 名称；根据方法语义可以是短属性名或完整 Plug。"),
        "attribute": ("str", u"需要查询、设置或连接的 Maya Attribute / Plug。"),
        "plug": ("str", u"完整 Maya Plug，例如 `node.translateX`。"),
        "side": ("str", u"Rig 方向标记；项目常用 `lf`、`rt`、`md`。"),
        "axis": ("str", u"操作使用的局部轴或世界轴，例如 X、Y、Z、X+、X-。"),
        "primary_axis": ("str", u"Joint / Aim 的 Primary Axis；通常沿骨骼主方向指向 Child。"),
        "secondary_axis": ("str", u"Joint Orient 使用的 Secondary Axis，用于确定剩余局部轴方向。"),
        "aim_vector": ("list[float] | tuple[float, float, float]", u"Aim Constraint 使用的本地 Aim Vector。"),
        "up_vector": ("list[float] | tuple[float, float, float]", u"Aim Constraint 使用的本地 Up Vector。"),
        "world_up_vector": ("list[float] | tuple[float, float, float]", u"用于稳定 Aim Constraint Roll / Twist 的 World Up Vector。"),
        "world_up_object": ("str | None", u"Aim Constraint 的 World Up Object；是否使用取决于 worldUpType。"),
        "world_up_type": ("str", u"Aim Constraint 的 World Up 计算方式，例如 scene、object、objectrotation、vector 或 none。"),
        "joint": ("str", u"需要创建、查询、定向或驱动的 Maya Joint 节点。"),
        "joints": ("str | list[str]", u"需要批量处理的 Maya Joint 节点或 Joint Chain。"),
        "joint_count": ("int", u"需要生成或重采样的 Joint 数量。"),
        "mouth_jnt_number": ("int", u"嘴唇分布系统需要创建的 Joint 总数量。"),
        "curve": ("str", u"用于采样、附着或驱动的 NURBS Curve Transform / Shape。"),
        "curves": ("str | list[str]", u"需要批量采样、附着或处理的 NURBS Curve。"),
        "parameter": ("float", u"NURBS Curve / Surface 参数空间中的 Parameter 值。"),
        "percentage": ("float", u"沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。"),
        "percent": ("float", u"沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。"),
        "degree": ("int", u"创建或重建 NURBS Curve 使用的 Degree。"),
        "mesh": ("str", u"需要检查、复制、绑定或变形的 Mesh Transform / Shape。"),
        "model": ("str", u"需要检查、复制、绑定或参与 Rig 的模型 Transform。"),
        "skin_cluster": ("str", u"需要查询或编辑的 Maya skinCluster Deformer 节点。"),
        "influence": ("str", u"影响 SkinCluster 权重的 Influence Transform / Joint。"),
        "influences": ("str | list[str]", u"影响 SkinCluster 的 Influence Joint / Transform 列表。"),
        "weight": ("float", u"当前 Influence、Constraint Target 或 BlendShape Target 使用的权重值。"),
        "weights": ("list[float] | dict", u"需要读取、写入或传递的权重数据。"),
        "normalize": ("bool", u"是否在写入 Skin Weight 后执行权重归一化。"),
        "maximum_influences": ("int", u"单个 Vertex 允许保留非零权重的最大 Influence 数量。"),
        "blendshape": ("str", u"需要查询或编辑的 Maya blendShape Deformer 节点。"),
        "blendshape_node": ("str", u"需要查询或编辑的 Maya blendShape Deformer 节点。"),
        "base_model": ("str", u"BlendShape Deformer 使用的 Base Shape / Base Model。"),
        "target_model": ("str", u"需要添加、替换或查询的 BlendShape Target Shape。"),
        "target_index": ("int", u"BlendShape Target 在 Weight / Target Group 中使用的逻辑索引。"),
        "target_weight": ("float", u"BlendShape Target 在指定目标位置上的权重值。"),
        "matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。"),
        "offset_matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"用于保持 Driver 与 Driven 初始空间差异的 Offset Matrix。"),
        "parent_inverse_matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"Driven Parent Space 的 Inverse Matrix，用于把 World Matrix 转换到 Parent Space。"),
        "control": ("str", u"需要创建、查询或修改的动画 Controller Transform。"),
        "controller": ("str", u"需要创建、查询或修改的动画 Controller Transform。"),
        "controls": ("str | list[str]", u"需要批量处理的动画 Controller Transform 列表。"),
        "shape": ("str", u"Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。"),
        "color": ("int | tuple[float, float, float]", u"Viewport Override 使用的 Index Color 或 RGB Color。"),
        "radius": ("float", u"Joint、Controller 或可视辅助对象使用的半径 / 尺寸。"),
        "guide": ("str", u"Face / Rig 定位系统中的 Guide Transform / Locator。"),
        "guides": ("str | list[str]", u"需要按顺序查询或传递给 Builder 的 Guide Transform / Locator 列表。"),
        "guide_root": ("str", u"当前 Guide 模板或 Guide System 的顶层 Root Group。"),
        "parent_group": ("str | None", u"新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。"),
        "force": ("bool", u"是否强制覆盖已有连接、属性值或构建结果。"),
        "required": ("bool", u"节点或数据缺失时是否直接抛出异常，而不是返回空结果。"),
        "strict": ("bool", u"是否按严格模式处理无效输入和缺失数据。"),
        "world_space": ("bool", u"是否使用 Maya World Space，而不是 Local / Parent Space。"),
        "step_value": ("int", u"Face Wizard / Build Pipeline 当前 Step 编号。"),
        "last_step": ("int", u"Step 状态查询或失效处理时的最后一个 Step 编号。"),
        "file_path": ("str", u"需要读取、写入、导入或导出的文件路径。"),
        "directory": ("str", u"需要扫描、创建或写入文件的目录路径。"),
        "window_key": ("str", u"Window Manager 用于唯一识别 Maya 工具窗口的键值。"),
        "window_factory": ("callable", u"负责创建对应 PySide Maya 工具窗口的 Factory / Callable。"),
    }

    if name in exact_rules:
        return exact_rules[name]

    if name.endswith("_path"):
        return "str", u"需要读取、写入、导入或导出的路径。"

    if name.endswith("_name"):
        return "str", u"创建、查询或匹配 Maya 节点时使用的名称。"

    if name.endswith("_index"):
        return "int", u"对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。"

    if name.endswith("_count") or name.endswith("_number"):
        return "int", u"当前构建、采样或查询过程使用的元素数量。"

    if name.endswith("_radius"):
        return "float", u"当前 Joint、Controller 或辅助对象使用的半径。"

    if name.endswith("_weight"):
        return "float", u"当前 Driver、Influence、Constraint Target 或 BlendShape Target 使用的权重。"

    if name.endswith("_matrix"):
        return "list[float] | maya.api.OpenMaya.MMatrix", u"用于 Maya Transform / Rig 空间计算的 4x4 Matrix 数据。"

    if name.endswith("_attr"):
        return "str", u"需要查询、设置或连接的 Maya Attribute / Plug。"

    if name.endswith("_plug"):
        return "str", u"完整 Maya Plug，例如 `node.translateX`。"

    if name.endswith("_group"):
        return "str", u"当前 Rig / Guide / Controller 层级中的 Maya Group Transform。"

    if name.endswith("_joint"):
        return "str", u"当前 Rig 计算或构建使用的 Maya Joint 节点。"

    if name.endswith("_curve"):
        return "str", u"当前采样、附着或驱动使用的 NURBS Curve。"

    if name.endswith("_model") or name.endswith("_mesh"):
        return "str", u"当前检查、绑定、复制或变形使用的模型 / Mesh 节点。"

    if name.endswith("_guide") or name.endswith("_locator"):
        return "str", u"当前 Rig 定位流程使用的 Guide / Locator Transform。"

    if name.endswith("_ctrl") or name.endswith("_control") or name.endswith("_controller"):
        return "str", u"当前 Rig 操作或驱动使用的动画 Controller Transform。"

    if name.startswith("is_") or name.startswith("has_") or name.startswith("use_"):
        return "bool", u"控制对应 Rig / Maya 行为是否启用。"

    return None


def is_generic_description(description):
    u"""判断说明是否属于 Normalizer 自动生成的通用占位文本。"""
    stripped_description = description.strip()

    for pattern in GENERIC_DESCRIPTION_PATTERNS:
        if pattern.match(stripped_description):
            return True

    return False


# =============================================================================
# Source Rewrite
# =============================================================================

def refine_source_text(source_text):
    u"""替换一个 Python 文件中的通用 Args 占位说明。"""
    lines = source_text.splitlines()
    changed = False
    line_index = 0

    argument_line_pattern = re.compile(
        r"^(\s+)([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\):\s*$"
    )

    while line_index < len(lines):
        line = lines[line_index]
        match = argument_line_pattern.match(line)

        if not match:
            line_index += 1
            continue

        indent = match.group(1)
        parameter_name = match.group(2)
        current_type = match.group(3).strip()
        semantic_info = infer_semantic_info(
            parameter_name
        )

        if semantic_info is None:
            line_index += 1
            continue

        semantic_type = semantic_info[0]
        semantic_description = semantic_info[1]
        description_index = line_index + 1

        if description_index >= len(lines):
            line_index += 1
            continue

        description_line = lines[description_index]
        description = description_line.strip()

        if not is_generic_description(description):
            line_index += 1
            continue

        if current_type in ["", "object"]:
            lines[line_index] = "{}{} ({}):".format(
                indent,
                parameter_name,
                semantic_type
            )
            changed = True

        expected_description_indent = indent + "    "
        lines[description_index] = expected_description_indent + semantic_description
        changed = True
        line_index += 2

    refined_text = "\n".join(
        lines
    )

    if source_text.endswith("\n"):
        refined_text += "\n"

    return refined_text, changed


def find_generic_descriptions(source_text, relative_path):
    u"""返回仍然存在的通用参数说明。"""
    errors = []

    for line_number, line in enumerate(source_text.splitlines(), start=1):
        description = line.strip()

        if not is_generic_description(description):
            continue

        errors.append(
            u"{}:{} 仍存在机械参数说明: {}".format(
                relative_path,
                line_number,
                description
            )
        )

    return errors


def run(write=False):
    u"""执行语义细化或质量检查。"""
    project_root = get_project_root()
    source_files = iter_runtime_source_files(
        project_root
    )
    changed_files = []
    errors = []

    for source_path in source_files:
        source_text = read_text(
            source_path
        )

        if write:
            refined_text, changed = refine_source_text(
                source_text
            )

            if changed:
                write_text(
                    source_path,
                    refined_text
                )
                source_text = refined_text
                changed_files.append(
                    source_path
                )

        relative_path = os.path.relpath(
            source_path,
            project_root
        )
        file_errors = find_generic_descriptions(
            source_text,
            relative_path
        )

        for error in file_errors:
            errors.append(
                error
            )

    print("=" * 78)
    print("Runtime Docstring Semantic Quality")
    print("=" * 78)
    print("Runtime files:  {}".format(len(source_files)))
    print("Changed files:  {}".format(len(changed_files)))
    print("Generic docs:   {}".format(len(errors)))

    if changed_files:
        print("Changed:")

        for source_path in changed_files:
            print(
                "  - " + os.path.relpath(
                    source_path,
                    project_root
                )
            )

    if errors:
        print("Remaining generic descriptions:")

        for error in errors:
            print(
                "  - " + error
            )

        print("=" * 78)
        return False

    print("Status:         PASS")
    print("=" * 78)
    return True


def main():
    u"""命令行入口。"""
    parser = argparse.ArgumentParser(
        description="Refine MuziTools runtime docstrings with Maya / rigging terminology."
    )
    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Check for generic placeholder parameter documentation."
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help="Replace generic parameter documentation with rigging semantics."
    )

    arguments = parser.parse_args()
    success = run(
        write=arguments.write
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
