# coding=utf-8
u"""
Face Rig Wizard UI
==================

Maya 2023 + PySide2

界面结构：
    顶部：
        Step 01 / Step 02 / Step 03 / Step 04

    中间：
        当前步骤页面

    底部：
        上一步 / 下一步

界面规则：
    1. 当前步骤高亮。
    2. 已完成步骤变暗。
    3. 已完成步骤可以点击返回。
    4. 未完成步骤不能直接跳转。
    5. “上一步”只切换 UI，不重新执行 Build。
    6. Step 01 点击“下一步”时执行 FaceSetup.build()。
    7. Step 01 Build 成功后才会进入 Step 02。
    8. 嘴唇关节数量只允许 4 的倍数。
"""

from imp import reload

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtWidgets

from shiboken2 import wrapInstance

from . import face_setup

reload(face_setup)


# =============================================================================
# Maya Main Window
# =============================================================================

def get_maya_main_window():
    u"""获取 Maya 主窗口。"""

    maya_main_window_ptr = omui.MQtUtil.mainWindow()

    if maya_main_window_ptr is None:
        return None

    maya_main_window = wrapInstance(
        int(maya_main_window_ptr),
        QtWidgets.QWidget
    )

    return maya_main_window


# =============================================================================
# Face Rig UI
# =============================================================================

