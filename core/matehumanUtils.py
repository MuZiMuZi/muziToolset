class MateHuman() :



    def __init__(self , name) :
        self.name = name
        self.side = None
        self.description = None
        self.index = None

        self.mateHuman_decompose()


    @staticmethod
    def get_mateHuman_drv_jnt(description) :
        u'''
        定义matehuman的骨架结构,查询到对应的模块后返回对应的关节
        '''
        mateHuman_joint_trunk_dict = {'root' : 'root_drv' ,
                                      'pelvis' : 'pelvis_drv' ,
                                      'spine' : ['spine_01_drv' , 'spine_02_drv' , 'spine_03_drv' , 'spine_04_drv' ,
                                                 'spine_05_drv'] ,
                                      'neck' : ['neck_01_drv' , 'neck_02_drv'] ,
                                      'head ' : 'head_drv'}

        mateHuman_joint_arm_dict = {'clavicle_l' : 'clavicle_l_drv' ,
                                    'arm_l' : ['upperarm_l_drv', 'lowerarm_l_drv', 'hand_l_drv'],
                                    'hand_l' : 'hand_l_drv' ,
                                    'index_finger_l' : ['index_metacarpal_l_drv','index_01_l_drv' , 'index_02_l_drv' , 'index_03_l_drv'] ,
                                    'middle_finger_l' : ['middle_metacarpal_l_drv','middle_01_l_drv' , 'middle_02_l_drv' , 'middle_03_l_drv'] ,
                                    'ring_finger_l' : ['ring_metacarpal_l_drv' ,'ring_01_l_drv' , 'ring_02_l_drv' , 'ring_03_l_drv'] ,
                                    'pinky_finger_l' : ['pinky_metacarpal_l_drv' ,'pinky_01_l_drv' , 'pinky_02_l_drv' , 'pinky_03_l_drv'] ,
                                    'thumb_finger_l' : ['thumb_01_l_drv' , 'thumb_02_l_drv' , 'thumb_03_l_drv'] ,

                                    'clavicle_r' : 'clavicle_r_drv' ,
                                    'upperarm_r' : 'upperarm_r_drv' ,
                                    'lowerarm_r' : 'lowerarm_r_drv' ,
                                    'arm_r' : ['upperarm_r_drv' , 'lowerarm_r_drv' , 'hand_r_drv'] ,
                                    'hand_r' : 'hand_r_drv' ,
                                    'index_finger_r' : ['index_metacarpal_r_drv' , 'index_01_r_drv' , 'index_02_r_drv' ,
                                                        'index_03_r_drv'] ,
                                    'middle_finger_r' : ['middle_metacarpal_r_drv' , 'middle_01_r_drv' ,
                                                          'middle_02_r_drv' , 'middle_03_r_drv'] ,
                                    'ring_finger_r' : ['ring_metacarpal_r_drv' , 'ring_01_r_drv' , 'ring_02_r_drv' ,
                                                        'ring_03_r_drv'] ,
                                    'pinky_finger_r' : ['pinky_metacarpal_r_drv' , 'pinky_01_r_drv' ,
                                                          'pinky_02_r_drv' , 'pinky_03_r_drv'] ,
                                    'thumb_finger_r' : ['thumb_01_r_drv' , 'thumb_02_r_drv' , 'thumb_03_r_drv']
                                    }

        mateHuman_joint_leg_dict = {'leg_l' : ['thigh_l_drv', 'calf_l_drv', 'foot_l_drv'] ,
                                    'thigh_l' : 'thigh_l_drv' ,
                                    'calf_l' : 'calf_l_drv' ,
                                    'foot_l' : 'foot_l_drv' ,
                                    'ball_l ' : 'ball_l_drv' ,

                                    'bigtoe_l' : ['bigtoe_01_l_drv' , 'bigtoe_02_l_drv'] ,
                                    'indextoe_l' : ['indextoe_01_l_drv' , 'indextoe_02_l_drv'] ,
                                    'middletoe_l' : ['middletoe_01_l_drv' , 'middletoe_02_l_drv'] ,
                                    'littletoe_l' : ['littletoe_01_l_drv' , 'littletoe_02_l_drv'] ,
                                    'ringtoe_l' : ['ringtoe_01_l_drv' , 'ringtoe_02_l_drv'] ,

                                    'leg_r' : ['thigh_r_drv' , 'calf_r_drv' , 'foot_r_drv'],
                                    'thigh_r' : 'thigh_r_drv' ,
                                    'calf_r' : 'calf_r_drv' ,
                                    'foot_r' : 'foot_r_drv' ,
                                    'ball_r' : 'ball_r_drv' ,

                                    'bigtoe_r' : ['bigtoe_01_r_drv' , 'bigtoe_02_r_drv'] ,
                                    'indextoe_r' : ['indextoe_01_r_drv' , 'indextoe_02_r_drv'] ,
                                    'middletoe_r' : ['middletoe_01_r_drv' , 'middletoe_02_r_drv'] ,
                                    'littletoe_r' : ['littletoe_01_r_drv' , 'littletoe_02_r_drv'] ,
                                    'ringtoe_r' : ['ringtoe_01_r_drv' , 'ringtoe_02_r_drv']
                                    }

        for mateHuman_dict in [mateHuman_joint_trunk_dict , mateHuman_joint_arm_dict , mateHuman_joint_leg_dict] :
            if description in mateHuman_dict:
                return mateHuman_dict[description]
            else:
                pass



    def mateHuman_decompose(self) :
        u'''
        拆分mateHuman的关节名称
        '''
        name_parts = self.name.split('_')
        self.description = name_parts[0]
        # 当len(name_parts) == 3 的时候，关节为spine_01_drv或者是clavicle_l_drv类型的关节
        if len(name_parts) == 3 :
            # 当关节为spine_01_drv类型的时候
            if self.description in ['spine' , 'neck'] :
                self.side = 'm'
                self.index = name_parts[1]
            # 当关节为clavicle_l_drv类型的关节
            else :
                self.side = name_parts[1]
                self.index = 1
        # 剩余的情况为关节为root，pelvis，head的drv关节
        else :
            self.side = 'm'
            self.index = 1