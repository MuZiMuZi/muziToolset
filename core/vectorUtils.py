import math


class Vector (object) :
    '''
    用于在maya中方便地计算vector3的数据类型类
    初始化：
    使用列表或元组：v = Vector([1, 2, 3])

    使用参数列表（3）：v = Vector(1, 2, 3)

    '''


    def __init__ (self , *args) :
        self._vector = None
        # 判断给定的参数为list的情况
        if len (args) == 1 :
            if isinstance (args [0] , (tuple , list)) :
                if len (args [0]) == 3 :
                    self._vector = args [0]

        # 判断给定的参数为三个独立的数值的情况
        elif len (args) == 3 :
            self._vector = args
        if not self._vector :
            raise TypeError (u'初始化失败，检查输入类型')

        self._axis = None


    def normalize (self) :
        u'''
        使长度的参数规范化，如果遇到除数为0的情况则pass
        '''
        if self._vector :
            try :
                return Vector (
                    self.x / self.length ,
                    self.y / self.length ,
                    self.z / self.length
                )
            except ZeroDivisionError :
                pass

        return Vector (0 , 0 , 0)


    @property
    def length (self) :
        u'''
        sqrt是更号的意思，求长度
        '''
        return math.sqrt (self.x ** 2 + self.y ** 2 + self.z ** 2)


    @property
    def x (self) :
        return self._vector [0]


    @property
    def y (self) :
        return self._vector [1]


    @property
    def z (self) :
        return self._vector [2]


    @property
    def as_list (self) :
        return [self.x , self.y , self.z]


    @property
    def axis (self) :
        if all (v1 == v2 for v1 , v2 in zip (self._vector , [1 , 0 , 0])) :
            self._axis = 'X+'
        elif all (v1 == v2 for v1 , v2 in zip (self._vector , [-1 , 0 , 0])) :
            self._axis = 'X-'
        elif all (v1 == v2 for v1 , v2 in zip (self._vector , [0 , 1 , 0])) :
            self._axis = 'Y+'
        elif all (v1 == v2 for v1 , v2 in zip (self._vector , [0 , -1 , 0])) :
            self._axis = 'Y-'
        elif all (v1 == v2 for v1 , v2 in zip (self._vector , [0 , 0 , 1])) :
            self._axis = 'Z+'
        elif all (v1 == v2 for v1 , v2 in zip (self._vector , [0 , 0 , -1])) :
            self._axis = 'Z-'
        return self._axis


    def mult_interval (self , interval) :
        return (self.x * interval , self.y * interval , self.z * interval)

