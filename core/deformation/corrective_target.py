# coding=utf-8
"""在当前姿势反算修型，并加入已有 BlendShape 的新 Target。"""

import re

import maya.cmds as cmds

from . import blendshape_utils
from ..common import rename_utils, scene_utils


def _unique_node(node):
    """取得唯一完整节点名，拒绝组件和重名节点。"""
    matches = cmds.ls(node, long=True) if node else []
    if not matches or len(matches) != 1 or "." in matches[0]:
        raise ValueError(u"请指定唯一节点：{}".format(node))
    return matches[0]


def _mesh_input(node):
    """验证单一可见 Mesh，并返回 Transform 与 Shape。"""
    node = _unique_node(node)
    shape = blendshape_utils.get_mesh_shape(node)
    if not shape:
        raise ValueError(u"不是有效 Mesh：{}".format(node))
    transform = blendshape_utils.get_transform(shape)
    shapes = cmds.listRelatives(transform, shapes=True, noIntermediate=True,
                                fullPath=True, type="mesh") or []
    if len(shapes) != 1:
        raise ValueError(u"模型必须只有一个可见 Mesh Shape：{}".format(transform))
    return transform, _unique_node(shape)


def _check_topology(base_shape, corrective_shape):
    """比较顶点数量和每个面的顶点索引，拒绝重排或不同拓扑。"""
    for flag in ("vertex", "edge", "face"):
        if cmds.polyEvaluate(base_shape, **{flag: True}) != cmds.polyEvaluate(
                corrective_shape, **{flag: True}):
            raise ValueError(u"基础模型与修型模型的拓扑数量不同。")
    base_faces = cmds.polyInfo(base_shape, faceToVertex=True) or []
    corrective_faces = cmds.polyInfo(corrective_shape, faceToVertex=True) or []
    if not base_faces or len(base_faces) != len(corrective_faces):
        raise ValueError(u"无法验证模型拓扑。")
    for base_face, corrective_face in zip(base_faces, corrective_faces):
        if base_face.split(":", 1)[-1].split() != corrective_face.split(":", 1)[-1].split():
            raise ValueError(u"模型的面连接或顶点索引不同，不能反算。")


def _target_alias(blendshape_node, corrective_mesh, target_name):
    """检查自定义 Alias，空名称自动生成不冲突的 Alias。"""
    alias = target_name.strip()
    if not alias:
        base = rename_utils.get_sanitized_short_name(corrective_mesh) + "_invert"
        alias = base
        suffix = 1
        while cmds.objExists(blendshape_node + "." + alias):
            alias = "{}_{:03d}".format(base, suffix)
            suffix += 1
    if not re.match(r"^[^\W\d]\w*$", alias, re.UNICODE):
        raise ValueError(u"Target 名称只能包含字母、数字和下划线，不能以数字开头。")
    if cmds.objExists(blendshape_node + "." + alias):
        raise ValueError(u"Target 名称已存在：{}".format(alias))
    return alias


