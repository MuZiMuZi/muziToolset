# coding=utf-8
u"""
nameUtils：Maya Rig 命名工具。

标准命名规则：
    [类型]_[方向]_[部位]_[功能]_[序号]

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003
    model_md_head_tweak_001

兼容旧版 Name 调用方式：
    Name(type="ctrl", side="lf", resolution="eye", description="main", index=1)

也支持新的语义写法：
    Name.create_name(
        node_type="ctrl",
        side="lf",
        part="eye",
        function="main",
        index=1
    )
"""
from transformers import pipeline


class Name(object):
    def __init__(self,
        name=None,
        type=None,
        side=None,
        part=None,
        function=None,
        index = None ):

        self.name = name
        self.type = type
        self.side = side
        self.part = part
        self.function = function
        self.index = index

        if self.name:
            self.decompose_name ()


    def decompose (self) :
        self.name_parts = self.name.split ('_')

        self.type = self.name_parts [0]
        self.side = self.name_parts [1]
        if len (self.name_parts) == 5 :
            self.part = self.name_parts [2]
        else :
            self.part = None
        self.function = self.name_parts [-2]
        self.index = int (self.name_parts [-1])

    def compose_name (self) :
        #组合名称
        if self.index is None :
            self.index = 1

        self.index = int (self.index)

        self.name = "{0}_{1}_{2}_{3}_{4:03d}".format (
            self.type ,
            self.side ,
            self.part ,
            self.function ,
            self.index
        )

    def flip(self):
        if self.side == 'lf':
            self.side = 'rt'
        elif self.side == 'rt':
            self.side = 'lf'



    @property
    def type(self):
        return self.type

    @type.setter
    def type(self, value):
        self.type = value

    @property
    def side(self):
        return self.side

    @side.setter
    def side(self, value):
        self.side = value

    @property
    def part(self):
        return self.part

    @resolution.setter
    def part(self, value):
        self.part = value

    @property
    def function(self):
        return self.function

    @description.setter
    def function(self, value):
        self.function = value

    @property
    def index(self):
        return self.index

    @index.setter
    def index(self, value):
        self.index = value

    @property
    def name(self):
        self.compose_name()
        return self.name
