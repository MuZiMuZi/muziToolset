# coding=utf-8
u"""
一次性 Joint -> Jnt 命名迁移
============================

目标：
    1. 从命名迁移前的稳定提交恢复正式 Runtime / Tests / Docs；
    2. 项目自有命名统一使用 jnt / Jnt；
    3. Maya 官方 joint API、Node Type 与 Attribute 名称保持原样；
    4. legacy_reference 与 Maya 资源文件不参与迁移；
    5. 生成静态命名契约，阻止后续误把 Maya joint API 改成 jnt。

这个脚本只由 one_time_jnt_migration.yml 执行一次，执行完成后会被工作流删除。
"""

from __future__ import print_function

import os
import re
import subprocess


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BASE_COMMIT = "b2cf9a5770c5a39bf54775d8211a447f5ced758a"

RESTORE_PATHS = [
    "app",
    "core",
    "systems",
    "tools",
    "ui",
    "tests",
    "docs",
    "scripts",
    "__init__.py",
    "config.py",
    "ARCHITECTURE.md",
    "README.md",
    "README.en.md",
    "mkdocs.yml",
]

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
}

ACTIVE_ROOTS = [
    "app",
    "core",
    "systems",
    "tools",
    "ui",
    "tests",
    "docs",
    "scripts",
    ".github",
]

ROOT_TEXT_FILES = [
    "__init__.py",
    "config.py",
    "ARCHITECTURE.md",
    "README.md",
    "README.en.md",
    "mkdocs.yml",
]

ONE_TIME_SCRIPT = "scripts/_one_time_jnt_migration.py"
ONE_TIME_WORKFLOW = ".github/workflows/one_time_jnt_migration.yml"


# Maya 官方名称必须保持 joint，而不是 jnt。
# 先替换为占位符，再执行项目命名迁移，最后恢复。
PROTECTED_PATTERNS = [
    r"\bcmds\.jointDisplayScale\b",
    r"\bcmds\.joint\b",
    r"\bmaya\.cmds\.jointDisplayScale\b",
    r"\bmaya\.cmds\.joint\b",
    r"\borientJoint\b",
    r"\bjointOrientX\b",
    r"\bjointOrientY\b",
    r"\bjointOrientZ\b",
    r"\bjointOrient\b",
    r"\bMFnIkJoint\b",
    r"\bkJoint\b",
]

EXACT_JOINT_STRING_PATTERN = re.compile(
    r"(?P<prefix>\b(?:u|r|ur|ru|b|br|rb|f|fr|rf)?)(?P<quote>['\"])joint(?P=quote)",
    re.IGNORECASE
)

URL_PATTERN = re.compile(
    r"https?://[^\s\]\[\)\(<>\"']+"
)


