# coding=utf-8
"""输出端点映射；角度、距离和普通数值分别使用对应的 Driven 曲线。"""
import math
import maya.cmds as cmds
from ...core.common import scene_utils, connection_utils

CURVE_TYPES = {'doubleAngle': 'animCurveUA', 'doubleLinear': 'animCurveUL',
               'double': 'animCurveUU', 'float': 'animCurveUU'}


def get_output_mappings(output):
    """返回所属输出映射节点；兼容未创建映射属性的旧场景。

    Args:
        output (str): 已构建的输出 network 名称。
    Returns:
        list[str]: 属于该网络的映射曲线，旧场景可返回空列表。
    """
    if not cmds.attributeQuery('outputMappings', node=output, exists=True):
        return []
    return cmds.listConnections(output + '.outputMappings', source=True, destination=False) or []


@scene_utils.undo_chunk
def connect_mapped_output(driver, name, destination, full_value, neutral_value=None):
    """将权重 0~1 线性映射为辅助骨或标量属性的两个端点，拒绝覆盖连接。

    Args:
        driver (RbfDriver): 已构建或已恢复驱动。
        name (str): 输出姿态名称。
        destination (str): 辅助骨 rotate / translate / scale 或浮点属性 Plug。
        full_value (float): 权重 1 对应数值，使用 Maya 当前角度或距离单位。
        neutral_value (float | None): 权重 0 对应数值，默认读取目标当前值。
    Returns:
        str: 所属映射曲线；重建保留曲线，删除 Driver 同时清理曲线。
    """
    source = driver.get_output_plug(name)
    if not cmds.objExists(destination):
        raise ValueError('目标属性不存在：' + destination)
    kind = cmds.getAttr(destination, type=True)
    if kind not in CURVE_TYPES:
        raise ValueError('映射目标必须为角度、距离或浮点属性')
    if not cmds.getAttr(destination, settable=True) or cmds.listConnections(destination, source=True, destination=False):
        raise RuntimeError('目标已有连接或不可设置：' + destination)
    if neutral_value is None:
        neutral_value = cmds.getAttr(destination)
    for value in (neutral_value, full_value):
        if not math.isfinite(value):
            raise ValueError('映射端点必须为有限数值')
    index = 1
    kind = CURVE_TYPES[kind]
    while cmds.objExists(driver.get_name(kind, 'rbfMapping', index)):
        index += 1
    curve = scene_utils.create_node(kind, driver.get_name(kind, 'rbfMapping', index))
    try:
        # float 是无时间输入；切线和无穷区间保证区间内线性、区间外端点保持。
        for weight, value in ((0.0, neutral_value), (1.0, full_value)):
            cmds.setKeyframe(curve, float=weight, value=value, inTangentType='linear', outTangentType='linear')
        cmds.setInfinity(curve, preInfinite='constant', postInfinite='constant')
        if not connection_utils.connect_plugs(source, curve + '.input'):
            raise RuntimeError('输出映射输入连接失败')
        if not connection_utils.connect_plugs(curve + '.output', destination):
            raise RuntimeError('输出映射目标已有连接：' + destination)
        if not cmds.attributeQuery('outputMappings', node=driver.output, exists=True):
            cmds.addAttr(driver.output, longName='outputMappings', attributeType='message', multi=True)
        indices = cmds.getAttr(driver.output + '.outputMappings', multiIndices=True) or []
        slot = max(indices) + 1 if indices else 0
        if not connection_utils.connect_plugs(curve + '.message', '{}.outputMappings[{}]'.format(driver.output, slot)):
            raise RuntimeError('输出映射所有权连接失败')
    except Exception:
        cmds.delete(curve)
        raise
    return curve


@scene_utils.undo_chunk
def disconnect_mapped_output(driver, destination):
    """删除当前 Driver 对目标属性的映射；不认领外部曲线。

    Args:
        driver (RbfDriver): 已构建或已恢复驱动。
        destination (str): 已通过当前 Driver 映射的目标 Plug。
    Returns:
        bool: 成功返回 True；没有所属映射则抛出 ValueError。
    """
    driver.get_output_plug(driver.model.get_output_names()[0])
    for curve in get_output_mappings(driver.output):
        targets = cmds.listConnections(curve + '.output', source=False, destination=True, plugs=True) or []
        if destination in targets:
            cmds.delete(curve)
            return True
    raise ValueError('该目标没有当前 Driver 的映射：' + destination)
