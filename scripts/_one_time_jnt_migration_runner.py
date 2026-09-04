# coding=utf-8
u"""修正一次性 Jnt Migration 的保护规则 / Contract 边界并执行迁移。"""

from __future__ import print_function

import os
import re
import runpy


SCRIPT_PATH = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "_one_time_jnt_migration.py"
)

namespace = runpy.run_path(
    SCRIPT_PATH,
    run_name="muzi_one_time_jnt_migration"
)

contract_source = namespace["JNT_CONTRACT_SOURCE"]

old_block = '''    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
'''

new_block = '''    for file_path in iter_python_files():
        file_name = os.path.basename(file_path)
        if file_name == "jnt_naming_contract_test.py":
            continue
        if file_name.startswith("_one_time_jnt_migration"):
            continue

        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
'''

if old_block not in contract_source:
    raise RuntimeError(
        u"没有找到 Jnt Contract 自扫描修正位置。"
    )

contract_source = contract_source.replace(
    old_block,
    new_block,
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
        if file_name.startswith("_one_time_jnt_migration"):
            continue

        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_MAYA_API_TEXT:
'''

if old_api_block not in contract_source:
    raise RuntimeError(
        u"没有找到 Jnt Maya API Contract 自扫描修正位置。"
    )

contract_source = contract_source.replace(
    old_api_block,
    new_api_block,
    1
)

main_function = namespace["main"]
main_globals = main_function.__globals__
main_globals["JNT_CONTRACT_SOURCE"] = contract_source

# GitHub Actions 的 GITHUB_TOKEN 不能修改 Workflow 文件。
# 一次性 Runner 只迁移 Runtime / Tests / Docs；Workflow 由外部 GitHub 连接随后单独维护。
active_roots = []
for root_name in main_globals["ACTIVE_ROOTS"]:
    if root_name == ".github":
        continue
    active_roots.append(root_name)
main_globals["ACTIVE_ROOTS"] = active_roots


def skip_workflow_registration():
    u"""迁移提交阶段不修改 .github；CI 注册由后续 GitHub 写操作完成。"""
    return None


main_globals["register_contract_test"] = skip_workflow_registration

# 普通 type="joint" / cmds.createNode("joint") 也必须被识别为 Maya Node Type。
main_globals["EXACT_JOINT_STRING_PATTERN"] = re.compile(
    r"(?P<prefix>(?:\b(?:u|r|ur|ru|b|br|rb|f|fr|rf))?)(?P<quote>['\"])joint(?P=quote)",
    re.IGNORECASE
)

main_function()
