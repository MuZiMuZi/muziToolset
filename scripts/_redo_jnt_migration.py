# coding=utf-8
u"""
最终一次性 Jnt Naming Migration Runner
======================================

从已经验证过的稳定提交读取原始迁移器，但修复两个关键边界：
    1. Maya API Protection Token 不再包含 joint / jnt 字样；
    2. 精确的 "joint" Maya Node Type 字符串始终先保护。

Runner 只服务本次迁移，完成后由 Workflow 删除。
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

MIGRATION_SOURCE_COMMIT = "15b17c9d2fb3d7e35924e462f33e5673f21762b3"
MIGRATION_SOURCE_PATH = "scripts/_one_time_jnt_migration.py"


# =============================================================================
# Load historical migration source
# =============================================================================

def load_migration_namespace():
    u"""从 Git History 读取原迁移器，不依赖当前工作树里的临时文件。"""
    git_spec = "{}:{}".format(
        MIGRATION_SOURCE_COMMIT,
        MIGRATION_SOURCE_PATH
    )

    source_bytes = subprocess.check_output(
        [
            "git",
            "show",
            git_spec,
        ],
        cwd=REPO_ROOT
    )
    source = source_bytes.decode(
        "utf-8"
    )

    fake_file_path = os.path.join(
        REPO_ROOT,
        "scripts",
        "_historical_jnt_migration_source.py"
    )

    namespace = {
        "__file__": fake_file_path,
        "__name__": "muzi_corrected_jnt_migration",
    }

    compiled_source = compile(
        source,
        fake_file_path,
        "exec"
    )
    exec(
        compiled_source,
        namespace
    )
    return namespace


# =============================================================================
# Correct protection behavior
# =============================================================================

def build_protect_text_function(main_globals):
    u"""构建不会被 joint -> jnt 二次替换破坏的 Maya Token Protection。"""
    url_pattern = main_globals["URL_PATTERN"]
    protected_patterns = main_globals["PROTECTED_PATTERNS"]
    exact_joint_string_pattern = main_globals["EXACT_JOINT_STRING_PATTERN"]

    def protect_text(text):
        u"""保护 Maya 官方 API / Node Type，并返回可恢复 Token。"""
        protected_values = []

        def add_value(value):
            # Token 故意不包含 joint / jnt，避免被命名迁移再次修改。
            token = "__MUZI_MAYA_PROTECTED_{:05d}__".format(
                len(protected_values)
            )
            protected_values.append(
                (token, value)
            )
            return token

        def replace_url(match):
            return add_value(
                match.group(0)
            )

        text = url_pattern.sub(
            replace_url,
            text
        )

        for pattern_text in protected_patterns:
            pattern = re.compile(
                pattern_text
            )

            def replace_pattern(match):
                return add_value(
                    match.group(0)
                )

            text = pattern.sub(
                replace_pattern,
                text
            )

        def replace_exact_joint_string(match):
            return add_value(
                match.group(0)
            )

        text = exact_joint_string_pattern.sub(
            replace_exact_joint_string,
            text
        )

        return text, protected_values

    return protect_text


# =============================================================================
# Contract self-scan fix
# =============================================================================

def patch_contract_source(contract_source):
    u"""让新 Contract 扫 Runtime，而不是把自己的规则常量判成旧命名。"""
    old_project_block = '''    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
'''

    new_project_block = '''    for file_path in iter_python_files():
        file_name = os.path.basename(file_path)
        if file_name == "jnt_naming_contract_test.py":
            continue
        if file_name.startswith("_redo_jnt_migration"):
            continue

        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
'''

    if old_project_block not in contract_source:
        raise RuntimeError(
            u"没有找到 Jnt Contract Project Naming 自扫描修正位置。"
        )

    contract_source = contract_source.replace(
        old_project_block,
        new_project_block,
        1
    )

    old_api_block = '''    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_MAYA_API_TEXT:
'''

    new_api_block = '''    for file_path in iter_python_files():
        file_name = os.path.basename(file_path)
        if file_name == "jnt_naming_contract_test.py":
            continue
        if file_name.startswith("_redo_jnt_migration"):
            continue

        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_MAYA_API_TEXT:
'''

    if old_api_block not in contract_source:
        raise RuntimeError(
            u"没有找到 Jnt Contract Maya API 自扫描修正位置。"
        )

    contract_source = contract_source.replace(
        old_api_block,
        new_api_block,
        1
    )
    return contract_source


# =============================================================================
# Final verification
# =============================================================================

def verify_runtime_source():
    u"""迁移完成后直接检查正式 Runtime 不含占位符和明显错误 Maya API。"""
    scan_roots = [
        "app",
        "core",
        "systems",
        "tools",
        "ui",
        "tests",
        "scripts",
    ]

    forbidden_texts = [
        "__MUZI_MAYA_PROTECTED_",
        "__MUZI_MAYA_JOINT_PROTECTED_",
        "__MUZI_MAYA_JNT_PROTECTED_",
        "cmds.jnt(",
        "cmds.jntDisplayScale(",
        "maya.cmds.jnt(",
        "maya.cmds.jntDisplayScale(",
        "orientjnt=",
    ]

    issues = []

    for root_name in scan_roots:
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

                file_path = os.path.join(
                    current_root,
                    file_name
                )
                relative_path = os.path.relpath(
                    file_path,
                    REPO_ROOT
                ).replace("\\", "/")

                if relative_path.startswith("legacy_reference/"):
                    continue

                # 当前 Runner 自己包含验证用 Forbidden Token 文本，不纳入源码扫描。
                if file_name == "_redo_jnt_migration.py":
                    continue

                with open(file_path, "r", encoding="utf-8") as file_object:
                    source = file_object.read()

                for forbidden_text in forbidden_texts:
                    if forbidden_text not in source:
                        continue

                    issues.append(
                        u"{} -> {}".format(
                            relative_path,
                            forbidden_text
                        )
                    )

    if issues:
        raise AssertionError(
            u"Corrected Jnt Migration Runtime Verification 失败：{}".format(
                "; ".join(issues)
            )
        )

    print(
        u"[PASS] Corrected Jnt Migration Runtime Source Verification"
    )


# =============================================================================
# Main
# =============================================================================

def main():
    u"""执行修正后的最终 Jnt Naming Migration。"""
    namespace = load_migration_namespace()
    migration_main = namespace["main"]
    main_globals = migration_main.__globals__

    # 精确 "joint" / 'joint' 字符串属于 Maya Node Type / API Value，先保护。
    main_globals["EXACT_JOINT_STRING_PATTERN"] = re.compile(
        r"(?P<prefix>(?:\b(?:u|r|ur|ru|b|br|rb|f|fr|rf))?)(?P<quote>['\"])joint(?P=quote)",
        re.IGNORECASE
    )

    # 使用不包含 joint / jnt 的 Protection Token。
    main_globals["protect_text"] = build_protect_text_function(
        main_globals
    )

    # 不在 Actions 内修改任何 Workflow；常规 CI 已由 GitHub Connector 单独维护。
    active_roots = []
    for root_name in main_globals["ACTIVE_ROOTS"]:
        if root_name == ".github":
            continue
        active_roots.append(
            root_name
        )
    main_globals["ACTIVE_ROOTS"] = active_roots

    def skip_workflow_registration():
        return None

    main_globals["register_contract_test"] = skip_workflow_registration

    contract_source = main_globals["JNT_CONTRACT_SOURCE"]
    main_globals["JNT_CONTRACT_SOURCE"] = patch_contract_source(
        contract_source
    )

    migration_main()
    verify_runtime_source()

    print(
        u"Corrected Joint -> Jnt Migration 完成。"
    )


if __name__ == "__main__":
    main()
