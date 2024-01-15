# coding:utf-8
import json
import os

import maya.cmds as cmds
from PySide2 import QtCore
from PySide2 import QtWidgets

from . import qtUtils


class File (object) :
    """
    文件操作的类
    """


    def __init__ (self , file_path = None) :
        self.file_path = file_path
        # 设置文件的选择类型过滤器
        self.file_filter = "Maya(*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"  # 全部的过滤项
        self.selected_filter = "Maya (*.ma *.mb)"  # 记录选择的过滤项，每次更改过滤项的同时会更改这个全局变量的值


    def show_file_select_dialog (self) :
        '''
        打开文件资源浏览器，让用户选择文件
        '''
        # 打开一个文件资源浏览器，file_path 是所选择的文件路径,selected_filter是选择过滤的文件类型
        self.file_path , self.selected_filter = QtWidgets.QFileDialog.getOpenFileName (
            qtUtils.get_maya_window () ,
            "选择文件" , "" ,
            self.file_filter ,
            self.selected_filter
        )
        return self.file_path


    def load_file (self , load_method) :
        """
        读取文件
        load_method(str): 三种不同的读取方式，open, import, reference
        """
        # 检查文件路径是否存在，如果不存在则返回
        if not self.file_path :
            return

        # 判断给定的文件路径是否正确有对应的文件
        file_info = QtCore.QFileInfo (self.file_path)
        if not file_info.exists () :
            cmds.warning ('文件不存在：{}'.format (self.file_path))
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
            result = QtWidgets.QMessageBox.question (
                qtUtils.get_maya_window () ,
                "提示" ,
                "当前场景有未保存的更改。是否确定打开新文件？" ,
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if result == QtWidgets.QMessageBox.StandardButton.Yes :
                force = True
            else :
                return
        cmds.file (self.file_path , open = True , ignoreVersion = True , force = force)


    def import_file (self) :
        # 导入文件
        cmds.file (self.file_path , i = True , ignoreVersion = True)


    def reference_file (self) :
        """
        引用文件
        """
        cmds.file (self.file_path , r = True , ignoreVersion = True)


    def load_from_given_path (self) :
        try :
            # 读取JSON文件
            with open (self.file_path , "r") as file :
                json_data = file.read ()
            # 解析JSON数据
            self.anim_data = json.loads (json_data)
            cmds.warning ("成功加载动画数据：{}".format (self.anim_data))
        except Exception as e :
            cmds.warning ("加载动画数据时发生错误：{}".format (str (e)))

        return self.anim_data


    # 导出所选控制器的动画到 JSON 文件

    def export_animation_json (self) :
        """
        导出所选控制器的动画到 JSON 文件
        来源: 37佬
        """

        # 获取所有选择的控制器列表
        ctrl_list = cmds.ls (sl = True)

        # 初始化动画数据字典
        anim_data = {}

        # 对每个控制器执行循环
        for ctrl in ctrl_list :
            attributes = []
            all_attrs = cmds.listAttr (ctrl)
            cb_attrs = cmds.listAnimatable (ctrl)
            if all_attrs and cb_attrs :
                ordered_attrs = [attr for attr in all_attrs for cb in cb_attrs if cb.endswith (attr)]
                attributes.extend (ordered_attrs)

            # 对每个属性执行循环
            for attr in ordered_attrs :
                # 获取属性的关键帧信息
                keyframe_info = cmds.keyframe (ctrl , attribute = attr , query = True , timeChange = True ,
                                               valueChange = True)
                # 将关键帧信息存储到动画数据字典中
                anim_data [ctrl + "." + attr] = keyframe_info

        # 如果指定了需要保存json文件的路径的话，则保存在对应的路径下
        # 没有指定文件路径的话则保存在当前打开的maya文件的同路径下
        if self.file_path :
            # 写入JSON数据到文件
            with open (self.file_path , "w") as file :
                file.write (json.dumps (anim_data))
        else :
            current_file_path = cmds.file (q = True , sceneName = True)
            # 构建保存JSON文件的路径，命名为'animation.json'
            self.file_path = os.path.join (os.path.dirname (current_file_path) , 'animation.json')
            # 写入JSON数据到文件
            with open (self.file_path , "w") as file :
                file.write (json.dumps (anim_data))
            cmds.warning ("成功导出动画数据为json放置在maya的同路径下。")


    # 从 JSON 文件导入动画数据并应用到相应的控制器
    def import_animation_json (self) :
        """
        从 JSON 文件导入动画数据并应用到相应的控制器
        """
        """
          从 JSON 文件导入动画数据并应用到相应的控制器
          """
        # 判断是否给定了动画数据JSON文件的路径名称
        if self.file_path :
            # 从指定路径加载JSON文件的参数
            self.anim_data = self.load_from_given_path ()
        else :
            # 获取当前Maya文件的路径
            current_file_path = cmds.file (q = True , sceneName = True)
            json_file_path_in_current_folder = os.path.join (os.path.dirname (current_file_path) , 'animation.json')

            # 判断动画数据JSON文件是否在Maya文件的同路径下存在
            if os.path.exists (json_file_path_in_current_folder) :
                # 从当前Maya文件路径下的JSON文件加载参数
                self.file_path = json_file_path_in_current_folder
                self.anim_data = self.load_from_given_path ()
            else :
                cmds.warning ("未找到动画数据JSON文件，请指定正确的路径或确保JSON文件与Maya文件在同一目录下。")
                return

        # 遍历字典中的每个属性
        for attr , keyframe_info in self.anim_data.items () :
            # 使用 keyframe 命令将关键帧数据添加到控制器中
            if keyframe_info is None :
                continue

            for i in range (int (len (keyframe_info) / 2)) :
                x = attr.split ('.' , 1)
                ctrl = x [0]
                attr_x = x [1]
                if i == 0 :
                    if cmds.objExists (ctrl) :
                        cmds.setKeyframe (ctrl , at = attr_x , time = (keyframe_info [0] , keyframe_info [0]) ,
                                          value = keyframe_info [1])
                else :
                    if cmds.objExists (ctrl) :
                        cmds.setKeyframe (ctrl , at = attr_x ,
                                          time = (int (keyframe_info [i * 2]) , int (keyframe_info [i * 2])) ,
                                          value = keyframe_info [i * 2 + 1])


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


    # 从 JSON 文件导入动画数据并应用到相应的控制器，测试动画的导入
    def import_test_animation_json (self) :
        """
        从 JSON 文件导入动画数据并应用到相应的控制器，进行测试动画的导入
        """
        """
          从 JSON 文件导入动画数据并应用到相应的控制器
          """
        #指定测试动画的路径
        self.file_path = r'C:\Users\lixin\Documents\maya\scripts\muziToolset\core\animation.json'

        #导入测试动画
        self.import_animation_json()

def text () :
    """
    对于文件操作的例子
    """
    path = 'D:/rig/701Car_Rig/701_car_Rig_003Constraint.mb'
    file_obj = fileUtils.File (path)

    file_obj.load_file ('open')
