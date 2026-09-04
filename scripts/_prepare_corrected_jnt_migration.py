# coding=utf-8
u"""
一次性清理已经存在的 Jnt Migration 目标路径。

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


def main():
    u"""清理本轮会重新生成的 Jnt Migration 目标。"""
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

    print(
        u"Jnt Migration 目标清理完成：{} 个。".format(
            len(removed_paths)
        )
    )


if __name__ == "__main__":
    main()
