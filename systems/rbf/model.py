# coding=utf-8
"""RBF 数据模型：输入尺度、周期、姿态及输出；不操作场景。"""
import copy
import math
import re


class RbfModel(object):
    """inputs 为属性路径，scales 为对应尺度，periods 为周期或零。"""

    def __init__(self, inputs, scales=None, periods=None, side='lf', part='arm',
                 index=1, radius=1.0, regularization=0.0, clamp=True,
                 normalize=False, poses=None, sampling=None, solver_type='rbf', smooth=None):
        self.inputs = list(inputs)
        self.scales = list(scales) if scales is not None else [90.0] * len(inputs)
        self.periods = list(periods) if periods is not None else [0.0] * len(inputs)
        self.side = side
        self.part = part
        self.index = index
        self.radius = radius
        self.regularization = regularization
        self.clamp = bool(clamp)
        self.normalize = bool(normalize)
        self.poses = copy.deepcopy(poses or [])
        self.sampling = copy.deepcopy(sampling or {})
        self.solver_type = solver_type
        self.smooth = copy.deepcopy(smooth or {'axes': [1, 2, 0], 'signs': [-1, 1], 'angles': [45.0, 45.0, 90.0]})
        self.validate()

    def validate(self):
        """验证导入数据；重复姿态由求解器按实际距离检查。"""
        if self.solver_type not in ('rbf', 'smoothstep'):
            raise ValueError('未知求解模式')
        if not self.inputs or len(set(self.inputs)) != len(self.inputs):
            raise ValueError('输入属性不能为空或重复')
        for plug in self.inputs:
            if not isinstance(plug, str) or '.' not in plug:
                raise ValueError('输入必须是节点.属性形式')
        if len(self.inputs) != len(self.scales) or len(self.inputs) != len(self.periods):
            raise ValueError('尺度、周期数量必须与输入数量一致')
        for value in self.scales:
            if not math.isfinite(value) or value <= 0:
                raise ValueError('输入尺度必须为有限正数')
        for value in self.periods:
            if not math.isfinite(value) or value < 0:
                raise ValueError('周期必须为有限非负数')
        if not math.isfinite(self.radius) or self.radius <= 0:
            raise ValueError('核半径必须为有限正数')
        if not math.isfinite(self.regularization) or self.regularization < 0:
            raise ValueError('正则项必须为有限非负数')
        if self.side not in ('lf', 'rt', 'md'):
            raise ValueError('侧别必须为 lf、rt、md')
        if not isinstance(self.part, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', self.part):
            raise ValueError('部位必须为字母开头的名称 token')
        if not isinstance(self.index, int) or isinstance(self.index, bool) or self.index < 1:
            raise ValueError('序号必须为正整数')
        names = set()
        for pose in self.poses:
            name = pose['name']
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name) or name in names:
                raise ValueError('姿态名称不合法或重复：' + name)
            names.add(name)
            if not pose['neutral'] and (re.fullmatch(r'(input|weight)\d+', name) or name in ('message', 'muziRbfData', 'ownedNodes')):
                raise ValueError('姿态名称占用了网络保留属性：' + name)
            self.validate_values(pose['values'])
            if not isinstance(pose['neutral'], bool):
                raise ValueError('neutral 必须为布尔值')
        if self.poses and not self.poses[0]['neutral']:
            raise ValueError('第一个姿态必须为中立姿态')
        for pose in self.poses[1:]:
            if pose['neutral']:
                raise ValueError('只能有一个中立姿态')

    def validate_values(self, values):
        """采样值必须与全部输入一一对应。"""
        if len(values) != len(self.inputs):
            raise ValueError('姿态输入数量不一致')
        for value in values:
            if not math.isfinite(value):
                raise ValueError('姿态值必须为有限数值')

    def add_pose(self, name, values, neutral=False):
        """新增样本；中立不产生输出，其他姿态各产生一个同名输出。"""
        candidate = {'name': name, 'values': list(values), 'neutral': bool(neutral)}
        self.poses.append(candidate)
        try:
            self.validate()
        except Exception:
            self.poses.pop()
            raise

    def get_output_names(self):
        """输出顺序与样本顺序保持一致。"""
        result = []
        for pose in self.poses:
            if not pose['neutral']:
                result.append(pose['name'])
        return result

    def to_dict(self):
        """序列化配置，不序列化可由样本重算的系数。"""
        result = {'version': 1}
        for key in ('inputs', 'scales', 'periods', 'side', 'part', 'index',
                    'radius', 'regularization', 'clamp', 'normalize', 'poses', 'sampling', 'solver_type', 'smooth'):
            result[key] = copy.deepcopy(getattr(self, key))
        return result

    @classmethod
    def from_dict(cls, data):
        """读取版本化配置并重新验证。"""
        values = copy.deepcopy(data)
        if values.pop('version') != 1:
            raise ValueError('不支持的 RBF 配置版本')
        return cls(**values)