JNT_CONTRACT_SOURCE = r'''# coding=utf-8
u"""
Jnt Naming Contract Test
========================

纯 Python 静态门禁，不需要 Autodesk Maya。

规则：
    1. Muzi Toolset 自有 Joint 命名统一使用 jnt / Jnt；
    2. Maya 官方 API 仍必须使用 cmds.joint / jointDisplayScale；
    3. Maya Joint Node Type 字符串仍必须是 "joint"；
    4. 禁止重新出现 joint_utils / tools.joint 等旧项目入口；
    5. legacy_reference 与 Maya Resource 不属于正式命名迁移范围。
"""

from __future__ import print_function

import os
import re


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SCAN_ROOTS = [
    "app",
    "core",
    "systems",
    "tools",
    "ui",
    "tests",
    "scripts",
]

FORBIDDEN_PROJECT_TEXT = [
    "joint_utils",
    "joint_chain_utils",
    "tools.joint",
    "tools/joint",
    "joint_tool",
    "joint_resamp_tool",
]

FORBIDDEN_MAYA_API_TEXT = [
    "cmds.jnt(",
    "cmds.jntDisplayScale(",
    "maya.cmds.jnt(",
    "maya.cmds.jntDisplayScale(",
    "orientjnt=",
    ".jntOrient",
]

MAYA_COMMANDS_WITH_NODE_TYPE = [
    "ls",
    "listRelatives",
    "listConnections",
    "createNode",
]


def iter_python_files():
    u"""遍历正式 Runtime / Tests 中的 Python 文件。"""
    for root_name in SCAN_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(root_path):
            dir_names[:] = [
                dir_name
                for dir_name in dir_names
                if dir_name != "__pycache__"
            ]

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                yield os.path.join(
                    current_root,
                    file_name
                )


def read_source(file_path):
    u"""读取 UTF-8 Python Source。"""
    with open(file_path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def assert_paths_use_jnt():
    u"""正式路径中禁止再使用 joint 作为项目命名。"""
    invalid_paths = []

    for root_name in SCAN_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.exists(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(root_path):
            relative_root = os.path.relpath(
                current_root,
                REPO_ROOT
            )

            path_parts = relative_root.replace("\\", "/").split("/")

            for path_part in path_parts:
                if "joint" in path_part.lower():
                    invalid_paths.append(relative_root)
                    break

            for file_name in file_names:
                if "joint" not in file_name.lower():
                    continue

                invalid_paths.append(
                    os.path.join(
                        relative_root,
                        file_name
                    )
                )

    if invalid_paths:
        raise AssertionError(
            u"正式项目路径仍包含 joint：{}".format(
                ", ".join(sorted(set(invalid_paths)))
            )
        )


def assert_project_imports_use_jnt():
    u"""禁止旧 Joint Project Import / Tool Entry。"""
    issues = []

    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
            if forbidden_text not in source:
                continue

            issues.append(
                u"{} -> {}".format(
                    os.path.relpath(file_path, REPO_ROOT),
                    forbidden_text
                )
            )

    if issues:
        raise AssertionError(
            u"仍存在旧 Joint Project 命名：{}".format(
                "; ".join(issues)
            )
        )


def assert_maya_api_is_not_renamed():
    u"""禁止把 Maya 官方 Joint API 错改为 jnt。"""
    issues = []

    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_MAYA_API_TEXT:
            if forbidden_text not in source:
                continue

            issues.append(
                u"{} -> {}".format(
                    os.path.relpath(file_path, REPO_ROOT),
                    forbidden_text
                )
            )

        # Maya 查询命令的 type 必须继续使用 joint。
        command_pattern = re.compile(
            r"cmds\.(?:ls|listRelatives|listConnections)\([^\)]*?type\s*=\s*['\"]jnt['\"]",
            re.DOTALL
        )
        if command_pattern.search(source):
            issues.append(
                u"{} -> Maya type='jnt'".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

        create_node_pattern = re.compile(
            r"cmds\.createNode\(\s*['\"]jnt['\"]"
        )
        if create_node_pattern.search(source):
            issues.append(
                u"{} -> cmds.createNode('jnt')".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

        node_type_pattern = re.compile(
            r"cmds\.nodeType\([^\)]*\)\s*(?:==|!=)\s*['\"]jnt['\"]"
        )
        if node_type_pattern.search(source):
            issues.append(
                u"{} -> cmds.nodeType(...) jnt".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

    if issues:
        raise AssertionError(
            u"Maya Joint API 被错误改名：{}".format(
                "; ".join(issues)
            )
        )


def main():
    u"""执行 Jnt Naming 静态契约。"""
    assert_paths_use_jnt()
    assert_project_imports_use_jnt()
    assert_maya_api_is_not_renamed()

    print(
        u"[PASS] Project Jnt Naming / Maya Joint API Contract 正常。"
    )


if __name__ == "__main__":
    main()
'''


def run_git(args):
    u"""执行 Git 命令并在失败时抛出。"""
    command = ["git"]
    command.extend(args)

    print(
        u"[git] {}".format(
            " ".join(command)
        )
    )

    subprocess.check_call(
        command,
        cwd=REPO_ROOT
    )


def restore_stable_runtime():
    u"""恢复到命名迁移前的稳定 Runtime / Tests / Docs 内容。"""
    args = [
        "checkout",
        BASE_COMMIT,
        "--",
    ]
    args.extend(RESTORE_PATHS)
    run_git(args)


def protect_text(text):
    u"""保护 Maya 官方 Joint Token、Node Type 和 URL。"""
    protected_values = []

    def add_value(value):
        token = "__MUZI_MAYA_JOINT_PROTECTED_{:05d}__".format(
            len(protected_values)
        )
        protected_values.append(
            (token, value)
        )
        return token

    # URL 必须最先保护，避免修改外部文档链接。
    def replace_url(match):
        return add_value(
            match.group(0)
        )

    text = URL_PATTERN.sub(
        replace_url,
        text
    )

    for pattern_text in PROTECTED_PATTERNS:
        pattern = re.compile(pattern_text)

        def replace_pattern(match):
            return add_value(
                match.group(0)
            )

        text = pattern.sub(
            replace_pattern,
            text
        )

    # 精确的 "joint" / 'joint' 字符串按 Maya Node Type 处理并保留。
    def replace_exact_joint_string(match):
        return add_value(
            match.group(0)
        )

    text = EXACT_JOINT_STRING_PATTERN.sub(
        replace_exact_joint_string,
        text
    )

    return text, protected_values


