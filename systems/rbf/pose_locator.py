# coding=utf-8
"""Pose Locator 样本容器；平移只负责显示，poseValue 属性负责训练数据。"""
import maya.cmds as cmds
from .model import RbfModel
from .solver_factory import create_solver


def create_pose_locators(driver):
    """自动为每个样本生成 Locator，采用 Driver 命名、所有权和异常回滚。

    driver(RbfDriver): 已创建 output 的驱动实例。
    返回 Locator 列表；poseValue0 等无单位数值按 model.inputs 顺序记录，角度为度。
    """
    group = driver.create_node('transform', 'rbfPoses')
    anchor = driver.model.inputs[0].split('.', 1)[0]
    if cmds.objectType(anchor, isAType='transform'):
        position = cmds.xform(anchor, query=True, worldSpace=True, translation=True)
        cmds.xform(group, worldSpace=True, translation=position)
    locators = []
    for index, pose in enumerate(driver.model.poses):
        locator = driver.create_node('transform', 'rbfPose' + pose['name'])
        shape = cmds.createNode('locator', parent=locator, name=locator + 'Shape')
        cmds.parent(locator, group, relative=True)
        # 网格排列便于选取；移动 Locator 不会暗中修改采样或现有绑定。
        cmds.setAttr(locator + '.translate', (index % 4) * 2.0, (index // 4) * 2.0, 0, type='double3')
        cmds.setAttr(shape + '.overrideEnabled', True)
        cmds.setAttr(shape + '.overrideColor', 17 if pose['neutral'] else 18)
        cmds.addAttr(locator, longName='muziPoseName', dataType='string')
        cmds.setAttr(locator + '.muziPoseName', pose['name'], type='string', lock=True)
        for slot, value in enumerate(pose['values']):
            attribute = 'poseValue{}'.format(slot)
            cmds.addAttr(locator, longName=attribute, attributeType='double', defaultValue=value)
            cmds.setAttr(locator + '.' + attribute, keyable=False, channelBox=True)
            label = 'poseInput{}'.format(slot)
            cmds.addAttr(locator, longName=label, dataType='string')
            cmds.setAttr(locator + '.' + label, driver.model.inputs[slot], type='string', lock=True)
        locators.append(locator)
    return locators


def get_pose_locators(driver):
    """只查询该网络拥有的 Locator；不根据名称扫描和认领其他节点。"""
    if not driver.output or not cmds.objExists(driver.output):
        raise RuntimeError('请先构建或恢复场景网络')
    result = {}
    nodes = cmds.listConnections(driver.output + '.ownedNodes', source=True, destination=False) or []
    for node in nodes:
        if cmds.attributeQuery('muziPoseName', node=node, exists=True):
            name = cmds.getAttr(node + '.muziPoseName')
            if name in result:
                raise RuntimeError('重复 Pose Locator：' + name)
            result[name] = node
    return result


def read_pose_locators(driver):
    """读全部 Locator 为新草稿并验证；失败不修改网络或原始模型。

    RBF 使用全部采样值；Smoothstep 只使用中立值和 smooth 设置。
    调用 driver.rebuild(candidate) 才会将编辑结果应用到实时输出。
    """
    candidate = RbfModel.from_dict(driver.model.to_dict())
    locators = get_pose_locators(driver)
    if len(locators) != len(candidate.poses):
        raise RuntimeError('Pose Locator 数量不一致，请检查删除或缺失的 Locator')
    for pose in candidate.poses:
        if pose['name'] not in locators:
            raise RuntimeError('缺少 Pose Locator：' + pose['name'])
        values = []
        for slot in range(len(candidate.inputs)):
            values.append(cmds.getAttr('{}.poseValue{}'.format(locators[pose['name']], slot)))
        candidate.update_pose(pose['name'], values)
    create_solver(candidate).train()
    return candidate


def write_pose_locator(driver, name, values):
    """将当前读取的输入值记录到单个 Locator；不触发训练或更改网络。"""
    driver.model.validate_values(values)
    locators = get_pose_locators(driver)
    if name not in locators:
        raise ValueError('找不到 Pose Locator：' + name)
    locator = locators[name]
    plugs = []
    original = []
    for slot in range(len(values)):
        plug = '{}.poseValue{}'.format(locator, slot)
        if not cmds.getAttr(plug, settable=True) or cmds.listConnections(plug, source=True, destination=False):
            raise RuntimeError('Locator 采样属性不可编辑：' + plug)
        plugs.append(plug)
        original.append(cmds.getAttr(plug))
    try:
        for slot, plug in enumerate(plugs):
            cmds.setAttr(plug, values[slot])
    except Exception:
        for slot, plug in enumerate(plugs):
            cmds.setAttr(plug, original[slot])
        raise
    return locator
