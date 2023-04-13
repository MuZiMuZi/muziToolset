def create_hand_rig(self) :
    u"""
    创建手指的FK绑定控制系统
    """
    hand_jnt = 'jnt_l_wristBind_001'
    hand_jnt_mirror = 'jnt_r_wristBind_001'
    hand_ctrl_grp = cmds.createNode('transform' , name = 'grp_l_handCtrl_001')
    hand_jnt_grp = cmds.createNode('transform' , name = 'grp_l_handJnt_001')
    hand_ctrl_grp_mirror = cmds.createNode('transform' , name = 'grp_r_handCtrl_001')
    hand_jnt_grp_mirror = cmds.createNode('transform' , name = 'grp_r_handJnt_001')
    cmds.parent(hand_jnt_grp , hand_jnt_grp_mirror , self.joint)
    cmds.parent(hand_ctrl_grp , hand_ctrl_grp_mirror , self.cog_ctrl)
    cmds.parentConstraint(hand_jnt , hand_ctrl_grp)
    cmds.parentConstraint(hand_jnt_mirror , hand_ctrl_grp_mirror)

    # 获取手指各模块的bp关节
    thumbHand_bp_joints = self.get_modular_bp_joints('thumbHand_rig')
    indexHand_bp_joints = self.get_modular_bp_joints('indexHand_rig')
    middleHand_bp_joints = self.get_modular_bp_joints('middleHand_rig')
    ringHand_bp_joints = self.get_modular_bp_joints('ringHand_rig')
    pinkyHand_bp_joints = self.get_modular_bp_joints('pinkyHand_rig')

    # 创建手指各模块的FK关节链
    thumbHand_fk_chain = jointUtils.Joint.create_chain(thumbHand_bp_joints , suffix = 'Bind' ,
                                                       joint_parent = hand_jnt_grp)
    thumbHand_fk_chain_mirror = cmds.mirrorJoint(thumbHand_fk_chain[0] , mirrorYZ = True , mirrorBehavior = True ,
                                                 searchReplace = ['_l_' , '_r_'])
    indexHand_fk_chain = jointUtils.Joint.create_chain(indexHand_bp_joints , suffix = 'Bind' ,
                                                       joint_parent = hand_jnt_grp)
    indexHand_fk_chain_mirror = cmds.mirrorJoint(indexHand_fk_chain[0] , mirrorYZ = True , mirrorBehavior = True ,
                                                 searchReplace = ['_l_' , '_r_'])
    middleHand_fk_chain = jointUtils.Joint.create_chain(middleHand_bp_joints , suffix = 'Bind' ,
                                                        joint_parent = hand_jnt_grp)
    middleHand_fk_chain_mirror = cmds.mirrorJoint(middleHand_fk_chain[0] , mirrorYZ = True , mirrorBehavior = True ,
                                                  searchReplace = ['_l_' , '_r_'])
    ringHand_fk_chain = jointUtils.Joint.create_chain(ringHand_bp_joints , suffix = 'Bind' ,
                                                      joint_parent = hand_jnt_grp)
    ringHand_fk_chain_mirror = cmds.mirrorJoint(ringHand_fk_chain[0] , mirrorYZ = True , mirrorBehavior = True ,
                                                searchReplace = ['_l_' , '_r_'])
    pinkyHand_fk_chain = jointUtils.Joint.create_chain(pinkyHand_bp_joints , suffix = 'Bind' ,
                                                       joint_parent = hand_jnt_grp)
    pinkyHand_fk_chain_mirror = cmds.mirrorJoint(pinkyHand_fk_chain[0] , mirrorYZ = True , mirrorBehavior = True ,
                                                 searchReplace = ['_l_' , '_r_'])
    # 根据手指各模块的FK关节链创建FK控制器
    fk_chains = [thumbHand_fk_chain , indexHand_fk_chain , middleHand_fk_chain , ringHand_fk_chain ,
                 pinkyHand_fk_chain]
    for fk_chain in fk_chains :
        self.fk_chain_rig(fk_chain , control_parent = hand_ctrl_grp)
        cmds.setAttr(fk_chain[0] + '.visibility' , 1)
    fk_chains_mirror = [thumbHand_fk_chain_mirror , indexHand_fk_chain_mirror , middleHand_fk_chain_mirror ,
                        ringHand_fk_chain_mirror ,
                        pinkyHand_fk_chain_mirror]
    for fk_chain_mirror in fk_chains_mirror :
        self.fk_chain_rig(fk_chain_mirror , control_parent = hand_ctrl_grp_mirror)
        cmds.setAttr(fk_chain_mirror[0] + '.visibility' , 1)
        cmds.parent(fk_chain_mirror[0] , hand_jnt_grp_mirror)

    pose_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_{}_handPose_001'.format('l') , shape = 'pPlatonic' ,
                                                     radius = 10 ,
                                                     axis = 'X+' ,
                                                     pos = thumbHand_fk_chain[0] , parent = hand_ctrl_grp)
    pose_ctrl_mirror_obj = controlUtils.Control.create_ctrl('ctrl_{}_handPose_001'.format('r') ,
                                                            shape = 'pPlatonic' ,
                                                            radius = 10 ,
                                                            axis = 'X+' ,
                                                            pos = thumbHand_fk_chain_mirror[0] ,
                                                            parent = hand_ctrl_grp_mirror)

    self.fingerCurlRig()



def fingerCurlRig(self) :
    u"""设置手指关节旋转的姿势。
         """
    # 获取手指名称
    finger_names = ['thumb' , 'index' , 'middle' , 'ring' , 'pinky']

    # 获取关节节数名称
    digit_names = {'thumb' : ['Metacarpal' , 'Base' , 'Tip']}

    # 获取curl的值
    curl_mult_values = {'thumb' : [-3 , -5 , -7] ,
                        'index' : [0 , -7.5 , -10.5 , -8] ,
                        'middle' : [0 , -7.5 , -10.5 , -8] ,
                        'ring' : [0 , -7.5 , -10.5 , -8] ,
                        'pinky' : [0 , -7.5 , -10.5 , -8]}

    # 循环到'lr'两边的每一侧
    for side in 'lr' :
        # 获取手姿势控制的控制器
        pose_ctrl = 'ctrl_{}_handPose_001'.format(side)
        # 循环到每个手指，并添加curl attr
        for finger in finger_names :
            cmds.addAttr(pose_ctrl , longName = finger + 'Curl' , attributeType = 'float' , keyable = True ,
                         minValue = 0 , maxValue = 10)
            curl_attr = '{}.{}Curl'.format(pose_ctrl , finger)

            # 获取卷曲值
            curl_values = curl_mult_values[finger]
            # 获取关节节数名称
            finger_digits = digit_names.get(finger , ['Metacarpal' , 'Base' , 'Mid' , 'Tip'])
            # 循环到每个手指并连接卷曲的值
            for digit , val in zip(finger_digits , curl_values) :
                offset_name = 'offset_{}_{}{}Bind_001'.format(side , finger , digit.title())

                if val :
                    # 创建乘法节点
                    mult_node = cmds.createNode('multDoubleLinear' ,
                                                name = 'mult_{}_{}{}Curl_001'.format(side , finger , digit.title()))
                    # 连接驱动的节点的属性
                    cmds.connectAttr(curl_attr , mult_node + '.input1')
                    # 设置卷曲值
                    cmds.setAttr(mult_node + '.input2' , val)

                    # 将输出连接到偏移组的rotateZ
                    cmds.connectAttr(mult_node + '.output' , offset_name + '.rotateZ')