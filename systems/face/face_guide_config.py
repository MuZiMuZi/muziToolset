# coding=utf-8
u"""
face_guide_config：Face Guide 命名与模板配置。

这个文件只维护 Face Guide 相关的稳定配置和命名规则，
不负责具体 Eye / Brow / Lip 等绑定模块的构建逻辑。

当前职责：
    1. 固定 Face Guide 模板和 Guide Root 名称。
    2. 统一 Face Locator 的标准命名规则。
    3. 普通定位器统一使用 function="bind"。
    4. Eye Ball / Iris / Aim 保留明确的功能字段。
    5. 提供旧版 loc_*_guide_* 名称到新版标准名称的迁移规则。

后续 Face Rig 的全局 Group、Joint Root、Controller Root、Deformer Root 等
稳定配置也可以继续统一放在这个文件中维护。

标准 Locator 命名：
    loc_<side>_<part>_<function>_<index>

例如：
    loc_lf_ear_bind_001
    loc_md_nose_center_bind_001
    loc_lf_upper_lid_bind_001
    loc_lf_eye_ball_001
    loc_lf_eye_iris_001
    loc_lf_eye_aim_001
"""

from ... import config as package_config
from ...core.common import name_utils


# =============================================================================
# Face Guide 全局配置
# =============================================================================
face_module_name = "face"
face_guide_template_file_name = package_config.module_guide_template_file_format.format(
    face_module_name
)
face_guide_root_name = package_config.module_guide_root_name_format.format(
    face_module_name
)


# =============================================================================
# Locator 命名配置
# =============================================================================
face_guide_default_locator_function = "bind"

# 只有确实需要表达独立功能语义的 Locator 才保留专用 function。
# 目前 Eye Ball / Iris / Aim 属于这种情况。
face_guide_special_locator_functions = (
    "ball",
    "iris",
    "aim",
)


def get_locator_name(
    side,
    part,
    function=face_guide_default_locator_function,
    index=1
):
    u"""
    根据 Face Guide 统一规则生成一个 Locator 名称。

    side(str): Locator 方向，例如 "lf"、"rt"、"md"。
    part(str): Locator 部位，允许使用复合名称，例如 "upper_lid"。
    function(str): Locator 功能，普通定位器默认使用 "bind"。
    index(int): Locator 序号，默认 1。

    Returns:
        str: 标准 Locator 名称。

    Maya 使用示例：

        from muziToolset.systems.face import face_guide_config

        locator_name = face_guide_config.get_locator_name(
            side="lf",
            part="upper_lid",
            function="bind",
            index=1
        )

        print(locator_name)
        # loc_lf_upper_lid_bind_001
    """

    name_object = name_utils.Name(
        type="loc",
        side=side,
        part=part,
        function=function,
        index=index
    )

    return name_object.name


def get_bind_locator_names(side, part, count, start_index=1):
    u"""
    批量生成普通 Face Bind Locator 名称。

    side(str): Locator 方向，例如 "lf"、"rt"、"md"。
    part(str): Locator 部位，例如 "ear"、"tongue"、"upper_lid"。
    count(int): 需要生成的 Locator 数量。
    start_index(int): 起始序号，默认 1。

    Returns:
        list: 按序号排列的标准 Locator 名称列表。

    Maya 使用示例：

        from muziToolset.systems.face import face_guide_config

        locator_names = face_guide_config.get_bind_locator_names(
            side="lf",
            part="ear",
            count=3
        )

        for locator_name in locator_names:
            print(locator_name)
    """

    locator_names = []

    for index in range(start_index, start_index + count):
        locator_name = get_locator_name(
            side=side,
            part=part,
            function=face_guide_default_locator_function,
            index=index
        )
        locator_names.append(locator_name)

    return locator_names


# =============================================================================
# Eye Guide 固定语义名称
# =============================================================================
# Eye 不能依赖 Locator 列表排序判断 Ball / Iris / Aim，
# 所以这里直接固定三个语义入口。
eye_guide_locators = {
    "lf": {
        "ball": get_locator_name("lf", "eye", "ball", 1),
        "iris": get_locator_name("lf", "eye", "iris", 1),
        "aim": get_locator_name("lf", "eye", "aim", 1),
    },
    "rt": {
        "ball": get_locator_name("rt", "eye", "ball", 1),
        "iris": get_locator_name("rt", "eye", "iris", 1),
        "aim": get_locator_name("rt", "eye", "aim", 1),
    },
}


def get_eye_locator(side, function):
    u"""
    获取 Eye Ball / Iris / Aim 的固定 Guide Locator 名称。

    side(str): 只接受 "lf" 或 "rt"。
    function(str): 只接受 "ball"、"iris" 或 "aim"。

    Returns:
        str: 对应 Eye Guide Locator 名称。

    Maya 使用示例：

        from muziToolset.systems.face import face_guide_config

        aim_guide = face_guide_config.get_eye_locator(
            "lf",
            "aim"
        )

        print(aim_guide)
        # loc_lf_eye_aim_001
    """

    if side not in eye_guide_locators:
        raise ValueError(
            u"Eye Guide side 只能使用 'lf' 或 'rt'，当前值：{}".format(side)
        )

    if function not in face_guide_special_locator_functions:
        raise ValueError(
            u"Eye Guide function 只能使用 ball / iris / aim，当前值：{}".format(function)
        )

    return eye_guide_locators[side][function]


