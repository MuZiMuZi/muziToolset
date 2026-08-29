from PySide2.QtCore import *
from importlib import reload

import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..core import pipelineUtils , jointUtils,weightsUtils


reload (jointUtils)
reload (pipelineUtils)
reload(weightsUtils)

class Joint_Tool (QWidget) :
    """
    一个关节工具的类
    """


    def __init__ (self , parent = None) :
        super (Joint_Tool , self).__init__ (parent)
        # 设置窗口标题
        self.setWindowTitle ("Joint Tool")
        self.setMinimumWidth (300)  # Adjust the minimum width as needed

        # 创建小部件、布局和连接
        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        # 关节显示大小的部件
        self.joint_size_label = QLabel ("关节显示大小:")
        self.joint_size_label.setStyleSheet (u"color: rgb(255, 0, 0);")
        self.joint_size_line = QLineEdit ()
        self.joint_size_line.setText ('0.50')
        self.joint_size_slider = QSlider (Qt.Horizontal)
        self.joint_size_slider.setSingleStep (0.10)
        self.joint_size_slider.setMinimum (0.01)
        self.joint_size_slider.setMaximum (10)
        self.joint_size_slider.setTickPosition (QSlider.TicksBelow)

        # 关节轴向的部件
        self.show_joint_axis_label = QLabel ('---------------关节轴向----------------')
        self.show_joint_axis_label.setStyleSheet ("color: rgb(255, 69, 0); font-weight: bold; font-size: 14px;")
        self.show_joint_axis_select_btn = QPushButton (QIcon (':menuIconModify.png') , '显示关节轴向(选择)')
        self.show_joint_axis_select_btn.setToolTip ('将所选择的关节显示关节轴向')
        self.show_joint_axis_hierarchy_btn = QPushButton (QIcon (':menuIconModify.png') , '显示关节轴向(层级)')
        self.show_joint_axis_hierarchy_btn.setToolTip ('将选择的关节的层级关节显示关节轴向')
        self.show_joint_axis_all_btn = QPushButton (QIcon (':menuIconModify.png') , '显示关节轴向(所有)')
        self.show_joint_axis_all_btn.setToolTip ('将场景里所有的关节显示关节轴向')
        self.hide_joint_axis_select_btn = QPushButton (QIcon (':menuIconModify.png') , '隐藏关节轴向(选择)')
        self.hide_joint_axis_hierarchy_btn = QPushButton (QIcon (':menuIconModify.png') , '隐藏关节轴向(层级)')
        self.hide_joint_axis_all_btn = QPushButton (QIcon (':menuIconModify.png') , '隐藏关节轴向(所有)')
        # 设置文本提示
        self.hide_joint_axis_select_btn.setToolTip ('将所选择的关节隐藏关节轴向')
        self.hide_joint_axis_hierarchy_btn.setToolTip ('将选择的关节的层级关节隐藏关节轴向')
        self.hide_joint_axis_all_btn.setToolTip ('将场景里所有的关节隐藏关节轴向')

        self.joint_axis_buttons = [self.show_joint_axis_select_btn , self.show_joint_axis_hierarchy_btn ,
                                   self.show_joint_axis_all_btn , self.hide_joint_axis_select_btn ,
                                   self.hide_joint_axis_hierarchy_btn , self.hide_joint_axis_all_btn
                                   ]
        # 关节设置的部件
        self.joint_setting_label = QLabel ('---------------关节设置----------------')
        self.joint_setting_label.setStyleSheet (u"color: rgb(255,170, 255);")
        self.joint_orient_btn = QPushButton (QIcon (':orientJoint.png') , '确定关节方向')
        self.mirror_joint_btn = QPushButton (QIcon (':kinMirrorJoint_S.png') , '镜像关节')
        self.create_ikHandle_btn = QPushButton (QIcon (':kinHandle.png') , '创建IK控制柄')
        self.create_ikSplineHandle_btn = QPushButton (QIcon (':kinSplineHandle.png') , '创建IK样条线控制柄')

        # 设置文本提示
        self.joint_orient_btn.setToolTip ('打开确认关节方向窗口')
        self.mirror_joint_btn.setToolTip ('打开镜像关节窗口')
        self.create_ikHandle_btn.setToolTip ('打开创建ik控制柄窗口')
        self.create_ikSplineHandle_btn.setToolTip ('打开创建ik样条线控制柄窗口')

        self.joint_setting_buttons = [self.joint_orient_btn , self.mirror_joint_btn ,
                                      self.create_ikHandle_btn , self.create_ikSplineHandle_btn
                                      ]

        # 蒙皮设置的部件
        self.skin_setting_label = QLabel ('---------------蒙皮设置----------------')
        self.skin_setting_label.setStyleSheet (u"color: rgb(0,85, 254);")
        self.bind_skin_btn = QPushButton (QIcon (':smoothSkin.png') , '绑定蒙皮')
        self.delete_skin_btn = QPushButton (QIcon (':detachSkin.png') , '取消绑定蒙皮')
        self.artPaint_skin_btn = QPushButton (QIcon (':paintSkinWeights.png') , '绘制蒙皮权重')
        self.mirror_skin_btn = QPushButton (QIcon (':mirrorSkinWeight.png') , '镜像蒙皮权重')

        # 设置文本提示
        self.bind_skin_btn.setToolTip ('打开绑定蒙皮窗口')
        self.delete_skin_btn.setToolTip ('打开取消绑定蒙皮窗口')
        self.artPaint_skin_btn.setToolTip ('打开绘制蒙皮权重窗口')
        self.mirror_skin_btn.setToolTip ('打开镜像蒙皮权重窗口')

        self.skin_setting_buttons = [self.bind_skin_btn ,
                                     self.delete_skin_btn ,
                                     self.artPaint_skin_btn ,

                                     self.mirror_skin_btn]

        # 关节工具的部件
        self.joint_tool_label = QLabel ('---------------关节工具----------------')
        self.joint_tool_label.setStyleSheet (u"color: rgb(0,255, 127);")
        self.create_snap_joint_btn = QPushButton (QIcon (':kinJoint.png') , '吸附——创建关节')
        self.create_child_joint_btn = QPushButton (QIcon (':kinJoint.png') , '创建子关节')
        self.create_more_joint_btn = QPushButton (QIcon (':kinConnect.png') , '关节链重采样')

        self.create_joint_chain_btn = QPushButton (QIcon (':kinConnect.png') , '组成关节链')
        self.create_curve_chain_btn = QPushButton (QIcon (':curveEP.png') , '曲线——创建关节链')
        self.create_edge_chain_btn = QPushButton (QIcon (':polyEdgeToCurves.png') , '多边形边——创建关节链')

        self.open_joint_scaleCompensate_btn = QPushButton (QIcon (':kinJoint.png') , '开启关节分段比例补偿')
        self.close_joint_scaleCompensate_btn = QPushButton (QIcon (':kinJoint.png') , '关闭关节分段比例补偿')
        self.create_constraint_joint_btn = QPushButton (QIcon (':parentConstraint.png') , '批量约束——关节')

        self.show_joint_orient_btn = QPushButton (QIcon (':menuIconModify.png') , '显示关节定向')
        self.hide_joint_orient_btn = QPushButton (QIcon (':menuIconModify.png') , '隐藏关节定向')
        self.clear_joint_orient_btn = QPushButton (QIcon (':menuIconModify.png') , '归零关节定向')
        self.create_curve_on_joints_btn = QPushButton (QIcon (':curveEP.png') , '选择关节链条创建曲线')
        self.copy_skin_btn = QPushButton (QIcon (':copySkinWeight.png') , '复制蒙皮权重')

        # 设置文本提示
        self.create_snap_joint_btn.setToolTip ('根据吸附的物体中心创建关节')
        self.create_child_joint_btn.setToolTip ('选中的物体底下创建子关节')
        self.create_more_joint_btn.setToolTip ('对关节链重新创建链数')

        self.create_joint_chain_btn.setToolTip ('根据选择的顺序将关节组成关节链')
        self.create_curve_chain_btn.setToolTip ('根据选择的曲线创建关节链')
        self.create_edge_chain_btn.setToolTip ('根据选择的多边形边创建关节链')

        self.open_joint_scaleCompensate_btn.setToolTip ('开启所选择的关节的分段比例补偿')
        self.close_joint_scaleCompensate_btn.setToolTip ('关闭所选择的关节的分段比例补偿')
        self.create_constraint_joint_btn.setToolTip ('批量约束所选择的关节')

        self.show_joint_orient_btn.setToolTip ('显示所选择的关节的关节定向在通道盒里')
        self.hide_joint_orient_btn.setToolTip ('隐藏所选择的关节的关节定向在通道盒里')
        self.clear_joint_orient_btn.setToolTip ('归零所选择的关节的关节定向')

        self.copy_skin_btn.setToolTip ('复制权重，先选择需要复制的蒙皮权重物体，再加选需要复制权重的物体')
        self.joint_tool_buttons = [self.create_snap_joint_btn ,
                                   self.create_child_joint_btn ,
                                   self.create_more_joint_btn ,

                                   self.create_joint_chain_btn ,
                                   self.create_curve_chain_btn ,
                                   self.create_edge_chain_btn ,

                                   self.open_joint_scaleCompensate_btn ,
                                   self.close_joint_scaleCompensate_btn ,
                                   self.create_constraint_joint_btn ,

                                   self.show_joint_orient_btn ,
                                   self.hide_joint_orient_btn ,
                                   self.clear_joint_orient_btn ,
                                   self.create_curve_on_joints_btn ,
                                   self.copy_skin_btn]


    def create_layouts (self) :
        """创建需要的布局"""
        # 创建关节大小的布局
        self.joint_size_layout = QHBoxLayout ()
        self.joint_size_layout.addWidget (self.joint_size_label)
        self.joint_size_layout.addWidget (self.joint_size_line)
        self.joint_size_layout.addWidget (self.joint_size_slider)

        # 创建关节轴向的布局
        self.joint_axis_layout = QGridLayout ()
        self.create_joint_axis_layout ()

        # 创建关节设置的布局
        self.joint_setting_layout = QGridLayout ()
        self.create_joint_setting_layout ()

        # 创建蒙皮设置的布局
        self.skin_setting_layout = QGridLayout ()
        self.create_skin_setting_layout ()

        # 创建关节工具的布局
        self.joint_tool_layout = QGridLayout ()
        self.create_joint_tool_layout ()

        # 创建关节主页面的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.joint_size_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.show_joint_axis_label)
        self.main_layout.addLayout (self.joint_axis_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.joint_setting_label)
        self.main_layout.addLayout (self.joint_setting_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.skin_setting_label)
        self.main_layout.addLayout (self.skin_setting_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.joint_tool_label)
        self.main_layout.addLayout (self.joint_tool_layout)
        self.main_layout.addStretch ()


    def create_joint_axis_layout (self) :
        # 添加joint_axis_layout的按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.joint_axis_buttons) :
            self.joint_axis_layout.addWidget (button , *position)


    def create_joint_setting_layout (self) :
        # 添加joint_setting_layout的按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.joint_setting_buttons) :
            self.joint_setting_layout.addWidget (button , *position)


    def create_skin_setting_layout (self) :
        # 添加joint_setting_layout的按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.skin_setting_buttons) :
            self.skin_setting_layout.addWidget (button , *position)


    def create_joint_tool_layout (self) :
        # 添加joint_tool_layout的按钮,关节工具面板的按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.joint_tool_buttons) :
            self.joint_tool_layout.addWidget (button , *position)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        # 关节显示大小的部件
        self.joint_size_line.textChanged.connect (self.set_joint_size)
        self.joint_size_slider.valueChanged.connect (self.set_joint_size_line)
        self.show_joint_axis_select_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_select ())
        self.show_joint_axis_hierarchy_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_hirerarchy ())
        self.show_joint_axis_all_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_all ())

        # 关节轴向的部件
        self.hide_joint_axis_select_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_axis_select ())
        self.hide_joint_axis_hierarchy_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_axis_hirerarchy ())
        self.hide_joint_axis_all_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_axis_all ())

        # 关节设置的部件
        self.joint_orient_btn.clicked.connect (lambda : mel.eval ("OrientJointOptions;"))
        self.mirror_joint_btn.clicked.connect (lambda : mel.eval ("MirrorJointOptions;"))
        self.create_ikHandle_btn.clicked.connect (lambda : mel.eval ("IKHandleToolOptions;"))
        self.create_ikSplineHandle_btn.clicked.connect (lambda : mel.eval ("IKSplineHandleToolOptions;"))

        # 蒙皮设置的部件连接
        self.bind_skin_btn.clicked.connect (lambda : mel.eval ("SmoothBindSkinOptions;"))
        self.delete_skin_btn.clicked.connect (lambda : mel.eval ("DetachSkinOptions;"))
        self.artPaint_skin_btn.clicked.connect (lambda : mel.eval ("ArtPaintSkinWeightsToolOptions;"))
        self.mirror_skin_btn.clicked.connect (lambda : mel.eval ("MirrorSkinWeightsOptions;"))

        # 创建关节工具面板的按钮的连接
        self.create_connections_joint_tool_layout ()


    def create_connections_joint_tool_layout (self) :
        """
        创建关节工具面板的按钮的连接
        """
        self.create_snap_joint_btn.clicked.connect (lambda : jointUtils.Joint.create_snap_joint ())
        self.create_child_joint_btn.clicked.connect (lambda : jointUtils.Joint.create_child_joint ())
        self.create_more_joint_btn.clicked.connect (lambda : jointUtils.Joint.create_more_joint ())

        self.create_joint_chain_btn.clicked.connect (lambda : jointUtils.Joint.joint_To_Chain_Selection ())
        self.create_curve_chain_btn.clicked.connect (lambda : jointUtils.Joint.create_joints_on_curve ())
        self.create_edge_chain_btn.clicked.connect (lambda : jointUtils.Joint.create_chain_on_polyToCurve ())

        self.open_joint_scaleCompensate_btn.clicked.connect (lambda : jointUtils.Joint.open_joint_scaleCompensate ())
        self.close_joint_scaleCompensate_btn.clicked.connect (lambda : jointUtils.Joint.close_joint_scaleCompensate ())
        self.create_constraint_joint_btn.clicked.connect (lambda : jointUtils.Joint.batch_Constraints_joint ())

        self.show_joint_orient_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_orient ())
        self.hide_joint_orient_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_orient ())
        self.clear_joint_orient_btn.clicked.connect (lambda : jointUtils.Joint.clear_joint_orient ())
        self.create_curve_on_joints_btn.clicked.connect (self.clicked_create_curve_on_joints_btn)
        self.copy_skin_btn.clicked.connect(lambda : weightsUtils.Weights.copy_weight ())


    def set_joint_size_line (self) :
        joint_size_value = float (self.joint_size_slider.value ())
        self.joint_size_line.setText (str (joint_size_value))


    def clicked_create_curve_on_joints_btn (self) :
        """
        选择关节链条，在对应的关节点上创建曲线
        """
        jnts = cmds.ls (sl = True , type = 'joint')
        # 对所有选中的关节做循环
        for jnt in jnts :
            # 获取所有选中的关节下方的所有关节链
            jnt_list = cmds.listRelatives (jnt , children = True , allDescendents = True , type = 'joint')
            jnt_list.append (jnt)
            jnt_list.reverse ()
            pipelineUtils.Pipeline.create_curve_on_joints (jnt_list , 'crv' + jnt , degree = 3)


    def set_joint_size (self) :
        joint_size_value = float (self.joint_size_line.text ())
        self.joint_size_slider.setValue (joint_size_value)
        jointUtils.Joint.set_jointSize (joint_size_value)


def show () :
    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Joint_Tool ()  # 创建实例
    window.show ()  # 显示窗口


def main () :
    return Joint_Tool ()


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Joint_Tool ()  # 创建实例
    window.show ()  # 显示窗口
