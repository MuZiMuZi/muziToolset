# coding=utf-8
u"""
controlUtils：这是一个控制器模块。用来对控制器进行一系列修改的操作。

实现的功能：

设置控制器的transform节点：set_transform
设置控制器的父对象：set_parent
设置控制器的形状：set_shape
设置控制器的名字：set_name
设置控制器的颜色：set_color
设置控制器的半径：set_radius
设置控制器的旋转：set_rotate
设置控制器的偏移：set_offset
设置控制器的属性锁定和隐藏：set_locked
上传控制器形状：upload
删除控制器形状：delete_shape
镜像控制器形状：mirror
获取形状信息：get_shape
获取transform节点：get_transform
获取控制器颜色：get_color
获取控制器大小：get_radius
创建绑定用的控制器层级组：create_ctrl
创建matehuman用的控制器层级组：create_mateHuman_ctrl
创建ribbon控制器：create_ribbon

"""
from __future__ import print_function

import json
import os
from importlib import reload

import maya.cmds as cmds
import pymel.core as pm

from . import nameUtils , pipelineUtils , matehumanUtils , hierarchyUtils , attrUtils


reload (pipelineUtils)
reload (nameUtils)


class Control (object) :
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
    # 设置控制器的颜色模版
    COLORS = {'l' : (6 , 18) , 'r' : (13 , 20) , 'm' : (17 , 22)}


    def __init__ (self , name ,shape = 'circle' , radius= 1 , ctrl_color = 17 ,axis='X+' ,
                  unset_sub_ctrl = True,unset_add_extra_group = True,
                  pos = None , parent = None,lock_attrs = None,animation_set = None) :
        #初始化参数
        #控制器的形状属性
        self.cv = None
        # Control 新建时必须先有真实的 transform 节点，后续 set_shape/getShapes 才能正常工作
        # 如果传入的名称已经存在，则直接包装现有 transform；否则创建一个空 transform。
        if name and pm.objExists(name):
            nodes = pm.ls(name, type='transform')
            self.transform = nodes[0] if nodes else pm.group(em=True)
        else:
            self.transform = pm.group(em=True)
        self.shape = shape
        self.radius = radius
        self.ctrl_color = ctrl_color
        self.axis = axis

        #控制器的额外设置
        self.unset_sub_ctrl =unset_sub_ctrl
        self.pos = pos
        self.parent = parent
        self.unset_add_extra_group = unset_add_extra_group
        self.lock_attrs = lock_attrs
        self.animation_set = animation_set

        # 初始化设置控制器的属性
        self.set(
            name=name, shape=shape, radius=radius, color=ctrl_color, axis=axis,
            pos=pos, parent=parent, lock_attrs=lock_attrs, animation_set=animation_set,
            unset_sub_ctrl=unset_sub_ctrl, unset_add_extra_group=unset_add_extra_group
        )


    def __repr__ (self) :
        return "{m}.{c}.(t = {t})".format (m = __name__ , c = self.__class__.__name__ ,
                                           t = self.get_transform ().name ())


    # 设置控制器属性
    def set (self , *args , **kwargs) :
        """快速设置控制器的各种属性。"""
        # 先创建/设置 Shape，再命名；Shape 创建依赖真实 transform 节点。
        self.set_shape(*args, **kwargs)
        self.set_name(*args, **kwargs)
        self.set_color(*args, **kwargs)
        self.set_radius(*args, **kwargs)
        self.set_offset(*args, **kwargs)
        self.set_rotate(*args, **kwargs)

        # 位置与属性
        self.set_pos(*args, **kwargs)
        self.set_locked(*args, **kwargs)
        self.set_animation_set(*args, **kwargs)

        # 层级最后创建，避免 parent 后又被额外组打断
        self.set_add_extra_group(*args, **kwargs)
        if self.unset_add_extra_group is False:
            self.set_parent(*args, **kwargs)

    # 设置控制器的transform节点
    def set_transform (self , *args , **kwargs) :
        u"""
        设置控制器的transform节点
        -t -transform string/node/Control 控制器节点
        """
        t = kwargs.get ("t" , kwargs.get ("transform" , self.get_arg (args)))
        # 如果没有给定t（transform）的值，或者选择的物体没有transform节点，则创建一个transform节点
        if t is None :
            self.transform = pm.group (em = 1)
        # 如果给定了t(transfrom) 的值
        elif isinstance (t , (str , u"".__class__)) :
            # 如果t(transfrom) ，不存在于该场景
            if not pm.objExists (t) :
                pm.warning ("没有与名称符合的物体 " + t)
                self.set_transform ()
            else :
                transforms = pm.ls (t , type = "transform")
                # 如果t(transfrom)，该场景存在多个重名的物体
                if len (transforms) != 1 :
                    pm.warning ("有多个名称相同的物体 " + t)
                    self.transform = transforms [0]
                else :
                    self.transform = transforms [0]
        elif isinstance (t , Control) :
            self.transform = t.transform

        # 检查有没有nodeType这个属性或者是nodeType这个属性是否为transform
        elif hasattr (t , "nodeType") and t.nodeType () == "transform" :
            self.transform = t


    # 设置控制器的父对象
    def set_parent (self , *args , **kwargs) :
        u"""
        设置控制器的父对象。

        这里不能直接长期保存 Maya 的绝对 DAG 路径。
        例如控制器刚创建时路径可能是 ``|ctrl_xxx``，创建 zero/driven/space 等
        上层组后，它会变成 ``|zero_xxx|...|ctrl_xxx``，旧路径就失效了。
        因此在真正 parent 前重新解析一次当前节点路径。
        """
        parent = kwargs.get("p", kwargs.get("parent", self.get_arg(args)))
        if not parent:
            return

        parent_name = parent.name() if hasattr(parent, "name") else str(parent)

        # 传入的可能是重父级前留下来的旧绝对路径，例如 |ctrl_zzz。
        # 如果旧路径已经不存在，则取最后一段短名称重新查询当前 DAG 路径。
        if not cmds.objExists(parent_name):
            short_name = parent_name.split("|")[-1]
            matches = cmds.ls(short_name, long=True) or []
            if len(matches) == 1:
                parent_name = matches[0]
            elif len(matches) > 1:
                raise RuntimeError(u"父节点名称不唯一，无法确定要父到哪个节点: {}".format(short_name))
            else:
                raise RuntimeError(u"父节点不存在: {}".format(parent_name))

        self.get_transform().setParent(parent_name)
        try:
            self.get_transform().t.set(0, 0, 0)
            self.get_transform().r.set(0, 0, 0)
            self.get_transform().s.set(1, 1, 1)
        except (RuntimeError, UnicodeEncodeError):
            pass


    # 设置控制器的形状
    def set_shape (self , *args , **kwargs) :
        u"""
        设置控制器的形状
        -s -shape data/name 形态
        """
        shape = kwargs.get ("s" , kwargs.get ("shape" , self.get_arg (args)))
        color = self.get_color ()
        radius = self.get_radius ()
        if shape is None :
            return
        if isinstance (shape , list) :
            shapes = self.get_transform ().getShapes ()
            if shapes :
                pm.delete (shapes)
            for data in shape :
                p = [[data ["points"] [i + j] for j in range (3)] for i in range (0 , len (data ["points"]) , 3)]
                if data ["periodic"] :
                    p = p + p [:data ["degree"]]
                curve = pm.curve (degree = data ["degree"] ,
                                  knot = data ["knot"] ,
                                  periodic = data ["periodic"] ,
                                  p = p)
                curve.getShape ().setParent (self.get_transform () , s = 1 , add = 1)
                curve.getShape ().rename (self.get_transform ().name ().split ("|") [-1] + "Shape")
                pm.delete (curve)
            self.set_color (color)
            self.set_radius (radius)
        elif isinstance (shape , (str , bool)) :
            # elif isinstance(shape , (str , unicode)) :
            data_file = os.path.join(self.get_shape_data_dir(), '{}.json'.format(shape))
            if not os.path.isfile (data_file) :
                pm.warning (u"找不到这个文件 " + data_file)
                return
            with open (data_file , "r") as fp :
                self.set_shape (s = json.load (fp))


    # 设置控制器的名称
    def set_name (self , *args , **kwargs) :
        u"""
        设置控制器的名称
        """
        self.name = kwargs.get ("n" , kwargs.get ("name" , self.get_arg (args)))
        if self.name is None :
            return
        if 'ctrl_' not in self.name:
            self.name = 'ctrl_' + self.name
        self.get_transform ().rename (self.name)
        for shape in self.get_transform ().getShapes () :
            shape.rename (self.name + "Shape")


    # 设置控制器的颜色
    def set_color (self , *args , **kwargs) :
        u"""
        设置控制器的颜色
        -c -color int 颜色
        """
        color = kwargs.get ("c" , kwargs.get ("color" , self.get_arg (args)))
        if color is None :
            return
        for shape in self.get_transform ().getShapes () :
            # 如果形状节点的节点类型不是曲线，则取消设置颜色
            if shape.nodeType () != "nurbsCurve" :
                continue
            shape.overrideEnabled.set (True)
            shape.overrideColor.set (color)


    # 设置控制器的半径大小
    def set_radius (self , *args , **kwargs) :
        u"""
        设置控制器的半径
        -r -radius (float) :半径
        """
        radius = kwargs.get ('r' , kwargs.get ('radius' , self.get_arg (args)))
        if radius is None :
            return
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        lengths = [self.get_length (p , [0 , 0 , 0]) for ps in points for p in ps]
        origin_radius = max(lengths) if lengths else 0.0
        if origin_radius == 0:
            return
        scale = float(radius) / origin_radius
        for shape , ps in zip (self.get_transform ().getShapes () , points) :
            for p , cv in zip (ps , shape.cv) :
                pm.xform (cv , t = [xyz * scale for xyz in p])


    def set_rotate(self, *args , **kwargs):
        """设置控制器 Shape 的朝向和额外旋转。"""
        rotateZ = kwargs.get('rz', kwargs.get('rotateZ', 0))
        rotateX = kwargs.get('rx', kwargs.get('rotateX', 0))
        rotateY = kwargs.get('ry', kwargs.get('rotateY', 0))
        axis = kwargs.get('axis', self.axis)

        axis_mapping = {
            'X+': (90, 0, 0), 'X-': (-90, 0, 0),
            'Y+': (0, 90, 0), 'Y-': (0, -90, 0),
            'Z+': (0, 0, 90), 'Z-': (0, 0, -90),
        }
        ax = axis_mapping.get(axis, (0, 0, 0))
        rx, ry, rz = ax[0] + rotateX, ax[1] + rotateY, ax[2] + rotateZ

        for shape in self.get_transform().getShapes():
            if shape.nodeType() != 'nurbsCurve':
                continue
            for cv in shape.cv:
                pm.rotate(cv, rx, ry, rz, relative=True, objectSpace=True)

    # 设置控制器的偏移
    def set_offset (self , *args , **kwargs) :
        u"""
        设置偏移
        kwargs – -o -offset [float, float,float] 偏移
        """
        offset = kwargs.get ("o" , kwargs.get ("offset" , self.get_arg (args)))
        if offset is None :
            return
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        for shape , ps in zip (self.get_transform ().getShapes () , points) :
            for p , cv in zip (ps , shape.cv) :
                pm.xform (cv , t = [p_xyz + o_xyz for p_xyz , o_xyz in zip (p , offset)])


    # 设置控制器的锁定
    def set_locked (self , *args , **kwargs) :
        #如果有需要锁定并隐藏的属性则进行锁定隐藏，没有的话则不需要操作
        if self.lock_attrs:
            set_attr = attrUtils.Attr(self.get_transform())
            set_attr.lock_and_hide_attrs(attrs_list=self.lock_attrs, lock=False, hide=False)
        else:
            pass

    #设置控制器的位置信息
    def set_pos(self, *args , **kwargs):
        if self.pos is None :
            cmds.xform(str(self.transform), worldSpace=True, translation=(0, 0, 0))
        else:
            cmds.matchTransform (str(self.transform) , self.pos , position = True , rotation = True , scale = True , piv = True)


    def set_animation_set(self, *args, **kwargs):
        # 将控制器添加到选择集里方便进行选择。
        # animation_set 为 None / False / 空字符串时表示不添加选择集。
        animation_set = kwargs.get('animation_set', self.animation_set)
        if animation_set in (None, False, ''):
            return None

        transform = self.get_transform()
        if transform is None:
            return None

        transform_name = transform.name() if hasattr(transform, 'name') else str(transform)
        if not cmds.objExists(transform_name):
            pm.warning(u'控制器不存在，无法添加到选择集: {}'.format(transform_name))
            return None

        return pipelineUtils.Pipeline.create_set(
            object=transform_name,
            set_name=animation_set,
            set_parent='ctrl_set'
        )


    def set_add_extra_group(self,*args , **kwargs):
        # 判断是否需要创建额外的层级结构
        if self.unset_add_extra_group is False:
            self.ctrl_transform = self.get_transform().name() if hasattr(self.get_transform(), 'name') else str(self.get_transform())
            self.zero_grp = None
            self.output_grp = None
            return

        # 组名只使用短名称，不保存会随着 parent 改变而失效的绝对 DAG 路径。
        transform_obj = self.get_transform()
        if hasattr(transform_obj, 'nodeName'):
            self.ctrl_transform = transform_obj.nodeName()
        else:
            self.ctrl_transform = str(transform_obj).split('|')[-1]

        self.offset_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=self.ctrl_transform, grp_name=self.ctrl_transform.replace('ctrl_', 'offset_'), world_orient=False)
        self.connect_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=self.offset_grp, grp_name=self.offset_grp.replace('offset_', 'connect_'), world_orient=False)
        self.space_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=self.connect_grp, grp_name=self.connect_grp.replace('connect_', 'space_'), world_orient=False)
        self.driven_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=self.space_grp, grp_name=self.space_grp.replace('space_', 'driven_'), world_orient=False)
        self.zero_grp = hierarchyUtils.Hierarchy.add_extra_group(
            obj=self.driven_grp, grp_name=self.driven_grp.replace('driven_', 'zero_'), world_orient=False)

        # add_extra_group 会改变 ctrl 的完整 DAG 路径，所以这里必须重新获取当前名称。
        transform_obj = self.get_transform()
        if hasattr(transform_obj, 'nodeName'):
            self.ctrl_transform = transform_obj.nodeName()
        else:
            self.ctrl_transform = str(transform_obj).split('|')[-1]

        # 创建 output 层级组
        output_name = self.ctrl_transform.replace('ctrl_', 'output_')
        if cmds.objExists(output_name):
            self.output_grp = output_name
        else:
            self.output_grp = cmds.createNode('transform', name=output_name, parent=self.ctrl_transform)

        # 父层级应该挂在最上层 zero 组
        if self.parent:
            hierarchyUtils.Hierarchy.parent(child_node=self.zero_grp, parent_node=self.parent)

        # 次级控制器在完整层级创建完成后再创建
        self.set_sub_ctrl()

    def set_sub_ctrl(self,*args , **kwargs):
        if self.unset_sub_ctrl is not True:
            return
        if not getattr(self, 'output_grp', None):
            return

        # 每次都从 PyNode 重新取得当前短名称，避免使用重父级之前的旧绝对 DAG 路径。
        transform_obj = self.get_transform()
        if hasattr(transform_obj, 'nodeName'):
            self.ctrl_transform = transform_obj.nodeName()
        else:
            self.ctrl_transform = str(transform_obj).split('|')[-1]

        self.sub_ctrl_name = self.ctrl_transform.replace('ctrl_', 'subctrl_')
        if cmds.objExists(self.sub_ctrl_name):
            self.sub_ctrl = self.sub_ctrl_name
            return

        self.sub_ctrl = Control.create_ctrl(
            name=self.sub_ctrl_name, shape=self.shape, radius=self.radius * 0.5,
            ctrl_color=self.ctrl_color, axis=self.axis, pos=None, parent=self.ctrl_transform,
            lock_attrs=['rotateOrder'], animation_set=self.animation_set,
            unset_sub_ctrl=False, unset_add_extra_group=False)

        if not cmds.attributeQuery('subCtrlVis', node=self.ctrl_transform, exists=True):
            cmds.addAttr(self.ctrl_transform, longName='subCtrlVis', attributeType='bool',
                         defaultValue=False, keyable=True)

        for attr in ['translate', 'rotate', 'scale', 'rotateOrder']:
            src = '{}.{}'.format(self.sub_ctrl, attr)
            dst = '{}.{}'.format(self.output_grp, attr)
            if cmds.objExists(src) and cmds.objExists(dst):
                try:
                    if not cmds.isConnected(src, dst):
                        cmds.connectAttr(src, dst, force=True)
                except RuntimeError:
                    pass

        vis_src = self.ctrl_transform + '.subCtrlVis'
        vis_dst = self.sub_ctrl + '.visibility'
        try:
            if not cmds.isConnected(vis_src, vis_dst):
                cmds.connectAttr(vis_src, vis_dst, force=True)
        except RuntimeError:
            pass

    @staticmethod
    def get_shape_data_dir():
        """返回控制器 Shape JSON/JPG 目录，兼容当前项目常见目录结构。"""
        core_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(core_dir)
        candidates = [
            os.path.join(project_dir, 'MuziTools', 'tools', 'image'),
            os.path.join(project_dir, 'tools', 'image'),
            os.path.join(core_dir, 'tools', 'image'),
        ]
        for path in candidates:
            if os.path.isdir(path):
                return os.path.normpath(path)
        # 默认返回新版项目结构路径；upload 时可自动创建。
        return os.path.normpath(candidates[0])

    # 上传控制器形状的信息到指定路径，并截取控制器形状的图像。
    def upload (self) :
        u"""
        上传控制器形状的信息到指定路径，并截取控制器形状的图像。
        """
        data_path = self.get_shape_data_dir()
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
        data_file = os.path.join (data_path , self.get_transform ().name ().split ("|") [-1] + ".json")
        # 打开并写入带有形状信息的date_file文件，open函数的参数有file_name，access_mode 和 buffering
        ##file_name：file_name变量是一个包含了你要访问的文件名称的字符串值。
        ##access_mode：access_mode决定了打开文件的模式：只读，写入，追加等。所有可取值见如下的完全列表。这个参数是非强制的，
        ## 默认文件访问模式为只读(r)。写入为(w)
        ##buffering:如果buffering的值被设为0，就不会有寄存。如果buffering的值取1，访问文件时会寄存行。
        ##如果将buffering的值设为大于1的整数，表明了这就是的寄存区的缓冲大小。如果取负值，寄存区的缓冲大小则为系统默认。
        with open (data_file , 'w') as fp :
            json.dump (self.get_shape () , fp , indent = 4)

        # 在视图面板中隐藏所有场景信息
        for hud in pm.headsUpDisplay (listHeadsUpDisplays = 1) :
            pm.headsUpDisplay (hud , edit = 1 , vis = False)

        # 创建一个撕下副本的面板用于截图控制器形状，如果创建的撕下副本的面板存在则关闭后重新开启
        panel = 'control_model_panel'
        if not pm.modelPanel (panel , exists = True) :
            pm.modelPanel (panel , tearOff = True , tearOffCopy = 1)

        # 关闭撕下副本视图中所有对象的显示，打开撕下副本视图的 nurbs 曲线显示，关闭撕下副本视图的网格显示。
        pm.modelEditor (panel , edit = 1 , allObjects = 0 , nurbsCurves = 1 , grid = 0)

        # 调整撕下副本视图的焦距，按键F
        pm.setFocus (panel)

        # 复制一个临时的用于截图的控制器，控制器的位置在原点中心
        temp = Control(name='ctrl_tempUpload', shape='circle', radius=1, unset_sub_ctrl=False, unset_add_extra_group=False)
        temp.set_shape (s = self.get_shape ())
        pm.select (temp.get_transform ())

        # 设置用来截图的摄影机的拍摄角度，将摄影机移动到选定对象的中心，指定应设置摄影机位置之间的过渡动画。
        pm.setAttr ('persp.rotate' , -27.938 , 45 , 0)
        pm.viewFit ('persp' , animate = 0)

        # 撕下副本面板开启隔离选择模式，将刚刚选择的需要截图的控制器添加到要显示的对象集中
        pm.isolateSelect (panel , state = 1)
        pm.isolateSelect (panel , addSelected = True)

        # 设定拍屏截图的文件名称和文件路径和拍屏的参数设置
        jpg_path = os.path.join (data_path , self.get_transform ().split ("|") [-1])
        file_name = pm.playblast (format = "image" , filename = jpg_path , c = "jpg" , widthHeight = [256 , 256] ,
                                  startTime = 0 , endTime = 0 , viewer = False , percent = 100 , quality = 100 ,
                                  framePadding = 1)

        # 修改拍屏截图后的保存的文件名称，如果有相同名称的文件存在则删除过去的截图文件
        if os.path.isfile (file_name.replace ("####" , "0")) :
            if os.path.isfile (file_name.replace ("####." , "")) :
                os.remove (file_name.replace ("####." , ""))
            os.rename (file_name.replace ("####" , "0") , file_name.replace ("####." , ""))

        # 关闭撕下副本面板
        if pm.modelPanel (panel , ex = 1) :
            pm.deleteUI (panel , panel = True)

        # 删除用来截图的控制器
        pm.delete (temp.get_transform ())


    # 镜像控制器，将指定控制器的形状信息镜像到当前控制器上。
    def mirror (self , other) :
        u"""
        镜像控制器，将指定控制器的形状信息镜像到当前控制器上。
        :param other: 镜像控制器的目标
        :return:
        """
        self.set_shape (s = other.get_shape ())
        for src_shape , dst_shape in zip (self.get_transform ().getShapes () , other.get_transform ().getShapes ()) :
            for src_cv , dst_cv in zip (src_shape.cv , dst_shape.cv) :
                point = pm.xform (dst_cv , q = 1 , t = 1 , ws = 1)
                point [0] = -point [0]
                pm.xform (src_cv , t = point , ws = 1)


    # 获取控制器形状的数据
    def get_shape (self) :
        u"""

        :return: data
        控制器形状的数据
        """
        return [dict (points = self.get_curve_shape_points (shape) ,
                      degree = shape.degree () ,
                      periodic = shape.form () == 3 ,
                      knot = shape.getKnots ())
                for shape in self.get_transform ().getShapes ()]


    # 获取控制器的transform节点
    def get_transform (self) :
        u"""
         -t -transform string/node/Control 控制器
        :return: transform node
        返回控制器的transform节点
        """
        return self.transform


    # 获取控制器的颜色
    def get_color (self) :
        """
        获得控制器的颜色
        -c - color int : 控制器颜色
        :return:
        """
        c = 0
        for shape in self.get_transform ().getShapes () :
            c = shape.overrideColor.get ()
        return c


    # 获取控制器的半径大小
    def get_radius (self) :
        """
        获得控制器的大小
        -r - radius int : 控制器大小
        :return:
        """
        if len (self.get_transform ().getShapes ()) == 0 :
            return self.get_soft_radius ()
        points = [self.get_curve_shape_points (shape) for shape in self.get_transform ().getShapes ()]
        points = [[[ps [i + j] for j in range (3)] for i in range (0 , len (ps) , 3)] for ps in points]
        lengths = [self.get_length (p , [0 , 0 , 0]) for ps in points for p in ps]
        radius = max (lengths)
        return radius

    def set_control_orientation(self, axis):
        """兼容旧版朝向接口。"""
        self.axis = axis
        self.set_rotate(axis=axis)


    # 基于给定的参数创建控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_ctrl (name ,shape = 'circle' , radius=2 , ctrl_color = 17 ,axis='X+' ,
                     pos = None , parent = None,lock_attrs = None,animation_set = None ,
                     unset_sub_ctrl = True,
                     unset_add_extra_group = True) :
        u"""基于给定的控制器名称创建控制器

        Args:
            name(str/None): 控制器的名称.
            shape (str): 控制器的形状.
            radius(float):控制器形状的大小.
            pos(str) : 被吸附物体的位置,为None的话则生成在坐标原地，或者指定要吸附位置的物体
            axis (str): 控制器的朝向. 'X+'/'X-'/'Y+'/'Y-'/'Z+'/'Z-'
            lock_attrs (list): 要锁定的控制器属性.
            parent (str/None): 控制器的父层级.
            animation_set (str/None): 动画控制器集.



        Raises:
            ValueError: 如果控制器名称已存在.

        Returns:
            str: 控制器的名称

        """


        final_name = name if 'ctrl_' in name else 'ctrl_' + name
        if cmds.objExists(final_name):
            raise ValueError(u'{} 在场景中已存在'.format(final_name))
        else :
            ctrl = Control(name = name ,shape = shape , radius = radius , ctrl_color = ctrl_color,axis=axis ,
                     pos = pos , parent = parent,lock_attrs = lock_attrs,animation_set = animation_set ,
                     unset_sub_ctrl = unset_sub_ctrl,
                     unset_add_extra_group = unset_add_extra_group)

        return ctrl.transform.name() if hasattr(ctrl.transform, 'name') else str(ctrl.transform)


    # 创建fk控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_fk_ctrl (objects) :
        parent = None
        for object in objects :
            ctrl_name = 'ctrl_{}'.format (object)
            ctrl = Control.create_ctrl (ctrl_name , shape = 'hexagon' ,
                                                radius = 4 ,
                                                axis = 'Z+' , pos = object ,
                                                parent = parent)
            # 制作约束
            pipelineUtils.Pipeline.create_constraint (driver = ctrl_name.replace ('ctrl' , 'output') , driven = object ,
                                                      point_value = False , orient_value = False , parent_value = True ,
                                                      scale_value = True ,
                                                      mo_value = True)
            # 指定关节的父层级为上一轮创建出来的控制器层级组
            parent = ctrl_name.replace ('ctrl' , 'output')
        cmds.warning ('创建了{}的fk链条'.format (objects))


    # 删除fk控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def delete_fk_ctrl (objects) :
        for object in objects :
            zero_name = 'zero_{}'.format (object)
            try :
                cmds.delete (zero_name)
                cmds.warning ('已经删除了{}的fk链条'.format (objects))
            except :
                # 已经被删除的情况就返回
                return


    # 创建ik控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_ikspine_ctrl (startIK_jnt , endIK_jnt) :
        u"""
        创建IKspine链的控制器绑定
        Args:
            startjnt(str):ik关节链条的起始关节
            endIK_jnt(bool):ik关节链条的结束关节
            ctrl_number(int):控制器的数量

        Returns: ik_ctrl_grp ：IK控制器的最顶层

        """
        # 获取startjnt底下所有的子物体关节作为列表
        startjnt_child_list = hierarchyUtils.Hierarchy.get_child_object (startIK_jnt , type = 'joint')
        # 获取endIK_jnt在这个关节列表里的索引值
        enjnt_index = startjnt_child_list.index (endIK_jnt)
        # ik关节链则是从0到endIK_jnt关节索引值
        ik_chain = startjnt_child_list [0 :enjnt_index]

        # 创建ik关节链条曲线
        ik_chain_crv = pipelineUtils.Pipeline.create_curve_on_joints (jnt_list = ik_chain ,
                                                                      curve = 'crvIKspine_' + ik_chain [0] ,
                                                                      degree = 3
                                                                      )
        cmds.setAttr (ik_chain_crv + '.visibility' , 0)

        # 创建开始的IK控制器
        startIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + startIK_jnt)
        cmds.matchTransform (startIK_crv_jnt , startIK_jnt , position = True , rotation = True , scale = True)

        startIK_ctrl = 'ctrl_' + startIK_jnt
        startIK_ctrl_obj = Control.create_ctrl (startIK_ctrl , shape = 'hexagon' ,
                                                        radius = 8 ,
                                                        axis = 'Z+' ,
                                                        pos = startIK_jnt , parent = None)
        startIK_ctrl_output = startIK_ctrl.replace ('ctrl_' , 'output_')
        startIK_zero = startIK_ctrl.replace ('ctrl_' , 'zero_')
        cmds.parent (startIK_crv_jnt , startIK_ctrl_output)
        cmds.setAttr (startIK_crv_jnt + '.visibility' , 0)

        # 创建尾端的ik控制器
        endIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + endIK_jnt)
        cmds.matchTransform (endIK_crv_jnt , endIK_jnt , position = True , rotation = True , scale = True)
        endIK_ctrl = 'ctrl_' + endIK_jnt
        endIK_ctrl_obj = Control.create_ctrl (endIK_ctrl , shape = 'Cube' , radius = 4 , axis = 'Y+' ,
                                                      pos = endIK_jnt , parent = None)
        endIK_ctrl_output = endIK_ctrl.replace ('ctrl_' , 'output_')
        endIK_zero = endIK_ctrl.replace ('ctrl_' , 'zero_')
        cmds.parent (endIK_crv_jnt , endIK_ctrl_output)
        cmds.setAttr (endIK_crv_jnt + '.visibility' , 0)

        #
        # 创建中间的ik控制器
        midIK_jnt = ik_chain [len (ik_chain) // 2]
        midIK_crv_jnt = cmds.createNode ('joint' , name = 'crvjnt_' + midIK_jnt)
        cmds.matchTransform (midIK_crv_jnt , midIK_jnt , position = True , rotation = True , scale = True)
        midIK_ctrl = 'ctrl_' + midIK_jnt
        midIK_ctrl_obj = Control.create_ctrl (midIK_ctrl , shape = 'Cube' , radius = 4 , axis = 'Y+' ,
                                                      pos = midIK_jnt , parent = None)
        midIK_ctrl_output = midIK_ctrl.replace ('ctrl_' , 'output_')
        cmds.parent (midIK_crv_jnt , midIK_ctrl_output)
        cmds.setAttr (midIK_crv_jnt + '.visibility' , 0)
        midIK_zero = midIK_ctrl.replace ('ctrl_' , 'zero_')

        # 曲线关节对ikspine曲线进行蒙皮
        cmds.skinCluster (startIK_crv_jnt , midIK_crv_jnt , endIK_crv_jnt , ik_chain_crv , tsb = True)

        # 曲线对ik关节做ik样条线手柄
        spine_ikhandle_node = \
            cmds.ikHandle (curve = ik_chain_crv , startJoint = ik_chain [0] , endEffector = ik_chain [-1] ,
                           solver = 'ikSplineSolver' , createCurve = 0 ,
                           name = 'ikhandle_' + startIK_jnt) [0]

        # 创建loc来制作ikhandle的横向旋转
        startIK_loc = cmds.spaceLocator (name = 'loc_' + startIK_jnt) [0]
        endIK_loc = cmds.spaceLocator (name = 'loc_' + endIK_jnt) [0]

        cmds.matchTransform (startIK_loc , startIK_jnt , position = True , rotation = True , scale = True)
        cmds.parent (startIK_loc , startIK_ctrl_output)
        cmds.matchTransform (endIK_loc , endIK_jnt , position = True , rotation = True , scale = True)
        cmds.parent (endIK_loc , endIK_ctrl_output)

        # 设置ikhandle的高级扭曲属性用来设置横向旋转
        cmds.setAttr (spine_ikhandle_node + '.dTwistControlEnable' , 1)
        cmds.setAttr (spine_ikhandle_node + '.dWorldUpType' , 4)
        cmds.connectAttr (startIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrix')
        cmds.connectAttr (endIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrixEnd')
        cmds.setAttr (spine_ikhandle_node + '.visibility' , 0)

        # 整理层级结构
        ik_ctrl_grp = cmds.createNode ('transform' , name = "grpIKspine_" + ik_chain [0])
        cmds.parent (spine_ikhandle_node , ik_chain_crv , startIK_zero , midIK_zero , endIK_zero , ik_ctrl_grp)

        # 添加拉伸效果
        # 获取ikspine曲线的形状节点
        ik_chain_crv_shape = cmds.listRelatives (ik_chain_crv , shapes = True) [0]

        # 创建curveinfo节点来获取ikspine曲线的长度
        curveInfo_node = cmds.createNode ('curveInfo' , name = 'crvInfo_' + ik_chain_crv)
        cmds.connectAttr (ik_chain_crv_shape + '.worldSpace' , curveInfo_node + '.inputCurve')
        ik_chain_crv_value = cmds.getAttr (curveInfo_node + '.arcLength')

        # 创建一个相加节点来获取ikspine曲线变换的数值
        add_curveInfo_node = cmds.createNode ('addDoubleLinear' , name = 'add_' + ik_chain_crv)
        cmds.connectAttr (curveInfo_node + '.arcLength' , add_curveInfo_node + '.input1')
        cmds.setAttr (add_curveInfo_node + '.input2' , ik_chain_crv_value * -1)

        # 创建一个相乘节点，来将变换的数值平均分配给每个关节
        mult_curveInfo_node = cmds.createNode ('multDoubleLinear' , name = 'mult_' + ik_chain_crv)
        cmds.connectAttr (add_curveInfo_node + '.output' , mult_curveInfo_node + '.input1')
        cmds.setAttr (mult_curveInfo_node + '.input2' , 0.25)

        # 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
        cmds.addAttr (endIK_ctrl , longName = 'stretch' , attributeType = 'double' ,
                      niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)

        # 根据对应的关节创建对应的相加节点，将变换后的数值连接到对应的关节上
        for jnt in ik_chain [1 :-1] :
            add_node = cmds.createNode ('addDoubleLinear' , name = 'add_' + jnt)
            cmds.connectAttr (mult_curveInfo_node + '.output' , add_node + '.input1')
            cmds.setAttr (add_node + '.input2' , cmds.getAttr (jnt + '.translateX'))
            # 创建blendcolor节点用来承载拉伸的设置
            blend_node = cmds.createNode ('blendColors' , name = 'blend_' + jnt)
            cmds.connectAttr (endIK_ctrl + '.stretch' , blend_node + '.blender')
            # 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 的值是原关节的长度
            cmds.setAttr (blend_node + '.color2R' , cmds.getAttr (jnt + '.translateX'))
            # 连接拉伸后的关节长度
            cmds.connectAttr (add_node + '.output' , blend_node + '.color1R')
            # 把混合后的关节长度连接给原关节
            cmds.connectAttr (blend_node + '.outputR' , jnt + '.translateX')


    # 删除ik控制器
    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def delete_ik_ctrl (objects) :
        for object in objects :
            grp_name = 'grpIKspine_{}'.format (object)
            try :
                cmds.delete (grp_name)
                cmds.warning ('已经删除了{}的ik链条'.format (objects))
            except :
                # 已经被删除的情况就返回
                return


    # 获取参数值
    @staticmethod
    def get_arg (args) :
        if len (args) > 0 :
            return args [0]
        return None


    # 获取控制器形状节点的曲线点位置信息
    @staticmethod
    def get_curve_shape_points (shape) :
        return pm.xform (shape.cv , q = 1 , t = 1)


    # 返回软选择的范围
    @staticmethod
    def get_soft_radius () :
        u"""
        ssd (float): 衰减半径
        return:返回软选择的范围
        """
        return pm.softSelect (query = 1 , ssd = 1)


    # 获取两点之间的距离
    @staticmethod
    def get_length (point1 , point2) :
        u"""
        point1[float,float,float]: 点1的坐标(x,y,z)
        point2[float,float,float]: 点2的坐标(x,y,z)
        return: 两点之间的距离
        原理：两点之间的距离等于两点之间x，y，z相减的和的平方再开方
        ((x1-x2)**2 +(y1-y2)**2 + (z1-z2)**2)**0.5
        ** 表示平方，**0.5表示开方
        """
        distance = sum ([(point1 [i] - point2 [i]) ** 2 for i in range (3)]) ** 0.5
        return distance


    # 获取选择的控制器
    @classmethod
    def selected (cls) :
        u"""
         [Control(), ]
        选择的控制器
        """
        return [cls(name=t.name(), shape=None, unset_sub_ctrl=False, unset_add_extra_group=False) for t in pm.selected(type="transform")]


    # 批量修改选择的控制器
    @classmethod
    def set_selected (cls , **kwargs) :
        u"""
        :param kwargs: 修改控制器的参数
        批量修改选择的控制器
        """
        selected = cls.selected ()
        for control in selected :
            control.set (**kwargs)
        pm.select ([control.get_transform () for control in selected])


    # 镜像两个选择的控制器
    @classmethod
    def mirror_selected (cls) :
        u"""
        镜像两个选择的控制器
        :return:
        """
        selected = cls.selected ()
        if not len (selected) == 2 :
            return
        src , dst = selected
        src.mirror (dst)


    # 删除形状
    @classmethod
    def delete_shape (cls , *args , **kwargs) :
        """
        删除形状
        :return:
        """
        s = kwargs.get ("s" , kwargs.get ("shape" , cls.get_arg (args)))
        if s is None :
            return
        json_path = os.path.join(cls.get_shape_data_dir(), '{}.json'.format(s))
        if os.path.isfile (json_path) :
            os.remove (json_path)
        jpg_path = os.path.join(cls.get_shape_data_dir(), '{}.jpg'.format(s))
        if os.path.isfile (jpg_path) :
            os.remove (jpg_path)


    # 批量删除形状
    @classmethod
    def delete_shapes (cls , *args) :
        """
        批量删除形状
        :return:
        """
        for s in args :
            cls.delete_shape (s)


    # 创建ribbon控制器
    @staticmethod
    def create_ribbon (name , control_parent , jnt_number = 5) :
        """
        创建ribbon控制器，给动画师更细致的动画效果
        思路：通过给定关节的名称来创建ribbon控制，通过曲线来生成曲面制作ribbon绑定，然后让生成的关节绑定在曲面上
        采用的变形器有twist，sine和wire变形器，通过这些变形器影响曲面，从而带动曲面上的关节

        Args:
            ribbon.side (str): ribbon's ribbon.side
            ribbon.description (str): ribbon's ribbon.description
            ribbon.index (int): ribbon's ribbon.index
            jnt_number (int): how many joints need to be attached to the ribbon, default is 9
            control_parent:

        """
        # 从名称中获取ribbon控制器的边，描述，和编号
        ribbon = nameUtils.Name (name = name)

        # 从ribbon控制器中的边获取偏移值
        if ribbon.side != 'r' :
            offset_val = 1
        else :
            offset_val = -1

        # 创建ribbon控制器对应的层级组
        ribbon_grp = cmds.createNode ('transform' ,
                                      name = 'grp_{}_{}Ribbon_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                              ribbon.index))
        ribbon_ctrl_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonCtrls_{:03d}'.format (ribbon.side ,
                                                                                        ribbon.description ,
                                                                                        ribbon.index) ,
                                           parent = ribbon_grp)
        ribbon_jnt_grp = cmds.createNode ('transform' ,
                                          name = 'grp_{}_{}RibbonJnts_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                      ribbon.index) ,
                                          parent = ribbon_grp)
        nodes_local_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonNodesLocal_{:03d}'.format (ribbon.side ,
                                                                                             ribbon.description ,
                                                                                             ribbon.index) ,
                                           parent = ribbon_grp)
        nodes_world_grp = cmds.createNode ('transform' ,
                                           name = 'grp_{}_{}RibbonNodesWorld_{:03d}'.format (ribbon.side ,
                                                                                             ribbon.description ,
                                                                                             ribbon.index) ,
                                           parent = ribbon_grp)
        cmds.setAttr (nodes_world_grp + '.inheritsTransform' , 0)

        cmds.setAttr (nodes_local_grp + '.visibility' , 0)
        cmds.setAttr (nodes_world_grp + '.visibility' , 0)

        # 创建对应的曲线以生成nurbs曲面
        temp_curve = cmds.curve (point = [[-5 * offset_val , 0 , 0] , [5 * offset_val , 0 , 0]] , knot = [0 , 1] ,
                                 degree = 1)
        # 根据关节数重建曲线
        cmds.rebuildCurve (temp_curve , degree = 3 , replaceOriginal = True , rebuildType = 0 , endKnots = 1 ,
                           keepRange = 0 ,
                           keepControlPoints = False , keepEndPoints = True , keepTangents = False ,
                           spans = jnt_number + 1)
        # 复制这条曲线
        temp_curve_02 = cmds.duplicate (temp_curve) [0]
        # 移动两条曲线的位置来制作曲面
        cmds.setAttr (temp_curve + '.translateZ' , 1)
        cmds.setAttr (temp_curve_02 + '.translateZ' , -1)

        # 通过两条曲线来放样制作曲面
        surf = \
            cmds.loft (temp_curve_02 , temp_curve , constructionHistory = False , uniform = True , degree = 3 ,
                       sectionSpans = 1 ,
                       range = False , polygon = 0 ,
                       name = 'surf_{}_{}Ribbon_{:03d}'.format (ribbon.side , ribbon.description , ribbon.index)) [0]
        cmds.parent (surf , nodes_local_grp)

        # 获得曲面的形状节点
        surf_shape = cmds.listRelatives (surf , shapes = True) [0]

        # 删除用来放样曲面的曲线
        cmds.delete (temp_curve , temp_curve_02)

        # 创建关节并附着到曲面
        fol_grp = cmds.createNode ('transform' ,
                                   name = 'grp_{}_{}RibbonFollicles_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                    ribbon.index) ,
                                   parent = nodes_world_grp)

        # 创建ribbon关节的集合
        ribbon_jnt_set = 'set_ribbonJnt'
        make_ribbon_jnt_set = 'set_' + ribbon.side + '_' + ribbon.description + 'Jnt'
        make_ribbon_jnt_set = cmds.sets (name = make_ribbon_jnt_set , empty = True)
        if not cmds.objExists (ribbon_jnt_set) or cmds.nodeType (ribbon_jnt_set) != 'objectSet' :
            ribbon_jnt_set = cmds.sets (name = ribbon_jnt_set , empty = True)
            cmds.sets (make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)
        else :
            cmds.sets (make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)

        for i in range (jnt_number) :
            # 创建毛囊
            fol_shape = cmds.createNode ('follicle' , name = 'fol_{}_{}Ribbon{:03d}_{:03d}Shape'.format (ribbon.side ,
                                                                                                         ribbon.description ,
                                                                                                         i + 1 ,
                                                                                                         ribbon.index))
            # 重命名毛囊的tran节点名称
            fol = cmds.listRelatives (fol_shape , parent = True) [0]
            fol = cmds.rename (fol , fol_shape [:-5])
            # 把毛囊放入对应的层级组
            cmds.parent (fol , fol_grp)
            # 连接毛囊属性
            cmds.connectAttr (surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
            # 连接毛囊的形状节点以进行变换
            cmds.connectAttr (fol_shape + '.outTranslate' , fol + '.translate')
            cmds.connectAttr (fol_shape + '.outRotate' , fol + '.rotate')
            # 设置uv值
            cmds.setAttr (fol_shape + '.parameterU' , 0.5)
            cmds.setAttr (fol_shape + '.parameterV' , float (i) / (jnt_number - 1))

            # 创建关节
            jnt = cmds.createNode ('joint' ,
                                   name = 'jnt_{}_{}Ribbon{:03d}_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                                 i + 1 ,
                                                                                 ribbon.index))
            parent_grp = ribbon_jnt_grp
            grp_nodes = []
            for node_type in ['zero' , 'offset'] :
                grp = cmds.createNode ('transform' , name = jnt.replace ('jnt' , node_type) , parent = parent_grp)
                grp_nodes.append (grp)
                parent_grp = grp

            cmds.parent (jnt , grp_nodes [-1])
            # 让对应的毛囊约束对应的关节点
            cmds.parentConstraint (fol , grp_nodes [0] , maintainOffset = False)
            # 将偏移组的旋转设置为零
            cmds.xform (grp_nodes [1] , rotation = [0 , 0 , 0] , worldSpace = True)

            # 将生成的ribbon关节放在对应的集里方便选择
            cmds.sets (jnt , edit = True , forceElement = make_ribbon_jnt_set)

        # 创建控制器
        ctrls = []
        for pos in ['start' , 'mid' , 'end'] :
            ctrl_name = 'ctrl_{}_{}{}_{:03d}'.format (ribbon.side , ribbon.description , pos.title () , ribbon.index)
            ctrl = Control.create_ctrl (ctrl_name , shape = 'hexagon' , radius = 5 ,
                                        axis = 'Z+' ,
                                        pos = jnt , parent = ribbon_ctrl_grp)

            ctrls.append (ctrl_name)
        # 放置控制器
        cmds.setAttr (ctrls [0].replace ('ctrl' , 'zero') + '.translateX' , -5 * offset_val)
        cmds.setAttr (ctrls [1].replace ('ctrl' , 'zero') + '.translateX' , 5 * offset_val)

        # 约束中间的控制器
        cmds.pointConstraint (ctrls [0] , ctrls [-1] , ctrls [1].replace ('ctrl' , 'driven') , maintainOffset = False)

        # 添加twist的控制属性在第一个控制器和最后一个控制器上,'start'和 'end'
        cmds.addAttr (ctrls [0] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        cmds.addAttr (ctrls [-1] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        # 创建twist变形器
        twist_node , twist_hnd = cmds.nonLinear (surf , type = 'twist' , name = surf.replace ('surf_' , 'twist_'))
        cmds.parent (twist_hnd , nodes_local_grp)
        cmds.setAttr (twist_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr (twist_hnd + '.scaleX')
        cmds.setAttr (twist_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        # 连接twist变形器的属性到控制器上
        twist_hnd_shape = cmds.listRelatives (twist_hnd , shapes = True) [0]
        cmds.connectAttr (ctrls [0] + '.twist' , twist_node + '.endAngle')
        cmds.connectAttr (ctrls [-1] + '.twist' , twist_node + '.startAngle')

        # 添加sine的控制属性在中间的控制器上,'mid'
        cmds.addAttr (ctrls [1] , longName = 'sineDivider' , niceName = u'sine变形器属性设置 ----------' ,
                      attributeType = 'enum' ,
                      enumName = ' ' , keyable = False)
        cmds.setAttr (ctrls [1] + '.sineDivider' , channelBox = True , lock = True)
        cmds.addAttr (ctrls [1] , longName = 'amplitude' , niceName = u'振幅' , attributeType = 'float' ,
                      keyable = True ,
                      minValue = 0)
        cmds.addAttr (ctrls [1] , longName = 'wavelength' , niceName = u'波长' , attributeType = 'float' ,
                      keyable = True ,
                      minValue = 0.1 ,
                      defaultValue = 2)
        cmds.addAttr (ctrls [1] , longName = 'offset' , niceName = u'偏移' , attributeType = 'float' , keyable = True)
        cmds.addAttr (ctrls [1] , longName = 'sineRotation' , niceName = u'正弦旋转' , attributeType = 'float' ,
                      keyable = True)
        # 创建sine变形器
        sine_node , sine_hnd = cmds.nonLinear (surf , type = 'sine' , name = surf.replace ('surf_' , 'sine_'))
        cmds.parent (sine_hnd , nodes_local_grp)
        cmds.setAttr (sine_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr (sine_hnd + '.scaleX')
        cmds.setAttr (sine_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        cmds.setAttr (sine_node + '.dropoff' , 1)
        # 连接sine变形器的属性到控制器上
        sine_hnd_shape = cmds.listRelatives (sine_hnd , shapes = True) [0]
        cmds.connectAttr (ctrls [1] + '.amplitude' , sine_node + '.amplitude')
        cmds.connectAttr (ctrls [1] + '.wavelength' , sine_node + '.wavelength')
        cmds.connectAttr (ctrls [1] + '.offset' , sine_node + '.offset')
        cmds.connectAttr (ctrls [1] + '.sineRotation' , sine_hnd + '.rotateY')

        # 创建wire变形器
        # 创建wire变形器需要的曲线
        wire_curve = cmds.curve (point = [[-5 * offset_val , 0 , 0] , [0 , 0 , 0] , [5 * offset_val , 0 , 0]] ,
                                 knot = [0 , 0 , 1 , 1] ,
                                 degree = 2 ,
                                 name = 'crv_{}_{}RibbonWire_{:03d}'.format (ribbon.side , ribbon.description ,
                                                                             ribbon.index))
        wire_curve_shape = cmds.listRelatives (wire_curve , shapes = True) [0]
        cmds.rename (wire_curve_shape , wire_curve + 'Shape')
        cmds.parent (wire_curve , nodes_world_grp)

        # 创建cluster 变形器，用控制器来约束cluster变形器的变化
        for ctrl , i in zip (ctrls , [0 , 1 , 2]) :
            cls_node , cls_hnd = cmds.cluster ('{}.cv[{}]'.format (wire_curve , i) ,
                                               name = ctrl.replace ('ctrl' , 'cls'))
            cmds.parent (cls_hnd , nodes_world_grp)
            cmds.pointConstraint (ctrl , cls_hnd , maintainOffset = False)

        # 创建wire变形器
        wire_node = surf.replace ('surf' , 'wire')
        cmds.wire (surf , wire = wire_curve , name = wire_node)
        cmds.setAttr (wire_node + '.dropoffDistance[0]' , 200)
        cmds.parent (wire_curve + 'BaseWire' , nodes_local_grp)

        # control = 'control'
        # joint = 'joint'
        # rigNode_Local = 'rigNode_Local'
        # rigNode_World = 'rigNode_World'
        cmds.parent (ribbon_ctrl_grp , control_parent)
        # cmds.parent(ribbon_jnt_grp, joint)
        # cmds.parent(nodes_local_grp, rigNode_Local)
        # cmds.parent(nodes_world_grp, rigNode_World)
        # cmds.delete(ribbon_grp)

        return ribbon_grp , ribbon_ctrl_grp , ribbon_jnt_grp , nodes_local_grp , nodes_world_grp




    @staticmethod
    @pipelineUtils.Pipeline.make_undo
    def create_ik_crv_ctrl_rig(crv_name,part = 'test',unrebuild_crv_value = False,jnt_number = 10):
        """
        给定曲线后，根据曲线上的点数量来创建关节点和控制器(也可自定义重建曲线点的数量)
        整体的控制为ik型
        最底下的main控制器是总组，上面有数值可以修改驱动的控制器比例多少
        crv_name(str):给定的曲线名称
        part(str):最后生成的绑定组名称描述
        unrebuild_crv_value(bool):是否需要重建曲线
        jnt_number(int):生成的关节点数量和控制器数量



        """
        #检查给定的曲线是否存在于场景里，没有的话则报错
        if not cmds.objExists (crv_name) :
            cmds.error (u"场景里不存在：{}".format (crv_name))
        else:
            #存在于场景里可以进行创建曲线和控制器
            #先判断曲线是否需要重建
            #当曲线需要重建的时候，点的数量就根据给定的来，
            if unrebuild_crv_value  :
                cmds.rebuildCurve (
                    crv_name ,
                    constructionHistory = False ,
                    replaceOriginal = True ,
                    rebuildType = 0 ,
                    endKnots = True ,
                    keepRange = 0 ,
                    keepControlPoints = False ,
                    keepEndPoints = True ,
                    keepTangents = False ,
                    spans = spans ,
                    degree = 3 ,
                    tolerance = 0.01
                )


