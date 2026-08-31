# coding=utf-8
u"""
API Reference Generator Smoke Test
==================================

验证静态 API 文档生成器的核心行为。

这个测试不 import Maya，也不依赖 MkDocs。
它只使用 Python 标准库在临时目录中构造一个最小项目，然后检查：

    1. 普通模块会生成独立 API 页面；
    2. ``__init__.py`` 会生成 Package 页面；
    3. 参数 / 返回值 / 异常 / 示例可以从 Docstring 提取；
    4. Class / __init__ / Method 都会生成详细 API；
    5. app / core / systems / tools / ui / config 都可以进入扫描范围；
    6. SUMMARY.md 会包含真实源码树导航。
"""

from __future__ import print_function

import importlib.util
import os
import shutil
import tempfile


def get_project_root():
    """返回测试文件所在仓库根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    project_root = os.path.dirname(
        tests_directory
    )
    return project_root


def load_generator_module(project_root):
    """从 scripts 目录加载生成器，不依赖包 Import。"""
    generator_path = os.path.join(
        project_root,
        "scripts",
        "generate_mkdocs_reference.py"
    )

    spec = importlib.util.spec_from_file_location(
        "muzi_reference_generator_test_module",
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


def write_text_file(file_path, content):
    """写入测试使用的 UTF-8 文件。"""
    parent_directory = os.path.dirname(
        file_path
    )

    if not os.path.isdir(parent_directory):
        os.makedirs(
            parent_directory
        )

    with open(
            file_path,
            "w",
            encoding="utf-8",
            newline="\n"
    ) as file_object:
        file_object.write(
            content
        )


def create_placeholder_docs(project_root):
    """创建 SUMMARY.md 会引用到的最小手写文档。"""
    docs_root = os.path.join(
        project_root,
        "docs"
    )

    relative_paths = [
        "index.md",
        "manual/index.md",
        "manual/tools.md",
        "manual/rigging.md",
        "manual/face-guide.md",
        "getting-started/installation.md",
        "getting-started/maya-usage.md",
        "architecture/index.md",
        "architecture/core.md",
        "architecture/tools-systems.md",
        "reference/index.md",
        "development/documentation.md",
        "development/core-style-guide.md",
        "development/testing.md",
        "migration/pipeline.md",
    ]

    for relative_path in relative_paths:
        file_path = os.path.join(
            docs_root,
            relative_path
        )

        write_text_file(
            file_path,
            "# Test\n"
        )


def create_test_project(project_root):
    """创建包含多层 Package 和一个完整 API 示例的临时源码树。"""
    package_files = [
        "__init__.py",
        "app/__init__.py",
        "core/__init__.py",
        "systems/__init__.py",
        "systems/face/__init__.py",
        "tools/__init__.py",
        "tools/basic/__init__.py",
        "ui/__init__.py",
    ]

    for relative_path in package_files:
        file_path = os.path.join(
            project_root,
            relative_path
        )

        write_text_file(
            file_path,
            '"""测试 Package。"""\n'
        )

    write_text_file(
        os.path.join(
            project_root,
            "config.py"
        ),
        '"""测试 Config。"""\n'
        'PROJECT_NAME = "MuziTools"\n'
    )

    write_text_file(
        os.path.join(
            project_root,
            "app",
            "main.py"
        ),
        '"""测试 App 入口。"""\n'
    )

    write_text_file(
        os.path.join(
            project_root,
            "ui",
            "theme.py"
        ),
        '"""测试 UI Theme。"""\n'
    )

    write_text_file(
        os.path.join(
            project_root,
            "tools",
            "basic",
            "attr_tool.py"
        ),
        '"""测试 Tool。"""\n'
        '\n'
        'def main():\n'
        '    """打开测试 Tool。"""\n'
        '    return True\n'
    )

    write_text_file(
        os.path.join(
            project_root,
            "systems",
            "face",
            "face_guide.py"
        ),
        '"""测试 Face Guide。"""\n'
    )

    demo_source = r'''# coding=utf-8
u"""
Demo Utils
==========

用于验证 API Reference Generator。

Usage:
    需要验证文档生成器时使用。
