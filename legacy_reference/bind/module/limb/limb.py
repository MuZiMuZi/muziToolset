# coding=utf-8
import os
from importlib import reload

import maya.cmds as cmds
import maya.mel as mel

from ..base import bone
from ..chain import chainIK , chainFK , chainIKFK
from ..limb import limbFK , limbIK
from ... import config
from ....core import hierarchyUtils , pipelineUtils , jointUtils , controlUtils


reload (hierarchyUtils)
reload (bone)
reload (chainIK)


class Limb (bone.Bone) :
    '''
    这段代码定义了一个名为`Limb`的类，它是`bone.Bone`类的子类。该类用于创建生物体的四肢或其他身体部位的模块化绑定系统。以下是对该类主要方法的中文解释：

    1. `__init__(self, side, name, jnt_number=3, limb_type='body', rig_type='limb', ikCtrl_value=False, fkCtrl_value=False, jnt_parent=None, ctrl_parent=None)`：初始化`Limb`对象的方法。参数包括侧边（'l'或'r'）、名称标识、关节数量、模块类型（'body'或'face'）、绑定类型（'arm'、'leg'、'spine'等等）、是否需要生成IK系统（ikCtrl_value）、是否需要生成FK系统（fkCtrl_value）、关节的父级（jnt_parent）和控制器的父级（ctrl_parent）。

    2. `_init_extra(self)`：根据IK和FK的控制器需求，初始化额外的绑定模块。根据`ikCtrl_value`判断是否需要创建IK控制模块，根据`fkCtrl_value`判断是否需要创建FK控制模块。

    3. `_create_base_namespace(self)`：创建绑定模块基础的命名空间。

    4. `_create_extra_namespace(self)`：创建绑定模块额外的命名空间。根据`ikCtrl_value`创建额外的IK控制的命名规范，根据`fkCtrl_value`创建额外的FK控制的命名规范，根据`is_ikfkCtrl`创建IKFK融合的命名规范。

    5. `_create_base_bpjnt(self)`：根据名称规范，创建基础的定位的bp关节，所有组件都需要用到的定位关节。

    6. `_import_base_bpjnt(self)`：根据给定的模块类型和绑定类型，导入基础定位关节。

    7. `_rename_base_bpjnt(self)`：根据给定的模块类型和绑定类型，修改定位关节组的名称。

    8. `_set_base_bpjnt(self)`：根据给定的参数，设置默认的定位关节的属性。

    9. `_create_extra_bpjnt(self)`：创建额外的定位关节。根据`ikCtrl_value`创建IK系统的定位关节，根据`fkCtrl_value`创建FK系统的定位关节。如果同时需要IK和FK系统，设置连接，让定位关节驱动IK和FK的关节链条。

    10. `_create_base_joint(self)`：根据bpjnt的位置，创建对应的关节吸附到对应位置，并且创建用来整理的集合。

    11. `_create_extra_joint(self)`：根据额外的定位关节来创建额外的模块关节。根据`ikCtrl_value`创建IK系统的关节，根据`fkCtrl_value`创建FK系统的关节。如果同时需要IK和FK系统，隐藏IK和FK系统的关节。

    12. `_create_ctrl_grp(self)`：创建控制器组。根据`ikCtrl_value`创建IK系统的控制器总组，根据`fkCtrl_value`创建FK系统的控制器总组。

    13. `_create_base_ctrl(self)`：创建基础控制器。

    14. `_create_extra_ctrl(self)`：创建额外的控制器。根据`ikCtrl_value`创建IK系统的基础控制器，根据`fkCtrl_value`创建FK系统的基础控制器。根据`is_ikfkCtrl`创建IKFK系统融合的控制器。

    15. `_create_ikfk_switch_ctrl(self)`：创建IKFK切换控制器。根据控制器工具类`controlUtils`创建带有IKFK切换属性的控制器。

    16. `_create_ctrl_hierarchy(self)`：整理控制器的层级结构。根据`ikCtrl_value`整理IK控制器组的层级结构，根据`fkCtrl_value`整理FK控制器组的层级结构。

    17. `_create_base_constraint(self)`：在基础的控制器与蒙皮关节之间创建连接。未提供具体实现。

    18. `_create_extra_constraint(self)`：在额外的控制器与额外的关节之间创建连接。根据`fkCtrl_value`创建FK系统的约束连接，根据`is_ikfkCtrl`创建IKFK系统融合的约束连接。

    19.

     `_create_ikfk_constraint(self, jnt_number)`：创建IKFK约束。使用`cmds.parentConstraint`创建IK关节链和FK关节链的约束，并将结果连接到IKFK关节链。

    20. `_set_ikfk_driven_keyframes(self, cons, jnt_number)`：连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条。使用`cmds.setDrivenKeyframe`设置IKFK切换属性值下的关键帧，以及对IK和FK关节链条的可见性进行关键帧设置。
    '''


    def __init__ (self , side , name , jnt_number = 3 , limb_type = 'body' , rig_type = 'limb' , ikCtrl_value = False ,
                  fkCtrl_value = False , jnt_parent = None ,
                  ctrl_parent = None) :
        """
        初始化 Limb 对象。

        Args:
            side (str): 侧边 ('l' 或 'r')。
            name (str): 名称标识。
            jnt_number (int): 关节的数量，默认为3。
            limb_type (str): 模块类型，可选('body' 或 'face')。
            rig_type (str): 绑定类型，可选。('arm','leg','spine'等等)
            ikCtrl_value(bool):判断是否需要生成ik系统
            fkCtrl_value(bool):判断是否需要生成fk系统
            jnt_parent (str): 关节的父级。
            ctrl_parent (str): 控制器的父级。

        Returns:
            None
        """
        # 调用父类的初始化方法
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)
        # 初始化参数，模块类型和绑定类型
        self.limb_type = limb_type
        self.rig_type = rig_type
        # 初始化self.ikCtrl_value，用来判断模块是否需要生成ik控制
        self.ikCtrl_value = ikCtrl_value
        # 初始化self.fkCtrl_value，用来判断模块是否需要生成fk控制
        self.fkCtrl_value = fkCtrl_value

        self.is_ikfkCtrl = False
        # 使用逻辑运算符 and 判断self.fkCtrl_value和self.ikCtrl_value的值是否都为1，如果都为1的情况则需要创建ikfk融合的控制
        if self.ikCtrl_value == True and self.fkCtrl_value == True :
            self.is_ikfkCtrl = True

        self.axis = 'X+'
        self.length = 10


    # 初始化额外的绑定模块
    def _init_extra (self) :
        '''
        初始化额外的绑定模块
        '''
        # 根据self.ikCtrl_value的值判断是否需要创建ik控制模块
        if self.ikCtrl_value :
            # 初始化 IK 系统
            self.ik_limb = limbIK.LimbIK (self.side , self.name , self.jnt_number , self.axis , self.length ,
                                          self.limb_type , self.rig_type , self.jnt_parent , self.ctrl_parent)
            self.ik_limb.rig_type = f"{self.rig_type}IK"
        # 根据self.fkCtrl_value的值判断是否需要创建fk控制模块
        if self.fkCtrl_value :
            # 初始化FK 系统
            self.fk_limb = limbFK.LimbFK (self.side , self.name , self.jnt_number , self.axis , self.length ,
                                          self.jnt_parent , self.ctrl_parent)
            self.fk_limb.rig_type = f"{self.rig_type}FK"


    # 创建绑定模块基础的命名规范
    def _create_base_namespace (self) :
        """
        创建绑定模块基础的命名规范

        Returns:
            None
        """
        # 调用父类的命名规范创建方法
        super ()._create_base_namespace ()


    # 创建绑定模块额外的命名规范
    def _create_extra_namespace (self) :
        """
        创建绑定模块额外的命名规范
        """
        if self.ikCtrl_value :
            # 创建额外的ik控制的命名规范
            self.ik_limb._create_base_namespace ()
            self.ik_limb._create_extra_namespace ()

        if self.fkCtrl_value :
            # 创建额外的fk控制的命名规范
            self.fk_limb._create_base_namespace ()
            self.fk_limb._create_extra_namespace ()

        # 判断self.is_ikfkCtrl是否存在，存在的话则需要创建ikfk融合的命名规范
        if self.is_ikfkCtrl :
            # 创建用于切换 IKFK 控制器的名称规范
            self.ctrl_ikfk_switch = 'ctrl_{}_{}{}IKFKSwitch_001'.format (self.side , self.name , self.rig_type)
            self.zero_ikfk_switch = 'zero_{}_{}{}IKFKSwitch_001'.format (self.side , self.name , self.rig_type)
            self.output_ikfk_switch = 'output_{}_{}{}IKFKSwitch_001'.format (self.side , self.name , self.rig_type)


    # 根据名称规范，创建基础的定位的bp关节,所有组件都需要用到的定位关节
    def _create_base_bpjnt (self) :
        '''
        根据名称规范，创建基础的定位的bp关节，所有组件都需要用到的定位关节

        Returns:
            None
        '''
        # 根据给定的模块类型和绑定类型，来导入基础定位关节。
        self._import_base_bpjnt ()

        # 根据给定的模块类型和绑定类型，修改定位关节组的名称。
        self._rename_base_bpjnt ()

        # 根据给定的参数，设置默认的定位关节的属性。
        self._set_base_bpjnt ()


    # 根据给定的模块类型和绑定类型，来导入基础定位关节。
    def _import_base_bpjnt (self) :
        """
        根据给定的模块类型和绑定类型，来导入基础定位关节。

        Returns:
            None
        """
        # 获得 base_bpjnt_path 的路径
        self.base_bpjnt_path = os.path.abspath (
            config.bpjnt_dir + "/{}_template_rig/{}_bpjnt.ma".format (self.limb_type , self.rig_type))

        # 导入关节
        cmds.file (self.base_bpjnt_path , i = True , rnn = True)


    # 根据给定的模块类型和绑定类型，修改定位关节组的名称。
    def _rename_base_bpjnt (self) :
        """
        根据给定的模块类型和绑定类型，修改定位关节组的名称。

        Returns:
            None
        """
        # 根据给定的模块类型和绑定类型，获取定位关节组的名称
        self.bpjnt_grp = 'grp_side_{}{}Bpjnt_001'.format (self.name , self.rig_type)

        # 选择定位关节组修改给定的关节命名
        cmds.select (self.bpjnt_grp , replace = True)
        mel.eval ('searchReplaceNames "side" "{}" "hierarchy"'.format (self.side))
        self.bpjnt_grp = 'grp_{}_{}{}Bpjnt_001'.format (self.side , self.name , self.rig_type)


    # 根据给定的参数，设置默认的定位关节的属性。
    def _set_base_bpjnt (self) :
        """
        根据给定的参数，设置默认的定位关节的属性。

        Returns:
            None
        """
        # 将定位关节添加到指定的set里
        # 获取所有的定位关节
        # self.bpjnt_list = hierarchyUtils.Hierarchy.get_child_object (object = self.bpjnt_grp ,
        #                                                              obj_type = 'joint')
        for self.bpjnt in self.bpjnt_list :
            # 给bp定位关节设置颜色方便识别
            cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
            cmds.setAttr (self.bpjnt + '.overrideColor' , 13)

            # 将bp关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (
                self.bpjnt ,
                set_name = 'set_{}_{}{}Bpjnt_001'.format (self.side , self.name , self.rig_type) ,
                set_parent = 'set_bpjnt'
            )
        # 根据获取的定位关节的边来设置定位关节的位置
        cmds.setAttr (self.bpjnt_list [0] + '.translateX' ,
                      cmds.getAttr (self.bpjnt_list [0] + '.translateX') * self.side_value)
        # 整理定位关节的层级结构到总定位关节组里
        hierarchyUtils.Hierarchy.parent (child_node = self.bpjnt_grp , parent_node = self.top_bpjnt_grp)


    # 创建额外的定位关节
    def _create_extra_bpjnt (self) :
        '''
        创建额外的定位关节
        '''
        # 根据self.ikCtrl_value的值创建ik系统的定位关节
        if self.ikCtrl_value :
            # 创建ik系统的定位关节
            self.ik_limb._create_base_bpjnt ()
            self.ik_limb._create_extra_bpjnt ()
            # 隐藏IK的定位关节，方便选择和调整位置
            cmds.setAttr (self.ik_limb.bpjnt_list [0] + '.visibility' , 0)
        # 根据self.fkCtrl_value的值判断是否需要创建fk系统的定位关节
        if self.fkCtrl_value :
            # 创建fk系统的定位关节
            self.fk_limb._create_base_bpjnt ()
            self.fk_limb._create_extra_bpjnt ()
            # 隐藏fK的定位关节，方便选择和调整位置
            cmds.setAttr (self.fk_limb.bpjnt_list [0] + '.visibility' , 0)

        if self.is_ikfkCtrl :
            # 设置连接，让定位关节驱动IK和FK的关节链条
            for bpjnt , ik_bpjnt , fk_bpjnt in zip (self.bpjnt_list , self.ik_limb.bpjnt_list ,
                                                    self.fk_limb.bpjnt_list) :
                cmds.parentConstraint (bpjnt , ik_bpjnt , mo = False)
                cmds.parentConstraint (bpjnt , fk_bpjnt , mo = False)


    # 根据定位关节的位置来创建基础的蒙皮关节
    def _create_base_joint (self) :
        """
        根据bpjnt的位置，创建对应的关节吸附到对应位置，并且创建用来整理的集合。

        对于每一个 bpjnt 和 jnt 的组合，调用 _create_and_attach_joint 函数，
        创建关节并将其吸附到对应位置。同时更新 jnt_parent 为当前创建的关节。

        Returns:
            None
        """
        # 遍历每一个 bpjnt 和 jnt 的组合
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            # 调用 _create_and_attach_joint 函数创建关节并吸附到对应位置
            self._create_and_attach_joint (bpjnt , jnt , parent = self.jnt_parent)
            # 更新 jnt_parent 为当前创建的关节
            self.jnt_parent = jnt


    # 根据额外的定位关节来创建额外的模块关节
    def _create_extra_joint (self) :
        '''
        根据额外的定位关节来创建额外的模块关节
        '''
        # 根据self.ikCtrl_value的值判断是否需要创建ik系统的关节
        if self.ikCtrl_value :
            # 创建ik系统的关节
            self.ik_limb._create_base_joint ()
            self.ik_limb._create_extra_joint ()
            # 隐藏ik系统的关节
            cmds.setAttr (self.ik_limb.jnt_list [0] + '.visibility' , 0)
        # 根据self.fkCtrl_value的值判断是否需要创建fk系统的关节
        if self.fkCtrl_value :
            # 创建fk系统的关节
            self.fk_limb._create_base_joint ()
            self.fk_limb._create_extra_joint ()
            # 隐藏fk系统的关节
            cmds.setAttr (self.fk_limb.jnt_list [0] + '.visibility' , 0)


    # 创建控制器组。
    def _create_ctrl_grp (self) :
        """
        创建控制器组。

        Returns:
            None
        """
        # 调用父类的控制器组创建方法
        super ()._create_ctrl_grp ()
        # 根据self.ikCtrl_value的值判断是否需要创建ik系统的控制器总组
        if self.ikCtrl_value :
            # 创建ik系统的控制器总组
            self.ik_limb._create_ctrl_grp ()
        # 根据self.fkCtrl_value的值判断是否需要创建fk系统的控制器总组
        if self.fkCtrl_value :
            # 创建fk系统的控制器总组
            self.fk_limb._create_ctrl_grp ()


    # 创建基础控制器。
    def _create_base_ctrl (self) :
        """
        创建基础控制器。

        Returns:
            None
        """
        pass


    # 创建额外的控制器
    def _create_extra_ctrl (self) :
        """
        创建额外的控制器
        Returns:
            None
        """
        # 调用父类的控制器组创建方法
        super ()._create_extra_ctrl ()
        # 根据self.ikCtrl_value的值判断是否需要创建IK系统的基础控制器
        if self.ikCtrl_value :
            # 创建IK系统的基础控制器
            self.ik_limb._create_base_ctrl ()
            self.ik_limb._create_extra_ctrl ()
        # 根据self.fkCtrl_value的值判断是否需要创建FK系统的基础控制器
        if self.fkCtrl_value :
            # 创建FK系统的基础控制器
            self.fk_limb._create_base_ctrl ()
            self.fk_limb._create_extra_ctrl ()

        # 根据self.is_ikfkCtrl的值判断是否需要创建ikfk系统融合的控制器
        if self.is_ikfkCtrl :
            # 创建IKFK切换控制器
            self._create_ikfk_switch_ctrl ()


    # 创建IKFK切换控制器。
    def _create_ikfk_switch_ctrl (self) :
        """
        创建IKFK切换控制器。

        Returns:
            None
        """
        # 使用Control工具类创建IKFK切换控制器
        self.ctrl_ikfk_switch = controlUtils.Control.create_ctrl (
            self.ctrl_ikfk_switch ,
            shape = 'pPlatonic' ,
            radius = self.radius * 1.2 ,
            axis = 'X+' ,
            pos = self.jnt_list [0] ,
            parent = self.ctrl_grp
        )

        # 设置IKFK切换控制器的位置
        cmds.setAttr (self.zero_ikfk_switch + '.translateZ' , -5)

        # 添加IKFK切换属性
        cmds.addAttr (self.ctrl_ikfk_switch , ln = 'ikfkSwitch' , at = 'double' , dv = 1 , min = 0 ,
                      max = 1 , k = 1)


    # 整理控制器的层级结构。
    def _create_ctrl_hierarchy (self) :
        """
        整理控制器的层级结构。

        Returns:
            None
        """
        # 调用父类 _create_ctrl_hierarchy 方法，创建控制器的层级结构
        super ()._create_ctrl_hierarchy ()

        # 根据self.ikCtrl_value的值判断是否需要整理ik控制器组的层级结构
        if self.ikCtrl_value :
            # 整理ik控制器组的层级结构
            hierarchyUtils.Hierarchy.parent (child_node = self.ik_limb.ctrl_grp , parent_node = self.ctrl_grp)
        # 根据self.fkCtrl_value的值判断是否需要整理fk控制器组的层级结构
        if self.fkCtrl_value :
            # 整理fk控制器组的层级结构
            hierarchyUtils.Hierarchy.parent (child_node = self.fk_limb.ctrl_grp , parent_node = self.ctrl_grp)


    # 在基础的控制器与蒙皮关节之间创建连接
    def _create_base_constraint (self) :
        """
        根据给定的控制器和关节创建基础的约束关系。

        对每个控制器和关节的组合调用 _create_controller_constraint 函数，创建约束关系。

        Returns:
            None
        """
        pass


    # 在额外的控制器与额外的关节之间创建连接
    def _create_extra_constraint (self) :
        '''
        在额外的控制器与额外的关节之间创建连接
        '''
        # ik系统的约束根据各模块自定义的设置添加

        # 根据self.fkCtrl_value的值判断是否需要创建FK系统的约束连接
        if self.fkCtrl_value :
            # 创建FK系统的约束连接
            self.fk_limb._create_base_constraint ()
            self.fk_limb._create_extra_constraint ()

        # 根据self.is_ikfkCtrl的值判断是否需要需要创建IKFK系统融合的约束连接
        if self.is_ikfkCtrl :
            # 创建IKFK约束。
            # 对IK关节链和FK关节链来约束IKFK关节链
            for jnt_number in range (self.jnt_number) :
                cons = self._create_ikfk_constraint (jnt_number)
                # 连接IKFK切换的属性以驱动关键帧来切换不同的关节链条
                self._set_ikfk_driven_keyframes (cons , jnt_number)


    # 创建IKFK约束。
    def _create_ikfk_constraint (self , jnt_number) :
        '''
        创建IKFK约束。

        步骤：
        1. 使用cmds.parentConstraint创建IK关节链的第jnt_number个关节和FK关节链的第jnt_number个关节的约束。
        2. 将约束结果连接到IKFK关节链的第jnt_number个关节。

        参数：
        - jnt_number (int): 要创建约束的关节的索引。

        返回：
        str: 创建的IKFK约束的名称。
        '''
        # 步骤1：使用cmds.parentConstraint创建IK关节链的第jnt_number个关节和FK关节链的第jnt_number个关节的约束
        cons = cmds.parentConstraint (
            self.ik_limb.jnt_list [jnt_number] ,
            self.fk_limb.jnt_list [jnt_number] ,
            self.jnt_list [jnt_number]
        ) [0]

        # 步骤2：将约束结果连接到IKFK关节链的第jnt_number个关节
        return cons


        # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条。


    # 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条。
    def _set_ikfk_driven_keyframes (self , cons , jnt_number) :
        '''
        连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条。

        步骤：
        1. 使用cmds.setDrivenKeyframe设置约束的权重，在不同的IKFK切换属性值下进行关键帧设置。
        2. 设置IK关节链条和IK控制器的可见性的关键帧。
        3. 设置FK关节链条和FK控制器的可见性的关键帧。

        参数：
        - cons (str): 创建的IKFK约束的名称。
        - jnt_number (int): 关节的索引。

        返回：
        无。
        '''
        # 步骤1：使用cmds.setDrivenKeyframe设置约束的权重，在不同的IKFK切换属性值下进行关键帧设置。
        cmds.setDrivenKeyframe ('{}.w0'.format (cons) , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' , dv = 1 , v = 1)
        cmds.setDrivenKeyframe ('{}.w1'.format (cons) , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' , dv = 1 , v = 0)
        cmds.setDrivenKeyframe ('{}.w0'.format (cons) , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' , dv = 0 , v = 0)
        cmds.setDrivenKeyframe ('{}.w1'.format (cons) , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' , dv = 0 , v = 1)

        # 步骤2：设置IK关节链条和IK控制器的可见性的关键帧。
        cmds.setDrivenKeyframe (self.ik_limb.ctrl_grp + '.v' , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' ,
                                dv = 1 , v = 1)
        cmds.setDrivenKeyframe (self.ik_limb.ctrl_grp + '.v' , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' ,
                                dv = 0 , v = 0)

        # 步骤3：设置FK关节链条和FK控制器的可见性的关键帧。
        cmds.setDrivenKeyframe (self.fk_limb.ctrl_grp + '.v' , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' ,
                                dv = 0 , v = 1)
        cmds.setDrivenKeyframe (self.fk_limb.ctrl_grp + '.v' , cd = self.ctrl_ikfk_switch + '.ikfkSwitch' ,
                                dv = 1 , v = 0)
