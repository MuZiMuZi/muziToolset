# coding=utf-8
"""Maya 通用修型驱动：采样、构建、恢复、连接和清理；命名复用 Name。"""
import json
import math
import maya.cmds as cmds
from ...core.common import scene_utils, connection_utils, file_utils
from ...core.common.name_utils import Name
from .model import RbfModel
from .solver import RbfSolver
from .expression import compile_expression

SCALAR_TYPES = ('double', 'float', 'long', 'short', 'byte', 'bool', 'doubleAngle')


def read_inputs(model):
    """只读采样；角度统一保存为度，支持 ADV 被连接的最终关节。"""
    result = []
    for plug in model.inputs:
        node, attribute = plug.split('.', 1)
        scene_utils.get_long_name(node)
        if not cmds.objExists(plug):
            raise ValueError('输入属性不存在：' + plug)
        kind = cmds.getAttr(plug, type=True)
        if kind not in SCALAR_TYPES:
            raise ValueError('仅支持角度与无单位标量输入：' + plug)
        value = float(cmds.getAttr(plug))
        if kind == 'doubleAngle' and cmds.currentUnit(query=True, angle=True) == 'rad':
            value = math.degrees(value)
        result.append(value)
    model.validate_values(result)
    return result


def capture_pose(model, name, neutral=False):
    """记录当前关节或控制器状态，不修改原绑定。"""
    model.add_pose(name, read_inputs(model), neutral=neutral)
    return model.poses[-1]


def save_model(model, path):
    """保存可移植训练数据，不保存场景运行时节点。"""
    model.validate()
    file_utils.write_json(path, model.to_dict())


def load_model(path):
    """导入后可修改 inputs 重映射到另一角色，再构建。"""
    return RbfModel.from_dict(file_utils.read_json(path))


class RbfDriver(object):
    """一个部位对应一个 output network 和一个表达式求解节点。"""

    def __init__(self, model):
        self.model = RbfModel.from_dict(model.to_dict())
        self.output = None
        self.nodes = []

    def get_name(self, type, function, index=None):
        """统一走仓库 Name 命名，不建立第二套 Rig 命名规则。"""
        return Name(type=type, side=self.model.side, part=self.model.part,
                    function=function, index=self.model.index if index is None else index).name

    def create_node(self, type, function, index=None):
        """记录本次创建节点，用于异常回滚。"""
        node = scene_utils.create_node(type, self.get_name(type, function, index))
        self.nodes.append(node)
        return node

    @scene_utils.undo_chunk
    def build(self):
        """先训练再修改场景；所有运行时输入采用固定角度单位转换。"""
        if self.output and cmds.objExists(self.output):
            raise RuntimeError('该实例已构建，请恢复实例或删除后重新构建')
        self.model.validate()
        read_inputs(self.model)
        solver = RbfSolver(self.model)
        solver.train()
        self.nodes = []
        try:
            self.output = self.create_node('network', 'rbf')
            cmds.addAttr(self.output, longName='muziRbfData', dataType='string')
            cmds.setAttr(self.output + '.muziRbfData', json.dumps(self.model.to_dict(), ensure_ascii=False), type='string')
            cmds.setAttr(self.output + '.muziRbfData', lock=True)
            cmds.addAttr(self.output, longName='ownedNodes', attributeType='message', multi=True)
            for index, plug in enumerate(self.model.inputs):
                attribute = 'input{}'.format(index)
                cmds.addAttr(self.output, longName=attribute, attributeType='double')
                source = plug
                if cmds.getAttr(plug, type=True) == 'doubleAngle':
                    conversion = self.create_node('unitConversion', 'rbfInput', index + 1)
                    connection_utils.connect_plugs(plug, conversion + '.input')
                    cmds.setAttr(conversion + '.conversionFactor', 180.0 / math.pi)
                    source = conversion + '.output'
                connection_utils.connect_plugs(source, self.output + '.' + attribute)
            for index, name in enumerate(self.model.get_output_names()):
                attribute = 'weight{}'.format(index)
                cmds.addAttr(self.output, longName=attribute, attributeType='double')
                cmds.aliasAttr(name, self.output + '.' + attribute)
                cmds.setAttr(self.output + '.' + attribute, channelBox=True)
            expression_name = self.get_name('expression', 'rbf')
            scene_utils.ensure_nodes_available([expression_name])
            expression = cmds.expression(name=expression_name, string=compile_expression(solver, self.output),
                                         alwaysEvaluate=False, unitConversion='none')
            self.nodes.append(expression)
            owner_index = 0
            for node in self.nodes:
                if node != self.output:
                    connection_utils.connect_plugs(node + '.message', '{}.ownedNodes[{}]'.format(self.output, owner_index))
                    owner_index += 1
            return self.output
        except Exception:
            for node in reversed(self.nodes):
                if cmds.objExists(node):
                    cmds.delete(node)
            self.output = None
            raise

    def get_output_plug(self, name):
        """使用样本名称取权重，内部属性序号保持稳定。"""
        if not self.output or not cmds.objExists(self.output):
            raise RuntimeError('请先构建网络')
        index = self.model.get_output_names().index(name)
        return '{}.weight{}'.format(self.output, index)

    def read(self):
        """查询场景实际权重，不调用 Python 求解器代替 DG。"""
        result = {}
        for name in self.model.get_output_names():
            result[name] = cmds.getAttr(self.get_output_plug(name))
        return result

    @scene_utils.undo_chunk
    def connect_output(self, name, destination):
        """连接 BlendShape 权重或修型标量属性；不覆盖已有驱动。"""
        connection_utils.connect_plugs(self.get_output_plug(name), destination, force=False)

    @scene_utils.undo_chunk
    def disconnect_output(self, name, destination):
        """只断开指定的当前输出连接。"""
        connection_utils.disconnect_plugs(self.get_output_plug(name), destination)

    @classmethod
    def from_scene(cls, output):
        """恢复场景中的训练数据，并从实际连接修正已重命名的输入。"""
        data = json.loads(cmds.getAttr(output + '.muziRbfData'))
        for index in range(len(data['inputs'])):
            sources = cmds.listConnections('{}.input{}'.format(output, index), source=True,
                                           destination=False, plugs=True, skipConversionNodes=True) or []
            if len(sources) != 1:
                raise RuntimeError('输入连接已丢失：input{}'.format(index))
            data['inputs'][index] = sources[0]
        instance = cls(RbfModel.from_dict(data))
        instance.output = output
        return instance

    @scene_utils.undo_chunk
    def delete(self):
        """仅删除 message 标记的所属节点；绑定和 BlendShape 目标保留。"""
        if not self.output or not cmds.objExists(self.output):
            return
        nodes = cmds.listConnections(self.output + '.ownedNodes', source=True, destination=False) or []
        for node in nodes:
            if cmds.objExists(node):
                cmds.delete(node)
        cmds.delete(self.output)
        self.output = None


def list_drivers():
    """查找场景中可恢复的 RBF 网络。"""
    result = []
    for node in scene_utils.get_nodes_by_type('network'):
        if cmds.attributeQuery('muziRbfData', node=node, exists=True):
            result.append(node)
    return result
