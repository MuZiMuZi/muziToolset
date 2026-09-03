# coding=utf-8
u"""
一次性修复 scene_utils / rename_utils 循环导入。

只做两个精确修改：
    1. 删除 scene_utils 对 rename_utils 的模块级导入；
    2. is_default_camera() 直接从 DAG Path 取得 Short Name。

脚本不会修改其它 Scene / Rename 业务逻辑。
"""

from __future__ import print_function

from pathlib import Path


SCENE_UTILS_PATH = Path("core/scene_utils.py")


def main():
    content = SCENE_UTILS_PATH.read_text(encoding="utf-8")

    old_import = "from . import file_utils\nfrom . import rename_utils\n"
    new_import = "from . import file_utils\n"

    if old_import in content:
        content = content.replace(
            old_import,
            new_import,
            1
        )

    old_camera_query = "    return rename_utils.get_short_name(node) in default_cameras\n"
    new_camera_query = (
        "    short_name = str(node).rsplit(\"|\", 1)[-1]\n"
        "    return short_name in default_cameras\n"
    )

    if old_camera_query in content:
        content = content.replace(
            old_camera_query,
            new_camera_query,
            1
        )

    if "from . import rename_utils" in content:
        raise RuntimeError(
            "scene_utils 仍然存在 rename_utils 模块级依赖。"
        )

    if "rename_utils.get_short_name" in content:
        raise RuntimeError(
            "scene_utils 仍然调用 rename_utils.get_short_name。"
        )

    SCENE_UTILS_PATH.write_text(
        content,
        encoding="utf-8"
    )

    print("Scene / Rename 循环导入修复已应用。")


if __name__ == "__main__":
    main()
