# coding=utf-8

'''
用Python代码生成一面砖墙

最好使用Pymel
如果没有时间写出完整代码,可以提交psudo code
有额外时间的同学可以考虑怎样在墙体上留下窗洞
要求：

砖墙形状为圆柱体的侧面
每一块砖由一个独立的polyCube组成
在代码开头定义几个参数，比如高度，半径，在运行之前，通过修改这些参数可以决定生成之后的砖墙有多高，半径有多大
提交代码及相关截图。
'''
import pymel.core as pm


def create_generate_cylinder(layers = 5, height = 1.5, radius = 10):
    """
    height(float):生成砖墙的polyCube的层数
    height(float):生成砖墙的polyCube的高度
    redaius(float):生成砖墙的半径
    """
    # 创建需要的polycube
    polycube_list = []
    locator_node = pm.spaceLocator()
    modle_grp = pm.createNode('transform',name = 'geo_m_mesh_001')
    for index in range(layers):
        pCube_node = pm.polyCube()[0]
        pCube_node.translate.set([0, height*index, radius])
        pCube_node.scaleY.set(height)
        pCube_node.setParent(modle_grp)
        pm.makeIdentity(pCube_node,apply = True,t = 1,r = 1,s =1,n = 0 ,pn =1)
        for i in range(72):
            # 进行特殊复制
            dur_node = pm.duplicate(pCube_node, returnRootsOnly = True)[0]
            pm.matchTransform(dur_node, locator_node, pivots = True)
            dur_node.rotateY.set(5 * i)
            dur_node.setParent(modle_grp)
            pm.makeIdentity(dur_node,apply = True,t = 1,r = 1,s =1,n = 0 ,pn =1)

create_generate_cylinder(layers =5, height = 1.5, radius = 10)