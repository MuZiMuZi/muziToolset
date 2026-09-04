# coding=utf-8
u"""
Architecture Cleanup Phase 2
============================

一次性架构迁移脚本。

目标：
    1. 删除 Controller / FaceGuide / Core 中已经只剩转发作用的兼容 Helper；
    2. 把 Generic DAG / Scene / Transform / Constraint 能力统一收回 Core；
    3. 让 Face Rig UI 正式使用 StepBase.run_step()；
    4. 清空 Upper Layer Compatibility Allowlist；
    5. 增加 Core Single Source Gate 与 Maya 2023 Smoke Contract；
    6. 保留业务算法，不做无关格式化。

本脚本使用 AST 删除明确指定的 Function / Method，并对少量稳定代码片段做严格替换。
任何预期结构缺失都会直接失败，避免静默写坏最新 main。
"""

from __future__ import print_function

import ast
import os


REPOSITORY_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


def get_path(relative_path):
    return os.path.join(
        REPOSITORY_ROOT,
        relative_path.replace("/", os.sep)
    )


def read_text(relative_path):
    with open(
            get_path(relative_path),
            "r",
            encoding="utf-8"
    ) as file_object:
        return file_object.read()


def write_text(relative_path, source_text):
    with open(
            get_path(relative_path),
            "w",
            encoding="utf-8",
            newline="\n"
    ) as file_object:
        file_object.write(source_text)


def replace_required(source_text, old_text, new_text, label, expected_count=1):
    actual_count = source_text.count(old_text)

    if actual_count != expected_count:
        raise RuntimeError(
            u"{} 替换数量异常：expected={} actual={}".format(
                label,
                expected_count,
                actual_count
            )
        )

    return source_text.replace(
        old_text,
        new_text
    )


