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

# Maya API 检查同样排除一次性迁移脚本和契约本身。
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

# runpy.run_path() 返回的是结果字典；函数真正使用的是自己的 __globals__。
# 必须修改函数绑定的全局空间，main() 内部才会真正使用修正规则。
main_function = namespace["main"]
main_globals = main_function.__globals__
main_globals["JNT_CONTRACT_SOURCE"] = contract_source

# 原始规则在普通引号前使用了 \b：
#     type="joint"
#     cmds.createNode("joint")
# 这类字符串的引号前不是 Word Boundary，因此没有被保护。
# 修正后：所有精确的 "joint" / 'joint' 字符串都会先保护；
# 后续只有 Muzi Naming 的 create_name(type="joint") 会被明确改成 jnt。
main_globals["EXACT_JOINT_STRING_PATTERN"] = re.compile(
    r"(?P<prefix>(?:\b(?:u|r|ur|ru|b|br|rb|f|fr|rf))?)(?P<quote>['\"])joint(?P=quote)",
    re.IGNORECASE
)

main_function()