class FaceRigUI(QtWidgets.QDialog):

    window_name = "muzi_face_rig_wizard_ui"

    step_count = 4

    def __init__(self, parent=get_maya_main_window()):

        super(FaceRigUI, self).__init__(parent)

        # ---------------------------------------------------------------------
        # 当前步骤
        # ---------------------------------------------------------------------

        self.current_step_index = 0

        # 已经完成的步骤。
        # 例如 Step 01 完成后，保存 0。
        self.completed_step_indexes = set()

        # ---------------------------------------------------------------------
        # Step 顶部按钮
        # ---------------------------------------------------------------------

        self.step_btn_list = []

        # ---------------------------------------------------------------------
        # 页面
        # ---------------------------------------------------------------------

        self.step_stack_widget = None

        self.step1_widget = None
        self.step2_widget = None
        self.step3_widget = None
        self.step4_widget = None

        # ---------------------------------------------------------------------
        # Step 01
        # ---------------------------------------------------------------------

        self.face_setup = None

        self.face_head_model_line_edit = None
        self.face_lf_eye_model_line_edit = None
        self.face_rt_eye_model_line_edit = None

        self.upper_teech_model_line_edit = None
        self.lower_teech_model_line_edit = None

        self.face_tongue_model_line_edit = None
        self.face_gum_model_line_edit = None

        self.mouth_jnt_number_slider = None
        self.mouth_jnt_number_value_label = None

        # ---------------------------------------------------------------------
        # 底部按钮
        # ---------------------------------------------------------------------

        self.previous_step_btn = None
        self.next_step_btn = None

        # ---------------------------------------------------------------------
        # 创建 UI
        # ---------------------------------------------------------------------

        self._set_window()

        self._create_widgets()

        self._create_layouts()

        self._create_connections()

        self.set_current_step(
            0
        )

    # =========================================================================
    # Window
    # =========================================================================

    def _set_window(self):

        self.setObjectName(
            self.window_name
        )

        self.setWindowTitle(
            u"木子 Face Rig"
        )

        self.resize(
            430,
            680
        )

        self.setMinimumWidth(
            400
        )

        self.setWindowFlags(
            self.windowFlags()
            ^ QtCore.Qt.WindowContextHelpButtonHint
        )

    # =========================================================================
    # Widgets
    # =========================================================================

    def _create_widgets(self):

        # ---------------------------------------------------------------------
        # Step 按钮
        # ---------------------------------------------------------------------

        for step_index in range(self.step_count):

            step_number = step_index + 1

            step_btn = QtWidgets.QPushButton(
                u"Step {:02d}".format(
                    step_number
                )
            )

            step_btn.setCheckable(
                False
            )

            step_btn.setMinimumHeight(
                34
            )

            step_btn.setCursor(
                QtCore.Qt.PointingHandCursor
            )

            step_btn.setProperty(
                "step_index",
                step_index
            )

            self.step_btn_list.append(
                step_btn
            )

        # ---------------------------------------------------------------------
        # Stack
        # ---------------------------------------------------------------------

        self.step_stack_widget = QtWidgets.QStackedWidget()

        self.step1_widget = QtWidgets.QWidget()
        self.step2_widget = QtWidgets.QWidget()
        self.step3_widget = QtWidgets.QWidget()
        self.step4_widget = QtWidgets.QWidget()

        self.step_stack_widget.addWidget(
            self.step1_widget
        )

        self.step_stack_widget.addWidget(
            self.step2_widget
        )

        self.step_stack_widget.addWidget(
            self.step3_widget
        )

        self.step_stack_widget.addWidget(
            self.step4_widget
        )

        # ---------------------------------------------------------------------
        # Step 01 Model
        # ---------------------------------------------------------------------

        self.face_head_model_line_edit = QtWidgets.QLineEdit()
        self.face_lf_eye_model_line_edit = QtWidgets.QLineEdit()
        self.face_rt_eye_model_line_edit = QtWidgets.QLineEdit()

        self.upper_teech_model_line_edit = QtWidgets.QLineEdit()
        self.lower_teech_model_line_edit = QtWidgets.QLineEdit()

        self.face_tongue_model_line_edit = QtWidgets.QLineEdit()
        self.face_gum_model_line_edit = QtWidgets.QLineEdit()

        self.face_head_model_line_edit.setPlaceholderText(
            u"指定头部模型"
        )

        self.face_lf_eye_model_line_edit.setPlaceholderText(
            u"指定左眼模型"
        )

        self.face_rt_eye_model_line_edit.setPlaceholderText(
            u"指定右眼模型"
        )

        self.upper_teech_model_line_edit.setPlaceholderText(
            u"指定上牙模型"
        )

        self.lower_teech_model_line_edit.setPlaceholderText(
            u"指定下牙模型"
        )

        self.face_tongue_model_line_edit.setPlaceholderText(
            u"指定舌头模型"
        )

        self.face_gum_model_line_edit.setPlaceholderText(
            u"指定牙龈模型"
        )

        # ---------------------------------------------------------------------
        # Mouth Joint Slider
        #
        # Slider 1 -> 4
        # Slider 2 -> 8
        # Slider 3 -> 12
        # ...
        # Slider 25 -> 100
        # ---------------------------------------------------------------------

        self.mouth_jnt_number_slider = QtWidgets.QSlider(
            QtCore.Qt.Horizontal
        )

        self.mouth_jnt_number_slider.setRange(
            1,
            25
        )

        # 默认嘴唇关节数量为 32。
        # Slider 的实际值乘以 4，所以这里设置为 8。
        self.mouth_jnt_number_slider.setValue(
            8
        )

        self.mouth_jnt_number_slider.setSingleStep(
            1
        )

        self.mouth_jnt_number_slider.setPageStep(
            1
        )

        self.mouth_jnt_number_slider.setTickPosition(
            QtWidgets.QSlider.TicksBelow
        )

        self.mouth_jnt_number_slider.setTickInterval(
            1
        )

        self.mouth_jnt_number_value_label = QtWidgets.QLabel(
            u"32"
        )

        self.mouth_jnt_number_value_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        self.mouth_jnt_number_value_label.setFixedWidth(
            45
        )

        # ---------------------------------------------------------------------
        # Bottom Buttons
        # ---------------------------------------------------------------------

        self.previous_step_btn = QtWidgets.QPushButton(
            u"上一步"
        )

        self.next_step_btn = QtWidgets.QPushButton(
            u"下一步"
        )

        self.previous_step_btn.setMinimumHeight(
            36
        )

        self.next_step_btn.setMinimumHeight(
            36
        )

    # =========================================================================
    # Layout
    # =========================================================================

    def _create_layouts(self):

        main_layout = QtWidgets.QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        main_layout.setSpacing(
            8
        )

        # ---------------------------------------------------------------------
        # 标题
        # ---------------------------------------------------------------------

        title_label = QtWidgets.QLabel(
            u"Face Rig Builder"
        )

        title_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        title_label.setMinimumHeight(
            30
        )

        main_layout.addWidget(
            title_label
        )

        # ---------------------------------------------------------------------
        # 顶部 Step 标识
        # ---------------------------------------------------------------------

        step_header_widget = QtWidgets.QWidget()

        step_header_layout = QtWidgets.QHBoxLayout(
            step_header_widget
        )

        step_header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        step_header_layout.setSpacing(
            4
        )

        for step_btn in self.step_btn_list:

            step_header_layout.addWidget(
                step_btn
            )

        main_layout.addWidget(
            step_header_widget
        )

        # ---------------------------------------------------------------------
        # 分隔线
        # ---------------------------------------------------------------------

        separator_line = QtWidgets.QFrame()

        separator_line.setFrameShape(
            QtWidgets.QFrame.HLine
        )

        separator_line.setFrameShadow(
            QtWidgets.QFrame.Sunken
        )

        main_layout.addWidget(
            separator_line
        )

        # ---------------------------------------------------------------------
        # Step 页面
        # ---------------------------------------------------------------------

        main_layout.addWidget(
            self.step_stack_widget,
            1
        )

        self._create_step1_layout()
        self._create_step2_layout()
        self._create_step3_layout()
        self._create_step4_layout()

        # ---------------------------------------------------------------------
        # Bottom
        # ---------------------------------------------------------------------

        bottom_separator_line = QtWidgets.QFrame()

        bottom_separator_line.setFrameShape(
            QtWidgets.QFrame.HLine
        )

        bottom_separator_line.setFrameShadow(
            QtWidgets.QFrame.Sunken
        )

        main_layout.addWidget(
            bottom_separator_line
        )

        bottom_layout = QtWidgets.QHBoxLayout()

        bottom_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        bottom_layout.addWidget(
            self.previous_step_btn
        )

        bottom_layout.addStretch(
            1
        )

        bottom_layout.addWidget(
            self.next_step_btn
        )

        main_layout.addLayout(
            bottom_layout
        )

    # =========================================================================
    # Step 01
    # =========================================================================

    def _create_step1_layout(self):

        main_layout = QtWidgets.QVBoxLayout(
            self.step1_widget
        )

        main_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        main_layout.setSpacing(
            8
        )

        # ---------------------------------------------------------------------
        # Step Title
        # ---------------------------------------------------------------------

        step_title_label = QtWidgets.QLabel(
            u"Step 01 - Face Setup"
        )

        step_title_label.setMinimumHeight(
            28
        )

        main_layout.addWidget(
            step_title_label
        )

        # ---------------------------------------------------------------------
        # 模型设置
        # ---------------------------------------------------------------------

        model_group_box = QtWidgets.QGroupBox(
            u"模型设置"
        )

        model_layout = QtWidgets.QGridLayout(
            model_group_box
        )

        model_layout.setColumnStretch(
            1,
            1
        )

        model_items = [
            (
                u"头部模型",
                self.face_head_model_line_edit
            ),
            (
                u"左眼模型",
                self.face_lf_eye_model_line_edit
            ),
            (
                u"右眼模型",
                self.face_rt_eye_model_line_edit
            ),
            (
                u"上牙模型",
                self.upper_teech_model_line_edit
            ),
            (
                u"下牙模型",
                self.lower_teech_model_line_edit
            ),
            (
                u"舌头模型",
                self.face_tongue_model_line_edit
            ),
            (
                u"牙龈模型",
                self.face_gum_model_line_edit
            )
        ]

        row = 0

        for model_item in model_items:

            label_text = model_item[0]

            line_edit = model_item[1]

            label = QtWidgets.QLabel(
                label_text
            )

            select_btn = QtWidgets.QPushButton(
                u"<<"
            )

            select_btn.setFixedWidth(
                36
            )

            model_layout.addWidget(
                label,
                row,
                0
            )

            model_layout.addWidget(
                line_edit,
                row,
                1
            )

            model_layout.addWidget(
                select_btn,
                row,
                2
            )

            select_btn.clicked.connect(
                lambda checked=False, target_line_edit=line_edit:
                self.set_selected_node(
                    target_line_edit
                )
            )

            row += 1

        main_layout.addWidget(
            model_group_box
        )

        # ---------------------------------------------------------------------
        # 数量设置
        # ---------------------------------------------------------------------

        number_group_box = QtWidgets.QGroupBox(
            u"数量设置"
        )

        number_layout = QtWidgets.QGridLayout(
            number_group_box
        )

        mouth_jnt_number_label = QtWidgets.QLabel(
            u"嘴唇关节数量"
        )

        mouth_jnt_number_hint_label = QtWidgets.QLabel(
            u"4 的倍数"
        )

        mouth_jnt_number_hint_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )

        number_layout.addWidget(
            mouth_jnt_number_label,
            0,
            0
        )

        number_layout.addWidget(
            mouth_jnt_number_hint_label,
            0,
            1
        )

        number_layout.addWidget(
            self.mouth_jnt_number_slider,
            1,
            0
        )

        number_layout.addWidget(
            self.mouth_jnt_number_value_label,
            1,
            1
        )

        number_layout.setColumnStretch(
            0,
            1
        )

        main_layout.addWidget(
            number_group_box
        )

        main_layout.addStretch(
            1
        )

    # =========================================================================
    # Step 02
    # =========================================================================

    def _create_step2_layout(self):

        main_layout = QtWidgets.QVBoxLayout(
            self.step2_widget
        )

        main_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        step_title_label = QtWidgets.QLabel(
            u"Step 02 - Face Guide"
        )

        main_layout.addWidget(
            step_title_label
        )

        info_label = QtWidgets.QLabel(
            u"这里后续接入 FaceGuide 的设置界面。"
        )

        info_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        main_layout.addWidget(
            info_label
        )

        main_layout.addStretch(
            1
        )

    # =========================================================================
    # Step 03
    # =========================================================================

    def _create_step3_layout(self):

        main_layout = QtWidgets.QVBoxLayout(
            self.step3_widget
        )

        main_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        step_title_label = QtWidgets.QLabel(
            u"Step 03"
        )

        main_layout.addWidget(
            step_title_label
        )

        info_label = QtWidgets.QLabel(
            u"Step 03 功能预留。"
        )

        info_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        main_layout.addWidget(
            info_label
        )

        main_layout.addStretch(
            1
        )

    # =========================================================================
    # Step 04
    # =========================================================================

    def _create_step4_layout(self):

        main_layout = QtWidgets.QVBoxLayout(
            self.step4_widget
        )

        main_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        step_title_label = QtWidgets.QLabel(
            u"Step 04"
        )

        main_layout.addWidget(
            step_title_label
        )

        info_label = QtWidgets.QLabel(
            u"Step 04 功能预留。"
        )

        info_label.setAlignment(
            QtCore.Qt.AlignCenter
        )

        main_layout.addWidget(
            info_label
        )

        main_layout.addStretch(
            1
        )

    # =========================================================================
    # Connections
    # =========================================================================

    def _create_connections(self):

        # ---------------------------------------------------------------------
        # Step 顶部按钮
        # ---------------------------------------------------------------------

        for step_btn in self.step_btn_list:

            step_btn.clicked.connect(
                self.clicked_step_btn
            )

        # ---------------------------------------------------------------------
        # Slider
        # ---------------------------------------------------------------------

        self.mouth_jnt_number_slider.valueChanged.connect(
            self.changed_mouth_jnt_number_slider
        )

        # ---------------------------------------------------------------------
        # Bottom
        # ---------------------------------------------------------------------

        self.previous_step_btn.clicked.connect(
            self.clicked_previous_step_btn
        )

        self.next_step_btn.clicked.connect(
            self.clicked_next_step_btn
        )

    # =========================================================================
    # Step State
    # =========================================================================

    def set_current_step(self, step_index):
        u"""切换当前显示的步骤。"""

        if step_index < 0:
            return

        if step_index >= self.step_count:
            return

        self.current_step_index = step_index

        self.step_stack_widget.setCurrentIndex(
            step_index
        )

        self.update_step_header()

        self.update_navigation_buttons()

    def update_step_header(self):
        u"""更新顶部 Step 标识状态。"""

        for step_index in range(len(self.step_btn_list)):

            step_btn = self.step_btn_list[step_index]

            # -----------------------------------------------------------------
            # 当前步骤
            # -----------------------------------------------------------------

            if step_index == self.current_step_index:

                step_btn.setEnabled(
                    True
                )

                step_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: rgb(85, 85, 85);
                        color: rgb(245, 245, 245);
                        font-weight: bold;
                        border: 1px solid rgb(130, 130, 130);
                        border-radius: 3px;
                        padding: 5px;
                    }
                    """
                )

                continue

            # -----------------------------------------------------------------
            # 已完成步骤
            # -----------------------------------------------------------------

            if step_index in self.completed_step_indexes:

                step_btn.setEnabled(
                    True
                )

                step_btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: rgb(45, 45, 45);
                        color: rgb(125, 125, 125);
                        border: 1px solid rgb(60, 60, 60);
                        border-radius: 3px;
                        padding: 5px;
                    }

                    QPushButton:hover {
                        color: rgb(175, 175, 175);
                    }
                    """
                )

                continue

            # -----------------------------------------------------------------
            # 未完成步骤
            # -----------------------------------------------------------------

            step_btn.setEnabled(
                False
            )

            step_btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgb(60, 60, 60);
                    color: rgb(165, 165, 165);
                    border: 1px solid rgb(75, 75, 75);
                    border-radius: 3px;
                    padding: 5px;
                }
                """
            )

    def update_navigation_buttons(self):
        u"""更新底部上一页 / 下一页按钮。"""

        # Step01 没有上一步。
        if self.current_step_index == 0:

            self.previous_step_btn.setEnabled(
                False
            )

        else:

            self.previous_step_btn.setEnabled(
                True
            )

        # Step04 使用“完成”。
        if self.current_step_index == self.step_count - 1:

            self.next_step_btn.setText(
                u"完成"
            )

        else:

            self.next_step_btn.setText(
                u"下一步"
            )

    def complete_current_step(self):
        u"""标记当前步骤已经完成。"""

        self.completed_step_indexes.add(
            self.current_step_index
        )

        self.update_step_header()

    # =========================================================================
    # Top Step Button
    # =========================================================================

    def clicked_step_btn(self):
        u"""点击顶部步骤标识。

        规则：
            当前步骤可以点击。
            已完成步骤可以返回。
            未完成步骤不能跳转。
        """

        step_btn = self.sender()

        if step_btn is None:
            return

        step_index = step_btn.property(
            "step_index"
        )

        if step_index is None:
            return

        step_index = int(
            step_index
        )

        if step_index == self.current_step_index:
            return

        if step_index not in self.completed_step_indexes:
            return

        self.set_current_step(
            step_index
        )

    # =========================================================================
    # Bottom Buttons
    # =========================================================================

    def clicked_previous_step_btn(self):
        u"""返回上一步。

        这里只切换 UI。
        不重新执行任何 Build。
        """

        previous_step_index = self.current_step_index - 1

        if previous_step_index < 0:
            return

        self.set_current_step(
            previous_step_index
        )

    def clicked_next_step_btn(self):
        u"""执行当前步骤并进入下一步。"""

        # ---------------------------------------------------------------------
        # Step 01
        # ---------------------------------------------------------------------

        if self.current_step_index == 0:

            build_result = self.build_step1()

            if not build_result:
                return

            self.complete_current_step()

            self.set_current_step(
                1
            )

            return

        # ---------------------------------------------------------------------
        # Step 02
        # ---------------------------------------------------------------------

        if self.current_step_index == 1:

            # 后续这里接：
            #
            # build_result = self.build_step2()
            #
            # if not build_result:
            #     return

            self.complete_current_step()

            self.set_current_step(
                2
            )

            return

        # ---------------------------------------------------------------------
        # Step 03
        # ---------------------------------------------------------------------

        if self.current_step_index == 2:

            # 后续这里接 Step03 Build。

            self.complete_current_step()

            self.set_current_step(
                3
            )

            return

        # ---------------------------------------------------------------------
        # Step 04
        # ---------------------------------------------------------------------

        if self.current_step_index == 3:

            # 后续这里接 Step04 Build。

            self.complete_current_step()

            self.show_message(
                u"Face Rig 全部步骤完成"
            )

            return

    # =========================================================================
    # Step 01 Selection
    # =========================================================================

    def set_selected_node(self, line_edit):
        u"""将 Maya 当前选择的第一个节点写入输入框。"""

        selected_nodes = cmds.ls(
            selection=True,
            long=False
        )

        if not selected_nodes:

            cmds.warning(
                u"【Face Rig】请先在 Maya 中选择一个模型。"
            )

            return

        selected_node = selected_nodes[0]

        line_edit.setText(
            selected_node
        )

    # =========================================================================
    # Step 01 Mouth Joint Number
    # =========================================================================

    def get_mouth_jnt_number(self):
        u"""获取嘴唇关节数量。

        Returns:
            int:
                4 / 8 / 12 / 16 ... 100
        """

        slider_value = self.mouth_jnt_number_slider.value()

        mouth_jnt_number = slider_value * 4

        return mouth_jnt_number

    def changed_mouth_jnt_number_slider(self, value):
        u"""更新嘴唇关节数量显示。"""

        mouth_jnt_number = value * 4

        self.mouth_jnt_number_value_label.setText(
            str(mouth_jnt_number)
        )

    # =========================================================================
    # Step 01 Data
    # =========================================================================

    def get_step1_data(self):
        u"""读取 Step01 UI 数据。"""

        step1_data = {
            "face_head_model": self.face_head_model_line_edit.text().strip(),
            "face_lf_eye_model": self.face_lf_eye_model_line_edit.text().strip(),
            "face_rt_eye_model": self.face_rt_eye_model_line_edit.text().strip(),
            "upper_teech_model": self.upper_teech_model_line_edit.text().strip(),
            "lower_teech_model": self.lower_teech_model_line_edit.text().strip(),
            "face_tongue_model": self.face_tongue_model_line_edit.text().strip(),
            "face_gum_model": self.face_gum_model_line_edit.text().strip(),
            "mouth_jnt_number": self.get_mouth_jnt_number()
        }

        return step1_data

    def create_face_setup(self):
        u"""根据当前 UI 数据创建 FaceSetup。"""

        step1_data = self.get_step1_data()

        self.face_setup = face_setup.FaceSetup(
            face_head_model=step1_data.get(
                "face_head_model"
            ),
            face_lf_eye_model=step1_data.get(
                "face_lf_eye_model"
            ),
            face_rt_eye_model=step1_data.get(
                "face_rt_eye_model"
            ),
            upper_teech_model=step1_data.get(
                "upper_teech_model"
            ),
            lower_teech_model=step1_data.get(
                "lower_teech_model"
            ),
            face_tongue_model=step1_data.get(
                "face_tongue_model"
            ),
            face_gum_model=step1_data.get(
                "face_gum_model"
            ),
            mouth_jnt_number=step1_data.get(
                "mouth_jnt_number"
            )
        )

        return self.face_setup

    # =========================================================================
    # Step 01 Build
    # =========================================================================

    def build_step1(self):
        u"""执行 Step01 Build。

        Returns:
            bool:
                True  -> Build 成功，可以进入下一步。
                False -> Build 失败，停留在当前页面。
        """

        try:

            face_setup_object = self.create_face_setup()

            face_setup_object.build()

            self.show_message(
                u"Step 01 Build 完成"
            )

            return True

        except Exception as error:

            self.show_error(
                u"Build Step 01 失败",
                error
            )

            return False

    # =========================================================================
    # Message
    # =========================================================================

    def show_message(self, message):

        cmds.inViewMessage(
            assistMessage=message,
            position="midCenter",
            fade=True
        )

    def show_error(self, title, error):

        cmds.warning(
            u"{}: {}".format(
                title,
                error
            )
        )

        QtWidgets.QMessageBox.critical(
            self,
            title,
            str(error)
        )


# =============================================================================
# Main
# =============================================================================

face_rig_ui = None


def main():
    u"""显示 Face Rig Wizard UI。"""

    global face_rig_ui

    try:

        if face_rig_ui is not None:

            face_rig_ui.close()

            face_rig_ui.deleteLater()

    except Exception:

        pass

    face_rig_ui = FaceRigUI()

    face_rig_ui.show()

    return face_rig_ui