def remove_definition(source_text, function_name, class_name=None):
    syntax_tree = ast.parse(source_text)
    target_node = None

    if class_name is None:
        for node in syntax_tree.body:
            if not isinstance(
                    node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue

            if node.name == function_name:
                target_node = node
                break
    else:
        for node in syntax_tree.body:
            if not isinstance(node, ast.ClassDef):
                continue

            if node.name != class_name:
                continue

            for child_node in node.body:
                if not isinstance(
                        child_node,
                        (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    continue

                if child_node.name == function_name:
                    target_node = child_node
                    break

            break

    if target_node is None:
        target_label = function_name

        if class_name is not None:
            target_label = "{}.{}".format(
                class_name,
                function_name
            )

        raise RuntimeError(
            u"找不到需要删除的定义：{}".format(
                target_label
            )
        )

    start_line = target_node.lineno

    if target_node.decorator_list:
        for decorator in target_node.decorator_list:
            if decorator.lineno < start_line:
                start_line = decorator.lineno

    end_line = target_node.end_lineno
    source_lines = source_text.splitlines(True)

    del source_lines[start_line - 1:end_line]

    # 删除定义后最多吞掉一个紧邻空行，保留正常模块 / 类方法间距。
    remove_index = start_line - 1

    if remove_index < len(source_lines):
        if not source_lines[remove_index].strip():
            del source_lines[remove_index]

    return "".join(source_lines)


def add_import_after(source_text, existing_import, new_import, label):
    if new_import in source_text:
        return source_text

    return replace_required(
        source_text,
        existing_import,
        existing_import + new_import,
        label
    )


def update_scene_utils():
    path = "core/scene_utils.py"
    source_text = read_text(path)

    source_text = replace_required(
        source_text,
        "def validate_node(node):\n",
        "def validate_node(node, label=None):\n",
        "scene_utils.validate_node signature"
    )

    source_text = replace_required(
        source_text,
        "        node (str):\n            需要查询或处理的 Maya 节点名称。\n\n    Returns:\n",
        "        node (str):\n            需要查询或处理的 Maya 节点名称。\n        label (str | None):\n            可选错误提示名称，例如 Driver、Controller、父节点。\n\n    Returns:\n",
        "scene_utils.validate_node Args"
    )

    source_text = replace_required(
        source_text,
        "    # 步骤 1：空名称没有任何查询意义，直接报错。\n    if not node:\n        raise RuntimeError(u\"节点名称不能为空。\")\n\n    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n    if not cmds.objExists(node):\n        raise RuntimeError(\n            u\"Maya 节点不存在：{}\".format(node)\n        )\n",
        "    display_label = label or u\"Maya 节点\"\n\n    # 步骤 1：空名称没有任何查询意义，直接报错。\n    if not node:\n        raise RuntimeError(\n            u\"{}名称不能为空。\".format(\n                display_label\n            )\n        )\n\n    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n    if not cmds.objExists(node):\n        raise RuntimeError(\n            u\"{}不存在：{}\".format(\n                display_label,\n                node\n            )\n        )\n",
        "scene_utils.validate_node body"
    )

    write_text(path, source_text)


def update_hierarchy_utils():
    path = "core/hierarchy_utils.py"
    source_text = read_text(path)

    source_text = remove_definition(
        source_text,
        "_validate_node",
        class_name="Hierarchy"
    )

    source_text = source_text.replace(
        "Hierarchy._validate_node(",
        "scene_utils.validate_node("
    )

    marker = (
        "    @staticmethod\n"
        "    def get_parent(node, full_path=True):\n"
    )

    method_text = (
        "    @staticmethod\n"
        "    def get_dag_depth(node):\n"
        "        u\"\"\"\n"
        "        返回唯一 DAG Long Path 的层级深度。\n\n"
        "        Args:\n"
        "            node (str):\n"
        "                需要查询层级深度的 Maya DAG 节点。\n\n"
        "        Returns:\n"
        "            int:\n"
        "                Root 为 1，层级越深数值越大。\n"
        "        \"\"\"\n"
        "        long_name = scene_utils.get_long_name(\n"
        "            node\n"
        "        )\n\n"
        "        if not long_name:\n"
        "            return 0\n\n"
        "        depth = long_name.count(\"|\")\n\n"
        "        if depth <= 0:\n"
        "            return 0\n\n"
        "        return depth\n\n"
        "    @staticmethod\n"
        "    def get_parent(node, full_path=True):\n"
    )

    source_text = replace_required(
        source_text,
        marker,
        method_text,
        "hierarchy_utils.get_dag_depth"
    )

    source_text = source_text.replace(
        "Hierarchy.get_parent(node, full_path=True)\n    返回节点直接 Parent。\n",
        "Hierarchy.get_dag_depth(node)\n    返回 DAG Long Path 层级深度。\n\nHierarchy.get_parent(node, full_path=True)\n    返回节点直接 Parent。\n"
    )

    write_text(path, source_text)


def update_name_utils():
    path = "core/name_utils.py"
    source_text = read_text(path)

    source_text = add_import_after(
        source_text,
        "from . import scene_utils\n",
        "from . import hierarchy_utils\n",
        "name_utils hierarchy import"
    )

    source_text = remove_definition(
        source_text,
        "maya_undo"
    )
    source_text = remove_definition(
        source_text,
        "dag_depth"
    )

    source_text = source_text.replace(
        "@maya_undo",
        "@scene_utils.undo_chunk"
    )
    source_text = source_text.replace(
        "key=dag_depth",
        "key=hierarchy_utils.Hierarchy.get_dag_depth"
    )

    source_text = source_text.replace(
        "maya_undo(function)\n    兼容旧装饰器名称；底层统一使用 scene_utils.undo_chunk，不再维护第二套 Undo 实现。\n\n",
        ""
    )

    source_text = source_text.replace(
        "    \"maya_undo\",\n",
        ""
    )
    source_text = source_text.replace(
        "    \"dag_depth\",\n",
        ""
    )

    write_text(path, source_text)


def update_constraint_utils():
    path = "core/constraint_utils.py"
    source_text = read_text(path)

    source_text = remove_definition(
        source_text,
        "validate_node"
    )
    source_text = source_text.replace(
        "    \"validate_node\",\n",
        ""
    )

    write_text(path, source_text)


def update_matrix_utils():
    path = "core/matrix_utils.py"
    source_text = read_text(path)

    source_text = remove_definition(
        source_text,
        "get_parent"
    )

    source_text = replace_required(
        source_text,
        "    driven_parent = get_parent(\n        driven\n    )\n",
        "    driven_parent = hierarchy_utils.Hierarchy.get_parent(\n        driven,\n        full_path=True\n    )\n",
        "matrix_utils parent query"
    )

    source_text = source_text.replace(
        "    \"get_parent\",\n",
        ""
    )

    write_text(path, source_text)


def update_controller_builder():
    path = "systems/controller/builder.py"
    source_text = read_text(path)

    source_text = add_import_after(
        source_text,
        "from ...core import control_shape_utils\n",
        "from ...core import constraint_utils\n",
        "controller constraint import"
    )

    source_text = remove_definition(
        source_text,
        "get_short_name"
    )

    source_text = replace_required(
        source_text,
        "    short_name = get_short_name(\n        target\n    )\n",
        "    short_name = rename_utils.get_short_name(\n        target\n    )\n    short_name = short_name.replace(\n        \":\",\n        \"_\"\n    )\n",
        "controller target short name"
    )

    source_text = replace_required(
        source_text,
        "            cmds.parentConstraint(\n                control,\n                target,\n                maintainOffset=False\n            )\n",
        "            constraint_utils.create_constraint(\n                driver_objects=control,\n                driven_object=target,\n                constraint_type=\"parentConstraint\",\n                maintain_offset=False\n            )\n",
        "controller FK constraint"
    )

    source_text = source_text.replace(
        "    \"get_short_name\",\n",
        ""
    )

    write_text(path, source_text)


def update_controller_space_blend():
    path = "systems/controller/space_blend.py"
    source_text = read_text(path)

    source_text = remove_definition(
        source_text,
        "get_short_name"
    )
    source_text = remove_definition(
        source_text,
        "validate_node"
    )

    source_text = source_text.replace(
        "get_short_name(",
        "rename_utils.get_short_name("
    )
    source_text = source_text.replace(
        "validate_node(",
        "scene_utils.validate_node("
    )

    source_text = source_text.replace(
        "    \"get_short_name\",\n",
        ""
    )
    source_text = source_text.replace(
        "    \"validate_node\",\n",
        ""
    )

    source_text = source_text.replace(
        "# Name\n",
        "# Naming\n"
    )
    source_text = source_text.replace(
        "# Validate - Compatibility\n# =============================================================================\n\n",
        ""
    )

    write_text(path, source_text)


def update_face_guide():
    path = "systems/face/face_guide.py"
    source_text = read_text(path)

    methods_to_remove = [
        "get_short_name",
        "get_dag_depth",
        "get_parent",
        "get_world_position",
        "build",
        "finalize",
    ]

    for method_name in methods_to_remove:
        source_text = remove_definition(
            source_text,
            method_name,
            class_name="FaceGuide"
        )

    source_text = source_text.replace(
        "self.get_short_name(",
        "rename_utils.get_short_name("
    )
    source_text = source_text.replace(
        "self.get_parent(",
        "hierarchy_utils.Hierarchy.get_parent("
    )
    source_text = source_text.replace(
        "self.get_world_position(",
        "transform_utils.get_world_translation("
    )
    source_text = source_text.replace(
        "key=self.get_dag_depth",
        "key=hierarchy_utils.Hierarchy.get_dag_depth"
    )

    compatibility_text = (
        "\n兼容：\n"
        "    - build() 保留为旧入口，内部只转调 build_guide()；\n"
        "    - finalize() 保留为旧入口，内部转调统一 run_step()；\n"
        "    - mirror_left_guide() / mirror_left_guides() 继续保留 Repair Symmetry 兼容 API。\n"
    )
    source_text = source_text.replace(
        compatibility_text,
        ""
    )

    source_text = source_text.replace(
        "    # =========================================================================\n    # Compatibility Entry\n    # =========================================================================\n\n",
        ""
    )

    write_text(path, source_text)


def update_face_setup():
    path = "systems/face/face_setup.py"
    source_text = read_text(path)

    source_text = remove_definition(
        source_text,
        "build",
        class_name="FaceSetup"
    )

    write_text(path, source_text)


def update_face_rig_ui():
    path = "systems/face/face_rig_ui.py"
    source_text = read_text(path)

    source_text = source_text.replace(
        "FaceSetup.build()",
        "FaceSetup.run_step()"
    )
    source_text = source_text.replace(
        "FaceGuide.build()",
        "FaceGuide.build_guide()"
    )
    source_text = source_text.replace(
        "FaceGuide.finalize()",
        "FaceGuide.run_step()"
    )

    source_text = replace_required(
        source_text,
        "            face_setup.build()\n",
        "            face_setup.run_step()\n",
        "Face UI Step01 run_step"
    )

    source_text = replace_required(
        source_text,
        "            result = face_guide.build()\n",
        "            result = face_guide.build_guide()\n",
        "Face UI Step02 build_guide"
    )

    source_text = replace_required(
        source_text,
        "            validation = face_guide.finalize(\n                check_symmetry=True\n            )\n",
        "            face_guide.check_symmetry = True\n            face_guide.run_step()\n            validation = face_guide.validation_result\n",
        "Face UI Step02 run_step"
    )

    write_text(path, source_text)


def update_upper_layer_gate():
    path = "tests/system_core_reuse_gate_test.py"
    source_text = read_text(path)

    source_text = source_text.replace(
        "静态检查 ``systems/`` 与 ``tools/`` 是否重新实现已经有明确 Core 归属的通用 Helper。",
        "静态检查 ``systems/``、``tools/`` 与 ``ui/`` 是否绕开已经有明确 Core 归属的通用能力。"
    )
    source_text = source_text.replace(
        "    _world_position()\n",
        "    get_parent()\n    get_long_name()\n    get_world_position()\n    get_world_translation()\n    get_world_rotation()\n"
    )

    source_text = replace_required(
        source_text,
        "    return [\n        \"systems\",\n        \"tools\",\n    ]\n",
        "    return [\n        \"systems\",\n        \"tools\",\n        \"ui\",\n    ]\n",
        "upper gate scan roots"
    )

    old_forbidden = (
        "    return {\n"
        "        \"validate_node\",\n"
        "        \"_validate_node\",\n"
        "        \"validate_transform\",\n"
        "        \"get_short_name\",\n"
        "        \"_short_name\",\n"
        "        \"_ensure_group\",\n"
        "        \"_world_position\",\n"
        "    }\n"
    )

    new_forbidden = (
        "    return {\n"
        "        \"validate_node\",\n"
        "        \"_validate_node\",\n"
        "        \"validate_transform\",\n"
        "        \"get_short_name\",\n"
        "        \"_short_name\",\n"
        "        \"get_long_name\",\n"
        "        \"_get_long_name\",\n"
        "        \"get_parent\",\n"
        "        \"_get_parent\",\n"
        "        \"get_world_position\",\n"
        "        \"_world_position\",\n"
        "        \"get_world_translation\",\n"
        "        \"_get_world_translation\",\n"
        "        \"get_world_rotation\",\n"
        "        \"_get_world_rotation\",\n"
        "        \"get_dag_depth\",\n"
        "        \"_ensure_group\",\n"
        "    }\n"
    )

    source_text = replace_required(
        source_text,
        old_forbidden,
        new_forbidden,
        "upper gate forbidden names"
    )

    source_text = remove_definition(
        source_text,
        "get_compatibility_allowlist"
    )

    source_text = replace_required(
        source_text,
        "    allowlist = get_compatibility_allowlist()\n    allowed_names = allowlist.get(\n        relative_path,\n        set()\n    )\n\n",
        "",
        "upper gate allowlist variables"
    )

    source_text = replace_required(
        source_text,
        "        if function_name in allowed_names:\n            continue\n\n",
        "",
        "upper gate allowlist branch"
    )

    source_text = source_text.replace(
        "当前 Compatibility Allowlist\n-----------------------------\n少量历史公开 API 目前仍作为薄兼容入口存在，但内部必须转发 Core。\n这些入口暂时列入 Allowlist；后续完成 API 迁移后应继续缩小 Allowlist，而不是新增条目。\n",
        "Compatibility Policy\n--------------------\n正式上层代码不保留 Generic Core Helper Allowlist。历史入口完成迁移后直接删除。\n"
    )

    source_text = source_text.replace(
        "遍历 systems / tools 下全部正式 Python 文件。",
        "遍历 systems / tools / ui 下全部正式 Python 文件。"
    )
    source_text = source_text.replace(
        "System / Tool",
        "System / Tool / UI"
    )
    source_text = source_text.replace(
        "49 个 System / Tool Python 文件",
        "49 个 System / Tool / UI Python 文件"
    )

    # 在 scan_file 中增加高确定性 cmds 绕过检查：Undo 与 Constraint Creation。
    scan_marker = (
        "    for node in ast.walk(syntax_tree):\n"
        "        if not isinstance(\n"
        "                node,\n"
        "                (ast.FunctionDef, ast.AsyncFunctionDef)\n"
        "        ):\n"
        "            continue\n\n"
        "        function_name = node.name\n\n"
        "        if function_name not in forbidden_names:\n"
        "            continue\n\n"
        "        issues.append({\n"
        "            \"file\": relative_path,\n"
        "            \"line\": getattr(\n"
        "                node,\n"
        "                \"lineno\",\n"
        "                None\n"
        "            ),\n"
        "            \"name\": function_name,\n"
        "        })\n\n"
        "    return issues\n"
    )

    scan_replacement = (
        "    for node in ast.walk(syntax_tree):\n"
        "        if isinstance(\n"
        "                node,\n"
        "                (ast.FunctionDef, ast.AsyncFunctionDef)\n"
        "        ):\n"
        "            function_name = node.name\n\n"
        "            if function_name in forbidden_names:\n"
        "                issues.append({\n"
        "                    \"file\": relative_path,\n"
        "                    \"line\": getattr(\n"
        "                        node,\n"
        "                        \"lineno\",\n"
        "                        None\n"
        "                    ),\n"
        "                    \"name\": function_name,\n"
        "                    \"kind\": \"helper\",\n"
        "                })\n\n"
        "        if not isinstance(node, ast.Call):\n"
        "            continue\n\n"
        "        call_function = node.func\n\n"
        "        if not isinstance(call_function, ast.Attribute):\n"
        "            continue\n\n"
        "        if not isinstance(call_function.value, ast.Name):\n"
        "            continue\n\n"
        "        if call_function.value.id != \"cmds\":\n"
        "            continue\n\n"
        "        command_name = call_function.attr\n\n"
        "        if command_name == \"undoInfo\":\n"
        "            issues.append({\n"
        "                \"file\": relative_path,\n"
        "                \"line\": getattr(node, \"lineno\", None),\n"
        "                \"name\": \"cmds.undoInfo\",\n"
        "                \"kind\": \"core_bypass\",\n"
        "            })\n"
        "            continue\n\n"
        "        constraint_commands = {\n"
        "            \"parentConstraint\",\n"
        "            \"pointConstraint\",\n"
        "            \"orientConstraint\",\n"
        "            \"scaleConstraint\",\n"
        "            \"aimConstraint\",\n"
        "            \"poleVectorConstraint\",\n"
        "        }\n\n"
        "        if command_name not in constraint_commands:\n"
        "            continue\n\n"
        "        is_query = False\n\n"
        "        for keyword in node.keywords:\n"
        "            if keyword.arg not in [\"query\", \"q\"]:\n"
        "                continue\n\n"
        "            if isinstance(keyword.value, ast.Constant):\n"
        "                is_query = bool(keyword.value.value)\n\n"
        "        if is_query:\n"
        "            continue\n\n"
        "        issues.append({\n"
        "            \"file\": relative_path,\n"
        "            \"line\": getattr(node, \"lineno\", None),\n"
        "            \"name\": \"cmds.{}\".format(command_name),\n"
        "            \"kind\": \"core_bypass\",\n"
        "        })\n\n"
        "    return issues\n"
    )

    source_text = replace_required(
        source_text,
        scan_marker,
        scan_replacement,
        "upper gate AST scan"
    )

    source_text = source_text.replace(
        "u\"[FAIL] {}:{} | 上层代码重新实现通用 Helper: {}\".format(",
        "u\"[FAIL] {}:{} | 上层代码绕开 Core: {}\".format("
    )

    write_text(path, source_text)


def create_core_single_source_gate():
    path = "tests/core_single_source_gate_test.py"

    source_text = r'''# coding=utf-8
u"""
Core Single Source Gate
=======================

检查 core/ 中高确定性的 Generic 能力只有一个正式实现位置。

本测试只扫描模块顶层 Function，不限制 Jnt / Hierarchy 等领域类自己的业务 Method。
"""

from __future__ import print_function

import ast
import os


OWNER_BY_FUNCTION = {
    "undo_chunk": "core/scene_utils.py",
    "validate_node": "core/scene_utils.py",
    "get_long_name": "core/scene_utils.py",
    "get_short_name": "core/rename_utils.py",
    "validate_transform": "core/transform_utils.py",
    "get_world_translation": "core/transform_utils.py",
    "set_world_translation": "core/transform_utils.py",
    "get_world_rotation": "core/transform_utils.py",
    "set_world_rotation": "core/transform_utils.py",
}

FORBIDDEN_TOP_LEVEL_COMPATIBILITY_FUNCTIONS = {
    "get_parent",
    "get_world_position",
    "maya_undo",
    "dag_depth",
}


def get_package_root():
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(tests_directory)


def iter_core_python_files():
    core_root = os.path.join(
        get_package_root(),
        "core"
    )

    for file_name in os.listdir(core_root):
        if not file_name.endswith(".py"):
            continue

        yield os.path.join(
            core_root,
            file_name
        )


def get_relative_path(file_path):
    relative_path = os.path.relpath(
        file_path,
        get_package_root()
    )
    return relative_path.replace(os.sep, "/")


def scan_file(file_path):
    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        source_text = source_file.read()

    syntax_tree = ast.parse(
        source_text,
        filename=file_path
    )
    relative_path = get_relative_path(file_path)
    issues = []

    for node in syntax_tree.body:
        if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue

        function_name = node.name

        if function_name in OWNER_BY_FUNCTION:
            owner_path = OWNER_BY_FUNCTION[function_name]

            if relative_path != owner_path:
                issues.append({
                    "file": relative_path,
                    "line": node.lineno,
                    "name": function_name,
                    "owner": owner_path,
                })

        if function_name in FORBIDDEN_TOP_LEVEL_COMPATIBILITY_FUNCTIONS:
            issues.append({
                "file": relative_path,
                "line": node.lineno,
                "name": function_name,
                "owner": "领域 Core API",
            })

    return issues


def run():
    print("=" * 78)
    print("Muzi Toolset - Core Single Source Gate")
    print("=" * 78)

    issues = []
    file_count = 0

    for file_path in iter_core_python_files():
        file_count += 1
        file_issues = scan_file(file_path)

        for issue in file_issues:
            issues.append(issue)

    if issues:
        for issue in issues:
            print(
                u"[FAIL] {}:{} | {} 应统一归属 {}".format(
                    issue["file"],
                    issue["line"],
                    issue["name"],
                    issue["owner"]
                )
            )

        return False

    print(
        u"[PASS] {} 个 Core Python 文件符合 Single Source 规则。".format(
            file_count
        )
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
'''

    write_text(path, source_text)


def create_maya2023_smoke_test():
    path = "tests/maya2023_smoke_test.py"

    source_text = r'''# coding=utf-8
u"""
Maya 2023 Runtime Smoke Test
============================

在真正 Autodesk Maya 2023 / mayapy 进程中运行的总 Smoke Runner。

推荐运行：

    import muziToolset.tests.maya2023_smoke_test as smoke
    result = smoke.run()

测试使用临时 Namespace，不保存 Scene。建议在空场景或 mayapy 中运行。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import hierarchy_utils
from ..core import rename_utils
from ..core import scene_utils
from ..core import transform_utils
from ..systems import controller as controller_system
from ..systems import face as face_system
from . import face_component_smoke_test


def create_namespace():
    token = uuid.uuid4().hex[:8]
    namespace = "muziMaya2023Smoke_{}".format(token)
    cmds.namespace(add=namespace)
    cmds.namespace(set=namespace)
    return namespace


def remove_namespace(namespace):
    try:
        cmds.namespace(set=":")
    except Exception:
        pass

    if not cmds.namespace(exists=namespace):
        return

    try:
        cmds.namespace(
            removeNamespace=namespace,
            deleteNamespaceContent=True
        )
    except Exception as error:
        cmds.warning(
            u"无法删除 Maya 2023 Smoke Namespace {}：{}".format(
                namespace,
                error
            )
        )


def require_maya_2023():
    version = str(cmds.about(version=True))

    if not version.startswith("2023"):
        raise RuntimeError(
            u"本 Smoke Runner 要求 Maya 2023，当前版本：{}".format(
                version
            )
        )

    return version


def test_core_contract(root_group):
    parent_node = cmds.createNode(
        "transform",
        name="grp_md_core_parent_smoke_001",
        parent=root_group
    )
    child_node = cmds.createNode(
        "transform",
        name="grp_md_core_child_smoke_001"
    )

    scene_utils.validate_node(
        parent_node,
        label=u"Smoke Parent"
    )

    hierarchy_utils.Hierarchy.parent(
        child_node,
        parent_node
    )

    queried_parent = hierarchy_utils.Hierarchy.get_parent(
        child_node,
        full_path=True
    )

    if rename_utils.get_short_name(queried_parent) != rename_utils.get_short_name(parent_node):
        raise RuntimeError(u"Hierarchy Core Parent 查询结果错误。")

    transform_utils.set_world_translation(
        child_node,
        [1.0, 2.0, 3.0]
    )
    position = transform_utils.get_world_translation(
        child_node
    )

    if len(position) != 3:
        raise RuntimeError(u"Transform Core World Translation 返回格式错误。")

    return u"Scene / Hierarchy / Transform / Rename Core 正常"


def test_controller_contract(root_group):
    target = cmds.createNode(
        "transform",
        name="jnt_lf_controller_target_smoke_001",
        parent=root_group
    )

    result = controller_system.create_controller(
        name="ctrl_lf_controller_smoke_001",
        shape="circle",
        radius=0.5,
        axis="Y+",
        target=target,
        color=6,
        create_sub_control=False,
        create_extra_groups=True,
        add_to_set=True
    )

    required_keys = [
        "control",
        "output",
        "top_group",
        "groups",
    ]

    for key in required_keys:
        if key not in result:
            raise RuntimeError(
                u"Controller Result 缺少 Key：{}".format(key)
            )

    scene_utils.validate_node(result["control"])
    scene_utils.validate_node(result["output"])
    scene_utils.validate_node(result["top_group"])

    return u"Controller System 标准层级创建正常"


def test_face_step_contract(root_group):
    head_model = cmds.polySphere(
        name="model_md_head_smoke_001",
        radius=2.0
    )[0]
    head_model = hierarchy_utils.Hierarchy.parent(
        head_model,
        root_group
    )

    face_setup = face_system.FaceSetup(
        face_head_model=head_model,
        mouth_jnt_number=32
    )
    face_setup.run_step()

    if not face_setup.is_step_completed(step_value=1):
        raise RuntimeError(u"FaceSetup.run_step() 没有完成 Step 01。")

    face_guide = face_system.FaceGuide()

    if not callable(getattr(face_guide, "run_step", None)):
        raise RuntimeError(u"FaceGuide 缺少统一 run_step()。")

    if not callable(getattr(face_guide, "build_guide", None)):
        raise RuntimeError(u"FaceGuide 缺少 Guide 编辑入口 build_guide()。")

    if hasattr(face_setup, "build"):
        raise RuntimeError(u"FaceSetup 仍残留 build() Compatibility Wrapper。")

    if hasattr(face_guide, "build") or hasattr(face_guide, "finalize"):
        raise RuntimeError(u"FaceGuide 仍残留 build/finalize Compatibility Wrapper。")

    return u"Face Step 01 run_step 与 Step 02 API Contract 正常"


def run_case(results, name, test_function, root_group):
    try:
        message = test_function(root_group)
        results.append({
            "name": name,
            "passed": True,
            "message": message,
            "traceback": "",
        })
    except Exception as error:
        results.append({
            "name": name,
            "passed": False,
            "message": str(error),
            "traceback": traceback.format_exc(),
        })


def run():
    maya_version = require_maya_2023()
    namespace = create_namespace()
    results = []

    print("")
    print("=" * 78)
    print("Muzi Toolset - Maya 2023 Runtime Smoke Test")
    print("Maya: {}".format(maya_version))
    print("=" * 78)

    try:
        root_group = cmds.createNode(
            "transform",
            name="grp_md_maya2023_smoke_root_001"
        )

        run_case(
            results,
            "Core Contract",
            test_core_contract,
            root_group
        )
        run_case(
            results,
            "Controller Contract",
            test_controller_contract,
            root_group
        )
        run_case(
            results,
            "Face Step Contract",
            test_face_step_contract,
            root_group
        )
    finally:
        remove_namespace(namespace)

    component_result = face_component_smoke_test.run()

    passed_count = 0
    failed_count = 0

    for result in results:
        if result["passed"]:
            passed_count += 1
            print(
                u"[PASS] {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
        else:
            failed_count += 1
            print(
                u"[FAIL] {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
            print(result["traceback"])

    failed_count += component_result["failed"]
    passed_count += component_result["passed"]

    print("-" * 78)
    print(
        "Passed: {} | Failed: {}".format(
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "maya_version": maya_version,
        "results": results,
        "face_components": component_result,
        "passed": passed_count,
        "failed": failed_count,
    }


__all__ = [
    "run",
]
'''

    write_text(path, source_text)


def create_maya2023_smoke_contract_test():
    path = "tests/maya2023_smoke_contract_test.py"

    source_text = r'''# coding=utf-8
u"""Maya 2023 Smoke Runner 的非 Maya 静态契约检查。"""

from __future__ import print_function

import ast
import os


REQUIRED_FUNCTIONS = {
    "require_maya_2023",
    "test_core_contract",
    "test_controller_contract",
    "test_face_step_contract",
    "run",
}


def get_smoke_path():
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.join(
        tests_directory,
        "maya2023_smoke_test.py"
    )


def run():
    smoke_path = get_smoke_path()

    if not os.path.isfile(smoke_path):
        print("[FAIL] maya2023_smoke_test.py 不存在。")
        return False

    with open(
            smoke_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        source_text = source_file.read()

    syntax_tree = ast.parse(
        source_text,
        filename=smoke_path
    )

    function_names = set()

    for node in syntax_tree.body:
        if isinstance(node, ast.FunctionDef):
            function_names.add(node.name)

    missing_functions = []

    for function_name in REQUIRED_FUNCTIONS:
        if function_name not in function_names:
            missing_functions.append(function_name)

    if missing_functions:
        print(
            "[FAIL] Maya 2023 Smoke Runner 缺少入口：{}".format(
                ", ".join(sorted(missing_functions))
            )
        )
        return False

    required_texts = [
        "import maya.cmds as cmds",
        "face_component_smoke_test",
        "face_setup.run_step()",
        "FaceGuide",
        "build_guide",
    ]

    for required_text in required_texts:
        if required_text not in source_text:
            print(
                "[FAIL] Maya 2023 Smoke Runner 缺少契约文本：{}".format(
                    required_text
                )
            )
            return False

    print("[PASS] Maya 2023 Smoke Runner 静态契约完整。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
'''

    write_text(path, source_text)


def update_docs_workflow():
    path = ".github/workflows/docs.yml"
    source_text = read_text(path)

    marker = (
        "      # -----------------------------------------------------------------------\n"
        "      # 步骤 2：禁止 System 重新实现已经有明确 Core 归属的通用 Helper。\n"
        "      # -----------------------------------------------------------------------\n"
        "      - name: Check System Core reuse\n"
        "        run: python tests/system_core_reuse_gate_test.py\n\n"
    )

    replacement = (
        "      # -----------------------------------------------------------------------\n"
        "      # 步骤 2：检查 Core 内部 Generic 能力是否保持唯一正式实现。\n"
        "      # -----------------------------------------------------------------------\n"
        "      - name: Check Core single source\n"
        "        run: python tests/core_single_source_gate_test.py\n\n"
        "      # -----------------------------------------------------------------------\n"
        "      # 步骤 3：禁止 System / Tool / UI 重复 Core Helper 或直接创建通用 Constraint。\n"
        "      # -----------------------------------------------------------------------\n"
        "      - name: Check upper layer Core reuse\n"
        "        run: python tests/system_core_reuse_gate_test.py\n\n"
        "      # -----------------------------------------------------------------------\n"
        "      # 步骤 4：静态检查 Maya 2023 Runtime Smoke Runner 契约。\n"
        "      # -----------------------------------------------------------------------\n"
        "      - name: Check Maya 2023 smoke contract\n"
        "        run: python tests/maya2023_smoke_contract_test.py\n\n"
    )

    source_text = replace_required(
        source_text,
        marker,
        replacement,
        "docs workflow architecture gates"
    )

    # 后续步骤编号只影响注释，不影响执行；统一顺延避免文档误导。
    step_number = 3

    while step_number <= 15:
        old_text = "# 步骤 {}：".format(step_number)
        new_text = "# 步骤 {}：".format(step_number + 2)
        source_text = source_text.replace(
            old_text,
            new_text
        )
        step_number += 1

    write_text(path, source_text)


def validate_removed_symbols():
    checks = {
        "systems/controller/builder.py": [
            "def get_short_name(",
        ],
        "systems/controller/space_blend.py": [
            "def get_short_name(",
            "def validate_node(",
        ],
        "systems/face/face_guide.py": [
            "def get_short_name(",
            "def get_parent(",
            "def get_world_position(",
            "def build(self):",
            "def finalize(self,",
        ],
        "systems/face/face_setup.py": [
            "def build(self):",
        ],
        "core/constraint_utils.py": [
            "def validate_node(",
        ],
        "core/matrix_utils.py": [
            "def get_parent(",
        ],
        "core/name_utils.py": [
            "def maya_undo(",
            "def dag_depth(",
            "@maya_undo",
        ],
        "core/hierarchy_utils.py": [
            "def _validate_node(",
        ],
    }

    for relative_path in checks:
        source_text = read_text(relative_path)

        for forbidden_text in checks[relative_path]:
            if forbidden_text in source_text:
                raise RuntimeError(
                    u"迁移后仍残留 {} | {}".format(
                        relative_path,
                        forbidden_text
                    )
                )


def run():
    update_scene_utils()
    update_hierarchy_utils()
    update_name_utils()
    update_constraint_utils()
    update_matrix_utils()
    update_controller_builder()
    update_controller_space_blend()
    update_face_guide()
    update_face_setup()
    update_face_rig_ui()
    update_upper_layer_gate()
    create_core_single_source_gate()
    create_maya2023_smoke_test()
    create_maya2023_smoke_contract_test()
    update_docs_workflow()
    validate_removed_symbols()

    print("[PASS] Architecture Cleanup Phase 2 migration completed.")


if __name__ == "__main__":
    run()
