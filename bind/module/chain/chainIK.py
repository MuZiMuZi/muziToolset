from importlib import reload

import maya.cmds as cmds

from . import chain
from ....core import vectorUtils


reload (chain)


class ChainIK (chain.Chain) :
    rigType = 'ChainIK'


    def __init__ (self , side , name , jnt_number , direction , length = 10 , is_stretch = 1 , jnt_parent = None ,
                  ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , length , jnt_parent , ctrl_parent)
        u"""
        用来创建ik关节Spline链条的绑定
        length(int)：关节的总长度
        direction（list）:从根节点到顶部节点的方向例如[1,0,0]或者[0,1,0]
        is_stretch(bool):是否允许ik关节链条进行拉伸
        """

        self.interval = length / (self.jnt_number - 1)
        self.direction = list (vectorUtils.Vector (direction).mult_interval (self.interval))
        self.is_stretch = is_stretch

        self.set_shape ('ball')
        self.radius = 1
        self.axis = vectorUtils.Vector (direction).axis


    def create_namespace (self) :
        u'''
        创建ik绑定系统的命名规范
        '''
        super ().create_namespace ()
        # 根据给定的边，名称和jnt_number生成列表来存储创建的名称
        self.cluster_list = list ()
        self.ik_curve = None
        self.ik_handle = None
        for i in range (self.jnt_number) :
            self.cluster_list.append ('cluster_{}_{}{}_{:03d}'.format (self.side , self.name , self.rigType , i + 1))

        self.ik_curve = ('curve_{}_{}{}_001'.format (self.side , self.name , self.rigType))
        self.ik_handle = ('handle_{}_{}{}_001'.format (self.side , self.name , self.rigType))


    def build_ikSpline (self) :
        u'''
        创建ikSpline的绑定系统
        '''

        # 创建ikSplineSolverHandle,选择自动创建曲线，防止出现关节位置的偏移
        cmds.ikHandle (sj = self.jnt_list [0] ,
                       ee = self.jnt_list [-1] ,
                       n = self.ik_handle , scv = False , sol = 'ikSplineSolver')
        # 获取ikhandle的输入曲线
        self.ik_curve = self._get_ikhandle_curve ()
        cmds.setAttr (self.ik_curve + '.v' , 0)

        # inherit变换将导致曲线移动/缩放两倍
        cmds.inheritTransform (self.ik_curve , off = 1)
        cmds.parent (self.ik_curve , self.ctrl_parent)

        # 选择self.ik_curve曲线上所有点来创建cluster
        cvs = cmds.ls (self.ik_curve + '.cv[0:]' , fl = 1)
        # 去掉第二个点和倒数第二个点，第二个点和倒数第二个曲线点是用来平滑曲线的，并不用来设置关节点位置
        modified_curve_cvs = cvs [:1] + cvs [2 :-2] + cvs [-1 :]

        # 从self.ik_curve第二个点和倒数第二个点后的列表里创建cluster用来控制曲线的位置
        for jnt_number , cv in enumerate (modified_curve_cvs) :
            cluster = cmds.cluster (cv , n = self.cluster_list [jnt_number]) [-1]
            cmds.parent (cluster , self.ctrl_parent)
            cmds.setAttr (cluster + '.v' , 0)

        cmds.setAttr (self.ik_handle + '.v' , 0)
        cmds.parent (self.ik_handle , self.ik_curve , self.ctrl_grp)


    # 获取ikhandle的输入曲线
    def _get_ikhandle_curve (self) :
        """

        """
        # 获取 IK Spline Handle 的输入曲线
        input_curve = cmds.ikHandle (self.ik_handle , q = True , c = True)

        # 获取曲线的选择集
        curve_selection = cmds.ls (input_curve , type = 'nurbsCurve')

        # 检查是否找到了曲线
        if curve_selection :
            # 获取曲线的变换节点
            curve_transform = cmds.listRelatives (curve_selection [0] , parent = True) [0]
            # 修改重命名ik输入曲线的名称为
            cmds.rename (curve_transform , self.ik_curve)

        else :
            print ("创建｛｝不成功，没有找到对应的输入曲线".format (self.ik_handle))

        return self.ik_curve


    def add_constraint (self) :
        """
        使用对应的控制器来约束对应的关节，并且添加ikSpline绑定系统和添加拉伸
        """

        # 添加ikspline绑定系统
        self.build_ikSpline ()

        # 将创建好的cluster 放到对应的控制器层级组下
        for jnt_number , cluster in enumerate (self.cluster_list) :
            cmds.parent (cluster + 'Handle' , self.ctrl_list [jnt_number])

        # 启用ikhandle的高级扭曲控制
        cmds.setAttr (self.ik_handle + '.dTwistControlEnable' , 1)
        cmds.setAttr (self.ik_handle + '.dWorldUpType' , 4)
        cmds.connectAttr (
            self.ctrl_list [0] + '.worldMatrix[0]' ,
            self.ik_handle + '.dWorldUpMatrix' , force = 1)
        cmds.connectAttr (
            self.ctrl_list [-1] + '.worldMatrix[0]' ,
            self.ik_handle + '.dWorldUpMatrixEnd' , force = 1)

        # 判断是否需要添加拉伸功能
        if not self.is_stretch :
            return
        else :
            self.add_stretch ()


    def add_stretch (self) :
        u"""
        添加拉伸功能
        """

        # 设置中间的cluster的权重
        for jnt_number , driven in enumerate (self.driven_list) :
            if self.ctrl_list [jnt_number] not in [self.ctrl_list [0] , self.ctrl_list [-1]] :
                weight = (1.00 / (self.jnt_number - 1)) * jnt_number
                cmds.pointConstraint (self.ctrl_list [-1] , driven , w = weight , mo = 1)
                cmds.pointConstraint (self.ctrl_list [0] , driven , w = 1 - weight , mo = 1)
        #
        # 设置脊椎的缩放功能
        # 打开曲线的构造历史记录
        arc_len = cmds.arclen (self.ik_curve , constructionHistory = 1)
        ik_info = self.ik_curve.replace ('curve' , 'info')
        cmds.rename (arc_len , ik_info)
        cmds.parent (self.ik_curve , self.ctrl_parent)
        cmds.setAttr (self.ik_curve + '.v' , 0)

        # 获取曲线的长度，并且创建相乘节点来链接关节的缩放
        init_len = cmds.getAttr ('{}.arcLength'.format (ik_info))
        stretch_node = cmds.shadingNode (
            'multiplyDivide' ,
            asUtility = 1 ,
            n = self.ctrl_list [0].replace ('ctrl' , 'div'))
        cmds.setAttr (stretch_node + '.operation' , 2)
        cmds.setAttr (stretch_node + '.input2X' , init_len)
        cmds.connectAttr ('{}.arcLength'.format (ik_info) , stretch_node + '.input1X')

        # 将曲线缩放的倍数连接回来链接关节的缩放
        for i in range (self.jnt_number) :
            mult_node = cmds.createNode ('multDoubleLinear' , name = self.jnt_list [i].replace (' jnt' , 'mult'))
            tx_value = cmds.getAttr (self.jnt_list [i] + '.translateX')
            cmds.setAttr (mult_node + '.input2' , tx_value)
            cmds.connectAttr (stretch_node + '.outputX' , mult_node + '.input1')
            cmds.connectAttr (mult_node + '.output' , self.jnt_list [i] + '.translateX')


if __name__ == '__main__' :
    def x () :
        custom = chainIK.ChainIK (side = 'l' , name = 'zz' , jnt_number = 5 , direction = [1 , 0 , 0] ,
                                  jnt_parent = None , ctrl_parent = None)
        custom.build_setup ()


    def y () :
        custom = chainIK.ChainIK (side = 'l' , name = 'zz' , jnt_number = 5 , direction = [1 , 0 , 0] ,
                                  jnt_parent = None , ctrl_parent = None)
        custom.build_rig ()


    x ()
    y ()
