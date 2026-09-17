# coding=utf-8
u"""
Rig Library Catalog
===================

绑定库的**纯 Python 模块目录、Template Catalog、配置 Schema 与 Naming Projection**。

这个文件刻意不 Import Maya。它负责回答：

    - 当前 Rig Library 正式接入了哪些 Module；
    - 每个 Module 默认需要多少 Guide、默认 Side 和 UI Metadata；
    - Template 会组合哪些 Module；
    - 一条 Module Record 的合法字段是什么；
    - 一个 Record 应该使用哪些 Guide 名称；
    - Build 前预期会生成哪些 Joint / Controller / Group / Output 名称；
    - 导入 JSON 时如何严格校验，避免部分写入或配置冲突。

当前正式 Module：
    ear
        三段 FK EarModule，支持 lf / rt。

    eye
        Main + Aim EyeModule，支持 lf / rt。

    tongue
        五段 FK TongueModule，使用 md。

    fk_chain
        通用 FKChain，需要用户明确提供有序 Guide。

设计边界：
    - 不 Import maya.cmds；
    - 不创建 / 删除 Maya Node；
    - 不执行 Build / Rebuild / Final；
    - 不负责 Qt；
    - Maya Scene 调度由 ``library_service.RigLibraryService`` 负责。

配置 Record 的关键状态：
    built
        Joint / Controller / Hierarchy 是否已经生成并通过输出检查。

    connected
        当前输出是否已经执行 Final Connection。

允许状态：
    built=False, connected=False
    built=True,  connected=False
    built=True,  connected=True

禁止状态：
    built=False, connected=True
"""

import copy
import math
import re
import uuid


modules = (
    {"key": "ear", "title": u"Ear / 耳朵", "code": "EAR", "color": "#167c89",
     "description": u"三段耳朵 FK 链，支持左右侧。", "count": 3, "side": "lf"},
    {"key": "eye", "title": u"Eye / 眼球", "code": "EYE", "color": "#3f6fb5",
     "description": u"眼球 Main + Aim 目光控制，支持左右侧。", "count": 3, "side": "lf"},
    {"key": "tongue", "title": u"Tongue / 舌头", "code": "TNG", "color": "#ad5077",
     "description": u"五段舌头 FK 链，沿用现有面部 Guide。", "count": 5, "side": "md"},
    {"key": "fk_chain", "title": u"FK Chain / 通用链", "code": "FK", "color": "#4677af",
     "description": u"按指定 Guide 顺序构建，可自定义名称与数量。", "count": 3, "side": "md"},
)

templates = (
    {"key": "face_starter", "title": u"Face Starter / 面部起步", "code": "01",
     "description": u"左耳 + 右耳 + 舌头 · 3 个模块 / 11 个关节",
     "modules": (("ear", "lf"), ("ear", "rt"), ("tongue", "md"))},
    {"key": "ear_pair", "title": u"Ear Pair / 左右耳", "code": "02",
     "description": u"左右耳朵 FK · 2 个模块 / 6 个关节",
     "modules": (("ear", "lf"), ("ear", "rt"))},
    {"key": "tongue", "title": u"Tongue / 舌头", "code": "03",
     "description": u"中央舌头 FK · 1 个模块 / 5 个关节",
     "modules": (("tongue", "md"),)},
    {"key": "eye_pair", "title": u"Eye Pair / 左右眼球", "code": "04",
     "description": u"左右眼球 Aim · 2 个模块 / 2 个关节",
     "modules": (("eye", "lf"), ("eye", "rt"))},
)

axes = ("X+", "X-", "Y+", "Y-", "Z+", "Z-")
side_colors = {"lf": 6, "rt": 13, "md": 17}


def get_module(key):
    u"""
    返回一个已正式接入 Rig Library 的 Module Catalog Entry。

    Args:
        key (str):
            Module 类型键。当前支持 ``ear``、``eye``、``tongue``、``fk_chain``。

    Returns:
        dict:
            Catalog Entry，包含 ``key / title / code / color / description / count / side``。

    Raises:
        ValueError:
            ``key`` 没有正式后端时抛出。函数不会偷偷退回到通用 FKChain。

    Example:
        >>> from muziToolset.systems.rig import library_catalog
        >>> eye = library_catalog.get_module("eye")
        >>> print(eye["count"])
        3
    """

    for entry in modules:
        if entry["key"] == key:
            return entry

    raise ValueError(
        u"绑定库尚未接入模块：{}".format(key)
    )


