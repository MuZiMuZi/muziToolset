
class MateHuman():
    def __init__(self,name):
        self.name = name
        self.side = None
        self.description = None
        self.index = None
        self.mateHuman_decompose()


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
        else:
            self.side = 'm'
            self.index = 1
