# coding=utf-8
"""BlendShape Target Alias 的左右复制命名整理。"""

import maya.cmds as cmds

from . import blendshape_utils
from ..common import scene_utils


def rename_mirrored_targets(blendshape_node):
    """把 lf_*_Copy 的 Alias 改为 rt_*，保持真实 Weight Index 与连接。

    Args:
        blendshape_node (str): 需要整理 Target Alias 的 BlendShape 节点。

    Returns:
        list[dict]: 每次改名的 old_alias、alias 和 index。

    Raises:
        ValueError: BS 无效或新 Alias 与已有属性发生冲突。
        RuntimeError: 改名失败；已经修改的 Alias 会尝试恢复。

    Notes:
        只替换开头 lf_ 和结尾 _Copy，不修改中间相同文本。
        只修改 Alias，不镜像几何，也不自动建立权重驱动。
    """
    if not cmds.objExists(blendshape_node) or cmds.nodeType(blendshape_node) != "blendShape":
        raise ValueError(u"请指定有效 BlendShape 节点。")
    targets = blendshape_utils.get_targets(blendshape_node)
    aliases = set()
    for target in targets:
        aliases.add(target["alias"])
    planned = []
    for target in targets:
        old_alias = target["alias"]
        if not old_alias.startswith("lf_") or not old_alias.endswith("_Copy"):
            continue
        new_alias = "rt_" + old_alias[3:-5]
        if new_alias in aliases or cmds.objExists(blendshape_node + "." + new_alias):
            raise ValueError(u"Target 名称已存在，未执行改名：{}".format(new_alias))
        aliases.add(new_alias)
        planned.append({"old_alias": old_alias, "alias": new_alias,
                        "index": target["index"]})
    if not planned:
        return []
    applied = []
    scene_utils.open_undo_chunk("MuziRenameMirroredTargets")
    try:
        for target in planned:
            plug = "{}.weight[{}]".format(blendshape_node, target["index"])
            cmds.aliasAttr(target["alias"], plug)
            applied.append(target)
    except Exception as error:
        recovery_errors = []
        for target in reversed(applied):
            try:
                cmds.aliasAttr(target["old_alias"], "{}.weight[{}]".format(
                    blendshape_node, target["index"]))
            except Exception as restore_error:
                recovery_errors.append(str(restore_error))
        raise RuntimeError(u"改名失败：{} {}".format(error, "; ".join(recovery_errors)))
    finally:
        scene_utils.close_undo_chunk()
    return planned
