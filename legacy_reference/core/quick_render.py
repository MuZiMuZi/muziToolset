import os
import maya.mel as mel
"""
给定一个文件目录，快速对文件目录内的所有maya文件进行渲染
"""

def get_type_file (data_path , file_type = ['ma' , 'mb'] , data_file_list = None , with_path = False) :
    """
    根据给定的文件类型。获取目录及子目录下所有文件名或者文件路径
    :param data_path: 给定的文件目录
    :param file_type: 文件类型,可以为列表或者字符串
    :param data_file_list: 返回的文件名或路径
    :param with_path: 是否返回路径
    :return: 文件名或文件路径
    """
    if data_file_list is None :
        data_file_list = []
    # 当文件类型是字符穿的时候，
    if file_type is not None :
        if not isinstance (file_type , list) :
            file_type = [file_type]
    # 获取文件目录下所有的文件
    data_files = os.listdir (data_path)
    for data_file in data_files :
        data_file_path = os.path.join (data_path , data_file)
        if os.path.isdir (data_file_path) :
            get_type_file (data_file_path , file_type , data_file_list , with_path)
        else :
            if file_type is None :
                if with_path :
                    data_file_list.append (data_file_path)
                else :
                    data_file_list.append (data_file)
            else :
                # 判断文件的文件类型是否符合给定的文件类型，如果符合的话则添加到data_file_list列表里
                _ , data_file_type = os.path.splitext (data_file)
                data_file_type = data_file_type.split ('.') [-1]
                if data_file_type in file_type :
                    if with_path :
                        data_file_list.append (data_file_path)
                    else :
                        data_file_list.append (data_file)
    return data_file_list


# 给定文件夹路径
folder_path = 'D:\\test'

# 获取需要的maya文件
folder_list = get_type_file (folder_path , file_type = ['ma' , 'mb'] , data_file_list = None , with_path = True)

# 对获取的maya列表文件做循环,引用进来渲染
for folder in folder_list :
    cmds.file (folder , r = True , ignoreVersion = True)

    # 进行渲染设置
    # 渲染设置是一个节点
    render_glob = "defaultRenderGlobals"
    # 设置图像文件的前缀为引用的文件名称
    folder_name = folder.split ('\\') [-1]
    cmds.setAttr (render_glob + '.imageFilePrefix' , folder_name , type = "string")

    # 图像文件路径的设置需要在渲染设置里自行更改
    # 进行渲染,渲染当前帧
    mel.eval ("renderWindowRenderCamera redoPreviousRender renderView persp;")
    # 渲染完成后，移除引用文件
    cmds.file (folder , removeReference = True)