def restore_protected_text(text, protected_values):
    u"""恢复之前保护的 Maya 官方 Token。"""
    for token, value in protected_values:
        text = text.replace(
            token,
            value
        )

    return text


def migrate_project_text(text):
    u"""把项目自有 Joint / joint 命名统一为 Jnt / jnt。"""
    text, protected_values = protect_text(
        text
    )

    # Class / 类型命名保持 PascalCase。
    text = text.replace(
        "JOINT",
        "JNT"
    )
    text = text.replace(
        "Joint",
        "Jnt"
    )
    text = text.replace(
        "joint",
        "jnt"
    )

    text = restore_protected_text(
        text,
        protected_values
    )

    # create_name(type="joint") 属于 Muzi Naming，不是 Maya Node Type。
    create_name_pattern = re.compile(
        r"(create_name\([^\)]*?type\s*=\s*)(['\"])joint\2",
        re.DOTALL
    )
    text = create_name_pattern.sub(
        r"\1\2jnt\2",
        text
    )

    return text


def should_process_file(file_path):
    u"""判断文件是否属于本次正式项目命名迁移范围。"""
    relative_path = os.path.relpath(
        file_path,
        REPO_ROOT
    ).replace("\\", "/")

    if relative_path.startswith("legacy_reference/"):
        return False

    if relative_path.startswith("resources/"):
        return False

    if relative_path == ONE_TIME_SCRIPT:
        return False

    extension = os.path.splitext(file_path)[1].lower()
    if extension not in TEXT_EXTENSIONS:
        return False

    return True


def iter_active_text_files():
    u"""遍历 Runtime / Tests / Docs / Workflow 的文本文件。"""
    for root_name in ACTIVE_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(root_path):
            dir_names[:] = [
                dir_name
                for dir_name in dir_names
                if dir_name not in {"__pycache__", ".git"}
            ]

            for file_name in file_names:
                file_path = os.path.join(
                    current_root,
                    file_name
                )

                if not should_process_file(file_path):
                    continue

                yield file_path

    for file_name in ROOT_TEXT_FILES:
        file_path = os.path.join(
            REPO_ROOT,
            file_name
        )

        if not os.path.isfile(file_path):
            continue

        yield file_path


def migrate_file_contents():
    u"""迁移正式文本文件中的项目命名。"""
    changed_files = []

    for file_path in iter_active_text_files():
        with open(file_path, "r", encoding="utf-8") as file_object:
            old_text = file_object.read()

        new_text = migrate_project_text(
            old_text
        )

        if new_text == old_text:
            continue

        with open(file_path, "w", encoding="utf-8", newline="\n") as file_object:
            file_object.write(
                new_text
            )

        changed_files.append(
            os.path.relpath(
                file_path,
                REPO_ROOT
            )
        )

    print(
        u"迁移文本文件：{}".format(
            len(changed_files)
        )
    )
    return changed_files


def replace_path_term(name):
    u"""迁移文件 / 目录名中的 Joint 项目命名。"""
    new_name = name.replace(
        "JOINT",
        "JNT"
    )
    new_name = new_name.replace(
        "Joint",
        "Jnt"
    )
    new_name = new_name.replace(
        "joint",
        "jnt"
    )
    return new_name


