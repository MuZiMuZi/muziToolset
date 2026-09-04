# coding=utf-8
u"""修正一次性 Jnt Migration Contract 的自扫描边界并执行迁移。"""

from __future__ import print_function

import os
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

namespace["JNT_CONTRACT_SOURCE"] = contract_source
namespace["main"]()
