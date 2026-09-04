# coding=utf-8
u"""
一次性清理已经存在的 Jnt Migration 目标路径，并修正最终验证器边界。

只删除上一轮命名迁移已经生成、并会由本轮从稳定基线重新生成的目标路径。
不处理 legacy_reference / resources。
"""

from __future__ import print_function

import os
import shutil


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

TARGET_PATHS = [
    "core/jnt_utils.py",
    "core/jnt_chain_utils.py",
    "tools/jnt",
    "docs/manual/jnt.md",
]


def remove_target(relative_path):
    u"""删除一个已存在的迁移目标文件或目录。"""
    absolute_path = os.path.join(
        REPO_ROOT,
        relative_path.replace("/", os.sep)
    )

    if not os.path.exists(absolute_path):
        return False

    if os.path.isdir(absolute_path):
        shutil.rmtree(
            absolute_path
        )
    else:
        os.remove(
            absolute_path
        )

    print(
        u"删除旧迁移目标：{}".format(
            relative_path
        )
    )
    return True


def patch_runtime_verifier():
    u"""让最终 Runtime 验证跳过契约文件自身，但继续扫描全部正式 Runtime。"""
    runner_path = os.path.join(
        REPO_ROOT,
        "scripts",
        "_redo_jnt_migration.py"
    )

    if not os.path.isfile(runner_path):
        raise RuntimeError(
            u"没有找到 Corrected Jnt Migration Runner。"
        )

    with open(runner_path, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    old_text = '''                # 当前 Runner 自己包含验证用 Forbidden Token 文本，不纳入源码扫描。
                if file_name == "_redo_jnt_migration.py":
                    continue
'''

    new_text = '''                # Runner 与命名契约自身包含“禁止字符串”作为测试规则，
                # 它们不是 Runtime API 使用点，因此不参与本轮源码错误扫描。
                if file_name == "_redo_jnt_migration.py":
                    continue
                if file_name == "jnt_naming_contract_test.py":
                    continue
'''

    if old_text not in source:
        raise RuntimeError(
            u"没有找到 Corrected Jnt Runtime Verifier 修正位置。"
        )

    source = source.replace(
        old_text,
        new_text,
        1
    )

    with open(runner_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(
            source
        )

    print(
        u"已修正 Corrected Jnt Runtime Verifier 自扫描边界。"
    )


def main():
    u"""清理本轮会重新生成的 Jnt Migration 目标，并准备最终验证器。"""
    removed_paths = []

    for relative_path in TARGET_PATHS:
        removed = remove_target(
            relative_path
        )
        if not removed:
            continue

        removed_paths.append(
            relative_path
        )

    patch_runtime_verifier()

    print(
        u"Jnt Migration 目标清理完成：{} 个。".format(
            len(removed_paths)
        )
    )


if __name__ == "__main__":
    main()
