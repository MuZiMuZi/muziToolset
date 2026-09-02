# coding=utf-8
u"""
Core Public API Gate
====================

静态检查 core/*.py 的 __all__ 是否只导出模块中真实存在的顶层名称。

本测试不 import Maya，也不执行 Core 模块，因此可以直接使用普通 Python 运行。

目的：
    1. Helper 被迁移 / 删除后，旧 __all__ 不允许继续残留；
    2. Core Public API 清单必须和真实实现保持一致；
    3. 避免为了兼容旧名字重新创建没有必要的包装方法。
"""

from __future__ import print_function

import ast
import os


def get_package_root():
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        tests_directory
    )


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
    return relative_path.replace(
        os.sep,
        "/"
    )


def collect_defined_names(syntax_tree):
    u"""收集模块顶层可被 __all__ 导出的名称。"""
    names = set()

    for node in syntax_tree.body:
        if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            names.add(
                node.name
            )
            continue

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(
                        target.id
                    )
            continue

        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                names.add(
                    node.target.id
                )
            continue

        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    names.add(
                        alias.asname
                    )
                else:
                    names.add(
                        alias.name.split(".", 1)[0]
                    )
            continue

        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue

                names.add(
                    alias.asname or alias.name
                )

    return names


def get_all_names(syntax_tree):
    u"""读取静态字符串形式的 __all__；未定义时返回 None。"""
    for node in syntax_tree.body:
        if not isinstance(node, ast.Assign):
            continue

        is_all_assignment = False

        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id == "__all__":
                    is_all_assignment = True
                    break

        if not is_all_assignment:
            continue

        if not isinstance(node.value, (ast.List, ast.Tuple)):
            raise RuntimeError(
                u"__all__ 必须使用静态 list / tuple。"
            )

        result = []

        for element in node.value.elts:
            if isinstance(element, ast.Str):
                result.append(
                    element.s
                )
                continue

            if isinstance(element, ast.Constant):
                if isinstance(element.value, str):
                    result.append(
                        element.value
                    )
                    continue

            raise RuntimeError(
                u"__all__ 只允许包含静态字符串。"
            )

        return result

    return None


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
    defined_names = collect_defined_names(
        syntax_tree
    )
    all_names = get_all_names(
        syntax_tree
    )
    issues = []

    if all_names is None:
        return issues

    seen_names = set()

    for exported_name in all_names:
        if exported_name in seen_names:
            issues.append(
                u"__all__ 重复导出：{}".format(
                    exported_name
                )
            )
            continue

        seen_names.add(
            exported_name
        )

        if exported_name not in defined_names:
            issues.append(
                u"__all__ 导出了不存在的名称：{}".format(
                    exported_name
                )
            )

    return issues


def run():
    print("=" * 78)
    print("Muzi Toolset - Core Public API Gate")
    print("=" * 78)

    issues = []
    file_count = 0

    for file_path in iter_core_python_files():
        file_count += 1
        relative_path = get_relative_path(
            file_path
        )

        try:
            file_issues = scan_file(
                file_path
            )
        except Exception as error:
            issues.append(
                u"{} | {}".format(
                    relative_path,
                    error
                )
            )
            continue

        for issue in file_issues:
            issues.append(
                u"{} | {}".format(
                    relative_path,
                    issue
                )
            )

    if issues:
        for issue in issues:
            print(
                u"[FAIL] {}".format(
                    issue
                )
            )

        return False

    print(
        u"[PASS] {} 个 Core Python 文件的 Public API Export 正常。".format(
            file_count
        )
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
