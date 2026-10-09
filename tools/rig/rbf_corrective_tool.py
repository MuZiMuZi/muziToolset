# coding=utf-8
"""ADV 通用修型驱动界面：自动旋转控制器采样、训练与连接。"""
import maya.cmds as cmds
try:
    from PySide2 import QtWidgets
except ImportError:
    from PySide6 import QtWidgets

from ...core.common import scene_utils
from ...systems.rbf import RbfModel
from ...systems.rbf.solver_factory import create_solver
from ...systems.rbf.driver import RbfDriver, capture_pose, save_model, load_model, list_drivers
from ...systems.rbf.presets import create_adv_model
from ...systems.rbf.sampling import get_adv_controller, create_pose_offsets, sample_controller
from ...ui import window_utils, theme

TOOL_MODE = 'ui'


class RbfCorrectiveTool(QtWidgets.QWidget):
    """界面负责流程，采样和求解统一由 systems.rbf 负责。"""

    def __init__(self, parent=None):
        """初始化当前对象并保存配置；不会隐式修改场景。

        Args:
            parent (QWidget | None):
                Maya 或工具箱传入的窗口父对象。

        Returns:
            None: 初始化完成。
        """
        super(RbfCorrectiveTool, self).__init__(parent)
        self.model = None
        self.driver = None
        self.setWindowTitle('ADV 通用 RBF 修型驱动')
        self.resize(560, 800)
        self.create_widgets()
        self.apply_preset()

    def add_button(self, layout, text, callback):
        """统一处理按钮异常，让错误出现在状态栏及 Maya 脚本编辑器。

        Args:
            layout (QLayout):
                用于放置按钮的 Qt 布局。
            text (str):
                逗号分隔文本，允许中文逗号。
            callback (callable):
                点击时执行的无参数操作，异常会显示在状态栏。

        Returns:
            QPushButton: 已绑定操作处理的按钮。
        """
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(lambda checked=False: self.run_action(callback))
        layout.addWidget(button)
        return button

    def run_action(self, callback):
        """保持窗口可用；场景回滚由业务接口负责。

        Args:
            callback (callable):
                点击时执行的无参数操作，异常会显示在状态栏。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        try:
            callback()
        except Exception as error:
            self.status.setText(str(error))
            cmds.warning(str(error))

    def create_widgets(self):
        """可滚动设置区、样本列表和连接区。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel('自动旋转 ADV 控制器 → 采样最终关节 → RBF 修型权重'))
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        content = QtWidgets.QWidget()
        body = QtWidgets.QVBoxLayout(content)
        form = QtWidgets.QFormLayout()
        self.part = QtWidgets.QComboBox()
        self.part.addItems(['arm', 'thigh', 'wrist'])
        self.part.setEditable(True)
        self.solver_type = QtWidgets.QComboBox()
        self.solver_type.addItems(['rbf', 'smoothstep'])
        self.side = QtWidgets.QComboBox()
        self.side.addItems(['lf', 'rt', 'md'])
        self.index = QtWidgets.QSpinBox()
        self.index.setRange(1, 999)
        self.controller = QtWidgets.QLineEdit()
        self.inputs = QtWidgets.QLineEdit()
        self.scales = QtWidgets.QLineEdit()
        self.periods = QtWidgets.QLineEdit()
        self.axes = QtWidgets.QLineEdit('Y,Z,X')
        self.signs = QtWidgets.QLineEdit('-1,1')
        self.angles = QtWidgets.QLineEdit('90,90,45,45,90')
        self.smooth_axes = QtWidgets.QLineEdit('1,2,0')
        self.smooth_signs = QtWidgets.QLineEdit('-1,1')
        self.smooth_angles = QtWidgets.QLineEdit('45,45,90')
        self.radius = QtWidgets.QDoubleSpinBox()
        self.radius.setRange(0.01, 100)
        self.radius.setValue(1)
        self.regularization = QtWidgets.QDoubleSpinBox()
        self.regularization.setDecimals(8)
        self.regularization.setRange(0, 1)
        self.clamp = QtWidgets.QCheckBox('夹到 0~1')
        self.clamp.setChecked(True)
        self.normalize = QtWidgets.QCheckBox('输出总量超过 1 时归一化')
        rows = [
            ('ADV 部位', self.part), ('求解器（rbf=真正 RBF）', self.solver_type), ('侧别', self.side), ('实例序号', self.index),
            ('自动采样控制器', self.controller), ('关节输入（逗号分隔）', self.inputs),
            ('输入尺度（度）', self.scales), ('输入周期（0=不绕回）', self.periods),
            ('采样轴：摆动1,摆动2,扭转', self.axes), ('摆动方向符号', self.signs),
            ('角度：单轴1,单轴2,对角1,对角2,扭转', self.angles),
            ('Smoothstep 输入索引：摆动1,摆动2,扭转', self.smooth_axes),
            ('Smoothstep 摆动符号', self.smooth_signs), ('Smoothstep 激活阈值', self.smooth_angles),
            ('RBF 半径', self.radius), ('正则项', self.regularization),
            ('输出范围', self.clamp), ('混合总量', self.normalize),
        ]
        for text, widget in rows:
            form.addRow(text, widget)
        body.addLayout(form)
        preset_row = QtWidgets.QHBoxLayout()
        self.add_button(preset_row, '应用 ADV 模板 / 新建配置', self.apply_preset)
        self.add_button(preset_row, '拾取采样控制器', self.pick_controller)
        self.add_button(preset_row, '拾取输入关节', self.pick_joint)
        body.addLayout(preset_row)
        self.add_button(body, '自动采样（旋转控制器并恢复）', self.auto_sample)
        self.poses = QtWidgets.QListWidget()
        self.poses.setMinimumHeight(160)
        body.addWidget(self.poses)
        manual_row = QtWidgets.QHBoxLayout()
        self.pose_name = QtWidgets.QLineEdit('customPose')
        manual_row.addWidget(self.pose_name)
        self.add_button(manual_row, '补充当前姿态', self.capture_current)
        self.add_button(manual_row, '删除选中样本', self.remove_pose)
        body.addLayout(manual_row)
        build_row = QtWidgets.QHBoxLayout()
        self.add_button(build_row, '训练并构建', self.build)
        self.add_button(build_row, '重建并保留连接', self.rebuild)
        self.add_button(build_row, '刷新权重', self.refresh_weights)
        body.addLayout(build_row)
        self.outputs = QtWidgets.QComboBox()
        self.destination = QtWidgets.QLineEdit()
        self.destination.setPlaceholderText('例如 blendShape1.armUp 或 blendShape1.weight[0]')
        body.addWidget(self.outputs)
        body.addWidget(self.destination)
        connect_row = QtWidgets.QHBoxLayout()
        self.add_button(connect_row, '连接输出', self.connect_output)
        self.add_button(connect_row, '断开输出', self.disconnect_output)
        body.addLayout(connect_row)
        scene_row = QtWidgets.QHBoxLayout()
        self.scene_drivers = QtWidgets.QComboBox()
        scene_row.addWidget(self.scene_drivers)
        self.add_button(scene_row, '刷新场景', self.refresh_scene)
        self.add_button(scene_row, '恢复所选网络', self.restore_scene)
        body.addLayout(scene_row)
        files_row = QtWidgets.QHBoxLayout()
        self.add_button(files_row, '保存配置', self.save)
        self.add_button(files_row, '加载配置', self.load)
        self.add_button(files_row, '删除当前网络', self.delete_network)
        body.addLayout(files_row)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        self.status = QtWidgets.QLabel('准备就绪')
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        theme.style_window(self, title='ADV 通用 RBF 修型驱动', minimum_width=560)

    @staticmethod
    def tokens(text):
        """读取逗号分隔设置，支持中文逗号。

        Args:
            text (str):
                逗号分隔文本，允许中文逗号。

        Returns:
            list[str]: 去除空白和空项的文本 token。
        """
        result = []
        for value in text.replace('，', ',').split(','):
            if value.strip():
                result.append(value.strip())
        return result

    def numbers(self, widget):
        """角度和尺度保留浮点精度。

        Args:
            widget (QLineEdit):
                包含逗号分隔数值的输入框。

        Returns:
            list[float]: 输入框中解析得到的数值。
        """
        result = []
        for value in self.tokens(widget.text()):
            result.append(float(value))
        return result

    def read_settings(self):
        """构建配置副本，防止失败时改变现有模型。

        Returns:
            RbfModel: 当前界面设置生成的独立数据草稿。
        """
        inputs = self.tokens(self.inputs.text())
        poses = [] if self.model is None else self.model.poses
        if self.model and inputs != self.model.inputs and poses:
            raise ValueError('输入属性已改变，请先应用模板建立新配置，再重新采样')
        axes = self.tokens(self.axes.text().upper())
        signs = self.numbers(self.signs)
        angles = self.numbers(self.angles)
        if len(axes) != 3 or len(angles) != 5:
            raise ValueError('采样轴需要三个值，采样角度需要五个值')
        sampling = {
            'controller': self.controller.text().strip(), 'swing_axes': axes[:2],
            'twist_axis': axes[2], 'swing_signs': signs,
            'swing_angles': angles[:2], 'diagonal_angles': angles[2:4], 'twist_angle': angles[4],
        }
        settings = dict(sampling)
        settings.pop('controller')
        create_pose_offsets(**settings)
        smooth_axes = []
        for token in self.tokens(self.smooth_axes.text()):
            smooth_axes.append(int(token))
        return RbfModel(inputs, scales=self.numbers(self.scales), periods=self.numbers(self.periods),
                        side=self.side.currentText(), part=self.part.currentText(), index=self.index.value(),
                        radius=self.radius.value(), regularization=self.regularization.value(),
                        clamp=self.clamp.isChecked(), normalize=self.normalize.isChecked(), poses=poses, sampling=sampling,
                        solver_type=self.solver_type.currentText(),
                        smooth={'axes': smooth_axes, 'signs': self.numbers(self.smooth_signs), 'angles': self.numbers(self.smooth_angles)})

    def apply_preset(self):
        """创建数据草稿；已有场景网络不会被删除。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.model = create_adv_model(self.part.currentText(), self.side.currentText(), index=self.index.value())
        self.driver = None
        self.controller.setText(get_adv_controller(self.model.part, self.model.side))
        self.angles.setText('45,45,22.5,22.5,45' if self.model.part == 'wrist' else '90,90,45,45,90')
        self.show_model()
        self.status.setText('已建立 ADV 模板；当前控制器姿态将作为采样中立')

    def pick_controller(self):
        """拾取选中控制器，不直接旋转。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        nodes = scene_utils.get_selected_nodes(long=True)
        if len(nodes) != 1:
            raise ValueError('请只选择一个采样控制器')
        self.controller.setText(nodes[0])

    def pick_joint(self):
        """更换关节意味着原采样不再有效，清空数据草稿。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        nodes = scene_utils.get_selected_nodes(long=True)
        if len(nodes) != 1:
            raise ValueError('请只选择一个输入关节')
        values = []
        for axis in 'XYZ':
            values.append(nodes[0] + '.rotate' + axis)
        self.inputs.setText(','.join(values))
        self.model.poses = []
        self.model.inputs = values
        self.show_poses()

    def auto_sample(self):
        """每次自动采样重新生成完整样本集；训练失败保留原草稿。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        model = self.read_settings()
        settings = dict(model.sampling)
        controller = settings.pop('controller')
        offsets = create_pose_offsets(**settings)
        candidate = sample_controller(model, controller, offsets)
        create_solver(candidate).train()
        self.model = candidate
        self.show_poses()
        self.status.setText('自动采样完成：{} 个姿态；控制器与自动关键帧已恢复'.format(len(candidate.poses)))

    def capture_current(self):
        """可选补充组合姿态；默认流程使用自动采样。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        model = self.read_settings()
        capture_pose(model, self.pose_name.text().strip(), neutral=not model.poses)
        self.model = model
        self.show_poses()

    def remove_pose(self):
        """保留中立样本，避免数据缺少基准。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        index = self.poses.currentRow()
        if index <= 0:
            raise ValueError('请选择非中立样本')
        self.model.poses.pop(index)
        self.show_poses()

    def show_poses(self):
        """显示样本值，输出选择器依据已构建网络保持稳定。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.poses.clear()
        for pose in self.model.poses:
            self.poses.addItem('{} : {}'.format(pose['name'], pose['values']))
        self.outputs.clear()
        names = self.driver.model.get_output_names() if self.driver else self.model.get_output_names()
        self.outputs.addItems(names)

    def show_model(self):
        """加载草稿或恢复场景后同步设置区。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.inputs.setText(','.join(self.model.inputs))
        self.scales.setText(','.join(map(str, self.model.scales)))
        self.periods.setText(','.join(map(str, self.model.periods)))
        self.part.setCurrentText(self.model.part)
        self.side.setCurrentText(self.model.side)
        self.index.setValue(self.model.index)
        self.radius.setValue(self.model.radius)
        self.regularization.setValue(self.model.regularization)
        self.solver_type.setCurrentText(self.model.solver_type)
        self.smooth_axes.setText(','.join(map(str, self.model.smooth['axes'])))
        self.smooth_signs.setText(','.join(map(str, self.model.smooth['signs'])))
        self.smooth_angles.setText(','.join(map(str, self.model.smooth['angles'])))
        self.clamp.setChecked(self.model.clamp)
        self.normalize.setChecked(self.model.normalize)
        if self.model.sampling:
            data = self.model.sampling
            self.controller.setText(data['controller'])
            self.axes.setText(','.join(list(data['swing_axes']) + [data['twist_axis']]))
            self.signs.setText(','.join(map(str, data['swing_signs'])))
            angles = list(data['swing_angles']) + list(data['diagonal_angles']) + [data['twist_angle']]
            self.angles.setText(','.join(map(str, angles)))
        self.show_poses()

    def build(self):
        """先构建成功，再将运行时实例交给界面。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        if self.driver and self.driver.output and cmds.objExists(self.driver.output):
            raise RuntimeError('已有当前网络，请使用重建按钮')
        candidate = RbfDriver(self.read_settings())
        candidate.build()
        self.driver = candidate
        self.model = RbfModel.from_dict(candidate.model.to_dict())
        self.show_poses()
        self.status.setText('已构建：' + self.driver.output)

    def require_driver(self):
        """把操作限制在当前已构建或已恢复网络。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        if not self.driver or not self.driver.output or not cmds.objExists(self.driver.output):
            raise RuntimeError('请先构建或恢复场景网络')

    def rebuild(self):
        """迁移同名修型输出到新训练结果。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.require_driver()
        self.driver.rebuild(self.read_settings())
        self.model = RbfModel.from_dict(self.driver.model.to_dict())
        self.show_poses()
        self.status.setText('已重建并保留同名输出连接：' + self.driver.output)

    def refresh_weights(self):
        """读取场景 DG 权重。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.require_driver()
        values = self.driver.read()
        self.status.setText(str(values))
        print(values)

    def connect_output(self):
        """拒绝覆盖其他工具已有连接。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.require_driver()
        self.driver.connect_output(self.outputs.currentText(), self.destination.text().strip())
        self.status.setText('输出连接完成')

    def disconnect_output(self):
        """断开指定输出。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.require_driver()
        self.driver.disconnect_output(self.outputs.currentText(), self.destination.text().strip())
        self.status.setText('输出连接已断开')

    def refresh_scene(self):
        """枚举场景网络，不重建。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.scene_drivers.clear()
        self.scene_drivers.addItems(list_drivers())

    def restore_scene(self):
        """关闭窗口或重开场景后恢复接口。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.driver = RbfDriver.from_scene(self.scene_drivers.currentText())
        self.model = RbfModel.from_dict(self.driver.model.to_dict())
        self.show_model()
        self.status.setText('已恢复：' + self.driver.output)

    def save(self):
        """保存当前草稿和自动采样配置。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '保存 RBF 配置', '', 'JSON (*.json)')
        if path:
            save_model(self.read_settings(), path)
            self.status.setText('配置已保存')

    def load(self):
        """载入为新草稿，不删除已有场景网络。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '加载 RBF 配置', '', 'JSON (*.json)')
        if path:
            self.model = load_model(path)
            self.driver = None
            self.show_model()
            self.status.setText('配置已加载；必要时修改关节映射并重新采样')

    def delete_network(self):
        """显式点击删除当前网络，操作可撤销。

        Returns:
            None: 界面状态已同步；场景操作委托给业务接口。
        """
        self.require_driver()
        self.driver.delete()
        self.driver = None
        self.status.setText('当前网络已删除，关节与修型目标保留')


def main():
    """主工具箱与脚本编辑器使用同一单实例入口。

    Returns:
        QWidget: 已显示且持有强引用的单实例工具窗口。
    """
    return window_utils.show_window('tools.rig.rbf_corrective_tool', RbfCorrectiveTool)


__all__ = ['RbfCorrectiveTool', 'main']
