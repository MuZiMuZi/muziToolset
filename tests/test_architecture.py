# coding=utf-8
u"""PyMEL-first architecture static checks。"""

from __future__ import print_function

import ast
import os
import re


repository_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
runtime_roots = [
    os.path.join(repository_root, "core"),
    os.path.join(repository_root, "systems"),
    os.path.join(repository_root, "tools"),
]


def iter_python_files():
    for runtime_root in runtime_roots:
        if not os.path.isdir(runtime_root):
            continue
        for current_root, folder_names, file_names in os.walk(runtime_root):
            filtered_folder_names = []
            for folder_name in folder_names:
                if folder_name == "__pycache__":
                    continue
                filtered_folder_names.append(folder_name)
            folder_names[:] = filtered_folder_names
            for file_name in file_names:
                if file_name.endswith(".py"):
                    yield os.path.join(current_root, file_name)


def read_source(file_path):
    with open(file_path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def test_runtime_has_no_legacy_imports():
    for file_path in iter_python_files():
        source = read_source(file_path)
        import_pattern = re.compile(
            r"(?:from|import)\s+[^\n]*legacy_reference"
        )
        assert import_pattern.search(source) is None


def test_runtime_has_no_old_utils_imports():
    pattern = re.compile(r"(?:from|import)\s+[^\n]*_utils")
    for file_path in iter_python_files():
        assert pattern.search(read_source(file_path)) is None


def test_module_variables_are_lower_snake_case():
    allowed_dunder_names = {"__all__", "__version__"}
    for file_path in iter_python_files():
        tree = ast.parse(read_source(file_path), filename=file_path)
        for statement in tree.body:
            if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
                continue
            target_nodes = []
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    target_nodes.append(target)
            else:
                target_nodes.append(statement.target)
            for target in target_nodes:
                if not isinstance(target, ast.Name):
                    continue
                variable_name = target.id
                if variable_name in allowed_dunder_names:
                    continue
                assert variable_name == variable_name.lower()
                assert re.match(r"^[a-z_][a-z0-9_]*$", variable_name)


def test_runtime_paths_use_snake_case():
    for runtime_root in runtime_roots:
        if not os.path.isdir(runtime_root):
            continue
        for current_root, folder_names, file_names in os.walk(runtime_root):
            for folder_name in folder_names:
                if folder_name == "__pycache__":
                    continue
                assert re.match(r"^[a-z_][a-z0-9_]*$", folder_name)
            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue
                stem = file_name[:-3]
                if stem == "__init__":
                    continue
                assert re.match(r"^[a-z_][a-z0-9_]*$", stem)
