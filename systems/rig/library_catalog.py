# coding=utf-8
u"""绑定库目录和配置校验。只登记当前正式后端，不导入 Maya 或历史模块。"""

import copy
import math
import re
import uuid


modules = (
    {"key": "ear", "title": u"Ear / 耳朵", "code": "EAR", "color": "#167c89",
     "description": u"三段耳朵 FK 链，支持左右侧。", "count": 3, "side": "lf"},
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
)

axes = ("X+", "X-", "Y+", "Y-", "Z+", "Z-")
side_colors = {"lf": 6, "rt": 13, "md": 17}


def get_module(key):
    u"""取得可用模块的登记信息；未实现模块不会隐式退回通用 FK。"""
    for entry in modules:
        if entry["key"] == key:
            return entry
    raise ValueError(u"绑定库尚未接入模块：{}".format(key))


def new_document():
    u"""创建空配置；打开窗口本身不会添加示例场景数据。"""
    return {"version": 1, "modules": []}


def new_module(key, side=None, name=None):
    u"""根据正式模块默认值创建可序列化配置。"""
    entry = get_module(key)
    side = side or entry["side"]
    return {
        "id": uuid.uuid4().hex, "kind": key,
        "name": name or ("chain" if key == "fk_chain" else key),
        "side": side, "enabled": True, "guides": [],
        "ctrl_size": 1.0, "ctrl_color": side_colors[side], "ctrl_axis": "X+",
        "jnt_radius": 1.0, "show_axis": False, "show_joints": True,
        "show_controls": True, "built": False,
    }


def guide_names(record):
    u"""优先使用明确指定的有序 Guide；耳朵和舌头可按模板名称读取。"""
    if record["guides"]:
        return list(record["guides"])
    if record["kind"] == "fk_chain":
        return []
    result = []
    count = get_module(record["kind"])["count"]
    for index in range(1, count + 1):
        result.append("loc_{}_{}_bind_{:03d}".format(record["side"], record["kind"], index))
    return result


def output_names(record):
    u"""返回后端实际使用的名称，用于构建前冲突检查与场景树查询。"""
    result = {"joints": [], "controls": [], "subcontrols": [], "groups": [], "outputs": []}
    for function in ("jnt", "ctrl"):
        result["groups"].append("grp_{}_{}_{}_001".format(record["side"], record["name"], function))
    for index in range(1, len(guide_names(record)) + 1):
        suffix = "{}_{}_fk_{:03d}".format(record["side"], record["name"], index)
        result["joints"].append("jnt_{}_{}_bind_{:03d}".format(record["side"], record["name"], index))
        result["controls"].append("ctrl_" + suffix)
        result["subcontrols"].append("subctrl_" + suffix)
        result["outputs"].append("output_" + suffix)
        for prefix in ("zero", "driven", "space", "connect", "offset"):
            result["groups"].append(prefix + "_" + suffix)
    return result


def validate_document(document):
    u"""严格校验配置后返回独立副本，防止部分参数写入或覆盖同名模块。"""
    if not isinstance(document, dict) or document.get("version") != 1:
        raise ValueError(u"无法识别绑定库配置版本。")
    records = document.get("modules")
    if not isinstance(records, list) or len(records) > 100:
        raise ValueError(u"配置必须包含模块列表，最多 100 个模块。")
    ids = set()
    identities = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(u"模块配置必须为字典。")
        required = set(new_module("ear"))
        if set(record) != required:
            raise ValueError(u"模块配置字段缺失或包含不支持的字段。")
        get_module(record["kind"])
        name = record["name"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name):
            raise ValueError(u"模块名使用小写英文、数字和下划线，并以字母开头。")
        if record["kind"] != "fk_chain" and name != record["kind"]:
            raise ValueError(u"耳朵和舌头沿用后端固定名称；自定义名称请使用 FK Chain。")
        side = record["side"]
        if side not in side_colors:
            raise ValueError(u"Side 只支持 lf / rt / md。")
        if record["kind"] == "ear" and side not in ("lf", "rt"):
            raise ValueError(u"耳朵请选择左侧或右侧。")
        if record["kind"] == "tongue" and side != "md":
            raise ValueError(u"舌头模板使用中央 md。")
        identity = (side, name)
        if identity in identities:
            raise ValueError(u"{} / {} 已在绑定结构中。".format(name, side))
        identities.add(identity)
        identity_id = record["id"]
        if not isinstance(identity_id, str) or not re.fullmatch(r"[0-9a-f]{32}", identity_id):
            raise ValueError(u"无效的模块标识。")
        if identity_id in ids:
            raise ValueError(u"模块标识重复。")
        ids.add(identity_id)
        for key in ("enabled", "built", "show_axis", "show_joints", "show_controls"):
            if type(record[key]) is not bool:
                raise ValueError(u"{} 必须为布尔值。".format(key))
        for key in ("ctrl_size", "jnt_radius"):
            value = record[key]
            if type(value) not in (int, float) or not math.isfinite(value) or not 0.01 <= value <= 100.0:
                raise ValueError(u"{} 必须在 0.01 到 100 之间。".format(key))
        if type(record["ctrl_color"]) is not int or not 0 <= record["ctrl_color"] <= 31:
            raise ValueError(u"颜色索引必须在 0 到 31 之间。")
        if record["ctrl_axis"] not in axes:
            raise ValueError(u"不支持的控制器轴向。")
        guides = record["guides"]
        if not isinstance(guides, list) or len(guides) > 99:
            raise ValueError(u"Guide 列表最多支持 99 个节点。")
        for guide in guides:
            if not isinstance(guide, str) or not guide or len(guide) > 1024:
                raise ValueError(u"Guide 必须为有效的 Maya 节点路径。")
        if len(set(guides)) != len(guides):
            raise ValueError(u"Guide 列表中有重复节点。")
        if guides and record["kind"] != "fk_chain":
            if len(guides) != get_module(record["kind"])["count"]:
                raise ValueError(u"{} 的 Guide 数量不符合模块要求。".format(name))
        if record["built"] and not guide_names(record):
            raise ValueError(u"已构建模块必须具有 Guide 数据。")
    return copy.deepcopy(document)


def add_template(document, key):
    u"""以原子方式添加模板；重复模块保留用户已经调整的设置。"""
    result = validate_document(document)
    template = None
    for entry in templates:
        if entry["key"] == key:
            template = entry
            break
    if template is None:
        raise ValueError(u"未知模板：{}".format(key))
    for kind, side in template["modules"]:
        exists = False
        for record in result["modules"]:
            if record["name"] == kind and record["side"] == side:
                exists = True
                break
        if not exists:
            result["modules"].append(new_module(kind, side))
    return validate_document(result)
