# coding=utf-8
u"""
这是一个控制器类。用来对控制器进行一系列修改的操作。

实现的功能：

设置控制器的transform节点：set_transform
设置控制器的父对象：set_parent
设置控制器的形状：set_shape
设置控制器的名字：set_name
设置控制器的颜色：set_color
设置控制器的半径：set_radius
# 设置控制器的旋转：set_rotate
# 设置控制器的偏移：set_offset
# 设置控制器的属性锁定和隐藏：set_locked
上传控制器形状：upload
删除控制器形状：delete_shape
镜像控制器形状：mirror
create_ctrl: 创建绑定用的控制器层级组

"""
from __future__ import print_function

import json
import os


import pymel.core as pm
import  maya.cmds as cmds
import nameUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.attrUtils as attrUtils

reload(attrUtils)

class Control(object):
    u"""
        kwargs – 修改控制器的参数
        kwargs – -n -name string 名字
        kwargs – -t -transform string/node/Control 控制器
        kwargs – -p -parent string/node 父对象
        kwargs – -s -shape data/name 形态
        kwargs – -c -color int 颜色
        kwargs – -r -radius float 半径
        kwargs – -ro -rotate [float, float,float] 旋转
        kwargs – -o -offset [float, float,float] 偏移
    """
    def __init__(self,*args,**kwargs):
        self.cv = None
        self.transform = None
        self.set_transform(*args,**kwargs)
        self.set(**kwargs)

    def __repr__(self):
        return "{m}.{c}.(t = {t})".format(m = __name__,c = self.__class__.__name__,t = self.get_transform().name())

    def set(self,**kwargs):
        self.set_parent(**kwargs)
        self.set_shape(**kwargs)
        self.set_name(**kwargs)
        self.set_color(**kwargs)
        self.set_radius(**kwargs)
        self.set_offset(**kwargs)
        self.set_locked(**kwargs)

    def set_transform(self,*args,**kwargs):
        u"""
        设置控制器的transform节点
        -t -transform string/node/Control 控制器节点
        """
        t = kwargs.get("t",kwargs.get("transform",self.get_arg(args)))
        # 如果没有给定t（transform）的值，或者选择的物体没有transform节点，则创建一个transform节点
        if t is None:
            self.transform = pm.group(em=1)
        # 如果给定了t(transfrom) 的值
        elif isinstance(t, (str, unicode)):
            # 如果t(transfrom) ，不存在于该场景
            if not pm.objExists(t):
                pm.warning("没有与名称符合的物体 " + t)
                self.set_transform()
            else:
                transforms = pm.ls(t, type="transform")
                # 如果t(transfrom)，该场景存在多个重名的物体
                if len(transforms) != 1:
                    pm.warning("有多个名称相同的物体 " + t)
                    self.transform = transforms[0]
                else:
                    self.transform = transforms[0]
        elif isinstance(t, Control):
            self.transform = t.transform

        # 检查有没有nodeType这个属性或者是nodeType这个属性是否为transform
        elif hasattr(t, "nodeType") and t.nodeType() == "transform":
            self.transform = t

    def set_parent(self,*args,**kwargs):
        u"""
        设置控制器的父对象
        -p -parent string/node 父对象
        """
        parent = kwargs.get("p", kwargs.get("parent", self.get_arg(args)))
        if parent:
            self.get_transform().setParent(parent)
            try:

                self.get_transform().t.set(0, 0, 0)
                self.get_transform().r.set(0, 0, 0)
                self.get_transform().s.set(1, 1, 1)
            except (RuntimeError, UnicodeEncodeError):
                pass

    def set_shape(self,*args,**kwargs):
        u"""
        设置控制器的形状
        -s -shape data/name 形态
        """
        shape = kwargs.get("s", kwargs.get("shape", self.get_arg(args)))
        color = self.get_color()
        radius = self.get_radius()
        if shape is None:
            return
        if isinstance(shape, list):
            shapes = self.get_transform().getShapes()
            if shapes:
                pm.delete(shapes)
            for data in shape:
                p = [[data["points"][i + j] for j in range(3)] for i in range(0, len(data["points"]), 3)]
                if data["periodic"]:
                    p = p + p[:data["degree"]]
                curve = pm.curve(degree=data["degree"],
                                 knot=data["knot"],
                                 periodic=data["periodic"],
                                 p=p)
                curve.getShape().setParent(self.get_transform(), s=1, add=1)
                curve.getShape().rename(self.get_transform().name().split("|")[-1] + "Shape")
                pm.delete(curve)
            self.set_color(color)
            self.set_radius(radius)
        elif isinstance(shape, (str, unicode)):
            data_file = os.path.abspath(__file__ + "/../../res/image/{s}.json".format(s=shape))
            if not os.path.isfile(data_file):
                pm.warning(u"找不到这个文件 " + data_file)
                return
            with open(data_file, "r") as fp:
                self.set_shape(s=json.load(fp))

    def set_name(self, *args, **kwargs):
        u"""
        设置名字
        """
        n = kwargs.get("n", kwargs.get("name", self.get_arg(args)))
        if n is None:
            return
        self.get_transform().rename(n)
        for s in self.get_transform().getShapes():
            s.rename(n+"Shape")

    def set_color(self,*args,**kwargs):
        u"""
        设置控制器的颜色
        -c -color int 颜色
        """
        color = kwargs.get("c", kwargs.get("color", self.get_arg(args)))
        if color is None:
            return
        for shape in self.get_transform().getShapes():
            # 如果形状节点的节点类型不是曲线，则取消设置颜色
            if shape.nodeType() != "nurbsCurve":
                continue
            shape.overrideEnabled.set(True)
            shape.overrideColor.set(color)

    def set_radius(self,*args,**kwargs):
        u"""
        设置控制器的半径
        -r -radius (float) :半径
        """
        radius = kwargs.get('r',kwargs.get('radius',self.get_arg(args)))
        if radius is None:
            return
        points = [self.get_curve_shape_points(shape) for shape in self.get_transform().getShapes()]
        points = [[[ps[i + j] for j in range(3)] for i in range(0, len(ps), 3)] for ps in points]
        lengths = [self.get_length(p, [0, 0, 0]) for ps in points for p in ps]
        origin_radius = max(lengths)
        scale = radius / origin_radius
        for shape, ps in zip(self.get_transform().getShapes(), points):
            for p, cv in zip(ps, shape.cv):
                pm.xform(cv, t=[xyz * scale for xyz in p])

    def set_rotateX(self,**kwargs):
        rotateX = kwargs.get('rx', kwargs.get('rotateX', 0))  # type: int
        shape_node = cmds.listRelatives('{}'.format(self.get_transform()), shapes=True)[0]
        points = '{}'.format(shape_node) +".cv[0:700000]"
        cmds.rotate(rotateX,0,0,points)

    def set_rotateY(self,**kwargs):
        rotateY = kwargs.get('ry', kwargs.get('rotateY', 0))  # type: int
        shape_node = cmds.listRelatives('{}'.format(self.get_transform()), shapes=True)[0]
        points = '{}'.format(shape_node) + ".cv[0:700000]"
        cmds.rotate(0,rotateY,0,points)

    def set_rotateZ(self,**kwargs):
        rotateZ = kwargs.get('rz', kwargs.get('rotateZ', 0))  # type: int
        shape_node = cmds.listRelatives('{}'.format(self.get_transform()), shapes=True)[0]
        points = '{}'.format(shape_node) + ".cv[0:700000]"
        cmds.rotate(0, 0, rotateZ, points)

    def set_offset(self, *args,**kwargs):
        u"""
        设置偏移
        kwargs – -o -offset [float, float,float] 偏移
        """
        offset = kwargs.get("o", kwargs.get("offset", self.get_arg(args)))
        if offset is None:
            return
        points = [self.get_curve_shape_points(shape) for shape in self.get_transform().getShapes()]
        points = [[[ps[i + j] for j in range(3)] for i in range(0, len(ps), 3)] for ps in points]
        for shape, ps in zip(self.get_transform().getShapes(), points):
            for p, cv in zip(ps, shape.cv):
                pm.xform(cv, t=[p_xyz + o_xyz for p_xyz, o_xyz in zip(p, offset)])

    def set_locked(self,*args,**kwargs):
        pass

    def upload(self):
        u"""
        上传控制器到data路径下，并且截图
        """
        data_path = os.path.abspath(__file__ + "/../../res/image")
        if not os.path.isdir(data_path):
            pm.warning(u"没有找到这个路径" + data_path)
            return
        data_file = os.path.join(data_path,self.get_transform().name().split("|")[-1] + ".json")
        # 打开并写入带有形状信息的date_file文件，open函数的参数有file_name，access_mode 和 buffering
        ##file_name：file_name变量是一个包含了你要访问的文件名称的字符串值。
        ##access_mode：access_mode决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。这个参数是非强制的，
        ## 默认文件访问模式为只读(r)。写入为(w)
        ##buffering:如果buffering的值被设为0，就不会有寄存。如果buffering的值取1，访问文件时会寄存行。
        ##如果将buffering的值设为大于1的整数，表明了这就是的寄存区的缓冲大小。如果取负值，寄存区的缓冲大小则为系统默认。
        with open(data_file,'w') as fp:
            json.dump(self.get_shape(),fp,indent=4)

        # 在视图面板中隐藏所有场景信息
        for hud in pm.headsUpDisplay(listHeadsUpDisplays=1):
            pm.headsUpDisplay(hud, edit=1, vis=False)

        # 创建一个撕下副本的面板用于截图控制器形状，如果创建的撕下副本的面板存在则关闭后重新开启
        panel = 'control_model_panel'
        if not pm.modelPanel(panel, exists=True):
            pm.modelPanel(panel, tearOff = True, tearOffCopy= 1)

        # 关闭撕下副本视图中所有对象的显示，打开撕下副本视图的 nurbs 曲线显示，关闭撕下副本视图的网格显示。
        pm.modelEditor(panel, edit=1, allObjects=0, nurbsCurves=1, grid=0)

        # 调整撕下副本视图的焦距，按键F
        pm.setFocus(panel)

        # 复制一个临时的用于截图的控制器，控制器的位置在原点中心
        temp = Control()
        temp.set_shape(s=self.get_shape())
        pm.select(temp.get_transform())

        # 设置用来截图的摄影机的拍摄角度，将摄影机移动到选定对象的中心，指定应设置摄影机位置之间的过渡动画。
        pm.setAttr('persp.rotate', -27.938, 45, 0)
        pm.viewFit('persp', animate = 0)

        # 撕下副本面板开启隔离选择模式，将刚刚选择的需要截图的控制器添加到要显示的对象集中
        pm.isolateSelect(panel, state=1)
        pm.isolateSelect(panel, addSelected=True)

        # 设定拍屏截图的文件名称和文件路径和拍屏的参数设置
        jpg_path = os.path.join(data_path, self.get_transform().split("|")[-1])
        file_name = pm.playblast(format="image", filename=jpg_path, c = "jpg", widthHeight=[256, 256],
                                 startTime=0, endTime=0, viewer=False, percent=100, quality=100, framePadding=1)

        # 修改拍屏截图后的保存的文件名称，如果有相同名称的文件存在则删除过去的截图文件
        if os.path.isfile(file_name.replace("####","0")):
            if os.path.isfile(file_name.replace("####.","")):
                os.remove(file_name.replace("####.",""))
            os.rename(file_name.replace("####","0"),file_name.replace("####.",""))

        # 关闭撕下副本面板
        if pm.modelPanel(panel,ex = 1):
            pm.deleteUI(panel, panel=True)

        # 删除用来截图的控制器
        pm.delete(temp.get_transform())

    def mirror(self,other):
        u"""
        镜像控制器
        :param other: 镜像控制器的目标
        :return:
        """
        self.set_shape(s=other.get_shape())
        for src_shape, dst_shape in zip(self.get_transform().getShapes(), other.get_transform().getShapes()):
            for src_cv, dst_cv in zip(src_shape.cv, dst_shape.cv):
                point = pm.xform(dst_cv, q=1, t=1, ws=1)
                point[0] = -point[0]
                pm.xform(src_cv, t=point, ws=1)

    def get_shape(self):
        u"""

        :return: data
        控制器形状的数据
        """
        return [dict(points = self.get_curve_shape_points(shape),
                     degree = shape.degree(),
                     periodic = shape.form() == 3,
                     knot = shape.getKnots())
                for shape in self.get_transform().getShapes()]

    def get_transform(self):
        u"""
         -t -transform string/node/Control 控制器
        :return: transform node
        返回控制器的transform节点
        """
        return self.transform

    def get_color(self):
        """
        获得控制器的颜色
        -c - color int : 控制器颜色
        :return:
        """
        c = 0
        for shape in self.get_transform().getShapes():
            c = shape.overrideColor.get()
        return c

    def get_radius(self):
        """
        获得控制器的大小
        -r - radius int : 控制器大小
        :return:
        """
        if len(self.get_transform().getShapes()) == 0:
            return self.get_soft_radius()
        points = [self.get_curve_shape_points(shape) for shape in self.get_transform().getShapes()]
        points = [[[ps[i + j] for j in range(3)] for i in range(0, len(ps), 3)] for ps in points]
        lengths = [self.get_length(p, [0, 0, 0]) for ps in points for p in ps]
        radius = max(lengths)
        return radius

    @staticmethod
    def create_ctrl(name, shape, radius , axis, pos, parent = None):
        u"""基于参数ctrl_side_name_index创建控制器

        Args:
            name(str/None): 控制器的名称.
            # side (str/None): 控制器的边.
            # description (str): 控制器的描述.
            # index (int/None): 控制器的编号.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            str: 控制器的名称

        """

        name_obj = nameUtils.Name(name = name)
        # 获得控制器边的参数
        if name_obj.side == 'l':
            ctrl_color = 6
            sub_color = 18
        elif name_obj.side == 'r':
            ctrl_color = 13
            sub_color = 20
        elif name_obj.side == 'm':
            ctrl_color = 17
            sub_color = 22

        if cmds.objExists(name_obj.name):
            raise ValueError(u'{} 在场景中已存在'.format(name_obj.name))
        else:
            ctrl = Control(n= name_obj.name, s = shape ,r= radius )
            ctrl_transform = '{}'.format(ctrl.transform)
            # 复制ctrl作为次级控制器
            sub_obj  =  nameUtils.Name(name = name)
            sub_obj.description = sub_obj.description + 'Sub'
            sub_ctrl = Control(n=sub_obj.name, s=shape,r = radius * 0.7)
            sub_ctrl.set_parent(ctrl.transform)
            # 设置控制器形状方向
            if axis == 'X+':
                ctrl.set_rotateX(rx = 90)
                sub_ctrl.set_rotateX(rx = 90)
            elif axis == 'X-':
                ctrl.set_rotateX(rx= -90)
                sub_ctrl.set_rotateX(rx = -90)
            elif axis == 'Y+':
                ctrl.set_rotateY(ry= 90)
                sub_ctrl.set_rotateY(ry = 90)
            elif axis == 'Y-':
                ctrl.set_rotateY(ry= -90)
                sub_ctrl.set_rotateY(ry = -90)
            elif axis == 'Z+':
                ctrl.set_rotateZ(rz= 90)
                sub_ctrl.set_rotateZ(rz = 90)
            elif axis == 'Z-':
                ctrl.set_rotateZ(rz= -90)
                sub_ctrl.set_rotateZ(rz = -90)
            # 设置颜色
            ctrl.set(c = ctrl_color)
            sub_ctrl.set(c = sub_color)
        # 添加上层层级组
        offset_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj = ctrl_transform, grp_name='{}'.format(name.replace('ctrl', 'offset')), world_orient=False)
        connect_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=offset_grp, grp_name=offset_grp.replace('offset', 'connect'), world_orient=False)
        driven_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj=connect_grp, grp_name=connect_grp.replace('connect', 'driven'), world_orient=False)
        zero_grp = hierarchyUtils.Hierarchy.add_extra_group (
            obj=driven_grp, grp_name=driven_grp.replace('driven', 'zero'), world_orient=False)

        # 创建output层级组
        output = cmds.createNode('transform', name=name.replace('ctrl_', 'output_'), parent = ctrl_transform)

        # 连接次级控制器的属性
        cmds.connectAttr(sub_ctrl.transform + '.translate', output + '.translate')
        cmds.connectAttr(sub_ctrl.transform  + '.rotate', output + '.rotate')
        cmds.connectAttr(sub_ctrl.transform + '.scale', output + '.scale')
        cmds.connectAttr(sub_ctrl.transform  + '.rotateOrder', output + '.rotateOrder')

        # # 添加次级控制器的属性控制在控制器上
        cmds.addAttr(ctrl_transform, longName='subCtrlVis', attributeType='bool')
        cmds.setAttr(ctrl_transform + '.subCtrlVis', channelBox=True)

        # 连接次级控制器的显示
        cmds.connectAttr(ctrl_transform + '.subCtrlVis', sub_ctrl.transform + '.visibility')

        # 锁定并且隐藏不需要的属性
        attrUtils.Attr.lock_and_hide_attrs(obj = ctrl_transform, attrs_list=['rotateOrder'], lock=False, hide=False)
        # attrUtils.Attr.lock_and_hide_attrs(obj = ctrl_transform, attrs_list = attrs_list, lock = True, hide = True)

        # 吸附到对应的位置
        if pos:
            cmds.matchTransform(zero_grp, pos, position=True, rotation=True, scale=True)
        #
        # 做父子层级
        if parent:
            hierarchyUtils.Hierarchy.parent(child_node = zero_grp , parent_node = parent )

        #
        # 将控制器添加到对应的选择集
        animation_ctrls_set = 'ctrl_set'
        if not cmds.objExists(animation_ctrls_set) or cmds.nodeType(animation_ctrls_set) != 'objectSet':
            animation_ctrls_set = cmds.sets(name = animation_ctrls_set, empty=True)
            cmds.sets('{}'.format(ctrl.transform), edit=True, forceElement=animation_ctrls_set)
        else:
            cmds.sets('{}'.format(ctrl.transform), edit=True, forceElement=animation_ctrls_set)

    @staticmethod
    def get_arg(args):
        if len(args) > 0:
            return args[0]
        return None

    @staticmethod
    def get_curve_shape_points(shape):
        return pm.xform(shape.cv, q=1, t=1)

    @staticmethod
    def get_soft_radius():
        u"""
        ssd (float): 衰减半径
        return:返回软选择的范围
        """
        return pm.softSelect(query=1, ssd=1)

    @staticmethod
    def get_length(point1, point2):
        u"""
        point1[float,float,float]: 点1的坐标(x,y,z)
        point2[float,float,float]: 点2的坐标(x,y,z)
        return: 两点之间的距离
        原理：两点之间的距离等于两点之间x，y，z相减的和的平方再开方
        ((x1-x2)**2 +(y1-y2)**2 + (z1-z2)**2)**0.5
        ** 表示平方，**0.5表示开方
        """
        distance = sum([(point1[i] - point2[i]) ** 2 for i in range(3)]) ** 0.5
        return distance

    @classmethod
    def selected(cls):
        u"""
         [Control(), ]
        选择的控制器
        """
        return [cls(t=t) for t in pm.selected(type="transform")]

    @classmethod
    def set_selected(cls, **kwargs):
        u"""
        :param kwargs: 修改控制器的参数
        批量修改选择的控制器
        """
        selected = cls.selected()
        for control in selected:
            control.set(**kwargs)
        pm.select([control.get_transform() for control in selected])

    @classmethod
    def mirror_selected(cls):
        u"""
        镜像两个选择的控制器
        :return:
        """
        selected = cls.selected()
        if not len(selected) == 2:
            return
        src, dst = selected
        src.mirror(dst)

    @classmethod
    def delete_shape(cls, *args, **kwargs):
        """
        删除形状
        :return:
        """
        s = kwargs.get("s", kwargs.get("shape", cls.get_arg(args)))
        if s is None:
            return
        json_path = os.path.abspath(__file__ + "/../../res/image/{s}.json".format(s=s))
        if os.path.isfile(json_path):
            os.remove(json_path)
        jpg_path = os.path.abspath(__file__ + "/../../res/image/{s}.jpg".format(s=s))
        if os.path.isfile(jpg_path):
            os.remove(jpg_path)

    @classmethod
    def delete_shapes(cls, *args):
        """
        批量删除形状
        :return:
        """
        for s in args:
            cls.delete_shape(s)