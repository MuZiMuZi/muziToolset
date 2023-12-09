# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds
from importlib import reload
from . import qtUtils
import os
import json


class File (object) :
    """
    对于文件操作的类
    """


    def __init__ (self , file_path) :
        self.file_path = file_path
        # 设置文件的选择类型过滤器
        self.file_filter = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项

        self.selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值


    def show_file_select_dialog (self) :
        '''
        打开文件资源浏览器
        '''
        # 打开一个文件资源浏览器，file_path 是所选择的文件路径,selected_filter是选择过滤的文件类型
        self.file_path , self.selected_filter = QtWidgets.QFileDialog.getOpenFileName (qtUtils.get_maya_window () ,
                                                                                       "Select File" , "" ,
                                                                                       self.file_filter ,
                                                                                       self.selected_filter)
        return self.file_path


    def load_file (self , load_method) :
        """
        读取文件
        load_method(str):三种不同的读取方式，open,import,reference
        """
        # 检查文件路径是否存在，如果不存在则返回
        if not self.file_path :
            return
        # 判断给定的文件路径是否正确有对应的文件
        file_info = QtCore.QFileInfo (self.file_path)
        if not file_info.exists () :
            om.MGlobal.displayError ('这个路径的文件不存在：{}'.format (self.file_path))
            return

        # 根据读取方式读取对应的文件
        self.load_method = load_method
        if self.load_method == 'open' :
            self.open_file ()
        elif self.load_method == 'import' :
            self.import_file ()
        else :
            self.reference_file ()


    def open_file (self) :
        force = False
        # 弹出一个对话框来让用户确认是否已经保存文件
        if not force and cmds.file (q = True , modified = True) :
            result = QtWidgets.QMessageBox.question (qtUtils.get_maya_window () , "提示" ,
                                                     "当前场景有未保存的更改。是否确定打开新文件？")
            if result == QtWidgets.QMessageBox.StandardButton.Yes :
                force = True
            else :
                return
        cmds.file (self.file_path , open = True , ignoreVersion = True , force = force)


    def import_file (self) :
        cmds.file (self.file_path , i = True , ignoreVersion = True)


    def reference_file (self) :
        cmds.file (self.file_path , r = True , ignoreVersion = True)


    @staticmethod
    def export_animation () :
        """
        选择所有需要导出动画的控制器导出动画,来源37佬
        """

        # 获取所有控制器的列表
        ctrlList = cmds.ls (sl = True)

        # 初始化动画数据字典
        animData = {}

        # 对列表中的每个控制器执行循环
        for ctrl in ctrlList :
            attributes = []
            allAttrs = cmds.listAttr (ctrl)
            cbAttrs = cmds.listAnimatable (ctrl)
            if allAttrs and cbAttrs :
                orderedAttrs = [attr for attr in allAttrs for cb in cbAttrs if cb.endswith (attr)]
                attributes.extend (orderedAttrs)
            # print(orderedAttrs)
            # 对列表中的每个属性执行循环
            for attr in orderedAttrs :
                # 获取属性的关键帧信息
                keyframeInfo = cmds.keyframe (ctrl , attribute = attr , query = True , timeChange = True ,
                                              valueChange = True)
                # 将关键帧信息存储到动画数据字典中
                animData [ctrl + "." + attr] = keyframeInfo

        # 使用 json.dumps 函数将动画数据存储在 JSON 文件中
        fpath1 = r"D:\animation.json"

        with open (fpath1 , "w") as f :
            f.write (json.dumps (animData))


    @staticmethod
    def import_animation () :
        """
        根据json文件里的动画来导入动画文件测试,来源37佬
        """

        # 从文本文件中读取动画数据并赋予 blendshape B
        project_root = os.path.dirname (__file__)
        fpath1 = os.path.abspath (__file__ + "/../animation.json")

        # Open the file and read the JSON data
        with open (fpath1 , "r") as f :
            data = f.read ()

        # Load the JSON data into a Python dictionary
        animData = json.loads (data)

        # 遍历字典中的每个属性
        for attr , keyframeInfo in animData.items () :
            # 使用 keyframe 命令将关键帧数据添加到控制器中
            if keyframeInfo == None :
                continue

            for i in range ((int (len (keyframeInfo) / 2))) :
                #   print(len(keyframeInfo))
                x = attr.split ('.' , 1)
                ctrl = x [0]
                attrX = x [1]
                if i == 0 :
                    if cmds.objExists (ctrl) :
                        cmds.setKeyframe (ctrl , at = attrX , time = (keyframeInfo [0] , keyframeInfo [0]) ,
                                          value = keyframeInfo [1])
                else :
                    if cmds.objExists (ctrl) :
                        cmds.setKeyframe (ctrl , at = attrX ,
                                          time = (int (keyframeInfo [i * 2]) , int (keyframeInfo [i * 2])) ,
                                          value = keyframeInfo [i * 2 + 1])

        # 获取第 10 帧到第 20 帧之间的关键帧信息

        #  keyframeInfo = cmds.keyframe(ctrl, attribute=attr, query=True, time=(keyframeInfo[0], keyframeInfo[2]), timeChange=True, valueChange=True)


    # 获取当前文件的绝对路径
    @staticmethod
    def get_current_scene_path () :
        u'''
        获取当前文件的绝对路径
        :return:
        '''
        return str (pm.sceneName ().abspath ()).replace ('\\' , '/')


    # 在maya里的当前文件创建引用,给定需要引用的文件路径和设置引用文件的名称空间
    def create_reference (self , name_space = None) :
        u'''
        在maya里的当前文件创建引用
        :param self.file_path: 需要引用的文件路径
        :param name_space: 引用文件的名称空间
        :return:
        '''
        if name_space is None :
            name_space = os.path.basename (self.file_path).split ('.') [0].upper ()
        try :
            pm.Namespace (name_space).remove ()
        except :
            pass
        # 设定引用的文件的组名，对应的引用文件放在这个组下
        grp_name = get_group_name (name_space)

        # 引用文件设置
        ref_node = pm.createReference (self.file_path ,
                                       namespace = name_space ,
                                       loadReferenceDepth = 'all' ,
                                       groupReference = True ,
                                       groupName = grp_name)

        return ref_node , pm.Namespace (name_space) , grp_name


    # 在 Maya 中导出所选物体为 FBX 文件的脚本,接受一个目标路径self.file_path参数。该路径指定了导出的 FBX 文件的保存位置。
    def fbxExport (self) :
        u"""
        在 Maya 中导出所选物体为 FBX 文件的脚本,接受一个目标路径self.file_path参数。该路径指定了导出的 FBX 文件的保存位置。
        : self.file_path: 该路径指定了导出的 FBX 文件的保存位置。
        :return:
        """
        # 将目标路径的反斜杠 \ 替换为正斜杠 /。
        path_string = self.file_path.replace ('\\' , '/')
        try :
            # 尝试创建目标路径的父目录，以确保导出路径存在。
            path (self.file_path).parent.makedirs_p ()
            # 使用 Mel 脚本命令 FBXExport 将所选物体导出为 FBX 文件，指定导出文件的路径。
            mel.eval (f'FBXExport -f "{path_string}" -s')
            # 在成功导出时，打印成功消息，并输出导出的物体列表。
            print (f'Export succeeded. {pm.selected ()} -> {path_string}')
        # 在导出失败时，打印错误消息和异常信息。
        except Exception as e :
            print ('Export failed. ' + path_string)
            print (e)


def text () :
    """
    对于文件操作的例子
    """
    path = 'D:/rig/701Car_Rig/701_car_Rig_003Constraint.mb'
    file_obj = fileUtils.File (path)

    file_obj.load_file ('open')
