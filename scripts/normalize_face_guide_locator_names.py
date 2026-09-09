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

该迁移脚本故意不导入 systems / maya，保证可以在普通 Python 和 GitHub Actions
环境中独立执行。正式运行时的 Face Guide 命名配置仍由
systems/face/face_guide_config.py 统一维护。

命令行使用：
    python scripts/normalize_face_guide_locator_names.py
"""

from __future__ import print_function

import os
import re


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
FACE_GUIDE_TEMPLATE_FILE_NAME = "face_guide.ma"

SPECIAL_EYE_FUNCTIONS = (
    "ball",
    "iris",
    "aim",
)

LOCATOR_PATTERN = re.compile(
    rb"loc_[A-Za-z0-9_]+_guide_[0-9]{3}(?:Shape)?"
)


def normalize_legacy_locator_name(locator_name):
    u"""
    将一个旧版 Face Guide Locator 名称转换成新版标准名称。

    普通 Locator 的最后功能字段统一由 guide 改为 bind；
    Eye Ball / Iris / Aim 则移除多余的 guide 字段，让特殊功能本身成为 function。

    locator_name(str): 旧版 Locator Transform 名称。

    Returns:
        str: 新版标准 Locator Transform 名称。

    使用示例：

        print(
            normalize_legacy_locator_name(
                "loc_lf_upper_lid_guide_001"
            )
        )
        # loc_lf_upper_lid_bind_001
    """

    name_parts = locator_name.split("_")

    if len(name_parts) < 5:
        return locator_name

    if name_parts[0] != "loc":
        return locator_name

    if name_parts[-2] != "guide":
        return locator_name

    try:
        index = int(name_parts[-1])
    except ValueError:
        return locator_name

    side = name_parts[1]
    part_tokens = name_parts[2:-2]

    if not part_tokens:
        return locator_name

    # Eye Ball / Iris / Aim：
    # loc_lf_eye_ball_guide_001 -> loc_lf_eye_ball_001
    if len(part_tokens) == 2 and part_tokens[0] == "eye":
        eye_function = part_tokens[1]

        if eye_function in SPECIAL_EYE_FUNCTIONS:
            return "loc_{0}_eye_{1}_{2:03d}".format(
                side,
                eye_function,
                index
            )

    # 其余 Locator 都把原有完整部位作为 part，统一 function="bind"。
    part = "_".join(part_tokens)

    return "loc_{0}_{1}_bind_{2:03d}".format(
        side,
        part,
        index
    )


def normalize_template(template_path=None):
    u"""
    将 Face Guide Maya ASCII 文件中的旧 Locator 名称替换成新版标准名称。

    template_path(str): 可选 face_guide.ma 路径。不传时使用项目默认模板。

    Returns:
        int: 实际替换的旧名称 Token 数量。

    使用示例：

        changed_count = normalize_template()
        print(changed_count)
    """

    if template_path is None:
        template_path = os.path.join(
            REPO_ROOT,
            "resources",
            "module_guide",
            FACE_GUIDE_TEMPLATE_FILE_NAME
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

        new_transform_name = normalize_legacy_locator_name(
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
