# coding=utf-8
"""ADV 控制器自动摆姿采样：修改控制器，读取最终关节，始终恢复。"""
import math
import maya.cmds as cmds
from ...core.common import scene_utils
from .model import RbfModel
from .driver import read_inputs

ADV_CONTROLLERS = {'arm': 'FKShoulder', 'thigh': 'FKHip', 'wrist': 'FKWrist'}


def get_adv_controller(part, side):
    """默认 ADV FK 控制器名称；不同 ADV 版本可由 UI 覆盖。

    Args:
        part (str):
            命名中的部位 token；ADV 模板支持 arm、thigh、wrist。
        side (str):
            生成节点的侧别：lf、rt、md。

    Returns:
        str: 当前部位与侧别的默认 ADV FK 控制器名。
    """
    return '{}_{}'.format(ADV_CONTROLLERS[part], 'R' if side == 'rt' else 'L')


def create_pose_offsets(swing_axes=('Y', 'Z'), twist_axis='X',
                        swing_signs=(-1, 1), swing_angles=(90.0, 90.0),
                        diagonal_angles=(45.0, 45.0), twist_angle=90.0):
    """生成 XYZ 控制器偏移；控制器轴与采样关节轴可以不同。

    Args:
        swing_axes (tuple[str,str]):
            采样控制器的两个摆动旋转轴。
        twist_axis (str):
            采样控制器的扭转轴，必须与两个摆动轴不同。
        swing_signs (tuple[int,int]):
            上与前分别对应的旋转符号，只能取 -1 或 1。
        swing_angles (tuple[float,float]):
            两个单轴方向的采样幅度，单位度。
        diagonal_angles (tuple[float,float]):
            对角样本在两个摆动轴上的偏移幅度，单位度。
        twist_angle (float):
            正负扭转样本的偏移幅度，单位度。

    Returns:
        list[tuple]: 中立加十个修型方向的控制器偏移。
    """
    if len(swing_axes) != 2 or set(tuple(swing_axes) + (twist_axis,)) != set('XYZ'):
        raise ValueError('摆动与扭转必须分别使用 X、Y、Z')
    if len(swing_signs) != 2 or len(swing_angles) != 2 or len(diagonal_angles) != 2:
        raise ValueError('摆动轴必须提供两个方向与角度')
    for sign in swing_signs:
        if sign not in (-1, 1):
            raise ValueError('采样方向只能是 -1 或 1')
    for angle in tuple(swing_angles) + tuple(diagonal_angles) + (twist_angle,):
        if not math.isfinite(angle) or angle <= 0:
            raise ValueError('采样角度必须为有限正数')
    definitions = [
        ('neutral', 0, 0, 0),
        ('up', swing_angles[0], 0, 0), ('down', -swing_angles[0], 0, 0),
        ('front', 0, swing_angles[1], 0), ('back', 0, -swing_angles[1], 0),
        ('frontUp', diagonal_angles[0], diagonal_angles[1], 0),
        ('frontDown', -diagonal_angles[0], diagonal_angles[1], 0),
        ('backUp', diagonal_angles[0], -diagonal_angles[1], 0),
        ('backDown', -diagonal_angles[0], -diagonal_angles[1], 0),
        ('twistPositive', 0, 0, twist_angle), ('twistNegative', 0, 0, -twist_angle),
    ]
    result = []
    for name, first, second, twist in definitions:
        values = [0.0, 0.0, 0.0]
        values['XYZ'.index(swing_axes[0])] = first * swing_signs[0]
        values['XYZ'.index(swing_axes[1])] = second * swing_signs[1]
        values['XYZ'.index(twist_axis)] = twist
        result.append((name, values))
    return result


@scene_utils.undo_chunk
def sample_controller(model, controller, offsets=None):
    """返回新采样数据，不破坏原 model；当前控制器姿态定义为中立。

    如果通道有关键帧、约束或其他输入连接，拒绝自动采样，避免修改已有动画。
    getAttr 会请求最终关节求值，无需依赖窗口刷新或改时间。

    Args:
        model (RbfModel):
            已通过数据验证的姿态配置；场景接口构建前检查输入连接。
        controller (str):
            采样控制器名称或完整 DAG 路径；必须允许写入 XYZ 旋转。
        offsets (list[tuple] | None):
            (姿态名, XYZ 度数偏移) 序列；首项必须 neutral 零偏移。

    Returns:
        RbfModel: 自动采样得到的新模型；原模型不修改。
    """
    controller = scene_utils.get_long_name(controller)
    read_inputs(model)
    if offsets is None:
        offsets = create_pose_offsets()
    if not offsets or offsets[0][0] != 'neutral' or tuple(offsets[0][1]) != (0, 0, 0):
        raise ValueError('自动采样序列必须从零偏移 neutral 开始')
    for name, values in offsets:
        if len(values) != 3:
            raise ValueError('控制器偏移必须是 XYZ 三个值')
        for value in values:
            if not math.isfinite(value):
                raise ValueError('控制器偏移必须为有限数值')
    plugs = []
    for axis in 'XYZ':
        plug = controller + '.rotate' + axis
        if not cmds.objExists(plug) or not cmds.getAttr(plug, settable=True):
            raise RuntimeError('控制器旋转无法设置：' + plug)
        if cmds.listConnections(plug, source=True, destination=False):
            raise RuntimeError('控制器通道已有动画或连接，不能自动采样：' + plug)
        limits = cmds.transformLimits(controller, query=True, **{'enableRotation' + axis: True})
        if any(limits):
            raise RuntimeError('控制器启用了旋转限制，请先确认采样范围：' + plug)
        plugs.append(plug)
    original = []
    for plug in plugs:
        original.append(cmds.getAttr(plug))
    auto_key = cmds.autoKeyframe(query=True, state=True)
    radians = cmds.currentUnit(query=True, angle=True) == 'rad'
    candidate = model.to_dict()
    candidate['poses'] = []
    sampled = RbfModel.from_dict(candidate)
    cmds.autoKeyframe(state=False)
    try:
        for name, offsets_xyz in offsets:
            for index, plug in enumerate(plugs):
                offset = offsets_xyz[index]
                if radians:
                    offset = math.radians(offset)
                cmds.setAttr(plug, original[index] + offset)
            sampled.add_pose(name, read_inputs(sampled), neutral=(name == 'neutral'))
    finally:
        # 即使采样中断，也继续尝试恢复每个轴和自动关键帧状态。
        restore_errors = []
        for index, plug in enumerate(plugs):
            try:
                cmds.setAttr(plug, original[index])
            except Exception as error:
                restore_errors.append(str(error))
        cmds.autoKeyframe(state=auto_key)
        if restore_errors:
            raise RuntimeError('控制器恢复失败：' + '; '.join(restore_errors))
    return sampled