def new_document():
    u"""
    创建一个空的 Rig Library Version 1 配置文档。

    打开窗口时使用空配置，而不是自动插入示例 Module，因此仅打开 UI 不会改变用户场景。

    Returns:
        dict:
            ``{"version": 1, "modules": []}``。

    Example:
        >>> document = new_document()
        >>> document["modules"]
        []
    """

    return {
        "version": 1,
        "modules": []
    }


def new_module(key, side=None, name=None):
    u"""
    根据 Catalog 默认值创建一条可序列化 Module Record。

    Args:
        key (str):
            正式 Module 类型键。
        side (str | None):
            可选方向。None 时使用 Catalog 默认值；有效值为 ``lf / rt / md``。
        name (str | None):
            可选 Module Part 名称。正式 Ear / Eye / Tongue 后续校验要求名称保持固定；
            自定义名称主要用于 ``fk_chain``。

    Returns:
        dict:
            包含唯一 ``id``、Guide、Controller / Joint 显示参数和 Build State 的 Module Record。

    Notes:
        新 Record 初始始终为 ``built=False``、``connected=False``。
        ``ctrl_color`` 根据 Side 使用 ``lf=6 / rt=13 / md=17`` 默认值。
    """

    entry = get_module(key)
    side = side or entry["side"]

    return {
        "id": uuid.uuid4().hex,
        "kind": key,
        "name": name or ("chain" if key == "fk_chain" else key),
        "side": side,
        "enabled": True,
        "guides": [],
        "ctrl_size": 1.0,
        "ctrl_color": side_colors[side],
        "ctrl_axis": "X+",
        "jnt_radius": 1.0,
        "show_axis": False,
        "show_joints": True,
        "show_controls": True,
        "built": False,
        "connected": False,
    }


def guide_names(record):
    u"""
    返回一条 Module Record 实际使用的有序 Guide 名称。

    解析优先级：

    1. ``record["guides"]`` 非空时，严格使用用户保存的显式顺序；
    2. ``fk_chain`` 没有显式 Guide 时返回空列表，强制用户指定；
    3. ``eye`` 使用 Ball / Iris / Aim 固定语义名称；
    4. Ear / Tongue 等标准线性模块按 ``bind_001...`` 生成。

    Args:
        record (dict):
            已通过或准备通过 ``validate_document`` 校验的 Module Record。

    Returns:
        list[str]:
            有序 Guide 名称列表。

    Example:
        >>> record = new_module("eye", "lf")
        >>> guide_names(record)
        ['loc_lf_eye_ball_001', 'loc_lf_eye_iris_001', 'loc_lf_eye_aim_001']

    Notes:
        Eye 不能把 Guide 简单当成 ``bind_001 / 002 / 003``，因为 Ball、Iris、Aim
        分别代表旋转中心、Main Ctrl 可见位置和 Aim Ctrl 位置。
    """

    if record["guides"]:
        return list(
            record["guides"]
        )

    if record["kind"] == "fk_chain":
        return []

    if record["kind"] == "eye":
        return [
            "loc_{}_eye_ball_001".format(
                record["side"]
            ),
            "loc_{}_eye_iris_001".format(
                record["side"]
            ),
            "loc_{}_eye_aim_001".format(
                record["side"]
            ),
        ]

    result = []
    count = get_module(
        record["kind"]
    )["count"]

    for index in range(1, count + 1):
        result.append(
            "loc_{}_{}_bind_{:03d}".format(
                record["side"],
                record["kind"],
                index
            )
        )

    return result


def _append_ctrl_outputs(result, side, part, function, index=1):
    u"""
    向 ``output_names()`` 结果追加一套标准 Controller Hierarchy 名称。

    Args:
        result (dict):
            ``output_names`` 正在构建的结果字典。
        side (str):
            Controller Side Token。
        part (str):
            Controller Part Token。
        function (str):
            Controller Function Token，例如 ``main`` 或 ``aim``。
        index (int):
            Controller 序号。

    Returns:
        None:
            直接修改传入 ``result``。
    """

    suffix = "{}_{}_{}_{:03d}".format(
        side,
        part,
        function,
        index
    )

    result["controls"].append(
        "ctrl_" + suffix
    )
    result["subcontrols"].append(
        "subctrl_" + suffix
    )
    result["outputs"].append(
        "output_" + suffix
    )

    for prefix in (
        "zero",
        "driven",
        "space",
        "connect",
        "offset"
    ):
        result["groups"].append(
            prefix + "_" + suffix
        )


