# coding=utf-8
"""原 V6 Smoothstep 十通道模式；明确区分于 Gaussian RBF。"""
import math
from .expression import number

OUTPUTS = ('up', 'down', 'front', 'back', 'frontUp', 'frontDown',
           'backUp', 'backDown', 'twistPositive', 'twistNegative')


class SmoothSolver(object):
    """按三个输入通道与中立差值计算，不做 RBF 训练。"""

    def __init__(self, model):
        """初始化当前对象并保存配置；不会隐式修改场景。

        Args:
            model (RbfModel):
                已通过数据验证的姿态配置；场景接口构建前检查输入连接。

        Returns:
            None: 初始化完成。
        """
        self.model = model
        self.trained = False

    def train(self):
        """验证固定十方向数据；轴索引是关节输入顺序，并非控制器轴。

        Returns:
            None: 固定方向配置检查通过。
        """
        self.model.validate()
        settings = self.model.smooth
        for axis in settings['axes']:
            if not isinstance(axis, int) or isinstance(axis, bool):
                raise ValueError('Smoothstep 轴索引必须为整数')
        if len(self.model.inputs) != 3 or set(settings['axes']) != {0, 1, 2}:
            raise ValueError('Smoothstep 模式需要三个输入和互不重复的轴索引 0,1,2')
        if len(settings['axes']) != 3 or len(settings['signs']) != 2 or len(settings['angles']) != 3:
            raise ValueError('Smoothstep 轴、符号、阈值数量错误')
        for sign in settings['signs']:
            if sign not in (-1, 1):
                raise ValueError('Smoothstep 方向符号只能为 -1 或 1')
        for angle in settings['angles']:
            if not math.isfinite(angle) or angle <= 0:
                raise ValueError('Smoothstep 阈值必须为有限正数')
        if tuple(self.model.get_output_names()) != OUTPUTS:
            raise ValueError('Smoothstep 模式需要自动采样生成的固定十方向名称与顺序')
        if any(self.model.periods):
            raise ValueError('Smoothstep 模式保留原 V6 连续角度语义，周期必须为 0')
        self.trained = True

    def evaluate(self, values):
        """中立为零、方向隔离、超限保持端点，扭转独立。

        Args:
            values (list[float]):
                按输入顺序排列的姿态值；角度输入统一为度。

        Returns:
            list[float]: 与 get_output_names 顺序一致的输出权重。
        """
        if not self.trained:
            raise RuntimeError('请先验证配置')
        self.model.validate_values(values)
        settings = self.model.smooth
        deltas = []
        for axis in settings['axes']:
            deltas.append(values[axis] - self.model.poses[0]['values'][axis])
        gates = []
        for delta, sign, angle in (
            (deltas[0], settings['signs'][0], settings['angles'][0]),
            (deltas[0], -settings['signs'][0], settings['angles'][0]),
            (deltas[1], settings['signs'][1], settings['angles'][1]),
            (deltas[1], -settings['signs'][1], settings['angles'][1]),
            (deltas[2], 1, settings['angles'][2]),
            (deltas[2], -1, settings['angles'][2]),
        ):
            t = max(0.0, min(1.0, delta * sign / angle))
            gates.append(t * t * (3.0 - 2.0 * t))
        up, down, front, back, positive, negative = gates
        return [up * (1-front-back), down * (1-front-back),
                front * (1-up-down), back * (1-up-down),
                front * up, front * down, back * up, back * down, positive, negative]

    def compile(self, node):
        """编译相同 Smoothstep 运算，保留独立扭转，不应用总量归一化。

        Args:
            node (str):
                输出 network 节点名称，由 Name 创建，供表达式绑定属性。

        Returns:
            str: Smoothstep 模式的 MEL 数值表达式。
        """
        if not self.trained:
            raise RuntimeError('请先验证配置')
        settings = self.model.smooth
        definitions = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))
        lines = []
        for index, (slot, direction) in enumerate(definitions):
            axis = settings['axes'][slot]
            sign = direction * (settings['signs'][slot] if slot < 2 else 1)
            neutral = self.model.poses[0]['values'][axis]
            factor = sign / settings['angles'][slot]
            lines.append('float $t{0} = clamp(0.0, 1.0, ({1}.input{2} - {3}) * {4});'.format(index, node, axis, number(neutral), number(factor)))
            lines.append('float $g{0} = $t{0} * $t{0} * (3.0 - 2.0 * $t{0});'.format(index))
        formulas = ('$g0 * (1.0-$g2-$g3)', '$g1 * (1.0-$g2-$g3)',
                    '$g2 * (1.0-$g0-$g1)', '$g3 * (1.0-$g0-$g1)',
                    '$g2*$g0', '$g2*$g1', '$g3*$g0', '$g3*$g1', '$g4', '$g5')
        for index, formula in enumerate(formulas):
            lines.append('{}.weight{} = {};'.format(node, index, formula))
        return '\n'.join(lines)
