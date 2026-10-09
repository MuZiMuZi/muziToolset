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
        """初始化当前对象并保存配置；不会隐式修改场景。

        Args:
            inputs (list[str]):
                要读取的 Maya 标量属性路径，顺序与 scales、periods、姿态值一致。
            scales (list[float] | None):
                各输入的正数尺度；省略时每个输入取 90。
            periods (list[float] | None):
                各输入的周期，0 为连续值，角度可用 360；默认全部为 0。
            side (str):
                生成节点的侧别：lf、rt、md。
            part (str):
                命名中的部位 token；ADV 模板支持 arm、thigh、wrist。
            index (int):
                实例序号，必须为正整数。
            radius (float):
                归一化输入空间中的 Gaussian 核宽度，必须大于 0。
            regularization (float):
                加在训练矩阵对角线上的非负正则项；0 表示精确插值。
            clamp (bool):
                是否将 RBF 输出限制到 0~1。
            normalize (bool):
                是否在输出总和大于 1 时按总量缩放。
            poses (list[dict] | None):
                包含 name、values、neutral 的样本序列；首项必须中立。
            sampling (dict | None):
                控制器名称和自动采样轴、方向、角度设置，用于保存与恢复。
            solver_type (str):
                rbf 使用 Gaussian 插值；smoothstep 使用原 V6 方向门。
            smooth (dict | None):
                Smoothstep 输入索引 axes、方向 signs 和阈值 angles。

        Returns:
            None: 初始化完成。
        """
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
        """验证导入数据；重复姿态由求解器按实际距离检查。

        Returns:
            None: 配置有效时正常返回，否则抛出 ValueError。
        """
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
            if not pose['neutral'] and (re.fullmatch(r'(input|weight)\d+', name) or name in ('message', 'muziRbfData', 'ownedNodes', 'outputMappings')):
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
        """采样值必须与全部输入一一对应。

        Args:
            values (list[float]):
                按输入顺序排列的姿态值；角度输入统一为度。

        Returns:
            None: 输入数量及有限数检查通过，否则抛出 ValueError。
        """
        if len(values) != len(self.inputs):
            raise ValueError('姿态输入数量不一致')
        for value in values:
            if not math.isfinite(value):
                raise ValueError('姿态值必须为有限数值')

    def add_pose(self, name, values, neutral=False):
        """新增样本；中立不产生输出，其他姿态各产生一个同名输出。

        Args:
            name (str):
                姿态名称或现有输出名称，使用字母开头的属性 token。
            values (list[float]):
                按输入顺序排列的姿态值；角度输入统一为度。
            neutral (bool):
                是否把新增样本标记为唯一中立姿态。

        Returns:
            None: 样本已添加；失败时撤销该次数据添加。
        """
        candidate = {'name': name, 'values': list(values), 'neutral': bool(neutral)}
        self.poses.append(candidate)
        try:
            self.validate()
        except Exception:
            self.poses.pop()
            raise

    def update_pose(self, name, values):
        """按名称替换样本值；验证失败保留原数据，名称和输出连接不变。

        Args:
            name (str): 已记录的姿态名称，包括中立姿态。
            values (list[float]): 按 inputs 顺序排列的新采样值，角度为度。
        Returns:
            None: 模型已更新，既有求解器需要重新训练。
        """
        candidate = RbfModel.from_dict(self.to_dict())
        for pose in candidate.poses:
            if pose['name'] == name:
                pose['values'] = list(values)
                candidate.validate()
                self.poses = candidate.poses
                return
        raise ValueError('找不到姿态：' + name)

    def remove_pose(self, name):
        """删除非中立样本；有场景连接时还需通过 Driver 重建检查。

        Args:
            name (str): 已记录的非中立姿态名称。
        Returns:
            None: 删除成功；输出连接由 Driver.rebuild 检查。
        """
        for index, pose in enumerate(self.poses):
            if pose['name'] == name:
                if pose['neutral']:
                    raise ValueError('不能删除中立姿态')
                self.poses.pop(index)
                return
        raise ValueError('找不到姿态：' + name)

    def get_output_names(self):
        """输出顺序与样本顺序保持一致。

        Returns:
            list[str]: 按采样顺序排列的非中立输出名称。
        """
        result = []
        for pose in self.poses:
            if not pose['neutral']:
                result.append(pose['name'])
        return result

    def to_dict(self):
        """序列化配置，不序列化可由样本重算的系数。

        Returns:
            dict: 独立配置副本，包含版本和采样设置。
        """
        result = {'version': 1}
        for key in ('inputs', 'scales', 'periods', 'side', 'part', 'index',
                    'radius', 'regularization', 'clamp', 'normalize', 'poses', 'sampling', 'solver_type', 'smooth'):
            result[key] = copy.deepcopy(getattr(self, key))
        return result

    @classmethod
    def from_dict(cls, data):
        """读取版本化配置并重新验证。

        Args:
            data (dict):
                包含 version 字段的配置数据。

        Returns:
            RbfModel: 已重新验证的配置对象。
        """
        values = copy.deepcopy(data)
        if values.pop('version') != 1:
            raise ValueError('不支持的 RBF 配置版本')
        return cls(**values)
