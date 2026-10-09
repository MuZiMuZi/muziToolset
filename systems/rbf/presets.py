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
    return RbfModel(inputs, scales=scales, side=side, part=part, index=index)