def add_inverted_target(controller, blendshape_node, corrective_mesh,
                        base_mesh, target_name=""):
    """反算当前姿势修型，暂时归零控制器并加入一个新 BS Target。

    Args:
        controller (str): 驱动模型的控制器；六个 TR 通道须未锁定且无输入连接。
        blendshape_node (str): 已有 BlendShape，当前仅接受单一基础模型。
        corrective_mesh (str): 当前姿势下雕刻完成的修型模型。
        base_mesh (str): 当前姿势下的基础模型，必须属于指定 BlendShape。
        target_name (str): 新 Target Alias；空字符串自动命名。

    Returns:
        dict: 新 Target 的 alias、index 和完整 weight Plug。

    Raises:
        ValueError: 输入、拓扑、名称或属性状态不满足要求。
        RuntimeError: 反算失败、状态恢复失败或 Undo 未启用。

    Notes:
        不自动连接控制器与 Weight；新 Target 权重为 0。
        失败会撤销本次 Undo Chunk，控制器姿态和原 envelope 均恢复。
        必须在 Maya 中验证模型的变形器顺序是否支持 invertShape。
    """
    controller = _unique_node(controller)
    if not cmds.objectType(controller, isAType="transform"):
        raise ValueError(u"控制器必须是 Transform 或 Joint。")
    blendshape_node = _unique_node(blendshape_node)
    if cmds.nodeType(blendshape_node) != "blendShape":
        raise ValueError(u"指定节点不是 BlendShape。")
    base_mesh, base_shape = _mesh_input(base_mesh)
    corrective_mesh, corrective_shape = _mesh_input(corrective_mesh)
    if base_shape == corrective_shape:
        raise ValueError(u"修型模型与基础模型不能是同一个模型。")
    geometries = cmds.blendShape(blendshape_node, query=True, geometry=True) or []
    if len(geometries) != 1 or _mesh_input(geometries[0])[1] != base_shape:
        raise ValueError(u"BS 必须只作用于指定的基础模型。")
    _check_topology(base_shape, corrective_shape)
    alias = _target_alias(blendshape_node, corrective_mesh, target_name)
    index = blendshape_utils.get_next_target_index(blendshape_node)
    weight_plug = "{}.weight[{}]".format(blendshape_node, index)

    # 修改前验证全部通道。拒绝输入连接，避免写入动画曲线或驱动网络。
    original_values = {}
    channels = ("tx", "ty", "tz", "rx", "ry", "rz")
    for channel in channels:
        plug = controller + "." + channel
        if not cmds.getAttr(plug, settable=True) or cmds.listConnections(
                plug, source=True, destination=False, plugs=True):
            raise ValueError(u"通道已锁定或存在驱动连接：{}".format(plug))
        original_values[plug] = cmds.getAttr(plug)
    envelope_plug = blendshape_node + ".envelope"
    if not cmds.getAttr(envelope_plug, settable=True) or cmds.listConnections(
            envelope_plug, source=True, destination=False, plugs=True):
        raise ValueError(u"BS envelope 已锁定或存在驱动连接。")
    envelope = cmds.getAttr(envelope_plug)
    if not cmds.undoInfo(query=True, state=True):
        raise RuntimeError(u"请先启用 Maya Undo，再添加反算 Target。")
    selection = cmds.ls(selection=True, long=True) or []
    temporary_nodes = []
    mutated = False
    error = None
    recovery_errors = []
    scene_utils.open_undo_chunk("MuziAddInvertedTarget")
    try:
        # 先冻结雕刻快照，再关闭当前 BS，保留其他变形器的姿势。
        snapshot = cmds.duplicate(corrective_mesh, returnRootsOnly=True)[0]
        mutated = True
        temporary_nodes.append(snapshot)
        cmds.delete(snapshot, constructionHistory=True)
        cmds.setAttr(envelope_plug, 0)
        inverted = cmds.invertShape(base_mesh, snapshot)
        if isinstance(inverted, (list, tuple)):
            inverted = inverted[0] if inverted else None
        if not inverted or not cmds.objExists(inverted):
            raise RuntimeError(u"invertShape 没有返回有效修型模型。")
        inverted = _unique_node(inverted)
        if inverted in (_unique_node(base_mesh), _unique_node(corrective_mesh),
                         _unique_node(snapshot)):
            raise RuntimeError(u"invertShape 返回了输入模型，不能作为临时结果删除。")
        temporary_nodes.append(inverted)
        # 在归零前烘焙反算结果，避免动态反算节点随控制器改变。
        cmds.delete(inverted, constructionHistory=True)
        for plug in original_values:
            cmds.setAttr(plug, 0)
        cmds.blendShape(blendshape_node, edit=True,
                        target=(base_mesh, index, inverted, 1.0))
        cmds.aliasAttr(alias, weight_plug)
        cmds.setAttr(weight_plug, 0)
    except Exception as operation_error:
        error = operation_error
    finally:
        # 每个恢复操作独立执行，一个通道失败不阻止其余状态恢复。
        if mutated:
            for plug, value in original_values.items():
                try:
                    cmds.setAttr(plug, value)
                except Exception as restore_error:
                    recovery_errors.append(str(restore_error))
            try:
                cmds.setAttr(envelope_plug, envelope)
            except Exception as restore_error:
                recovery_errors.append(str(restore_error))
            for node in reversed(temporary_nodes):
                try:
                    if cmds.objExists(node):
                        cmds.delete(node)
                except Exception as cleanup_error:
                    recovery_errors.append(str(cleanup_error))
        try:
            if selection:
                cmds.select(selection, replace=True)
            else:
                cmds.select(clear=True)
        except Exception as selection_error:
            recovery_errors.append(str(selection_error))
        scene_utils.close_undo_chunk()
    if error is not None or recovery_errors:
        # 只有已经成功创建快照的 Chunk 才可撤销，避免误撤销用户之前的操作。
        if mutated:
            try:
                cmds.undo()
            except Exception as rollback_error:
                raise RuntimeError(u"添加失败且撤销失败：{}；{}；{}".format(
                    error, recovery_errors, rollback_error))
        raise RuntimeError(u"添加反算 Target 失败：{} {}".format(
            error or "", "; ".join(recovery_errors)))
    return {"alias": alias, "index": index, "plug": weight_plug}
