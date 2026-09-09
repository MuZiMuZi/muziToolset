# coding=utf-8
u"""
统一 Face Guide Maya ASCII 模板中的 Locator 名称。

迁移规则：
    普通 Locator：
        loc_*_*_guide_###
            -> loc_*_*_bind_###

    Eye 特殊 Locator：
        loc_lf_eye_ball_guide_001 -> loc_lf_eye_ball_001
        loc_lf_eye_iris_guide_001 -> loc_lf_eye_iris_001
        loc_lf_eye_aim_guide_001  -> loc_lf_eye_aim_001

脚本直接按照二进制方式处理 Maya ASCII 文件，
只替换 ASCII 节点名称，不改变 face_guide.ma 原有 CP936 文件内容和其他场景数据。

命令行使用：
    python scripts/normalize_face_guide_locator_names.py
"""

from __future__ import print_function

import os
import re
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from systems.face import face_guide_config


LOCATOR_PATTERN = re.compile(
    rb"loc_[A-Za-z0-9_]+_guide_[0-9]{3}(?:Shape)?"
)


def normalize_template(template_path=None):
    u"""
    将 Face Guide Maya ASCII 文件中的旧 Locator 名称替换成新版标准名称。

    template_path(str): 可选 face_guide.ma 路径。不传时使用项目默认模板。

    Returns:
        int: 实际替换的旧名称 Token 数量。
    """

    if template_path is None:
        template_path = os.path.join(
            REPO_ROOT,
            "resources",
            "module_guide",
            face_guide_config.FACE_GUIDE_TEMPLATE_FILE_NAME
        )

    if not os.path.exists(template_path):
        raise IOError(
            u"找不到 Face Guide 模板：{}".format(template_path)
        )

    with open(template_path, "rb") as file_object:
        source_data = file_object.read()

    replace_count = [0]

    def replace_locator(match_object):
        old_token = match_object.group(0).decode("ascii")
        is_shape = old_token.endswith("Shape")

        if is_shape:
            old_transform_name = old_token[:-5]
        else:
            old_transform_name = old_token

        new_transform_name = face_guide_config.normalize_legacy_locator_name(
            old_transform_name
        )

        if new_transform_name == old_transform_name:
            return match_object.group(0)

        if is_shape:
            new_token = new_transform_name + "Shape"
        else:
            new_token = new_transform_name

        replace_count[0] = replace_count[0] + 1
        return new_token.encode("ascii")

    target_data = LOCATOR_PATTERN.sub(
        replace_locator,
        source_data
    )

    if target_data != source_data:
        with open(template_path, "wb") as file_object:
            file_object.write(target_data)

    return replace_count[0]


def main():
    u"""执行 Face Guide Locator 模板命名迁移。"""

    replace_count = normalize_template()

    print(
        u"Face Guide Locator naming normalized. Tokens changed: {}".format(
            replace_count
        )
    )


if __name__ == "__main__":
    main()
