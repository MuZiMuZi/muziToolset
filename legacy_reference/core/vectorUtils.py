import math
import maya.api.OpenMaya as om
import maya.cmds as cmds

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


#尝试用矩阵代替父子约束


def get_matrix(attr):
    """
    获取 Maya Matrix 属性并转换成 MMatrix。

    Args:
        attr (str):
            Matrix 属性名字。

            例如：
            ctrl_l_arm.worldMatrix[0]
            jnt_l_arm.matrix

    Returns:
        maya.api.OpenMaya.MMatrix
    """

    matrix_value = cmds.getAttr(attr)

    if isinstance(matrix_value, (list, tuple)):

        if len(matrix_value) == 1:

            first_value = matrix_value[0]

            if isinstance(first_value, (list, tuple)):

                matrix_value = first_value

    matrix = om.MMatrix(matrix_value)

    return matrix


def matrix_to_list(matrix):
    """
    将 MMatrix 转换成 Maya setAttr 可以使用的 16 个浮点数。

    Args:
        matrix (maya.api.OpenMaya.MMatrix):
            Maya API 2.0 的矩阵对象。

    Returns:
        list:
            包含 16 个 float 的列表。
    """

    matrix_list = []

    for index in range(16):

        value = matrix[index]

        matrix_list.append(value)

    return matrix_list

def matrix_parent_constraint (
        driver ,
        driven ,
        maintain_offset = True
) :
    """
    使用矩阵代替 parentConstraint。

    Args:
        driver (str):
            驱动对象。

        driven (str):
            被驱动对象。

        maintain_offset (bool):
            是否保持当前偏移。

            True:
                相当于 parentConstraint(mo=True)

            False:
                相当于 parentConstraint(mo=False)

    Returns:
        str:
            创建出来的 multMatrix 节点。

    Example:

        matrix_parent_constraint(
            'ctrl_l_arm_fk',
            'jnt_l_arm_fk',
            maintain_offset=True
        )
    """

    # ------------------------------------------------------------
    # 检查对象是否存在
    # ------------------------------------------------------------

    if not cmds.objExists (driver) :
        cmds.error (
            'Driver 不存在: {0}'.format (driver)
        )

        return None

    if not cmds.objExists (driven) :
        cmds.error (
            'Driven 不存在: {0}'.format (driven)
        )

        return None

    # ------------------------------------------------------------
    # 检查 offsetParentMatrix 是否已经存在输入
    # ------------------------------------------------------------

    offset_parent_matrix_attr = (
            driven + '.offsetParentMatrix'
    )

    connections = cmds.listConnections (
        offset_parent_matrix_attr ,
        source = True ,
        destination = False ,
        plugs = True
    )

    if connections :
        cmds.warning (
            '{0}.offsetParentMatrix 已经存在输入连接。'.format (
                driven
            )
        )

        return None

    # ------------------------------------------------------------
    # 获取 Driven 当前 Local Matrix
    # ------------------------------------------------------------
    #
    # Maya 最终世界矩阵可以简单理解成：
    #
    # localMatrix
    #     *
    # offsetParentMatrix
    #     *
    # parentWorldMatrix
    #
    # 所以如果我们直接：
    #
    # driver.worldMatrix
    #     ->
    # driven.offsetParentMatrix
    #
    # driven 原来的 localMatrix 还会继续参与计算。
    #
    # 因此需要先把 Driven 自己原来的 Local Matrix 抵消掉。
    #
    # ------------------------------------------------------------

    driven_local_matrix = get_matrix (
        driven + '.matrix'
    )

    driven_local_inverse_matrix = (
        driven_local_matrix.inverse ()
    )

    # ------------------------------------------------------------
    # 计算 Maintain Offset
    # ------------------------------------------------------------

    if maintain_offset :

        # 获取当前 Driver 世界矩阵
        driver_world_matrix = get_matrix (
            driver + '.worldMatrix[0]'
        )

        # 获取当前 Driven 世界矩阵
        driven_world_matrix = get_matrix (
            driven + '.worldMatrix[0]'
        )

        # --------------------------------------------------------
        # Offset Matrix
        #
        # drivenWorld
        #     *
        # driverWorldInverse
        #
        # 这样 Driver 移动的时候，
        # Driven 会保持当前相对位置。
        # --------------------------------------------------------

        driver_world_inverse_matrix = (
            driver_world_matrix.inverse ()
        )

        offset_matrix = (
                driven_world_matrix
                *
                driver_world_inverse_matrix
        )

    else :

        # 不保持 Offset
        # 使用单位矩阵
        offset_matrix = om.MMatrix ()

    # ------------------------------------------------------------
    # 创建 multMatrix
    # ------------------------------------------------------------

    driven_short_name = driven.split ('|') [-1]

    # namespace 中的 ":" 不适合作为普通工具节点命名的一部分
    driven_short_name = driven_short_name.replace (
        ':' ,
        '_'
    )

    mult_matrix_name = (
            driven_short_name
            +
            '_parent_mm'
    )

    mult_matrix = cmds.createNode (
        'multMatrix' ,
        name = mult_matrix_name
    )

    # ------------------------------------------------------------
    # matrixIn[0]
    #
    # Driven Local Matrix 的逆矩阵
    #
    # 用来抵消 driven 本身已有的：
    #
    # translate
    # rotate
    # scale
    # jointOrient
    # ------------------------------------------------------------

    driven_local_inverse_list = matrix_to_list (
        driven_local_inverse_matrix
    )

    cmds.setAttr (
        mult_matrix + '.matrixIn[0]' ,
        *driven_local_inverse_list ,
        type = 'matrix'
    )

    # ------------------------------------------------------------
    # matrixIn[1]
    #
    # Offset Matrix
    # ------------------------------------------------------------

    offset_matrix_list = matrix_to_list (
        offset_matrix
    )

    cmds.setAttr (
        mult_matrix + '.matrixIn[1]' ,
        *offset_matrix_list ,
        type = 'matrix'
    )

    # ------------------------------------------------------------
    # matrixIn[2]
    #
    # Driver World Matrix
    # ------------------------------------------------------------

    cmds.connectAttr (
        driver + '.worldMatrix[0]' ,
        mult_matrix + '.matrixIn[2]' ,
        force = True
    )

    # ------------------------------------------------------------
    # matrixIn[3]
    #
    # Driven Parent Inverse Matrix
    #
    # 把 Driver 的 World Space
    # 转换到 Driven 的 Parent Space。
    # ------------------------------------------------------------

    cmds.connectAttr (
        driven + '.parentInverseMatrix[0]' ,
        mult_matrix + '.matrixIn[3]' ,
        force = True
    )

    # ------------------------------------------------------------
    # 输出到 offsetParentMatrix
    # ------------------------------------------------------------

    cmds.connectAttr (
        mult_matrix + '.matrixSum' ,
        driven + '.offsetParentMatrix' ,
        force = True
    )

    return mult_matrix