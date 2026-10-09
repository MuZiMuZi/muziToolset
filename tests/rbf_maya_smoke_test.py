# coding=utf-8
"""真实 Maya 验证：临时控制器驱动关节，自动采样、DG、重建和恢复。

在 Maya Python 页执行：
    from muziToolset.tests.rbf_maya_smoke_test import run
    print(run())
本脚本不会清空场景；所有测试对象会清理，不替代真实 ADV 角色验收。
"""
import math
import maya.cmds as cmds
from ..core.common import scene_utils, connection_utils
from ..systems.rbf import RbfModel, RbfSolver
from ..systems.rbf.driver import RbfDriver, read_inputs
from ..systems.rbf.sampling import create_pose_offsets, sample_controller


def run():
    """失败时抛出 AssertionError，finally 清理并恢复全局设置。"""
    names = ['ctrl_md_rbfSmoke_sample_001', 'jnt_md_rbfSmoke_sample_001', 'network_md_rbfSmoke_target_001']
    scene_utils.ensure_nodes_available(names + ['network_md_rbfSmoke_rbf_001', 'network_md_rbfSmokeSecond_rbf_001'])
    selection = cmds.ls(selection=True, long=True) or []
    angle_unit = cmds.currentUnit(query=True, angle=True)
    auto_key = cmds.autoKeyframe(query=True, state=True)
    owned = []
    driver = None
    second = None
    try:
        cmds.currentUnit(angle='deg')
        ctrl = scene_utils.create_node('transform', names[0])
        owned.append(ctrl)
        joint = scene_utils.create_node('joint', names[1])
        owned.append(joint)
        target = scene_utils.create_node('network', names[2])
        owned.append(target)
        cmds.addAttr(target, longName='corrective', attributeType='double')
        for axis in 'XYZ':
            connection_utils.connect_plugs(ctrl + '.rotate' + axis, joint + '.rotate' + axis)
        cmds.setAttr(ctrl + '.rotate', 10, 20, 30, type='double3')
        cmds.autoKeyframe(state=True)
        model = RbfModel([joint + '.rotateX', joint + '.rotateY', joint + '.rotateZ'], part='rbfSmoke', side='md')
        offsets = create_pose_offsets()
        model = sample_controller(model, ctrl, offsets)
        assert tuple(cmds.getAttr(ctrl + '.rotate')[0]) == (10, 20, 30), '未恢复控制器'
        assert cmds.autoKeyframe(query=True, state=True), '未恢复自动关键帧'
        cmds.autoKeyframe(state=False)
        driver = RbfDriver(model)
        driver.build()
        solver = RbfSolver(model)
        solver.train()
        for name, offset in offsets:
            for index, axis in enumerate('XYZ'):
                cmds.setAttr(ctrl + '.rotate' + axis, [10, 20, 30][index] + offset[index])
            expected = solver.evaluate(read_inputs(model))
            actual = driver.read()
            for index, output_name in enumerate(model.get_output_names()):
                assert abs(actual[output_name] - expected[index]) < 0.00005, (name, output_name, actual)
        driver.connect_output('up', target + '.corrective')
        assert cmds.isConnected(driver.get_output_plug('up'), target + '.corrective')
        changed = RbfModel.from_dict(model.to_dict())
        changed.radius = 0.8
        driver.rebuild(changed)
        assert cmds.isConnected(driver.get_output_plug('up'), target + '.corrective'), '重建丢失输出连接'
        driver = RbfDriver.from_scene(driver.output)
        joint = cmds.rename(joint, 'jnt_md_rbfSmoke_renamed_001')
        owned[1] = joint
        driver = RbfDriver.from_scene(driver.output)
        assert driver.model.inputs[0].split('.')[0].split('|')[-1] == joint.split('|')[-1], '重命名后恢复失败'
        # 验证固定单位转换：网络构建后切换 radians 仍得到同一姿态权重。
        cmds.currentUnit(angle='rad')
        cmds.setAttr(ctrl + '.rotateX', math.radians(10))
        cmds.setAttr(ctrl + '.rotateY', math.radians(-70))
        cmds.setAttr(ctrl + '.rotateZ', math.radians(30))
        assert abs(driver.read()['up'] - 1.0) < 0.00005, '角度单位转换错误'
        cmds.currentUnit(angle='deg')
        # 真实撤销检查只针对新网络构建，不撤销用户场景内容。
        undo_model = RbfModel.from_dict(driver.model.to_dict())
        undo_model.part = 'rbfSmokeSecond'
        second = RbfDriver(undo_model)
        created = second.build()
        cmds.undo()
        assert not cmds.objExists(created), '构建撤销后仍有输出节点'
        second.output = None
        driver.delete()
        assert cmds.objExists(ctrl) and cmds.objExists(joint) and cmds.objExists(target), '清理误删源绑定或目标'
        return {'passed': True, 'samples': len(model.poses), 'outputs': len(model.get_output_names())}
    finally:
        if second and second.output and cmds.objExists(second.output):
            second.delete()
        if driver and driver.output and cmds.objExists(driver.output):
            driver.delete()
        for node in reversed(owned):
            if cmds.objExists(node):
                cmds.delete(node)
        cmds.currentUnit(angle=angle_unit)
        cmds.autoKeyframe(state=auto_key)
        remaining = scene_utils.existing_nodes(selection)
        if remaining:
            cmds.select(remaining, replace=True)
        else:
            cmds.select(clear=True)