def output_names(record):
    u"""
    计算 Module Build 后应存在的全部稳定输出名称。

    这个函数不查询 Maya Scene，只根据 Record 的 Naming Contract 生成预期名称。
    ``RigLibraryService`` 使用结果进行：

    - Build 前名称冲突检查；
    - Build 完整性验证；
    - Ownership Tag；
    - Rebuild 删除范围；
    - Structure / Display 查询。

    Args:
        record (dict):
            Module Record。

    Returns:
        dict:
            包含 ``joints / controls / subcontrols / groups / outputs`` 五类名称列表。

    Notes:
        Eye 使用 Main + Aim 两套 Controller Hierarchy；FK 类模块按 Guide 数量生成
        ``fk_001...`` Controller 与 ``bind_001...`` Joint。
    """

    result = {
        "joints": [],
        "controls": [],
        "subcontrols": [],
        "groups": [],
        "outputs": []
    }

    for function in (
        "jnt",
        "ctrl"
    ):
        result["groups"].append(
            "grp_{}_{}_{}_001".format(
                record["side"],
                record["name"],
                function
            )
        )

    if record["kind"] == "eye":
        result["joints"].append(
            "jnt_{}_eye_bind_001".format(
                record["side"]
            )
        )

        _append_ctrl_outputs(
            result,
            record["side"],
            record["name"],
            "main"
        )
        _append_ctrl_outputs(
            result,
            record["side"],
            record["name"],
            "aim"
        )

        return result

    for index in range(
        1,
        len(guide_names(record)) + 1
    ):
        suffix = "{}_{}_fk_{:03d}".format(
            record["side"],
            record["name"],
            index
        )

        result["joints"].append(
            "jnt_{}_{}_bind_{:03d}".format(
                record["side"],
                record["name"],
                index
            )
        )
        result["controls"].append(
            "ctrl_" + suffix
        )
        result["subcontrols"].append(
            "subctrl_" + suffix
        )
        result["outputs"].append(
            "output_" + suffix
        )

        for prefix in (
            "zero",
            "driven",
            "space",
            "connect",
            "offset"
        ):
            result["groups"].append(
                prefix + "_" + suffix
            )

    return result


