# coding=utf-8
"""将训练系数编译为 MEL 纯数值表达式；不执行 Python 回调。"""
import math


def number(value):
    """生成带小数点的有限 MEL 常量，避免整数除法。

    Args:
        value (float):
            要写入 MEL 表达式的有限数值。

    Returns:
        str: 用于表达式的浮点数常量。
    """
    text = '{:.17g}'.format(float(value))
    if '.' not in text and 'e' not in text:
        text += '.0'
    return text


def compile_expression(solver, node):
    """输入为已转换单位的 double 属性，输出不绑定具体 BlendShape。

    Args:
        solver (RbfSolver):
            已经 train 得到系数的 RBF 求解器。
        node (str):
            输出 network 节点名称，由 Name 创建，供表达式绑定属性。

    Returns:
        str: 可直接传给 cmds.expression 的 MEL 数值表达式。
    """
    model = solver.model
    if solver.coefficients is None:
        raise RuntimeError('请先训练')
    lines = []
    for index in range(len(model.inputs)):
        lines.append('float $x{} = {}.input{};'.format(index, node, index))
    for sample_index, pose in enumerate(model.poses):
        terms = []
        for index, value in enumerate(pose['values']):
            delta = '($x{} - {})'.format(index, number(value))
            period = model.periods[index]
            if period:
                delta = '({} * sin({} * {}))'.format(number(period / math.pi), number(math.pi / period), delta)
            lines.append('float $d{}_{} = {} / {};'.format(sample_index, index, delta, number(model.scales[index])))
            terms.append('$d{0}_{1} * $d{0}_{1}'.format(sample_index, index))
        lines.append('float $k{} = exp(-0.5 * ({}) / {});'.format(sample_index, ' + '.join(terms), number(model.radius ** 2)))
    for column in range(len(model.get_output_names())):
        terms = []
        for index, coefficients in enumerate(solver.coefficients):
            terms.append('({} * $k{})'.format(number(coefficients[column]), index))
        lines.append('float $w{} = {};'.format(column, ' + '.join(terms)))
        if model.clamp:
            lines.append('$w{0} = clamp(0.0, 1.0, $w{0});'.format(column))
    if model.normalize:
        terms = []
        for column in range(len(model.get_output_names())):
            terms.append('$w{}'.format(column))
        lines.append('float $total = max(1.0, {});'.format(' + '.join(terms)))
    for column in range(len(model.get_output_names())):
        divisor = ' / $total' if model.normalize else ''
        lines.append('{}.weight{} = $w{}{};'.format(node, column, column, divisor))
    return '\n'.join(lines)
