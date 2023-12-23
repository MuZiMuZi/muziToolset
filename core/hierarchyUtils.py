# coding=utf-8
import maya.cmds as cmds


u"""
hierarchyUtils：这是一个用来对层级结构进行修改的类

目前已有的功能：

parent：查找子物体和父物体之间是否有父子层级关系
add_extra_group：在对象上方添加一个额外的组.
control_hierarchy:做控制器的层级结构
get_child_object:获取对象的所有子物体包括对象本身
"""


class Hierarchy (object) :

    #先查找子物体和父物体之间是否有父子层级关系，没有的话制作父子层级关系
    @staticmethod
    def parent (child_node , parent_node) :
        u"""
        先查找子物体和父物体之间是否有父子层级关系，没有的话制作父子层级关系
        :param child_node（str）:子物体的节点名称
        :param parent_nodestr）:父物体的节点名称
        :return:
        """
        if parent_node :
            parent_original = cmds.listRelatives (child_node , parent = True)
            if not parent_original or parent_original [0] != parent_node :
                cmds.parent (child_node , parent_node)
            else :
                cmds.warning (u'{} 已为 {}的子物体'.format (child_node , parent_node))
        else :
            cmds.warning (u'没有给定父物体节点')

    #在对象上方添加一个额外的组.
    @staticmethod
    def add_extra_group (obj , grp_name , world_orient = False) :
        u"""在对象上方添加一个额外的组.

        Args:
            obj (str):要添加额外组的Maya对象.
            grp_name (str): 额外的组名
            world_orient (bool): 设置新组的世界位置是否改变。

        Returns:
            str: 新添加的组.

        """

        obj_grp = cmds.group (name = grp_name , empty = True)
        t_pos = cmds.xform (obj , query = True , worldSpace = True , translation = True)
        r_pos = cmds.xform (obj , query = True , worldSpace = True , rotation = True)
        if world_orient :
            r_pos = [0 , 0 , 0]
        s_pos = cmds.xform (obj , q = True , worldSpace = True , s = True)
        cmds.xform (obj_grp , s = s_pos)
        cmds.xform (obj_grp , ws = True , t = t_pos)
        cmds.xform (obj_grp , ws = True , ro = r_pos)

        obj_parent = cmds.listRelatives (obj , parent = True)
        if obj_parent :
            cmds.parent (obj_grp , obj_parent [0] , absolute = True)
            cmds.parent (obj , obj_grp , absolute = True)
        else :
            cmds.parent (obj , obj_grp , absolute = True)

        return obj_grp

    #自定义的预设控制器打组
    @staticmethod
    def control_hierarchy () :
        """Add an upper level group to the controller.

            The naming convention is
            Type_Side_describe_index

            """
        CTRL_COLORS = {
            'm' : 17 ,
            'l' : 6 ,
            'r' : 13
        }

        SUB_COLORS = {
            'm' : 25 ,
            'l' : 15 ,
            'r' : 4
        }

        # get selected nurbs curve as controller
        ctrls = cmds.ls (selection = True)

        # loop in each ctrl and create hierarchy
        for ctrl in ctrls :
            # get name parts
            name_parts = ctrl.split ('_')

            # create zero group
            zero = cmds.createNode ('transform' , name = ctrl.replace ('ctrl_' , 'zero_'))
            # create driven group
            driven = cmds.createNode ('transform' , name = ctrl.replace ('ctrl_' , 'driven_') , parent = zero)
            # create connect group
            connect = cmds.createNode ('transform' , name = ctrl.replace ('ctrl_' , 'connect_') , parent = driven)
            # create offset group
            offset = cmds.createNode ('transform' , name = ctrl.replace ('ctrl_' , 'offset_') , parent = connect)

            # snap to control position
            cmds.matchTransform (zero , ctrl , position = True , rotation = True)

            # parent control to offset group
            cmds.parent (ctrl , offset)

            # freeze transformation for controller
            cmds.makeIdentity (ctrl , apply = True , translate = True , rotate = True , scale = True)
            # delete history
            cmds.select (ctrl)
            cmds.DeleteHistory ()

            # duplicate ctrl as sub control
            sub = cmds.duplicate (ctrl , name = ctrl.replace (name_parts [2] , name_parts [2] + 'Sub')) [0]
            cmds.parent (sub , ctrl)
            cmds.setAttr (sub + '.scale' , 0.5 , 0.5 , 0.5)
            cmds.makeIdentity (sub , apply = True , scale = True)

            # create output group
            output = cmds.createNode ('transform' , name = ctrl.replace ('ctrl_' , 'output_') , parent = ctrl)

            # connect attrs
            cmds.connectAttr (sub + '.translate' , output + '.translate')
            cmds.connectAttr (sub + '.rotate' , output + '.rotate')
            cmds.connectAttr (sub + '.scale' , output + '.scale')
            cmds.connectAttr (sub + '.rotateOrder' , output + '.rotateOrder')

            # show rotate order
            cmds.setAttr (ctrl + '.rotateOrder' , channelBox = True)
            cmds.setAttr (sub + '.rotateOrder' , channelBox = True)

            # add sub vis attr
            cmds.addAttr (ctrl , longName = 'subCtrlVis' , attributeType = 'bool')
            cmds.setAttr (ctrl + '.subCtrlVis' , channelBox = True)

            # connect sub vis
            cmds.connectAttr (ctrl + '.subCtrlVis' , sub + '.visibility')
            # set color
            for ctrl_node , col_idx in zip ([ctrl , sub] ,
                                            [CTRL_COLORS [name_parts [1]] , SUB_COLORS [name_parts [1]]]) :
                # get shape node
                shape_node = cmds.listRelatives (ctrl_node , shapes = True) [0]
            # set color
            cmds.setAttr(shape_node + '.overrideEnabled', 1)
            cmds.setAttr(shape_node + '.overrideColor', col_idx)


    # 获取对象的所有子物体包括对象本身,可以指定需要获取的对象类型
    @staticmethod
    def get_child_object (object,type = 'joint') :
        u'''
        获取对象的所有子物体包括对象本身
        :param object: 需要获取所有子物体的对象
        type（str）:需要获取对象的类型
        return: 所有子物体的名称列表
        '''
        object_list = cmds.listRelatives (object , type = type,children = True , allDescendents = True)
        object_list.append (object)
        object_list.reverse ()
        return object_list


    # 快速选择所选择物体的所有子对象的类型,将所有选择的对象名称返回出去方便其他函数调用
    @staticmethod
    def select_sub_objects (obj_type = 'transform') :
        u'''
        快速选择所选择物体的所有子对象,将所有选择的对象名称返回出去方便其他函数调用
        obj_type（type）:需要选择的物体的子对象的类型，比如'transform','joint'
        '''
        selection = cmds.ls (sl = True)  # 获取选择的所有对象
        for obj in selection :
            cmds.select (obj , add = True)
            cmds.select (cmds.listRelatives (obj , allDescendents = True , type = obj_type) , add = True)
        selection = cmds.ls (sl = True)  # 获取选择的所有对象
        return selection


    # 创建绑定的默认层级组
    @staticmethod
    def create_rig_grp () :
        """
        创建绑定的默认层级组
        """
        top_main_group = 'grp_m_group_001'
        top_bpjnt_grp = 'grp_m_bpjnt_001'
        top_ctrl_grp = 'grp_m_control_001'
        top_jnt_grp = 'grp_m_jnt_001'
        top_mesh_grp = 'grp_m_mesh_001'
        top_node_grp = 'grp_m_node_001'

        for grp in [top_main_group , top_bpjnt_grp , top_ctrl_grp , top_jnt_grp , top_mesh_grp , top_node_grp] :
            if not cmds.ls (grp) :
                cmds.group (em = 1 , name = grp)

        cmds.parent (top_bpjnt_grp , top_ctrl_grp , top_jnt_grp , top_mesh_grp , top_node_grp , top_main_group)

        return top_bpjnt_grp , top_ctrl_grp , top_jnt_grp , top_mesh_grp , top_node_grp , top_main_group


    # 添加绑定的初始层级组，并隐藏连接对应的属性
    @staticmethod
    def create_default_grp () :
        u'''
        添加绑定的初始层级组，并隐藏连接对应的属性
        '''
        # 创建顶层的Group组
        Group = cmds.createNode ('transform' , name = 'Group')

        # 创建Group层级下的子层级组，并做层级关系
        Geometry = cmds.createNode ('transform' , name = 'Geometry')
        Control = cmds.createNode ('transform' , name = 'Control')
        Custom = cmds.createNode ('transform' , name = 'Custom')
        cmds.parent (Geometry , Custom , Control , Group)

        # 创建RigNode层级下的子层级组并做层级关系
        RigNodes = cmds.createNode ('transform' , name = 'RigNodes')
        Joints = cmds.createNode ('transform' , name = 'Joints')
        RigNodes_Local = cmds.createNode ('transform' , name = 'RigNodesLocal')
        RigNodes_World = cmds.createNode ('transform' , name = 'RigNodesWorld')
        nCloth_geo_grp = cmds.createNode ('transform' , name = 'nCloth_geo_grp')
        cmds.parent (RigNodes_Local , RigNodes_World , RigNodes)
        cmds.parent (RigNodes , Joints , nCloth_geo_grp , Custom)

        # 创建Modle层级下的子层级组并且做层级关系
        Low_modle_grp = cmds.createNode ('transform' , name = 'grp_m_low_Modle_001')
        Mid_modle_grp = cmds.createNode ('transform' , name = 'grp_m_mid_Modle_001')
        High_modle_grp = cmds.createNode ('transform' , name = 'grp_m_high_Modle_001')
        cmds.parent (Low_modle_grp , Mid_modle_grp , High_modle_grp , Geometry)

        World_zero = [Group , Geometry , RigNodes_Local , RigNodes_World , RigNodes , Control , Joints , Custom]
        attrs_list = ['.translateX' , '.translateY' , '.translateZ' , '.rotateX' , '.rotateY' , '.rotateZ' ,
                      '.scaleX' ,
                      '.scaleY' ,
                      '.scaleZ' , '.visibility' , '.rotateOrder' , '.subCtrlVis']
        rig_top_grp = 'Group'
        if not cmds.objExists (rig_top_grp) :
            selections = cmds.ls (sl = True)
            if selections :
                rig_top_grp = selections [0]

        # 创建总控制器Character
        character_ctrl_obj = controlUtils.Control.create_ctrl ('ctrl_m_Character_001' , shape = 'circle' , radius = 10 ,
                                                               axis = 'X+' ,
                                                               pos = None ,
                                                               parent = Control)

        # 创建世界控制器
        world_ctrl_obj = controlUtils.Control.create_ctrl ('ctrl_m_world_001' , shape = 'local' , radius = 8 ,
                                                           axis = 'Z-' ,
                                                           pos = None ,
                                                           parent = 'ctrl_m_Character_001')

        cog_ctrl_obj = controlUtils.Control.create_ctrl ('ctrl_m_cog_001' , shape = 'circle' , radius = 3 ,
                                                         axis = 'X+' ,
                                                         pos = None ,
                                                         parent = 'output_m_world_001')

        # 创建一个自定义的控制器，用来承载自定义的属性
        lock_ctrl_obj = controlUtils.Control.create_ctrl ('ctrl_m_custom_001' , shape = 'cross' , radius = 3 ,
                                                          axis = 'X+' ,
                                                          pos = None ,
                                                          parent = Custom)
        lock_ctrl = 'ctrl_m_custom_001'
        cmds.parentConstraint ('ctrl_m_Character_001' , lock_ctrl , mo = True)
        cmds.scaleConstraint ('ctrl_m_Character_001' , lock_ctrl , mo = True)

        # 创建自定义的控制器属性
        for attr in ['GeometryVis' , 'ControlsVis' , 'RigNodesVis' , 'JointsVis'] :
            if not cmds.objExists ('{}.{}'.format (lock_ctrl , attr)) :
                cmds.addAttr (lock_ctrl , ln = attr , at = 'bool' , dv = 1 , keyable = True)

        # 添加精度切换的属性
        if not cmds.objExists ('{}.Resolution'.format (lock_ctrl)) :
            cmds.addAttr (lock_ctrl , ln = 'Resolution' , at = 'enum' , en = 'low:mid:high' , keyable = True)
            for idx , res in {0 : 'low' , 1 : 'mid' , 2 : 'high'}.items () :
                cnd_node = 'resolution_{}_conditionNode'.format (res)
                if not cmds.objExists (cnd_node) :
                    cnd_node = cmds.createNode ('condition' , n = cnd_node)
                cmds.connectAttr ('{}.Resolution'.format (lock_ctrl) , '{}.firstTerm'.format (cnd_node) , f = True)
                cmds.setAttr ('{}.secondTerm'.format (cnd_node) , idx)
                cmds.setAttr ('{}.colorIfTrueR'.format (cnd_node) , 1)
                cmds.setAttr ('{}.colorIfFalseR'.format (cnd_node) , 0)
                cmds.connectAttr ('{}.outColorR'.format (cnd_node) , 'grp_m_{}_Modle_001.visibility'.format (res) ,
                                  f = True)

        # 添加模型显示方式的属性
        if not cmds.objExists ('{}.GeometryDisplayType'.format (lock_ctrl)) :
            cmds.addAttr (lock_ctrl , ln = 'GeometryDisplayType' , at = 'enum' , en = 'Normal:Template:Reference' ,
                          keyable = True)

        # 连接 GeometryVis
        cmds.connectAttr ('{}.GeometryVis'.format (lock_ctrl) , '{}.visibility'.format (Geometry) , f = True)

        # 连接 controlsVis
        cmds.connectAttr ('{}.ControlsVis'.format (lock_ctrl) , '{}.visibility'.format (Control) , f = True)

        # 连接 RigNodesVis
        cmds.connectAttr ('{}.RigNodesVis'.format (lock_ctrl) , '{}.visibility'.format (RigNodes) , f = True)

        # 连接 jointsVis
        cmds.connectAttr ('{}.JointsVis'.format (lock_ctrl) , '{}.visibility'.format (Joints) , f = True)

        # 连接模型的可编辑属性
        cmds.setAttr (Geometry + '.overrideDisplayType' , 2)
        cmds.connectAttr ('{}.GeometryDisplayType'.format (lock_ctrl) , Geometry + '.overrideEnabled' , f = True)

        # 显示和隐藏属性
        for attr in attrs_list :
            cmds.setAttr (lock_ctrl + attr , l = True , k = False , cb = False)

        return {
            'Geometry' : Geometry ,
            'Control' : Control ,
            'RigNodes' : RigNodes ,
            'Joints' : Joints ,
            'RigNodes_Local' : RigNodes_Local ,
            'RigNodes_World' : RigNodes_World ,
            'nCloth_geo_grp' : nCloth_geo_grp
        }