# =============================================================================
# 旧 Locator 名称迁移
# =============================================================================
def normalize_legacy_locator_name(locator_name):
    u"""
    将旧版 loc_*_guide_* Locator 名称转换成新版标准名称。

    普通 Locator：
        loc_lf_ear_guide_001
            -> loc_lf_ear_bind_001

        loc_lf_upper_lid_guide_001
            -> loc_lf_upper_lid_bind_001

        loc_md_nose_center_guide_001
            -> loc_md_nose_center_bind_001

    Eye 特殊 Locator：
        loc_lf_eye_ball_guide_001
            -> loc_lf_eye_ball_001

        loc_lf_eye_iris_guide_001
            -> loc_lf_eye_iris_001

        loc_lf_eye_aim_guide_001
            -> loc_lf_eye_aim_001

    已经符合新版规则的名称会原样返回。

    locator_name(str): 需要检查的 Locator Transform 名称。

    Returns:
        str: 新版标准 Locator 名称。

    Maya 使用示例：

        from muziToolset.systems.face import face_guide_config

        new_name = face_guide_config.normalize_legacy_locator_name(
            "loc_lf_upper_lid_guide_001"
        )

        print(new_name)
        # loc_lf_upper_lid_bind_001
    """

    if not locator_name:
        return locator_name

    # 这里只处理 Transform 短名称。
    # Maya DAG Path 或 Namespace 如果存在，先保留前缀，最后再拼回去。
    dag_prefix = ""
    short_name = locator_name

    if "|" in short_name:
        dag_parts = short_name.split("|")
        short_name = dag_parts[-1]
        dag_prefix = "|".join(dag_parts[:-1])

        if dag_prefix:
            dag_prefix = dag_prefix + "|"

    namespace_prefix = ""

    if ":" in short_name:
        namespace_parts = short_name.rsplit(":", 1)
        namespace_prefix = namespace_parts[0] + ":"
        short_name = namespace_parts[1]

    name_parts = short_name.split("_")

    # 新规则至少需要：loc / side / part / function / index。
    if len(name_parts) < 5:
        return locator_name

    if name_parts[0] != "loc":
        return locator_name

    # 只迁移旧版 function="guide" 的 Locator。
    if name_parts[-2] != "guide":
        return locator_name

    index_text = name_parts[-1]

    try:
        index = int(index_text)
    except ValueError:
        return locator_name

    side = name_parts[1]
    legacy_part_tokens = name_parts[2:-2]

    if not legacy_part_tokens:
        return locator_name

    # Eye Ball / Iris / Aim 需要把最后一段语义作为真正的 function。
    # 例如 eye_ball -> part="eye", function="ball"。
    if len(legacy_part_tokens) == 2:
        if legacy_part_tokens[0] == "eye":
            special_function = legacy_part_tokens[1]

            if special_function in face_guide_special_locator_functions:
                part = "eye"
                function = special_function
            else:
                part = "_".join(legacy_part_tokens)
                function = face_guide_default_locator_function
        else:
            part = "_".join(legacy_part_tokens)
            function = face_guide_default_locator_function

    else:
        part = "_".join(legacy_part_tokens)
        function = face_guide_default_locator_function

    normalized_name = get_locator_name(
        side=side,
        part=part,
        function=function,
        index=index
    )

    return dag_prefix + namespace_prefix + normalized_name


def rename_scene_locators():
    u"""
    将当前 Maya 场景中的旧版 Face Locator 批量重命名为新版标准名称。

    该方法只修改真正带 Locator Shape 的 Transform，
    不会修改 zero_*_guide_*、grp_*_guide_*、crv_*_guide_* 等 Guide 基础层级名称。

    在真正改名之前会先检查所有目标名称是否已经被其他节点占用，
    避免迁移过程中出现名称冲突。

    Returns:
        dict: {旧名称: 新名称} 的实际重命名结果。

    Maya 使用示例：

        from muziToolset.systems.face import face_guide_config

        rename_result = face_guide_config.rename_scene_locators()

        for old_name in sorted(rename_result):
            print(old_name, "->", rename_result[old_name])
    """

    # Lazy Import：让这个配置文件在普通 Python / CI 环境中也可以被导入。
    import maya.cmds as cmds

    locator_shapes = cmds.ls(type="locator", long=False) or []
    locator_transforms = []

    for locator_shape in locator_shapes:
        parent_nodes = cmds.listRelatives(
            locator_shape,
            parent=True,
            fullPath=False
        ) or []

        if not parent_nodes:
            continue

        locator_transform = parent_nodes[0]

        if locator_transform not in locator_transforms:
            locator_transforms.append(locator_transform)

    rename_map = {}

    for locator_transform in locator_transforms:
        normalized_name = normalize_legacy_locator_name(
            locator_transform
        )

        if normalized_name == locator_transform:
            continue

        rename_map[locator_transform] = normalized_name

    # 先检查所有 Target，任何一个冲突都不进行场景修改。
    for old_name in rename_map:
        new_name = rename_map[old_name]

        if cmds.objExists(new_name):
            raise RuntimeError(
                u"无法重命名 {} -> {}，目标名称已经存在。".format(
                    old_name,
                    new_name
                )
            )

    rename_result = {}

    for old_name in sorted(rename_map):
        new_name = rename_map[old_name]
        renamed_transform = cmds.rename(
            old_name,
            new_name
        )

        # Maya 通常会随着 Transform 一起更新同前缀 Shape 名称。
        # 这里再检查一次，确保 Locator Shape 最终也使用 <Transform>Shape。
        locator_shapes = cmds.listRelatives(
            renamed_transform,
            shapes=True,
            noIntermediate=True,
            fullPath=False
        ) or []

        for locator_shape in locator_shapes:
            if cmds.nodeType(locator_shape) != "locator":
                continue

            target_shape_name = renamed_transform + "Shape"

            if locator_shape != target_shape_name:
                if not cmds.objExists(target_shape_name):
                    cmds.rename(
                        locator_shape,
                        target_shape_name
                    )

        rename_result[old_name] = renamed_transform

    return rename_result
