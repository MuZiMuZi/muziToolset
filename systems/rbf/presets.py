# coding=utf-8
"""ADV 最终关节模板；模板名称可覆盖，不根据名字猜测解剖方向。"""
from .model import RbfModel

ADV_JOINTS = {'arm': 'Shoulder', 'thigh': 'Hip', 'wrist': 'Wrist'}


def create_adv_model(part='arm', side='lf', joint=None, index=1):
    """返回 XYZ 旋转输入；读取最终关节可响应 FK 和 IK 求值结果。

    Args:
        part (str):
            命名中的部位 token；ADV 模板支持 arm、thigh、wrist。
        side (str):
            生成节点的侧别：lf、rt、md。
        joint (str | None):
            实际 ADV 最终关节名称；None 时根据模板与侧别填入。
        index (int | None):
            实例或节点序号；可选 None 时使用模型实例序号。

    Returns:
        RbfModel: 尚未采样的 ADV 最终关节配置。
    """
    if part not in ADV_JOINTS:
        raise ValueError('未知 ADV 部位：' + part)
    if joint is None:
        joint = '{}_{}'.format(ADV_JOINTS[part], 'R' if side == 'rt' else 'L')
    inputs = []
    for axis in ('X', 'Y', 'Z'):
        inputs.append(joint + '.rotate' + axis)
    scales = [90.0, 90.0, 90.0]
    if part == 'wrist':
        scales = [45.0, 45.0, 45.0]
    # 默认 Euler 连续值保留多圈语义；可显式改 periods 为 360 处理绕回。
    return create_joint_model(joint, side=side, part=part, index=index, scales=scales)


def create_joint_model(joint, side='lf', part='arm', index=1, scales=None,
                       solver_type='rbf', swing_axes=('Y', 'Z'), twist_axis='X',
                       swing_signs=(-1, 1), smooth_angles=None):
    """任意关节 XYZ 输入模板；关节名称与解剖方向均由调用方明确指定。

    joint(str): Maya 关节或控制器名称，可带命名空间。
    swing_axes(tuple): 两个摆动轴，顺序决定 up/front 方向。
    smooth_angles(list): 两个交叉激活阈值和 Twist 阈值，单位为度。
    返回未采样 RbfModel，不访问或修改场景。
    """
    if len(swing_axes) != 2 or set(tuple(swing_axes) + (twist_axis,)) != set('XYZ'):
        raise ValueError('摆动和扭转轴必须是互不重复的 X、Y、Z')
    inputs = []
    axes = []
    for axis in 'XYZ':
        inputs.append(joint + '.rotate' + axis)
    for axis in tuple(swing_axes) + (twist_axis,):
        axes.append('XYZ'.index(axis))
    if smooth_angles is None:
        smooth_angles = [22.5, 22.5, 45.0] if part == 'wrist' else [45.0, 45.0, 90.0]
    return RbfModel(inputs, scales=scales, side=side, part=part, index=index,
                    solver_type=solver_type,
                    smooth={'axes': axes, 'signs': list(swing_signs), 'angles': list(smooth_angles)})