def validate_document(document):
    u"""
    严格校验 Rig Library 配置，并返回深拷贝后的安全 Document。

    校验内容包括：

    - Schema Version；
    - Module 数量上限；
    - Record 字段集合；
    - Module 是否已正式登记；
    - Name / Side / ID；
    - 重复 Module Identity；
    - bool / float / color / axis 类型和范围；
    - Guide 数量、路径类型和重复项；
    - ``connected`` 不能先于 ``built``；
    - 已 Build Module 必须能够解析 Guide。

    Version 1 的早期 Record 如果只缺 ``connected`` 字段，会把它迁移为与旧 ``built``
    状态一致，再继续完整校验。

    Args:
        document (dict):
            待校验的 JSON-compatible Rig Library Document。

    Returns:
        dict:
            与输入隔离的深拷贝、安全配置。后续 Service 修改这个副本不会修改调用方对象。

    Raises:
        ValueError:
            Version、字段、Module、命名、Side、数值、Guide 或 Build State 任一项不合法时抛出。

    Notes:
        这个函数是配置写入 Scene Network、JSON Import 和 Service Commit 前的共同边界。
        不要为了“尽量加载”而忽略未知字段，否则旧 / 损坏配置会部分进入 Maya Scene。
    """

    if not isinstance(document, dict) or document.get("version") != 1:
        raise ValueError(
            u"无法识别绑定库配置版本。"
        )

    document = copy.deepcopy(
        document
    )
    records = document.get(
        "modules"
    )

    if not isinstance(records, list) or len(records) > 100:
        raise ValueError(
            u"配置必须包含模块列表，最多 100 个模块。"
        )

    ids = set()
    identities = set()

    for record in records:
        if not isinstance(record, dict):
            raise ValueError(
                u"模块配置必须为字典。"
            )

        required = set(
            new_module("ear")
        )
        legacy_required = required - {
            "connected"
        }

        if set(record) == legacy_required:
            record["connected"] = record["built"]

        if set(record) != required:
            raise ValueError(
                u"模块配置字段缺失或包含不支持的字段。"
            )

        get_module(
            record["kind"]
        )

        name = record["name"]

        if not isinstance(name, str) or not re.fullmatch(
            r"[a-z][a-z0-9_]{0,39}",
            name
        ):
            raise ValueError(
                u"模块名使用小写英文、数字和下划线，并以字母开头。"
            )

        if record["kind"] != "fk_chain" and name != record["kind"]:
            raise ValueError(
                u"正式模块沿用后端固定名称；自定义名称请使用 FK Chain。"
            )

        side = record["side"]

        if side not in side_colors:
            raise ValueError(
                u"Side 只支持 lf / rt / md。"
            )

        if record["kind"] in (
            "ear",
            "eye"
        ):
            if side not in (
                "lf",
                "rt"
            ):
                raise ValueError(
                    u"{} 请选择左侧或右侧。".format(
                        name
                    )
                )

        if record["kind"] == "tongue" and side != "md":
            raise ValueError(
                u"舌头模板使用中央 md。"
            )

        identity = (
            side,
            name
        )

        if identity in identities:
            raise ValueError(
                u"{} / {} 已在绑定结构中。".format(
                    name,
                    side
                )
            )

        identities.add(
            identity
        )

        identity_id = record["id"]

        if not isinstance(identity_id, str) or not re.fullmatch(
            r"[0-9a-f]{32}",
            identity_id
        ):
            raise ValueError(
                u"无效的模块标识。"
            )

        if identity_id in ids:
            raise ValueError(
                u"模块标识重复。"
            )

        ids.add(
            identity_id
        )

        for key in (
            "enabled",
            "built",
            "connected",
            "show_axis",
            "show_joints",
            "show_controls"
        ):
            if type(record[key]) is not bool:
                raise ValueError(
                    u"{} 必须为布尔值。".format(
                        key
                    )
                )

        if record["connected"] and not record["built"]:
            raise ValueError(
                u"模块尚未生成，不能标记为已经连接。"
            )

        for key in (
            "ctrl_size",
            "jnt_radius"
        ):
            value = record[key]

            if type(value) not in (int, float) or not math.isfinite(value) or not 0.01 <= value <= 100.0:
                raise ValueError(
                    u"{} 必须在 0.01 到 100 之间。".format(
                        key
                    )
                )

        if type(record["ctrl_color"]) is not int or not 0 <= record["ctrl_color"] <= 31:
            raise ValueError(
                u"颜色索引必须在 0 到 31 之间。"
            )

        if record["ctrl_axis"] not in axes:
            raise ValueError(
                u"不支持的控制器轴向。"
            )

        guides = record["guides"]

        if not isinstance(guides, list) or len(guides) > 99:
            raise ValueError(
                u"Guide 列表最多支持 99 个节点。"
            )

        for guide in guides:
            if not isinstance(guide, str) or not guide or len(guide) > 1024:
                raise ValueError(
                    u"Guide 必须为有效的 Maya 节点路径。"
                )

        if len(set(guides)) != len(guides):
            raise ValueError(
                u"Guide 列表中有重复节点。"
            )

        if guides and record["kind"] != "fk_chain":
            if len(guides) != get_module(record["kind"])["count"]:
                raise ValueError(
                    u"{} 的 Guide 数量不符合模块要求。".format(
                        name
                    )
                )

        if record["built"] and not guide_names(record):
            raise ValueError(
                u"已构建模块必须具有 Guide 数据。"
            )

    return document


def add_template(document, key):
    u"""
    原子地把一个 Catalog Template 追加到现有配置中。

    已存在的 ``(side, module name)`` 不会重复插入，因此用户已经调整的 Size、Color、
    Guide 或显示参数会被保留。新增 Record 使用 ``new_module()`` 默认值；最终结果再次
    经过 ``validate_document()``。

    Args:
        document (dict):
            当前 Rig Library Document。
        key (str):
            Template Key，例如 ``face_starter``、``ear_pair``、``tongue``、``eye_pair``。

    Returns:
        dict:
            添加完成并重新校验后的独立 Document。

    Raises:
        ValueError:
            Template Key 不存在，或输入 / 最终 Document 不满足 Schema 时抛出。

    Example:
        >>> document = new_document()
        >>> document = add_template(document, "eye_pair")
        >>> len(document["modules"])
        2
    """

    result = validate_document(
        document
    )
    template = None

    for entry in templates:
        if entry["key"] == key:
            template = entry
            break

    if template is None:
        raise ValueError(
            u"未知模板：{}".format(
                key
            )
        )

    for kind, side in template["modules"]:
        exists = False

        for record in result["modules"]:
            if record["name"] == kind and record["side"] == side:
                exists = True
                break

        if not exists:
            result["modules"].append(
                new_module(
                    kind,
                    side
                )
            )

    return validate_document(
        result
    )
