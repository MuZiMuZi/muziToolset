# coding=utf-8

u"""
这是一个用来编写权重工具的基本类

目前已有的功能：

 save_skinWeights：       将蒙皮几何体对象的权重保存到给定权重文件夹，权重将保存在对象短名称下，并附加存储其蒙皮影响的文件
 ik_chain_rig：创建ik链的控制器绑定

bind_chain_rig:创建混合IKFk链的bind链控制器绑定
"""
import json
import os

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

from . import pipelineUtils


class Weights (object) :

    def __init__ (self , geo) :
        """
        geo(str) : 需要进行蒙皮操作的物体
        """
        self.geo = geo

        # 初始化权重文件夹路径,创建权重文件夹
        self._init_file_path ()

        # 初始权重文件的路径，将权重文件放在对应的文件夹下
        self._init_skin_folder ()

        # 初始化模型为一个pymel对象
        self.geo_pynode = pm.PyNode (self.geo)


    # 初始化权重文件夹路径 , 创建权重文件夹
    def _init_file_path (self) :
        """
        初始化权重文件夹路径,创建权重文件夹
        """
        # 获取打开的maya文件的路径信息
        self.current_file_path = cmds.file (q = True , location = True)
        if not self.current_file_path :
            cmds.warning ("未打开任何Maya文件。")
            return

        # 提取文件夹和文件名
        self.folder_path , self.file_name = os.path.split (self.current_file_path)

        # 在文件夹旁边创建名为 "文件名_skin" 的文件夹,用来整理保存权重文件
        self.skin_folder_name = "{}_skin".format (self.file_name)
        self.skin_folder_path = os.path.join (self.folder_path , self.skin_folder_name)

        # 检查文件夹是否已存在，如果不存在则创建
        if not os.path.exists (self.skin_folder_path) :
            os.makedirs (self.skin_folder_path)
            print (f"成功创建文件夹：{self.skin_folder_name}，路径为：{self.skin_folder_path}")
        else :
            pass


    # 初始权重文件的路径，将权重文件放在对应的文件夹下
    def _init_skin_folder (self) :
        """
        初始权重文件的路径，将权重文件放在对应的文件夹下
        """
        # 规定蒙皮权重文件和关节影响文件的后缀名
        self.weightsFileExt = '.xml'
        self.influencesFileExt = '.infs'

        # 设定蒙皮权重导出的文件名
        self.skinWeights_FileName = 'sc_' + self.geo + self.weightsFileExt
        self.skinWeights_Path = self.skin_folder_path

        # 设定关节影响导出的文件名
        self.influences_FileName = 'sc_' + self.geo + self.influencesFileExt
        self.influences_Path = os.path.join (self.skin_folder_path , self.influences_FileName)


    # 选择物体，导出保存的权重文件
    def save_skinWeights (self) :
        u'''
       将蒙皮几何体对象的权重保存到给定权重文件夹，权重将保存在对象短名称下，并附加存储其蒙皮影响的文件
        :return:
        '''
        # 查询物体是否有蒙皮节点，没有的话报错
        self.skin_node = self.get_skin_node ()

        if not self.skin_node :
            cmds.warning (u'{}这个物体没有蒙皮节点'.format (self.geo))
        else :
            skin_node = self.skin_node [0]
            # 导出蒙皮权重
            cmds.deformerWeights (self.skinWeights_FileName , path = self.skinWeights_Path , export = True ,
                                  deformer = skin_node)

            # 保存影响的权重
            influences = cmds.skinCluster (skin_node , q = True , inf = True)
            influences_file = open (self.influences_Path , mode = 'w')
            json.dump (influences , influences_file , sort_keys = True , indent = 4 , separators = (',' , ': '))


    # 选择物体，读取保存的权重文件
    def load_skinWeights (self) :
        u'''
       从给定权重文件夹加载蒙皮几何体对象的权重将从与对象短名称匹配的文件名加载权重，并添加其他文件以获取其影响
        :return:
        '''
        # 查询物体是否有蒙皮节点
        self.skin_node = self.get_skin_node ()

        # 如果物体本身就具有蒙皮节点的话则先删除原本的蒙皮节点
        if self.skin_node :
            cmds.delete (self.skin_node)

        # 判断物体导出权重的的文件路径是否存在，如果不存在的话则报错
        if not os.path.exists (self.skinWeights_Path) :
            cmds.warning (u'{}这个物体没有导出权重的文件'.format (self.geo))
            return
        # 判断物体导出权重关节影响的文件路径是否存在，如果不存在的话则报错
        if not os.path.exists (self.influences_Path) :
            cmds.warning (u'{}这个物体没有导出权重关节影响的文件'.format (self.geo))
            return

        # 获得关节影响
        influences_file = open (self.influences_Path , mode = 'rb')
        influences_Str = influences_file.read ()
        influences = json.loads (influences_Str)
        influences_file.close ()

        # 创建关节蒙皮
        skin_node = cmds.skinCluster (self.geo , influences , tsb = True) [0]

        # 获取蒙皮权重
        cmds.deformerWeights (self.skinWeights_FileName , path = self.skinWeights_Path , im = True ,
                              deformer = skin_node)
        cmds.warning (u'{}这个物体导入权重成功'.format (self.geo))


    # 复制权重，先选择需要复制的蒙皮权重物体，再加选需要复制权重的物体
    @staticmethod
    def copy_weight () :
        u'''

        Returns:复制权重，先选择需要复制的蒙皮权重物体，再加选需要复制权重的物体

        '''
        # 获取选择
        sel = cmds.ls (selection = True)

        source_mesh = sel [0]
        target_meshes = sel [1 :]

        # 查询目标对象是否具有蒙皮信息
        for target_mesh in target_meshes :
            target_skin = mel.eval ('findRelatedSkinCluster("' + target_mesh + '")')
            if target_skin :
                cmds.delete (target_skin)

        # 获取源对象的蒙皮信息
        source_skin = mel.eval ('findRelatedSkinCluster("' + source_mesh + '")')

        # 获取源对象受影响的蒙皮信息
        source_joints = cmds.skinCluster (source_skin , query = True , influence = True)

        # 在每个目标对象中循环
        for target_mesh in target_meshes :
            # 用源关节绑定蒙皮
            target_skin = cmds.skinCluster (source_joints , target_mesh , toSelectedBones = True) [0]

            # 复制蒙皮权重
            cmds.copySkinWeights (sourceSkin = source_skin , destinationSkin = target_skin , noMirror = True ,
                                  surfaceAssociation = 'closestPoint' , influenceAssociation = ['label' , 'oneToOne'])
            #
            # # 重命名对象蒙皮
            # cmds.select (sel)
            # pipelineUtils.Pipeline.rename_bs_sc ()


    # 批量重命名对象的蒙皮和混合变形节点
    @staticmethod
    def rename_bs_sc () :
        u'''
        批量重命名对象的蒙皮和混合变形节点
        '''
        geos = cmds.ls (sl = True)
        for geo in geos :
            geo_shape = cmds.listRelatives (geo , shapes = True)
            sc = cmds.listConnections (geo_shape , type = 'skinCluster')
            if sc :
                cmds.rename (sc , 'sc_{}'.format (geo))
            bs = cmds.listConnections (geo_shape , type = 'blendShape')
            if bs :
                cmds.rename (bs , 'bs_{}'.format (geo))

    # 获取物体的蒙皮节点信息
    def get_skin_node (self) :
        """
        获取物体的蒙皮节点信息，返回蒙皮节点
        """

        # 查询物体是否有蒙皮节点，没有的话报错
        history = cmds.listHistory (self.geo)
        self.skin_node = cmds.ls (history , type = 'skinCluster')
        # 如果蒙皮节点存在，则返回出蒙皮节点
        if self.skin_node :
            return self.skin_node
        # 如果不存在则提出报错，物体没有蒙皮节点
        else :
            cmds.warning (u'{}这个物体没有蒙皮节点'.format (self.geo))
            return None


    # 获取物体的蒙皮节点的关节信息
    def get_skin_node_jnt (self) :
        self.skin_node_nt = pm.PyNode (self.skin_node)
        self.all_weight_joints = pm.skinCluster (self.skin_node_nt , q = True , wi = True)

        return self.all_weight_joints


    # 重命名物体的蒙皮节点名称
    def rename_skin_node (self) :
        self.skin_node = self.get_skin_node ()
        if self.skin_node :
            self.skin_node = cmds.rename (self.skin_node , 'sc_{}'.format (self.geo))


    # 使用线变形的方式来生成链式关节的蒙皮信息
    @pipelineUtils.Pipeline.make_undo
    def set_deformer_skin (self , jnt_list) :
        """
        使用线变形的方式来生成链式关节的蒙皮信息，适用于有规律的条状物体，布料状物体等，可以刷手臂的链式关节权重。
        jnt_list(list):需要绘制权重的关节列表
        思路：
        1.根据需要绘制权重的关节列表创建一根吸附的曲线
        2.将需要绘制权重的模型所选择的点或边制作一个简模出来，作为用以线变形的模型
        3.曲线对简模进行线变形
        4.模拟模型上的点的位置信息位移，模拟成为权重值
        5.将权重值设置到对应的关节上

        """
        # 1.根据需要绘制权重的关节列表创建一根吸附的曲线
        self.skin_curve_name = 'skinCurve_' + self.geo
        self.skin_curve = pipelineUtils.Pipeline.create_curve_on_joints (jnt_list , self.skin_curve_name , degree = 3)

        # 2.将需要绘制权重的模型所选择的点或边制作一个简模出来，作为用以线变形的模型
        # 复制一个模型出来用于制作简模
        self.skin_geo = pipelineUtils.Pipeline.copy_surface_create_geo ()

        # 3.曲线对简模进行线变形
        # 控制器曲线对蒙皮曲线做wire变形，让控制器曲线控制蒙皮曲线,注意如果是两条曲线做wire变形器的话，被控制的曲线需要给个w参数
        self.wire_node = cmds.wire (self.skin_curve , w = self.skin_geo , gw = False , en = 1.000000 , ce = 0.000000 ,
                                    li = 0.000000) [0]
        cmds.setAttr (self.wire_node + '.dropoffDistance[0]' , 200)

        # 获取模型上的所有的点
        self.skin_geo_nt = pm.PyNode (self.skin_geo)

        count_vertex = pm.polyEvaluate (self.skin_geo_nt , v = True)
        # 获取所有蒙皮骨骼
        self.all_weight_joints = self.get_skin_node_jnt ()
