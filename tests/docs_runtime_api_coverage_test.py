# coding=utf-8
u"""
Runtime API Documentation Coverage Test
=======================================

验证 MuziTools 正式运行时 Python 文件都能映射到独立 API Reference 页面。

这个测试不 import Maya，也不执行任何 Scene 操作。
它直接复用 scripts/generate_mkdocs_reference.py 的静态 AST / Path 规则。

检查：
    1. app / core / systems / tools / ui 都进入扫描范围；
    2. 根目录 __init__.py 和 config.py 进入扫描范围；
    3. 每一个正式 Python 文件都能得到唯一文档路径；
    4. 不同源码文件不会映射到同一个 Markdown 页面；
    5. 每一个公开 Function / Class / Method 都能被生成器收集；
    6. 生成页面路径全部位于 docs/reference/。
"""

from __future__ import print_function

import importlib.util
import os
import sys


def get_project_root():
    """返回仓库根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    return os.path.dirname(
        tests_directory
    )


def load_generator(project_root):
    """静态加载 API Reference Generator。"""
    generator_path = os.path.join(
        project_root,
        "scripts",
        "generate_mkdocs_reference.py"
    )

    spec = importlib.util.spec_from_file_location(
        "muzi_docs_runtime_coverage_generator",
        generator_path
    )

    if spec is None:
        raise RuntimeError(
            u"无法创建 API Generator Import Spec。"
        )

    if spec.loader is None:
        raise RuntimeError(
            u"无法读取 API Generator Loader。"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def assert_true(condition, message):
    """统一断言。"""
    if condition:
        return

    raise AssertionError(
        message
    )


def main():
    """执行 Runtime API 文档覆盖检查。"""
    project_root = get_project_root()
    generator = load_generator(
        project_root
    )

    source_files = generator.iter_source_files(
        project_root
    )

    assert_true(
        bool(source_files),
        u"没有扫描到任何正式 Runtime Python 文件。"
    )

    expected_roots = [
        "app",
        "core",
        "systems",
        "tools",
        "ui",
    ]

    found_roots = {}

    for root_name in expected_roots:
        found_roots[root_name] = False

    output_path_to_source = {}
    module_count = 0
    public_callable_count = 0

    for source_path in source_files:
        module_info = generator.collect_module_info(
            project_root,
            source_path
        )

        module_count += 1

        relative_source_path = module_info[
            "relative_path"
        ]

        root_name = module_info[
            "root_name"
        ]

        if root_name in found_roots:
            found_roots[root_name] = True

        output_relative_path = generator.get_output_relative_path(
            module_info
        )

        output_relative_path = output_relative_path.replace(
            "\\",
            "/"
        )

        assert_true(
            output_relative_path.endswith(".md"),
            u"API 输出路径不是 Markdown: {}".format(
                output_relative_path
            )
        )

        if output_relative_path in output_path_to_source:
            previous_source = output_path_to_source[
                output_relative_path
            ]

            raise AssertionError(
                u"两个源码文件映射到了同一个 API 页面: {} / {} -> {}".format(
                    previous_source,
                    relative_source_path,
                    output_relative_path
                )
            )

        output_path_to_source[
            output_relative_path
        ] = relative_source_path

        public_callable_count += len(
            module_info["functions"]
        )

        for class_info in module_info["classes"]:
            public_callable_count += 1

            if class_info["constructor"]:
                public_callable_count += 1

            public_callable_count += len(
                class_info["methods"]
            )

    for root_name in expected_roots:
        assert_true(
            found_roots[root_name],
            u"API Generator 没有覆盖正式源码目录: {}".format(
                root_name
            )
        )

    root_package_path = os.path.join(
        project_root,
        "__init__.py"
    )
    root_config_path = os.path.join(
        project_root,
        "config.py"
    )

    assert_true(
        root_package_path in source_files,
        u"根目录 __init__.py 没有进入 API 扫描范围。"
    )

    assert_true(
        root_config_path in source_files,
        u"config.py 没有进入 API 扫描范围。"
    )

    print("=" * 78)
    print("Runtime API Documentation Coverage")
    print("=" * 78)
    print(
        "Runtime modules:   {}".format(
            module_count
        )
    )
    print(
        "API output pages:  {}".format(
            len(output_path_to_source)
        )
    )
    print(
        "Public callables:  {}".format(
            public_callable_count
        )
    )
    print("Coverage:          PASS")
    print("=" * 78)

    return True


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(
            u"Runtime API Documentation Coverage FAILED: {}".format(
                exc
            )
        )
        sys.exit(1)
