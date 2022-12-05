# coding=utf-8
u"""
这是一个命名类。用来对命名进行一系列修改的操作。

目前已有的功能：

根据所给的类型—边-描述-编号，整合名称：name
根据所给的名称拆分为，类型—边-描述-编号：compose
自动翻转命名的边：flip
替换新的名称：set_rename
添加前缀：add_prefix
添加后缀：add_suffix
返回选择的物体下所有的子层级的节点命名：_selection_list_nodes
添加层级前缀：add_hierarchy_prefix
添加层级后缀：add_hierarchy_suffix
根据关键字搜索替换名称：search_replace_name
根据正则表达式搜索替换名称：regex_search_replace_name
检查并列出场景里所有重名的物体：print_duplicate_object
检查并修改场景里所有重名的物体：rename_duplicate_object

"""
from __future__ import print_function

import re

import maya.cmds as cmds


class Name(object):
    """
    This is a docstring
    """

    def __init__(self, name = None, type = None, side = None, resolution = None, description = None, index = None):
        """

        Returns:
            object:
        """
        self.nodes = []
        self._type = type
        self._side = side
        self._resolution = resolution
        self._description = description
        self._index = index

        self._name = name

        if self._name:
            self.decompose()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        self._side = value

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def name(self):
        self.compose()
        return self._name

    def compose(self):
        self._name = ''

        # loop in each part and add to node name
        for name_part in [self._type, self._side, self._resolution, self._description]:
            if name_part:
                self._name += '{}_'.format(name_part)

        # add index
        self._name = '{}{:03d}'.format(self._name, self._index)

    def decompose(self):
        name_parts = self._name.split('_')

        self._type = name_parts[0]
        self._side = name_parts[1]
        if len(name_parts) == 5:
            self._resolution = name_parts[2]
        else:
            self._resolution = None
        self._description = name_parts[-2]
        self._index = int(name_parts[-1])

    def flip(self):
        if self._side == 'l':
            self._side = 'r'
        elif self._side == 'r':
            self._side = 'l'

    def set_rename(self, new_name):
        names = cmds.ls(sl = True)
        for self._name in names:
            self._name = self._name.split("|")[-1]
            cmds.rename(self._name, new_name)

    def add_prefix(self, prefix):
        """
        添加前缀名称
        Args:
            prefix(str): 前缀名称

        Returns:

        """
        names = cmds.ls(sl = True)
        for self._name in names:
            # 让新的节点名字加上前缀
            object_name = self._name.split("|")[-1]
            new_object_name = prefix+object_name
            # 重命名节点
            cmds.rename(self._name, new_object_name)


    def add_suffix(self, suffix):
        """
        添加后缀名称
        Args:
            suffix(str): 后缀名称

        Returns:
            Object name after modification
        """
        names = cmds.ls(sl = True)
        for self._name in names:
            # 让新的节点名字加上前缀
            object_name = self._name.split("|")[-1]
            new_object_name = object_name+suffix
            # 重命名节点
            cmds.rename(self._name, new_object_name)

    def _selection_list_nodes(self):
        """
        Returns: 返回选择的物体下所有的子层级的节点命名

        """
        selected = cmds.ls(sl = True)
        self.nodes = self.nodes + selected
        for select in selected:
            self.nodes = self.nodes + cmds.listRelatives(select, allDescendents = True, children = True)

        return self.nodes

    def add_hierarchy_prefix(self, prefix):
        """
        添加层级前缀名称
        Args:
            prefix（str）:前缀名

        Returns:

        """
        self.nodes = self._selection_list_nodes()
        for node in self.nodes:
            cmds.rename(node, prefix + node)

    def add_hierarchy_suffix(self, suffix):
        """
        添加层级后缀名称
        Args:
            suffix（str）:后缀名

        Returns:

        """
        self.nodes = self._selection_list_nodes()
        for node in self.nodes:
            cmds.rename(node, node + suffix)

    def search_replace_name(self, search, replace):
        """
            搜索替换对应的名称
        Args:
            search: 搜索的名称
            replace:替换的名称

        Returns:

        """
        names = cmds.ls(sl = True)
        for self._name in names:
            search_name = self._name.split("|")[-1]
            cmds.rename(search_name, search_name.replace(search, replace))

    def regex_search_replace_name(self, search, replace):
        re_o = re.compile(search)
        for uid in self._selection_list_nodes():
            self._name = cmds.ls(uid)[0]
            search_name = self._name.split("|")[-1]
            cmds.rename(self._name, re_o.sub(replace, search_name))

    @staticmethod
    def print_duplicate_object():
        u'''
        检查并列出场景里重名的物体
        '''
        all_object = cmds.ls(visible = 1)
        duplicate_object_list = []
        for i in all_object:
            if '|' in i:
                if i.count('|')>1:
                    duplicate_object_list.append(i)
                    cmds.warning(u'场景里有重名的物体{}'.format(i))
        if len(duplicate_object_list) == 0:
            cmds.warning(u'场景里没有重名的物体')
        return duplicate_object_list

    @staticmethod
    def rename_duplicate_object():
        u'''
        检查并重命名场景内所有重名的物体
        '''
        duplicate_object_list = Name.print_duplicate_object()
        # 定义一个计数器
        count = 0
        for duplicate_object in duplicate_object_list:
            # 将计数器加1
            count += 1
            # 让新的节点名字加上计数器
            object_name = duplicate_object.split("|")[-1]
            new_object_name = object_name + '_{:03d}'.format(count)
            # 重命名节点
            cmds.rename(duplicate_object, new_object_name)

