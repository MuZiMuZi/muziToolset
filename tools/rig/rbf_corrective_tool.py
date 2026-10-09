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
from ...systems.rbf.presets import create_adv_model, create_joint_model
from ...systems.rbf.driver import read_inputs
from ...systems.rbf.pose_locator import get_pose_locators, read_pose_locators, write_pose_locator
from ...systems.rbf.output_driver import connect_mapped_output, disconnect_mapped_output
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
        self.setWindowTitle('通用 Pose Driver / RBF')
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
        layout.addWidget(QtWidgets.QLabel('Pose Driver · Shoulder / Hip / Wrist / 自定义关节'))
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
            ('部位（可输入自定义名称）', self.part), ('求解器（rbf=真正 RBF）', self.solver_type), ('侧别', self.side), ('实例序号', self.index),
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
        locator_group = QtWidgets.QGroupBox('Pose Locator 编辑')
        locator_layout = QtWidgets.QVBoxLayout(locator_group)
        self.add_button(locator_layout, '选择样本 Locator（Channel Box 编辑 poseValue）', self.select_pose_locator)
        self.add_button(locator_layout, '用当前姿态覆盖选中样本', self.replace_current_pose)
        self.add_button(locator_layout, '读取 Locator 编辑为草稿', self.read_locators)
        locator_layout.addWidget(QtWidgets.QLabel('修改草稿后点击重建。Smoothstep 使用中立值和阈值；RBF 使用全部样本。'))
        body.addWidget(locator_group)
        build_row = QtWidgets.QHBoxLayout()
        self.add_button(build_row, '训练并构建', self.build)
        self.add_button(build_row, '重建并保留连接', self.rebuild)
        self.add_button(build_row, '刷新权重', self.refresh_weights)
        body.addLayout(build_row)
        self.add_button(body, '选择输出网络（Channel Box 实时权重）', self.select_output)
        self.outputs = QtWidgets.QComboBox()
        self.destination = QtWidgets.QLineEdit()
        self.destination.setPlaceholderText('例如 blendShape1.armUp 或 blendShape1.weight[0]')
        body.addWidget(self.outputs)
        body.addWidget(self.destination)
        connect_row = QtWidgets.QHBoxLayout()
        self.add_button(connect_row, '连接输出', self.connect_output)
        self.add_button(connect_row, '断开输出', self.disconnect_output)
        body.addLayout(connect_row)
        mapping_group = QtWidgets.QGroupBox('辅助骨 / 标量端点映射')
        mapping_layout = QtWidgets.QFormLayout(mapping_group)
        self.mapping_neutral = QtWidgets.QDoubleSpinBox()
        self.mapping_full = QtWidgets.QDoubleSpinBox()
        for widget in (self.mapping_neutral, self.mapping_full):
            widget.setRange(-100000, 100000)
            widget.setDecimals(4)
        self.mapping_full.setValue(30)
        self.use_current_neutral = QtWidgets.QCheckBox('权重 0 使用目标当前值')
        self.use_current_neutral.setChecked(True)
        mapping_layout.addRow(self.use_current_neutral)
        mapping_layout.addRow('权重 0 的目标值', self.mapping_neutral)
        mapping_layout.addRow('权重 1 的目标值', self.mapping_full)
        self.add_button(mapping_layout, '将所选输出映射到上述目标属性', self.connect_mapping)
        self.add_button(mapping_layout, '删除上述目标的当前映射', self.disconnect_mapping)
        body.addWidget(mapping_group)
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
        theme.style_window(self, title='通用 Pose Driver / RBF', minimum_width=560)

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
        part = self.part.currentText().strip()
        solver_type = self.solver_type.currentText()
        if part in ('arm', 'thigh', 'wrist'):
            self.model = create_adv_model(part, self.side.currentText(), index=self.index.value())
            self.controller.setText(get_adv_controller(self.model.part, self.model.side))
        else:
            inputs = self.tokens(self.inputs.text())
            if not inputs:
                raise ValueError('自定义部位请先拾取输入关节')
            self.model = create_joint_model(inputs[0].split('.', 1)[0], part=part,
                                            side=self.side.currentText(), index=self.index.value())
        self.model.solver_type = solver_type
        self.driver = None
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
        self.model.remove_pose(self.model.poses[index]['name'])
        self.show_poses()

    def selected_pose_name(self):
        """取得所选样本，包括中立；避免用当前输出选择替代样本选择。

        Returns:
            str: 当前样本列表中选中的姿态名称；没有选择则抛出 ValueError。
        """
        index = self.poses.currentRow()
        if index < 0 or index >= len(self.model.poses):
            raise ValueError('请先选择一个姿态样本')
        return self.model.poses[index]['name']

    def select_pose_locator(self):
        """选择当前网络的样本 Locator，在 Channel Box 编辑 poseValue 数值。"""
        self.require_driver()
        name = self.selected_pose_name()
        locators = get_pose_locators(self.driver)
        if name not in locators:
            raise ValueError('样本尚未构建为 Locator，请先构建或重建')
        cmds.select(locators[name], replace=True)

    def replace_current_pose(self):
        """覆盖选中样本；已构建的 Locator 同步记录，实时输出仍需重建。"""
        name = self.selected_pose_name()
        candidate = self.read_settings()
        values = read_inputs(candidate)
        candidate.update_pose(name, values)
        if self.driver and name in get_pose_locators(self.driver):
            if candidate.inputs != self.driver.model.inputs:
                raise ValueError('输入已改变，请重新采样')
            write_pose_locator(self.driver, name, values)
        self.model = candidate
        self.show_poses()
        self.status.setText('已记录姿态到草稿；点击重建应用到实时输出')

    def read_locators(self):
        """只读取 Locator 数据；保留当前 UI 的核设置和方向阈值。"""
        self.require_driver()
        draft = self.read_settings()
        if draft.inputs != self.driver.model.inputs:
            raise ValueError('输入已改变，请重新采样')
        candidate = read_pose_locators(self.driver)
        draft.poses = candidate.poses
        create_solver(draft).train()
        self.model = draft
        self.show_poses()
        self.status.setText('Locator 编辑已读取；点击重建应用到实时输出')

    def select_output(self):
        """选择输出网络；DG 实时更新 Channel Box，无需 UI 定时回调。"""
        self.require_driver()
        cmds.select(self.driver.output, replace=True)

    def connect_mapping(self):
        """辅助骨以当前 Maya 单位设置端点，使用所属 Driven 曲线。"""
        self.require_driver()
        neutral = None if self.use_current_neutral.isChecked() else self.mapping_neutral.value()
        curve = connect_mapped_output(self.driver, self.outputs.currentText(),
                                      self.destination.text().strip(), self.mapping_full.value(), neutral)
        self.status.setText('输出映射完成：' + curve)

    def disconnect_mapping(self):
        """删除当前网络的目标映射，保留目标骨骼。"""
        self.require_driver()
        disconnect_mapped_output(self.driver, self.destination.text().strip())
        self.status.setText('输出映射已删除')

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
