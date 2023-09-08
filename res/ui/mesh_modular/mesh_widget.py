# coding=utf-8
u"""
这是一个完整的maya材质工具实例

目前已有的功能：

●选择一个或者多个物体，可以选择自动展示所有材质,或者手动载入并展示
●选择组，可以选择示所有子物体的材质
●选择对象自动保存在场景中
●按材质选择时，可以灵活切换添加选择与覆盖选择两种模式
●工具设置保存在工具中,关闭Maya或者重新打开文件后不会丢失
各物体上的材质按照组动态展示
●每个按钮上的labeI与材质节点名相同,且显示面数
●窗口可以浮动显示，可以吸附到侧边栏
●自动记录日志
●当材质数量改变，或者被重命名,或者模型被更改，或者shading engine
members发生改变时，可以通过手动刷新看到新的列表

"""

import maya.cmds as cmds

class Selector:
    """
    这个工具可以根据材质来选择模型不同的面
    """
    def __init__(self):
        self.winTitle = 'Select_mesh_Face'
        self.winName = 'MeshSelectTool'

    def init_ui(self):
        """
        创建ui界面
        """
        if window(self.winName)