"""


def create_node(node, count=2):
    u"""
    创建测试节点。

    Args:
        node (str):
            Maya 节点名称。

        count (int):
            创建数量。

    Returns:
        list:
            创建后的节点名称列表。

    Raises:
        RuntimeError:
            创建失败时抛出。

    Example:
        >>> result = create_node("pCube1", count=2)
    """
    return [node] * count


class Builder(object):
    u"""测试 Builder。"""

    def __init__(self, target):
        u"""
        初始化 Builder。

        Args:
            target (str):
                目标 Maya 节点。
        """
        self.target = target

    def build(self, force=False):
        u"""
        执行 Build。

        Args:
            force (bool):
                是否强制重新构建。

        Returns:
            bool:
                构建成功返回 True。
        """
        return True
'''

    write_text_file(
        os.path.join(
            project_root,
            "core",
            "demo_utils.py"
        ),
        demo_source
    )

    create_placeholder_docs(
        project_root
    )


def assert_text_contains(text, expected_text, label):
    """统一检查字符串包含关系。"""
    if expected_text in text:
        return

    raise AssertionError(
        u"{} 缺少预期内容: {}".format(
            label,
            expected_text
        )
    )


def run_test():
    """运行 API Reference Generator Smoke Test。"""
    repository_root = get_project_root()
    generator = load_generator_module(
        repository_root
    )

    temporary_root = tempfile.mkdtemp(
        prefix="muzi_docs_reference_test_"
    )

    try:
        create_test_project(
            temporary_root
        )

        result = generator.generate_reference_docs(
            project_root=temporary_root
        )

        if result["generated_modules"] < 10:
            raise AssertionError(
                u"扫描到的测试模块数量异常: {}".format(
                    result["generated_modules"]
                )
            )

        demo_doc_path = os.path.join(
            temporary_root,
            "docs",
            "reference",
            "core",
            "demo_utils.md"
        )

        if not os.path.isfile(demo_doc_path):
            raise AssertionError(
                u"没有生成 core/demo_utils.py 对应 API 页面。"
            )

        with open(
                demo_doc_path,
                "r",
                encoding="utf-8"
        ) as file_object:
            demo_doc = file_object.read()

        expected_demo_texts = [
            "## API 一览",
            "## Functions 详细 API",
            "`create_node()`",
            "| `node` | `str` | 是 |",
            "| `count` | `int` | 否 | `2` |",
            "创建后的节点名称列表",
            "`RuntimeError`",
            'result = create_node("pCube1", count=2)',
            "## Classes 详细 API",
            "`Builder`",
            "`__init__()`",
            "`build()`",
            "是否强制重新构建",
        ]

        for expected_text in expected_demo_texts:
            assert_text_contains(
                demo_doc,
                expected_text,
                "demo_utils.md"
            )

        package_doc_path = os.path.join(
            temporary_root,
            "docs",
            "reference",
            "core",
            "package.md"
        )

        if not os.path.isfile(package_doc_path):
            raise AssertionError(
                u"core/__init__.py 没有生成 package.md。"
            )

        summary_path = os.path.join(
            temporary_root,
            "docs",
            "SUMMARY.md"
        )

        if not os.path.isfile(summary_path):
            raise AssertionError(
                u"没有生成 docs/SUMMARY.md。"
            )

        with open(
                summary_path,
                "r",
                encoding="utf-8"
        ) as file_object:
            summary_text = file_object.read()

        expected_summary_texts = [
            "* 用户手册",
            "* API 参考",
            "[Core](reference/core/index.md)",
            "[`demo_utils.py`](reference/core/demo_utils.md)",
            "[Tools](reference/tools/index.md)",
            "Basic",
            "[`attr_tool.py`](reference/tools/basic/attr_tool.md)",
            "[Systems](reference/systems/index.md)",
            "Face",
            "[`face_guide.py`](reference/systems/face/face_guide.md)",
            "[UI](reference/ui/index.md)",
            "[App](reference/app/index.md)",
        ]

        for expected_text in expected_summary_texts:
            assert_text_contains(
                summary_text,
                expected_text,
                "SUMMARY.md"
            )

    finally:
        shutil.rmtree(
            temporary_root,
            ignore_errors=True
        )

    print(
        u"API Reference Generator Smoke Test: PASS"
    )
    return True


if __name__ == "__main__":
    run_test()
