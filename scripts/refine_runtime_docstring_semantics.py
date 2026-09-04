# coding=utf-8
u"""
Runtime Docstring Semantic Refiner
==================================

把第一轮自动补齐的 Runtime Docstring 从“字段完整”继续提升到“绑定师可直接阅读”。

只替换 Normalizer 生成的通用占位说明，不覆盖已经人工编写的参数文档。
术语优先采用 Maya / Rigging 常用表达，例如 Driver、Driven、Constraint、Jnt Orient、
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

def get_exact_semantic_rules():
    u"""返回 MuziTools 高频 Maya / Rigging 参数语义表。"""
    rules = {
        # ------------------------------------------------------------------
        # DAG / Driver / Driven / Connection
        # ------------------------------------------------------------------
        "node": ("str", u"需要查询或处理的 Maya 节点名称。"),
        "nodes": ("str | list[str]", u"需要批量查询或处理的 Maya 节点名称或节点列表。"),
        "object": ("str", u"需要处理的 Maya 场景对象名称。"),
        "objects": ("str | list[str]", u"需要批量处理的 Maya 场景对象名称或对象列表。"),
        "obj": ("str", u"当前操作使用的 Maya DAG 节点或场景对象。"),
        "item": ("str | object", u"当前查询、吸附或 UI 操作使用的 Maya Item / 数据项。"),
        "child": ("str", u"需要挂接到新 Parent 下的 Child DAG 节点。"),
        "parent": ("str", u"Child DAG 节点需要挂接到的 Parent 节点。"),
        "child_node": ("str", u"需要重新挂接父级的 Child DAG 节点名称。"),
        "parent_node": ("str", u"Child 最终需要挂接到的 Parent DAG 节点名称。"),
        "left_parent": ("str", u"左侧 Guide 当前 Parent；镜像修复时用于解析对应的右侧 Parent。"),
        "driver": ("str", u"驱动关系中的 Driver 节点。"),
        "driven": ("str", u"驱动关系中接收结果的 Driven 节点。"),
        "driver_object": ("str", u"作为 Constraint、Matrix 或属性关系 Driver 的 Maya 节点。"),
        "driver_objects": ("str | list[str]", u"一个或多个 Driver Maya 节点；输入顺序会保留。"),
        "driven_object": ("str", u"接收 Constraint、Matrix 或属性驱动结果的 Driven 节点。"),
        "driven_objects": ("str | list[str]", u"需要批量接收驱动结果的 Driven 节点或节点列表。"),
        "source": ("str", u"数据、连接或复制关系的 Source 节点。"),
        "target": ("str", u"接收数据、连接或匹配结果的 Target 节点。"),
        "targets": ("str | list[str]", u"需要批量处理的 Target 节点；在 Constraint / BlendShape / Controller API 中保持输入顺序。"),
        "source_node": ("str", u"作为数据来源、复制来源或驱动来源的 Maya 节点。"),
        "target_node": ("str", u"接收数据、匹配结果或操作结果的 Target Maya 节点。"),
        "source_object": ("str", u"提供 Attribute、Transform 或连接数据的 Source Maya 对象。"),
        "target_objects": ("str | list[str]", u"接收 Source 数据或连接的一个或多个 Target Maya 对象。"),
        "source_attr": ("str", u"驱动端完整 Maya Plug，例如 `ctrl.translateX`。"),
        "destination_attr": ("str", u"接收连接的完整 Maya Plug，例如 `jnt.rotateY`。"),
        "driver_attribute": ("str", u"驱动 Set Driven Key / 属性关系的 Driver Plug，例如 `ctrl.smile`。"),
        "driven_controls": ("str | list[str]", u"接收 Driver Attribute 结果的 Driven Controller 列表。"),
        "attribute_pairs": ("list[tuple[str, str]] | dict", u"需要批量建立连接的 Source Plug / Destination Plug 配对数据。"),
        "attribute_names": ("str | list[str]", u"需要查询、复制或批量连接的 Maya Attribute 名称列表。"),
        "attr": ("str", u"Maya Attribute 名称；根据方法语义可以是短属性名或完整 Plug。"),
        "attribute": ("str", u"需要查询、设置或连接的 Maya Attribute / Plug。"),
        "plug": ("str", u"完整 Maya Plug，例如 `node.translateX`。"),
        "plugs": ("bool", u"查询连接时是否返回完整 Plug；False 时通常只返回节点名称。"),

        # ------------------------------------------------------------------
        # Constraint / Matrix / Aim
        # ------------------------------------------------------------------
        "constraint_type": ("str", u"Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。"),
        "maintain_offset": ("bool", u"是否保持建立 Constraint / Matrix 关系前 Driver 与 Driven 的当前空间偏移。"),
        "search_types": ("str | list[str] | None", u"需要查询的 Maya 节点类型；None 表示使用方法默认的类型集合。"),
        "ik_handle": ("str", u"接收 Pole Vector Constraint 或 IK 操作的 Maya ikHandle 节点。"),
        "aim_vector": ("list[float] | tuple[float, float, float]", u"Aim Constraint 使用的本地 Aim Vector。"),
        "up_vector": ("list[float] | tuple[float, float, float]", u"Aim Constraint 使用的本地 Up Vector。"),
        "world_up_vector": ("list[float] | tuple[float, float, float]", u"用于稳定 Aim Constraint Roll / Twist 的 World Up Vector。"),
        "world_up_object": ("str | None", u"Aim Constraint 的 World Up Object；是否使用取决于 worldUpType。"),
        "world_up_type": ("str", u"Aim Constraint 的 World Up 计算方式，例如 scene、object、objectrotation、vector 或 none。"),
        "matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。"),
        "offset_matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"用于保持 Driver 与 Driven 初始空间差异的 Offset Matrix。"),
        "parent_inverse_matrix": ("list[float] | maya.api.OpenMaya.MMatrix", u"Driven Parent Space 的 Inverse Matrix，用于把 World Matrix 转换到 Parent Space。"),

        # ------------------------------------------------------------------
        # Jnt / Skeleton
        # ------------------------------------------------------------------
        "joint": ("str", u"需要创建、查询、定向或驱动的 Maya Jnt 节点。"),
        "jnts": ("str | list[str]", u"需要批量处理的 Maya Jnt 节点或 Jnt Chain。"),
        "blueprint_jnts": ("str | list[str]", u"作为正式 Skeleton 构建来源的 Blueprint / Guide Jnt 列表。"),
        "jnt_parent": ("str | None", u"新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。"),
        "jnt_count": ("int", u"需要生成或重采样的 Jnt 数量。"),
        "mouth_jnt_number": ("int", u"嘴唇分布系统需要创建的 Jnt 总数量。"),
        "position": ("list[float] | tuple[float, float, float]", u"Jnt / Transform 使用的 XYZ Position。"),
        "rotation": ("list[float] | tuple[float, float, float]", u"Jnt / Transform 使用的 XYZ Rotation。"),
        "component": ("str", u"用于创建 Jnt 或查询位置的 Maya Component，例如 Vertex、CV 或 Edge。"),
        "match_rotation": ("bool", u"根据目标 Transform 创建 Jnt 时是否同时匹配目标 Rotation。"),
        "parent_chain": ("bool", u"创建多个 Jnt 时是否按输入顺序建立父子 Jnt Chain。"),
        "all_descendents": ("bool", u"Jnt 查询时是否包含当前节点以下的全部 Descendant Jnt。"),
        "include_descendents": ("bool", u"Jnt 查询或显示操作是否递归包含 Descendant Jnt。"),
        "visible": ("bool", u"Jnt / Guide / UI 元素是否保持可见。"),
        "secondary_axis_orient": ("str", u"Maya Jnt Orient 使用的 Secondary Axis World Orientation，例如 `yup`、`zdown`。"),
        "hide_blueprint": ("bool", u"生成正式 Skeleton 后是否隐藏 Blueprint / Guide Jnt。"),
        "name_prefix": ("str", u"批量创建 Jnt 时写入节点名称前部的 Prefix。"),

        # ------------------------------------------------------------------
        # Curve / Surface / Vector
        # ------------------------------------------------------------------
        "curve": ("str", u"用于采样、附着或驱动的 NURBS Curve Transform / Shape。"),
        "curves": ("str | list[str]", u"需要批量采样、附着或处理的 NURBS Curve。"),
        "parameter": ("float", u"NURBS Curve / Surface 参数空间中的 Parameter 值。"),
        "parameter_u": ("float", u"NURBS Surface U 方向 Parameter。"),
        "parameter_v": ("float", u"NURBS Surface V 方向 Parameter。"),
        "percentage": ("float", u"沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。"),
        "percent": ("float", u"沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。"),
        "degree": ("int", u"创建或重建 NURBS Curve 使用的 Degree。"),
        "form": ("int", u"NURBS Curve Form 枚举值，用于区分 Open、Closed 或 Periodic Curve。"),
        "world_position": ("list[float] | tuple[float, float, float]", u"用于 Curve 最近点、参数查询或节点放置的 World Space Position。"),
        "offset": ("float | list[float]", u"当前 Rig / Shape / Surface 操作使用的 Offset 数值或偏移向量。"),
        "offset_axis": ("str", u"应用 Surface / Attachment Offset 的轴向。"),
        "vector": ("list[float] | tuple[float, float, float]", u"参与方向、长度或向量计算的 XYZ Vector。"),
        "vector_a": ("list[float] | tuple[float, float, float]", u"向量计算中的第一个 XYZ Vector。"),
        "vector_b": ("list[float] | tuple[float, float, float]", u"向量计算中的第二个 XYZ Vector。"),
        "start_position": ("list[float] | tuple[float, float, float] | float", u"插值、Remap 或 Jnt 分布的起始位置 / 起始值。"),
        "end_position": ("list[float] | tuple[float, float, float] | float", u"插值、Remap 或 Jnt 分布的结束位置 / 结束值。"),
        "ratio": ("float", u"Start 与 End 之间的插值比例，通常为 0.0～1.0。"),

        # ------------------------------------------------------------------
        # Mesh / Model Check
        # ------------------------------------------------------------------
        "mesh": ("str", u"需要检查、复制、绑定或变形的 Mesh Transform / Shape。"),
        "meshes": ("str | list[str]", u"需要批量检查、清理或处理的 Mesh Transform / Shape 列表。"),
        "mesh_shape": ("str", u"需要拓扑、Normal 或 History 检查的 Mesh Shape 节点。"),
        "model": ("str", u"需要检查、复制、绑定或参与 Rig 的模型 Transform。"),
        "geometry": ("str", u"需要查询或绑定 SkinCluster / Deformer 的 Geometry Transform / Shape。"),
        "geometries": ("str | list[str]", u"需要批量查询 SkinCluster / Deformer 的 Geometry 列表。"),
        "geometry_or_skin_cluster": ("str", u"Geometry 或 skinCluster 节点；方法会先解析到对应 SkinCluster。"),
        "issue_type": ("str", u"模型检查结果的 Issue 类型标记，例如 NonManifold、History 或 Transform。"),
        "details": ("str | dict | list", u"模型检查 Issue 的详细节点、Component 或诊断数据。"),
        "fixable": ("bool", u"当前模型检查 Issue 是否支持由工具自动修复。"),
        "issue": ("dict | object", u"单条模型检查 Issue 数据。"),
        "issues": ("list", u"模型检查产生的 Issue 结果列表。"),
        "sample_limit": ("int", u"模型检查报告中单类问题最多展示的 Component 样本数量。"),
        "check_nonmanifold": ("bool", u"是否检查 Nonmanifold Vertex / Edge。"),
        "check_lamina": ("bool", u"是否检查 Lamina Face。"),
        "check_duplicates": ("bool", u"是否检查重复模型、重复 Shape 或重复命名问题。"),
        "check_history": ("bool", u"是否检查不需要的 Modeling History。"),
        "check_transform": ("bool", u"是否检查异常 Translate / Rotate / Scale / Pivot。"),
        "check_normals": ("bool", u"是否检查 Mesh Normal 方向和相关异常。"),

        # ------------------------------------------------------------------
        # SkinCluster / Weight
        # ------------------------------------------------------------------
        "skin_cluster": ("str", u"需要查询或编辑的 Maya skinCluster Deformer 节点。"),
        "influence": ("str", u"影响 SkinCluster 权重的 Influence Transform / Jnt。"),
        "influences": ("str | list[str]", u"影响 SkinCluster 的 Influence Jnt / Transform 列表。"),
        "weight": ("float", u"当前 Influence、Constraint Target 或 BlendShape Target 使用的权重值。"),
        "weights": ("list[float] | dict", u"需要读取、写入或传递的 Skin / Blend / Constraint 权重数据。"),
        "normalize": ("bool", u"写入 Skin Weight 后是否执行权重 Normalize，使 Influence Weight 总和符合 SkinCluster 设置。"),
        "maximum_influences": ("int", u"单个 Vertex 允许保留非零权重的最大 Influence 数量。"),

        # ------------------------------------------------------------------
        # BlendShape / Corrective
        # ------------------------------------------------------------------
        "blendshape": ("str", u"需要查询或编辑的 Maya blendShape Deformer 节点。"),
        "blendshape_node": ("str", u"需要查询或编辑的 Maya blendShape Deformer 节点。"),
        "base_model": ("str", u"BlendShape Deformer 使用的 Base Shape / Base Model。"),
        "target_model": ("str", u"需要添加、替换或查询的 BlendShape Target Shape。"),
        "target_transform": ("str", u"对应 BlendShape Target Shape 的 Transform 节点。"),
        "target_index": ("int", u"BlendShape Target 在 Weight / Target Group 中使用的逻辑索引。"),
        "target_weight": ("float", u"BlendShape Target 在指定 Target Group 中的权重位置。"),
        "corrective_meshes": ("str | list[str]", u"需要作为 Corrective Shape / BlendShape Target 处理的 Mesh 列表。"),

        # ------------------------------------------------------------------
        # Controller / Shape / Space
        # ------------------------------------------------------------------
        "control": ("str", u"需要创建、查询或修改的动画 Controller Transform。"),
        "controller": ("str", u"需要创建、查询或修改的动画 Controller Transform。"),
        "controls": ("str | list[str]", u"需要批量处理的动画 Controller Transform 列表。"),
        "control_set": ("str", u"创建后的 Controller 需要加入的 Maya Set 名称。"),
        "shape": ("str", u"Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。"),
        "shape_data_list": ("list[dict]", u"Controller Shape 的 CV、Degree、Form 等序列化数据列表。"),
        "color": ("int | tuple[float, float, float]", u"Viewport Override 使用的 Index Color 或 RGB Color。"),
        "radius": ("float", u"Jnt、Controller 或可视辅助对象使用的半径 / 尺寸。"),
        "scale_value": ("float | tuple[float, float, float]", u"Controller Shape CV 使用的统一或 XYZ Scale 值。"),
        "rotate_x": ("float", u"Controller Shape / Transform 绕 X 轴应用的旋转角度。"),
        "rotate_y": ("float", u"Controller Shape / Transform 绕 Y 轴应用的旋转角度。"),
        "rotate_z": ("float", u"Controller Shape / Transform 绕 Z 轴应用的旋转角度。"),
        "create_extra_groups": ("bool", u"是否创建 Zero、Driven、Space、Connect、Offset 等标准 Controller Extra Groups。"),
        "add_to_set": ("bool", u"是否把创建后的 Controller 加入指定 Controller Set。"),
        "constrain": ("bool", u"创建 Controller 后是否建立 Controller / Output 到 Target 的约束关系。"),
        "delete_previews": ("bool", u"写入正式 Controller Shape 资源前是否删除临时 Preview 节点。"),

        # ------------------------------------------------------------------
        # Face Guide / Face System
        # ------------------------------------------------------------------
        "guide": ("str", u"Face / Rig 定位系统中的 Guide Transform / Locator。"),
        "guides": ("str | list[str]", u"需要按顺序查询或传递给 Builder 的 Guide Transform / Locator 列表。"),
        "locator": ("str", u"Face Guide 系统中的 Locator Transform。"),
        "guide_root": ("str", u"当前 Guide 模板或 Guide System 的顶层 Root Group。"),
        "template_root": ("str", u"刚导入的 Face Guide 模板临时 Root，用于合并到正式 Guide Group。"),
        "imported_nodes": ("list[str]", u"本次导入 face_guide.ma 后 Maya 返回的新节点列表。"),
        "part": ("str", u"Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。"),
        "region": ("str", u"Face Component 的区域标记，例如 upper、lower、inner、outer。"),
        "feature": ("str", u"Face Component 的功能部位标记，例如 lid、bag、lip。"),
        "role": ("str", u"当前 Face Node 在构建网络中的角色标记，例如 bind、aim、attach、driver。"),
        "up_object": ("str", u"Eyelid / Radial Jnt Aim 系统用于稳定 Orientation 的 Up Object。"),
        "include_tokens": ("str | list[str] | None", u"Guide 名称必须包含的额外 Token；用于缩小部位查询范围。"),
        "exclude_tokens": ("str | list[str] | None", u"Guide 名称出现这些 Token 时排除该节点。"),
        "check_symmetry": ("bool", u"Guide Validation / Finalize 时是否同时检查 LF → RT 镜像节点、Parent 和连接。"),
        "work_model_name_dict": ("dict", u"Step 01 三个 Head Work Model（tweak / stretch / deform）的名称映射。"),
        "zip_offset": ("str", u"Zip Lip 网络中位于 Lip Jnt 上方、接收闭合 Matrix 结果的 Offset Transform。"),
        "remap_node": ("str", u"Zip / Falloff 计算使用的 remapValue 节点。"),
        "falloff": ("float", u"Zip Lip 或局部驱动沿嘴唇分布的衰减范围 / Falloff。"),

        # ------------------------------------------------------------------
        # Attr / Config
        # ------------------------------------------------------------------
        "attr_type": ("str", u"创建 Maya Attribute 使用的数据类型，例如 double、long、bool、string 或 message。"),
        "attrs_list": ("str | list[str]", u"需要批量查询、Lock、Hide 或处理的 Attribute 名称列表。"),
        "attrs_dict": ("dict", u"Attribute 名称到 Value / Config 数据的批量映射。"),
        "attr_types": ("dict | None", u"Attribute 名称到 Maya Attribute Type 的映射；未指定的属性由调用方默认规则处理。"),
        "default_value": ("object", u"新建 Attribute、UI 控件或 Rig 参数使用的默认值。"),
        "min_value": ("float | int | None", u"Attribute / UI 数值允许的最小值；None 表示不设置下限。"),
        "max_value": ("float | int | None", u"Attribute / UI 数值允许的最大值；None 表示不设置上限。"),
        "minimum": ("float | int", u"数值 Attribute、Remap 或 UI 控件使用的最小值。"),
        "maximum": ("float | int", u"数值 Attribute、Remap 或 UI 控件使用的最大值。"),
        "multi": ("bool", u"创建 Maya Attribute 时是否使用 Multi / Array Attribute。"),
        "lock": ("bool", u"是否 Lock 对应 Maya Channel / Attribute。"),
        "hide": ("bool", u"是否从 Channel Box 隐藏对应 Maya Attribute。"),
        "keyable": ("bool", u"对应 Maya Attribute 是否允许 Animator Keyframe。"),
        "clear_empty": ("bool", u"批量保存 Message / Config 时，空值是否主动断开旧连接。"),
        "information": ("dict | list | object", u"需要写入、恢复或应用到 Maya Attribute 的结构化信息。"),
        "attribute_info": ("dict", u"动画 / Attribute 数据中的单个 Attribute 描述、Key 或 Value 信息。"),
        "up": ("bool", u"是否把目标 Attribute 在 Channel Box 中上移。"),
        "down": ("bool", u"是否把目标 Attribute 在 Channel Box 中下移。"),

        # ------------------------------------------------------------------
        # Naming / Rename
        # ------------------------------------------------------------------
        "prefix": ("str", u"添加到 Maya 节点名称前部的 Prefix。"),
        "suffix": ("str", u"添加到 Maya 节点名称尾部的 Suffix。"),
        "search": ("str", u"节点名称中需要查找并替换的字符串。"),
        "replace": ("str", u"替换 Search 内容的新字符串。"),
        "search_text": ("str", u"名称过滤、工具搜索或 Search / Replace 使用的搜索文本。"),
        "replace_text": ("str", u"Search / Replace 操作中写回节点名称的新文本。"),
        "number": ("int", u"自动编号或字母编号转换使用的序号。"),
        "padding": ("int", u"数字编号输出时保留的位数，例如 3 表示 001。"),
        "number_type": ("str", u"自动编号格式，例如数字、字母或项目定义的编号模式。"),
        "uppercase": ("bool", u"字母编号是否输出为大写。"),
        "show_warning": ("bool", u"遇到无效命名或空输入时是否在 Maya 中显示 Warning。"),
        "function": ("str | callable", u"当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。"),

        # ------------------------------------------------------------------
        # Scene / File
        # ------------------------------------------------------------------
        "file_path": ("str", u"需要读取、写入、导入或导出的文件路径。"),
        "directory": ("str", u"需要扫描、创建或写入文件的目录路径。"),
        "extensions": ("str | list[str] | None", u"允许匹配的文件扩展名，例如 `.ma`、`.mb`、`.json`。"),
        "indent": ("int | None", u"写入 JSON 时使用的缩进空格数；None 表示紧凑输出。"),
        "ensure_ascii": ("bool", u"写 JSON 时是否把非 ASCII 字符转义。"),
        "sort_keys": ("bool", u"写 JSON 时是否按 Key 排序，便于版本控制 Diff。"),
        "data": ("dict | list | object", u"需要序列化、恢复或传递的结构化数据。"),
        "node_map": ("dict | None", u"源 Maya 节点名到目标 Maya 节点名的映射；常用于 Namespace / 动画数据恢复。"),
        "namespace": ("str | None", u"Reference / Import 或节点解析使用的 Maya Namespace。"),
        "ignore_version": ("bool", u"导入 / 打开 Maya Scene 时是否忽略文件版本警告。"),
        "group_reference": ("bool", u"Reference Scene 时是否把引用内容放入独立 Group。"),
        "long": ("bool", u"Maya 节点查询时是否返回完整 DAG Path。"),
        "flatten": ("bool", u"Maya Selection / Component 查询时是否展开 Range 为单独 Component。"),

        # ------------------------------------------------------------------
        # Cleanup
        # ------------------------------------------------------------------
        "selected_only": ("bool", u"清理 / 检查范围是否限制为当前 Maya Selection。"),
        "delete_empty": ("bool", u"场景清理时是否删除确认无 Child / Shape 的空 Transform。"),
        "delete_history_enabled": ("bool", u"清理流程是否执行 Modeling History 删除。"),
        "freeze_enabled": ("bool", u"清理流程是否执行 Freeze Transform。"),
        "unlock_enabled": ("bool", u"清理流程是否解除可安全处理的 Locked Channel。"),
        "center_pivot_enabled": ("bool", u"清理流程是否执行 Center Pivot。"),
        "delete_unknown_enabled": ("bool", u"清理流程是否删除确认无用的 Unknown Node。"),

        # ------------------------------------------------------------------
        # UI / Tool Dispatch
        # ------------------------------------------------------------------
        "tool_key": ("str", u"Tool Registry / Window Manager 中唯一识别工具的 Key。"),
        "tool_function": ("callable", u"执行当前工具功能的 Callable。"),
        "tool_module": ("module | object", u"已经加载的工具 Python Module，用于调用其公开入口。"),
        "run_callback": ("callable", u"用户触发按钮或 Tool Item 时执行的回调函数。"),
        "tools_dict": ("dict", u"Tool Key 到工具元数据、入口和分类信息的 Registry 字典。"),
        "refresh_registry": ("bool", u"打开 / 刷新 Toolbox 前是否重新扫描 Tool Registry。"),
        "test_window_manager": ("bool", u"包初始化阶段是否运行 Window Manager 自检。"),
        "widget": ("QtWidgets.QWidget", u"需要应用 MuziTools Theme / UI 状态的 Qt Widget。"),
        "button": ("QtWidgets.QPushButton", u"需要应用 MuziTools Button 样式或状态的 QPushButton。"),
        "line_edit": ("QtWidgets.QLineEdit", u"需要应用 MuziTools 输入框样式的 QLineEdit。"),
        "event": ("QtCore.QEvent | object", u"Qt Event 回调传入的事件对象。"),
        "label": ("str", u"UI、Rig Node 或日志中展示的简短 Label。"),
        "label_text": ("str", u"Object Picker 左侧显示的 Label 文本。"),
        "title": ("str", u"窗口、Section、Dialog 或报告使用的标题文本。"),
        "description": ("str", u"UI Step / Section 中展示的功能说明文本。"),
        "placeholder": ("str", u"QLineEdit / Object Picker 在没有输入时显示的 Placeholder 文本。"),
        "text_value": ("str", u"需要显示、验证或写入 Qt 文本控件的字符串。"),
        "slider_value": ("int | float", u"UI Slider 当前值；回调用于同步对应 Rig / Setup 参数。"),
        "margins": ("tuple[int, int, int, int]", u"Qt Layout 的 Left / Top / Right / Bottom Contents Margins。"),
        "spacing": ("int", u"Qt Layout 中相邻控件之间的间距。"),
        "minimum_width": ("int", u"Qt Widget / Dialog 的最小宽度。"),
        "node_types": ("str | list[str] | None", u"Object Picker 允许选择的 Maya Node Type；None 表示不限制类型。"),
        "role": ("str", u"当前 UI / Rig 元素的语义角色，用于命名、Style 或构建分类。"),
        "active": ("bool", u"Button / UI State 当前是否处于 Active 状态。"),
        "enabled": ("bool", u"当前 UI 控件或 Rig 功能是否启用。"),

        # ------------------------------------------------------------------
        # General build / status
        # ------------------------------------------------------------------
        "node_type": ("str", u"需要创建、查询或过滤的 Maya Node Type。"),
        "parent_group": ("str | None", u"新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。"),
        "force": ("bool", u"是否强制覆盖已有连接、属性值或构建结果。"),
        "required": ("bool", u"节点或数据缺失时是否直接抛出异常，而不是返回空结果。"),
        "strict": ("bool", u"是否按严格模式处理无效输入和缺失数据。"),
        "world_space": ("bool", u"是否使用 Maya World Space，而不是 Local / Parent Space。"),
        "world_orient": ("bool", u"创建 Extra Group 时是否使用 World Orientation，而不是继承目标对象旋转。"),
        "refresh": ("bool", u"读取数据前是否先从 Maya Scene / Config 重新刷新缓存。"),
        "completed": ("bool", u"当前 Face Wizard / Build Step 是否标记为已完成。"),
        "step_value": ("int", u"Face Wizard / Build Pipeline 当前 Step 编号。"),
        "last_step": ("int", u"Step 状态查询或失效处理时的最后一个 Step 编号。"),
        "kwargs": ("dict", u"继续传递给底层 maya.cmds、Qt 或 Builder API 的关键字参数。"),
        "default": ("object", u"当前查询、配置或 UI 逻辑在没有显式值时使用的默认值。"),
        "result": ("object", u"上一步 Maya / Tool 操作返回的结果数据。"),
        "hierarchy": ("bool | str", u"Jnt Tool 当前是否按 Skeleton Hierarchy 工作，或用于指定层级范围。"),
        "all_jnts": ("str | list[str]", u"当前 Jnt Tool 已解析出的完整 Jnt 列表。"),
    }

    return rules


def infer_semantic_info(parameter_name, current_type):
    u"""根据参数名和已有类型推断更明确的 Maya / Rigging 说明。"""
    name = parameter_name.lower()
    exact_rules = get_exact_semantic_rules()

    if name in exact_rules:
        return exact_rules[name]

    if name.endswith("_path"):
        return "str", u"需要读取、写入、导入或导出的文件 / 资源路径。"

    if name.endswith("_name"):
        return "str", u"创建、查询或匹配 Maya 节点 / Rig 元素时使用的名称。"

    if name.endswith("_index"):
        return "int", u"对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。"

    if name.endswith("_count") or name.endswith("_number"):
        return "int", u"当前构建、采样或查询过程使用的元素数量。"

    if name.endswith("_radius"):
        return "float", u"当前 Jnt、Controller 或辅助对象使用的半径。"

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

    if name.endswith("_jnt"):
        return "str", u"当前 Rig 计算或构建使用的 Maya Jnt 节点。"

    if name.endswith("_curve"):
        return "str", u"当前采样、附着或驱动使用的 NURBS Curve。"

    if name.endswith("_model") or name.endswith("_mesh"):
        return "str", u"当前检查、绑定、复制或变形使用的模型 / Mesh 节点。"

    if name.endswith("_guide") or name.endswith("_locator"):
        return "str", u"当前 Rig 定位流程使用的 Guide / Locator Transform。"

    if name.endswith("_ctrl") or name.endswith("_control") or name.endswith("_controller"):
        return "str", u"当前 Rig 操作或驱动使用的动画 Controller Transform。"

    if name.endswith("_dict") or name.endswith("_map"):
        return "dict", u"当前方法使用的结构化配置 / 映射数据。"

    if name.endswith("_list"):
        return "list", u"当前方法需要保持顺序批量处理的数据列表。"

    if name.startswith("check_"):
        return "bool", u"是否执行 `{}` 对应的 Maya / Rig Validation 项。".format(
            parameter_name
        )

    if name.startswith("delete_"):
        return "bool", u"当前清理 / 重建流程是否执行 `{}` 对应的删除步骤。".format(
            parameter_name
        )

    if name.startswith("is_") or name.startswith("has_") or name.startswith("use_"):
        return "bool", u"控制 `{}` 所代表的 Maya / Rig 状态是否启用。".format(
            parameter_name
        )

    normalized_type = current_type.lower()

    if "bool" in normalized_type:
        return current_type, u"控制当前方法中的 `{}` 选项是否启用。".format(
            parameter_name
        )

    if "int" in normalized_type:
        return current_type, u"当前 Maya / Rig 操作使用的 `{}` 整数参数。".format(
            parameter_name
        )

    if "float" in normalized_type:
        return current_type, u"当前 Maya / Rig 计算使用的 `{}` 数值参数。".format(
            parameter_name
        )

    if "dict" in normalized_type:
        return current_type, u"当前方法使用的 `{}` 配置 / 映射数据。".format(
            parameter_name
        )

    if "list" in normalized_type or "tuple" in normalized_type:
        return current_type, u"当前方法按顺序处理的 `{}` 数据集合。".format(
            parameter_name
        )

    if "str" in normalized_type:
        return current_type, u"当前 Maya / Rig 操作使用的 `{}` 名称或标记。".format(
            parameter_name
        )

    return current_type or "object", u"当前方法执行 Maya / Rig 操作时使用的 `{}` 数据。".format(
        parameter_name
    )


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
        match = argument_line_pattern.match(
            line
        )

        if not match:
            line_index += 1
            continue

        indent = match.group(1)
        parameter_name = match.group(2)
        current_type = match.group(3).strip()
        description_index = line_index + 1

        if description_index >= len(lines):
            line_index += 1
            continue

        description_line = lines[description_index]
        description = description_line.strip()

        if not is_generic_description(description):
            line_index += 1
            continue

        semantic_type, semantic_description = infer_semantic_info(
            parameter_name,
            current_type
        )

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
