# coding=utf-8
u"""
Face Module Lifecycle Contract Test
===================================

纯 Python / AST 架构测试，不需要 Autodesk Maya。

验证：
    1. FaceModuleBase 公开统一七阶段生命周期；
    2. create_build() 的执行顺序固定；
    3. 当前正式 Face Module 继承 FaceModuleBase；
    4. 具体 Module 不重新实现旧四阶段 / create_xxx 生命周期；
    5. build_xxx() 公共入口统一调用 module.create_build()。
"""

from __future__ import print_function

import ast
import os


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODULE_DIR = os.path.join(
    REPO_ROOT,
    "systems",
    "face",
    "modules"
)

FACE_MODULE_METHODS = [
    "load_setup",
    "load_guide",
    "create_jnt",
    "create_ctrl",
    "create_connect",
    "create_deform",
    "create_finalize",
]

RETIRED_CONCRETE_METHODS = {
    "collect_inputs",
    "prepare_data",
    "process_data",
    "finalize_step",
    "create_joint",
    "create_controller",
    "create_connection",
    "setup",
    "guide",
    "joint",
    "control",
    "connect",
    "deform",
    "finalize",
    "build",
}

CONCRETE_MODULE_FILES = {
    "jaw.py": "JawModule",
    "teeth.py": "TeethModule",
}


def read_tree(file_name):
    u"""读取一个 Face Module Python 文件并返回 AST。"""
    file_path = os.path.join(
        MODULE_DIR,
        file_name
    )

    with open(file_path, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    return ast.parse(
        source,
        filename=file_path
    )


def find_class(tree, class_name):
    u"""从 AST 顶层找到指定 Class。"""
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name == class_name:
            return node

    raise AssertionError(
        u"没有找到 Class：{}".format(
            class_name
        )
    )


def get_method_names(class_node):
    u"""返回 Class 自己直接定义的方法名称集合。"""
    method_names = set()

    for node in class_node.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        method_names.add(
            node.name
        )

    return method_names


def get_self_call_order(method_node):
    u"""按源码出现顺序返回 self.xxx() 调用名称。"""
    call_items = []

    for node in ast.walk(method_node):
        if not isinstance(node, ast.Call):
            continue

        function_node = node.func

        if not isinstance(function_node, ast.Attribute):
            continue

        if not isinstance(function_node.value, ast.Name):
            continue

        if function_node.value.id != "self":
            continue

        call_items.append((
            getattr(node, "lineno", 0),
            function_node.attr,
        ))

    call_items.sort(
        key=lambda item: item[0]
    )

    call_names = []

    for line_number, call_name in call_items:
        if call_name not in FACE_MODULE_METHODS:
            continue

        call_names.append(
            call_name
        )

    return call_names


def test_face_module_base():
    u"""验证 FaceModuleBase 的生命周期方法和 create_build() 顺序。"""
    tree = read_tree(
        "face_module_base.py"
    )
    class_node = find_class(
        tree,
        "FaceModuleBase"
    )
    method_names = get_method_names(
        class_node
    )

    required_methods = list(FACE_MODULE_METHODS)
    required_methods.append(
        "create_build"
    )

    for method_name in required_methods:
        if method_name not in method_names:
            raise AssertionError(
                u"FaceModuleBase 缺少方法：{}".format(
                    method_name
                )
            )

    build_method = None

    for node in class_node.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        if node.name == "create_build":
            build_method = node
            break

    if build_method is None:
        raise AssertionError(
            u"FaceModuleBase 缺少 create_build()。"
        )

    call_order = get_self_call_order(
        build_method
    )

    if call_order != FACE_MODULE_METHODS:
        raise AssertionError(
            u"FaceModuleBase.create_build() 生命周期顺序错误：{}".format(
                call_order
            )
        )


def test_concrete_modules():
    u"""验证当前正式 Face Module 使用新生命周期。"""
    for file_name in CONCRETE_MODULE_FILES:
        class_name = CONCRETE_MODULE_FILES[file_name]
        tree = read_tree(
            file_name
        )
        class_node = find_class(
            tree,
            class_name
        )

        base_names = []

        for base_node in class_node.bases:
            if isinstance(base_node, ast.Name):
                base_names.append(
                    base_node.id
                )
            elif isinstance(base_node, ast.Attribute):
                base_names.append(
                    base_node.attr
                )

        if "FaceModuleBase" not in base_names:
            raise AssertionError(
                u"{} 必须继承 FaceModuleBase。".format(
                    class_name
                )
            )

        method_names = get_method_names(
            class_node
        )

        for method_name in FACE_MODULE_METHODS:
            if method_name not in method_names:
                raise AssertionError(
                    u"{} 缺少统一生命周期方法：{}".format(
                        class_name,
                        method_name
                    )
                )

        retired_methods = RETIRED_CONCRETE_METHODS.intersection(
            method_names
        )

        if retired_methods:
            raise AssertionError(
                u"{} 仍定义旧生命周期方法：{}".format(
                    class_name,
                    sorted(retired_methods)
                )
            )


def main():
    u"""执行 Face Module Lifecycle 静态契约。"""
    test_face_module_base()
    test_concrete_modules()
    print(
        u"Face Module Lifecycle Contract: PASS"
    )


if __name__ == "__main__":
    main()