def migrate_paths():
    u"""迁移正式目录和文件名；Legacy / Resources 保持原样。"""
    migrated_paths = []

    for root_name in ACTIVE_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(
                root_path,
                topdown=False
        ):
            for file_name in file_names:
                old_path = os.path.join(
                    current_root,
                    file_name
                )
                relative_path = os.path.relpath(
                    old_path,
                    REPO_ROOT
                ).replace("\\", "/")

                if relative_path in {
                        ONE_TIME_SCRIPT,
                        ONE_TIME_WORKFLOW,
                }:
                    continue

                new_file_name = replace_path_term(
                    file_name
                )

                if new_file_name == file_name:
                    continue

                new_path = os.path.join(
                    current_root,
                    new_file_name
                )
                os.rename(
                    old_path,
                    new_path
                )
                migrated_paths.append(
                    u"{} -> {}".format(
                        relative_path,
                        os.path.relpath(new_path, REPO_ROOT)
                    )
                )

            for dir_name in dir_names:
                old_path = os.path.join(
                    current_root,
                    dir_name
                )

                if not os.path.isdir(old_path):
                    continue

                new_dir_name = replace_path_term(
                    dir_name
                )

                if new_dir_name == dir_name:
                    continue

                new_path = os.path.join(
                    current_root,
                    new_dir_name
                )
                os.rename(
                    old_path,
                    new_path
                )
                migrated_paths.append(
                    u"{} -> {}".format(
                        os.path.relpath(old_path, REPO_ROOT),
                        os.path.relpath(new_path, REPO_ROOT)
                    )
                )

    print(
        u"迁移路径：{}".format(
            len(migrated_paths)
        )
    )
    return migrated_paths


def write_contract_test():
    u"""写入 Jnt Naming 静态契约。"""
    file_path = os.path.join(
        REPO_ROOT,
        "tests",
        "jnt_naming_contract_test.py"
    )

    with open(file_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(
            JNT_CONTRACT_SOURCE
        )


def register_contract_test():
    u"""把 Jnt Naming Contract 接入 Static CI。"""
    workflow_path = os.path.join(
        REPO_ROOT,
        ".github",
        "workflows",
        "static_contract_tests.yml"
    )

    with open(workflow_path, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    command_text = "python tests/jnt_naming_contract_test.py"
    if command_text in source:
        return

    anchor = "      - name: Test Core import style\n        run: python tests/core_import_style_test.py\n"
    addition = (
        anchor +
        "\n      - name: Test Jnt naming contract\n" +
        "        run: python tests/jnt_naming_contract_test.py\n"
    )

    if anchor not in source:
        raise RuntimeError(
            u"无法找到 Static Contract Workflow 插入位置。"
        )

    source = source.replace(
        anchor,
        addition,
        1
    )

    with open(workflow_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(
            source
        )


def repair_maya_api_false_replacements():
    u"""
    对迁移结果再执行一次 Maya API 防线修复。

    这些替换只修复明确不可能属于 Muzi Project Naming 的 Maya API。
    """
    replacements = {
        "cmds.jntDisplayScale": "cmds.jointDisplayScale",
        "maya.cmds.jntDisplayScale": "maya.cmds.jointDisplayScale",
        "cmds.jnt(": "cmds.joint(",
        "maya.cmds.jnt(": "maya.cmds.joint(",
        "orientjnt=": "orientJoint=",
        ".jntOrient": ".jointOrient",
        "\"jntOrient\"": "\"jointOrient\"",
        "'jntOrient'": "'jointOrient'",
    }

    changed_files = []

    for file_path in iter_active_text_files():
        with open(file_path, "r", encoding="utf-8") as file_object:
            old_text = file_object.read()

        new_text = old_text

        for old_value, new_value in replacements.items():
            new_text = new_text.replace(
                old_value,
                new_value
            )

        if new_text == old_text:
            continue

        with open(file_path, "w", encoding="utf-8", newline="\n") as file_object:
            file_object.write(
                new_text
            )

        changed_files.append(
            os.path.relpath(file_path, REPO_ROOT)
        )

    return changed_files


def main():
    u"""执行一次性受控 Jnt Naming Migration。"""
    os.chdir(
        REPO_ROOT
    )

    restore_stable_runtime()
    migrate_file_contents()
    migrate_paths()

    # 路径迁移后再执行一次文本迁移，确保目录名引用全部同步。
    migrate_file_contents()
    repair_maya_api_false_replacements()

    write_contract_test()
    register_contract_test()

    # 先做 Python 语法检查和新的命名契约。
    subprocess.check_call(
        [
            "python",
            "-m",
            "compileall",
            "-q",
            "app",
            "core",
            "systems",
            "tools",
            "ui",
            "tests",
            "__init__.py",
            "config.py",
        ],
        cwd=REPO_ROOT
    )

    subprocess.check_call(
        [
            "python",
            "tests/jnt_naming_contract_test.py",
        ],
        cwd=REPO_ROOT
    )

    print(
        u"受控 Joint -> Jnt 命名迁移完成。"
    )


if __name__ == "__main__":
    main()
