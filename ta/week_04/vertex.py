import pymel.core as pm

from pprint import pprint
from  pymel.core import dt
import os.path

def export_vertex(vertices,file_name):
    "导出选择的点的位置信息"
    v_dict = dict()

    for v in vertices:
        #判断v的类型如果不是点的话就取消获取信息
        if type(v) is not pm.general.MeshVertex:
            continue
        i = v.index()
        v_dict[i] = v.getPosition(space = 'world')

    #如何获取当前文件的文件路径 __file__
    # 如何获取当前文件的文件夹路径 os.path.dirname(__file__)
    folder_path = os.path.dirname(__file__).replace('\\','/')
    file_path = folder_path + '/{}.vtx'.format(file_name)

    with open(file_path,'w') as f:
        f.write(repr(v_dict))

    return file_path

def import_vertex(mesh,file_name):
    '''导入模型对应的点的位置信息'''
    # 判断给定的mesh的类型是否为mesh
    if type(mesh) is not pm.nt.Transform or not pm.nt.Mesh:
        return
    # 如何获取当前文件的文件路径 __file__
    # 如何获取当前文件的文件夹路径 os.path.dirname(__file__)
    folder_path = os.path.dirname(__file__).replace('\\', '/')
    file_path = folder_path + '/{}.vtx'.format(file_name)

    with open(file_path, 'r') as f:
        str_dict = f.readline()
        vert_dict = eval(str_dict)
        for i,p in vert_dict:
            mesh.vtx[i].setPositon(p ,space = 'world')

    return  file_path



# # 用法
# export_vertex(pm.selected(flatten = True),'vetex_01')
# import_vertex(pm.selected()[0],'vetex_01')