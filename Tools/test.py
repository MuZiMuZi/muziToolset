import muziToolset.Tools.Tool_main as Tool_main

from importlib import reload


reload (Tool_main)

try :
    window.close ()  # 关闭窗口
    window.deleteLater ()  # 删除窗口
except :
    pass
window = Tool_main.Tool_main_Window ()  # 创建实例
window.show ()  # 显示窗口