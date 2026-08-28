
class Joint_Resampling (QDialog) :
    """
    关节重采样工具的页面编写
    """


    def __init__ (self , parent = qtUtils.get_maya_window ()) :
        super (Joint_Resampling , self).__init__ (parent)
        self.setWindowTitle ("关节重采样工具")
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        # 在start_layout里面添加控件
        self.start_label = QLabel ('startJoint:')
        self.start_line = QLineEdit ()
        self.start_pick_btn = QPushButton ('拾取起始关节')

        # 在end_layout里面添加控件
        self.end_label = QLabel ('endJoint:')
        self.end_line = QLineEdit ()
        self.end_pick_btn = QPushButton ('拾取末端关节')

        # 在jnt_number_layout 里面添加控件
        self.jnt_number_label = QLabel ('jnt_number:')
        self.jnt_number_spine = QSpinBox ()
        self.jnt_number_spine.setValue (2)

        #
        self.resample_btn = QPushButton ('resample')


    def create_layouts (self) :
        # 添加页面布局
        self.start_layout = QHBoxLayout ()
        self.start_layout.addWidget (self.start_label)
        self.start_layout.addWidget (self.start_line)
        self.start_layout.addWidget (self.start_pick_btn)

        self.end_layout = QHBoxLayout ()
        self.end_layout.addWidget (self.end_label)
        self.end_layout.addWidget (self.end_line)
        self.end_layout.addWidget (self.end_pick_btn)

        self.joint_layout = QHBoxLayout ()
        self.joint_layout.addWidget (self.jnt_number_label)
        self.joint_layout.addWidget (self.jnt_number_spine)
        self.joint_layout.addStretch ()

        self.main_layout = QVBoxLayout (self)

        self.main_layout.addLayout (self.start_layout)
        self.main_layout.addLayout (self.end_layout)
        self.main_layout.addLayout (self.joint_layout)
        self.main_layout.addWidget (self.resample_btn)


    def create_connections (self) :
        self.start_pick_btn.clicked.connect (self.pick_startJoint_line)
        self.end_pick_btn.clicked.connect (self.pick_endJoint_line)

        self.resample_btn.clicked.connect (self.clicked_resample_btn)


    # 拾取起始关节
    def pick_startJoint_line (self) :
        """
        拾取起始关节
        """
        startJoint = cmds.ls (sl = True , type = 'joint')
        if len (startJoint) != 1 :
            cmds.warning ("选择数量不正确，请只选择一个关节作为关节重采样的起始关节: {}".format (startJoint))
            return
        else :
            self.start_line.setText (startJoint [0])
            cmds.warning ("设定了{}为关节重采样的起始关节 ".format (startJoint [0]))


    # 拾取末端关节
    def pick_endJoint_line (self) :
        """
                拾取末端关节
                """
        endJoint = cmds.ls (sl = True , type = 'joint')
        if len (endJoint) != 1 :
            cmds.warning ("选择数量不正确，请只选择一个关节作为关节重采样的末端关节: {}".format (endJoint))
            return
        else :
            self.end_line.setText (endJoint [0])
            cmds.warning ("设定了{}为关节重采样的末端关节 ".format (endJoint [0]))


    def clicked_resample_btn (self) :
        startJoint = self.start_line.text ()
        endJoint = self.end_line.text ()
        jnt_number = self.jnt_number_spine.value ()

        Joint.resample_joint (startJoint , endJoint , jnt_number)


# 关节重采样工具
@staticmethod
def create_more_joint () :
    """
    关节重采样工具
    """
    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Joint_Resampling ()  # 创建实例
    window.show ()  # 显示窗口


# 关节重采样，选择起始关节和末端关节，在二者中间重新构建指定数量的关节链条
@staticmethod
def resample_joint (startJoint , endJoint , jnt_number) :
    """
    关节重采样，选择起始关节和末端关节，在二者中间重新构建指定数量的关节链条
    startJoint(str):起始关节
    endJoint(str):末端关节
    jnt_number(int)：指定数量的关节链条
    """
    jnt_parent = startJoint
    # 获取起始关节与末端关节之间的距离
    try :
        cmds.parent (endJoint , startJoint)
    except :
        pass
    tx_value = cmds.getAttr (endJoint + '.translateX') / jnt_number
    cmds.parent (endJoint , world = True)
    cmds.delete (cmds.listRelatives (startJoint , children = True))
    # 根据指定的关节数量，循环创建对应的关节
    for index in range (jnt_number) :
        jnt = cmds.createNode ('joint' , name = startJoint + '_{:03d}'.format (index))
        cmds.matchTransform (jnt , startJoint)
        cmds.parent (jnt , jnt_parent)
        cmds.setAttr (jnt + '.translateX' , tx_value)
        jnt_parent = jnt
    cmds.parent (endJoint , startJoint + '_{:03d}'.format (jnt_number - 1))
