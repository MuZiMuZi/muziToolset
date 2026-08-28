# coding:utf-8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
import os
import sys


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QWidget)


class Skirt_ctrl_tool (QDialog) :
    '''
    创建一个拾取驱动工具的窗口
    用法：用于拾取设置驱动关键帧的驱动工具
    '''


    def __init__ (self , parent = maya_main_window ()) :
        super (Skirt_ctrl_tool , self).__init__ (parent)

        self.setWindowTitle (u'裙子控制器工具')

        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()


    def create_widgets (self) :
        # 创建需要创建的子部件
        # 创建名称的子部件
        self.name_label = QLabel (u'裙子名称:')
        self.name_line = QLineEdit ()
        self.name_line.setText ('skirt')

        # 创建横向关节数量的子部件
        self.horizontally_joint_label = QLabel (u'横向关节数量:')
        self.horizontally_joint_spin_box = QSpinBox ()
        self.horizontally_joint_spin_box.setFixedWidth (80)
        self.horizontally_joint_spin_box.setMinimum (1)
        self.horizontally_joint_spin_box.setMaximum (100)
        self.horizontally_joint_spin_box.setSingleStep (1)
        self.horizontally_joint_spin_box.setValue (8)

        # 创建生成定位的按钮
        self.setup_btn = QPushButton ('生成定位')

        # 创建纵向关节数量的子部件
        self.vertical_joint_label = QLabel (u'纵向关节数量:')
        self.vertical_joint_spin_box = QSpinBox ()
        self.vertical_joint_spin_box.setFixedWidth (80)
        self.vertical_joint_spin_box.setMinimum (1)
        self.vertical_joint_spin_box.setMaximum (100)
        self.vertical_joint_spin_box.setSingleStep (1)
        self.vertical_joint_spin_box.setValue (4)

        # 创建生成绑定的按钮
        self.build_btn = QPushButton ('生成绑定')


    def create_layouts (self) :
        """
        创建layout面板
        """
        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)

        # 创建生成裙子名称的布局
        self.name_layout = QHBoxLayout ()
        self.name_layout.addWidget (self.name_label)
        self.name_layout.addWidget (self.name_line)
        self.main_layout.addLayout (self.name_layout)

        # 创建生成横向定位的布局
        self.horizontally_joint_layout = QHBoxLayout ()
        self.horizontally_joint_layout.addWidget (self.horizontally_joint_label)
        self.horizontally_joint_layout.addWidget (self.horizontally_joint_spin_box)
        self.main_layout.addLayout (self.horizontally_joint_layout)

        # 添加创建定位按钮
        self.main_layout.addWidget (self.setup_btn)

        # 创建生成纵向定位的布局
        self.vertical_joint_layout = QHBoxLayout ()
        self.vertical_joint_layout.addWidget (self.vertical_joint_label)
        self.vertical_joint_layout.addWidget (self.vertical_joint_spin_box)
        self.main_layout.addLayout (self.vertical_joint_layout)

        # 添加创建绑定按钮
        self.main_layout.addWidget (self.build_btn)


    def create_connections (self) :
        self.setup_btn.clicked.connect (self.create_skirt_setup)


    def create_skirt_setup (self) :
        """
        创建生成裙子的绑定定位
        """
        # 获取需要生成的裙子的名称
        self.name = self.name_line.text ()

        # 获取需要生成的裙子的横向关节数量
        self.horizontally_joint_value = self.horizontally_joint_spin_box.value ()

        # 创建生成裙子所需要的层级组结构
        self.create_skirt_grp ()

        # 根据上下方位生成定位的曲线和曲面
        for place in ['Up' , 'Down'] :
            self.place_setup_curve = 'crv_m_{}{}_001'.format (self.name , place)
            # 如果定位的上曲线不存在于场景中的话，则正常创建曲线
            if not cmds.objExists (self.place_setup_curve) :
                print (1)
                self.place_setup_curve = cmds.circle (name = self.place_setup_curve , center = (0 , 5 , 0) ,
                                                      normal = (0 , 1 , 0) ,
                                                      sweep = 360 , radius = 1 , degree = 3 ,
                                                      useTolerance = 0 , tolerance = 0.01 ,
                                                      sections = self.horizontally_joint_value ,
                                                      ch = 1) [0]
                cmds.DeleteHistory (self.place_setup_curve)
                cmds.parent (self.place_setup_curve , self.skirt_nodes_world_grp)
                self.create_skirt_curve (place)

            # 如果定位的上曲线存在于场景中的话，则只重建曲线点数量
            else :
                # 删除wire的base节点
                cmds.delete (self.place_setup_curve + 'BaseWire')
                self.place_setup_curve = cmds.rebuildCurve (self.place_setup_curve , ch = 1 , rpo = 1 , rt = 0 ,
                                                            end = 1 , kr = 0 , kcp = 0 ,
                                                            kep = 1 ,
                                                            kt = 0 , spans = self.horizontally_joint_value , d = 3 ,
                                                            tol = 0.01) [0]
                self.create_skirt_curve (place)

        # 整理关节的层级结构
        down_bpjnt_list = cmds.ls ('bpjnt_m_*Down_*' , type = 'joint')
        for down_bpjnt in down_bpjnt_list :
            up_bpjnt = down_bpjnt.replace ('Down' , 'Up')
            cmds.parent (down_bpjnt , up_bpjnt)


    def create_skirt_curve (self , place) :
        """
        根据给定的方向和方位生成对应的曲线和曲面
        """
        # 根据上曲线创建用来钉毛囊的曲面
        # 判断需要放样的曲面是否存在，如果存在的话则只重建曲面，不存在的话则通过复制曲线进行放样曲面
        surf = 'surf_m_{}{}_001'.format (self.name , place)
        wire = 'wire_m_{}{}_001'.format (self.name , place)
        if not cmds.objExists (surf) :
            # 复制这条曲线
            temp_curve_01 = cmds.duplicate (self.place_setup_curve) [0]
            temp_curve_02 = cmds.duplicate (self.place_setup_curve) [0]
            # 移动两条曲线的位置来制作曲面
            cmds.setAttr (temp_curve_01 + '.translateY' , 0.1)
            cmds.setAttr (temp_curve_02 + '.translateY' , -0.1)
            # 放样曲面
            surf = \
                cmds.loft (temp_curve_01 , temp_curve_02 , constructionHistory = False , uniform = True , degree = 3 ,
                           sectionSpans = 1 ,
                           range = False , polygon = 0 ,
                           name = 'surf_m_{}{}_001'.format (self.name , place)) [0]
            cmds.parent (surf , self.skirt_nodes_world_grp)
            cmds.setAttr (surf + '.visibility' , 0)

            # 删除用来放样曲面的曲线
            cmds.delete (temp_curve_01 , temp_curve_02)
        else :
            cmds.delete (wire)
            surf = \
            cmds.rebuildSurface (surf , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kc = 0 , su = 1 ,
                                 du = 3 , sv = self.horizontally_joint_value , dv = 3 , tol = 0.01 , fr = 0 , dir = 2) [
                0]
        # 获得曲面的形状节点
        surf_shape = cmds.listRelatives (surf , shapes = True) [0]
        # 曲线对曲面进行wire控制，让曲线点移动的时候可以控制曲面点的移动
        wire_node = cmds.wire (surf , w = self.place_setup_curve , gw = False , en = 1.000000 , ce = 0.000000 ,
                               li = 0.000000 , name = wire) [0]
        cmds.setAttr (wire_node + '.dropoffDistance[0]' , 10000000)

        # 创建毛囊节点的总组
        self.fol_main_grp = cmds.createNode ('transform' ,
                                             name = 'grp_m_{}{}Follicles_001'.format (self.name , place) ,
                                             parent = self.skirt_nodes_local_grp)
        # 创建关节节点的总组
        self.bpjnt_main_grp = cmds.createNode ('transform' ,
                                               name = 'grp_m_{}{}Bpjnts_001'.format (self.name , place) ,
                                               parent = self.skirt_nodes_local_grp)
        # 根据需要生成的横向关节数量进行循环，对应创建对应的关节和毛囊节点
        for index in range (self.horizontally_joint_value) :
            # 创建关节并附着到曲面
            fol_grp = cmds.createNode ('transform' ,
                                       name = 'grp_m_{}{}Follicles_hor{:03d}_ver001'.format (self.name , place ,
                                                                                             index + 1) ,
                                       parent = self.fol_main_grp)
            cmds.setAttr (fol_grp + '.visibility' , 0)
            # 创建毛囊
            fol_shape = cmds.createNode ('follicle' , name = 'fol_m_{}{}_hor{:03d}Shape'.format (self.name , place ,
                                                                                                 index + 1))
            # 重命名毛囊的tran节点名称
            fol = cmds.listRelatives (fol_shape , parent = True) [0]
            fol = cmds.rename (fol , fol_shape [:-5])
            # 把毛囊放入对应的层级组
            cmds.parent (fol , fol_grp)
            # 连接毛囊属性
            cmds.connectAttr (surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
            # 连接毛囊的形状节点以进行变换
            cmds.connectAttr (fol_shape + '.outTranslate' , fol + '.translate')
            cmds.connectAttr (fol_shape + '.outRotate' , fol + '.rotate')
            # 设置uv值
            cmds.setAttr (fol_shape + '.parameterU' , 0.5)
            cmds.setAttr (fol_shape + '.parameterV' , float (index * (1 / self.horizontally_joint_value)))

            # 创建用来定位的bp关节
            bpjnt = cmds.createNode ('joint' ,
                                     name = 'bpjnt_m_{}{}_hor{:03d}_ver001'.format (self.name , place , index + 1) ,
                                     parent = self.bpjnt_main_grp)

            # 让对应的毛囊约束对应的关节点
            cmds.pointConstraint (fol , bpjnt , maintainOffset = False)
            # 设置关节的旋转值
            cmds.xform (bpjnt , rotation = [0 , float (index * (360 / self.horizontally_joint_value)) , 0] ,
                        worldSpace = True)


    def create_skirt_grp (self) :
        "创建裙子控制器对应的层级组"
        # 创建skirt所有节点的纵对应的层级组
        self.skirt_grp = 'grp_m_{}_001'.format (self.name)
        if not cmds.objExists (self.skirt_grp) :
            self.skirt_grp = cmds.createNode ('transform' ,
                                              name = 'grp_m_{}_001'.format (self.name))
        # 创建skirt控制器对应的层级组
        self.skirt_ctrl_grp = 'grp_m_{}Ctrls_001'.format (self.name)
        if not cmds.objExists (self.skirt_ctrl_grp) :
            self.skirt_ctrl_grp = cmds.createNode ('transform' ,
                                                   name = 'grp_m_{}Ctrls_001'.format (self.name) ,
                                                   parent = self.skirt_grp)
        # 创建skirt定位关节对应的层级组
        self.skirt_bpjnt_grp = 'grp_m_{}Bpjnts_001'.format (self.name)
        if not cmds.objExists (self.skirt_bpjnt_grp) :
            self.skirt_bpjnt_grp = cmds.createNode ('transform' ,
                                                    name = 'grp_m_{}Bpjnts_001'.format (self.name) ,
                                                    parent = self.skirt_grp)
        # 创建skirt蒙皮关节对应的层级组
        self.skirt_jnt_grp = 'grp_m_{}Jnts_001'.format (self.name)
        if not cmds.objExists (self.skirt_jnt_grp) :
            self.skirt_jnt_grp = cmds.createNode ('transform' ,
                                                  name = 'grp_m_{}Jnts_001'.format (self.name) ,
                                                  parent = self.skirt_grp)

        # 创建local节点的层级的层级组
        self.skirt_nodes_local_grp = 'grp_m_{}NodesLocal_001'.format (self.name)
        if not cmds.objExists (self.skirt_nodes_local_grp) :
            self.skirt_nodes_local_grp = cmds.createNode ('transform' ,
                                                          name = 'grp_m_{}NodesLocal_001'.format (self.name) ,
                                                          parent = self.skirt_grp)
        else :
            cmds.delete (self.skirt_nodes_local_grp)
            self.skirt_nodes_local_grp = cmds.createNode ('transform' ,
                                                          name = 'grp_m_{}NodesLocal_001'.format (self.name) ,
                                                          parent = self.skirt_grp)
        # 创建world节点的层级的层级组
        self.skirt_nodes_world_grp = 'grp_m_{}NodesWorld_001'.format (self.name)
        if not cmds.objExists (self.skirt_nodes_world_grp) :
            self.skirt_nodes_world_grp = cmds.createNode ('transform' ,
                                                          name = 'grp_m_{}NodesWorld_001'.format (self.name) ,
                                                          parent = self.skirt_grp)


def main () :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = Skirt_ctrl_tool ()
    ui.show ()


if __name__ == '__main__' :
    try :
        ui.close ()
        ui.deleteLater ()
    except :
        pass
    ui = Skirt_ctrl_tool ()
    ui.show ()
