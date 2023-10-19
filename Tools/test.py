import muziToolset.tools.Tool_main as Tool_main

from importlib import reload


reload (Tool_main)

try :
    window.close ()  # 关闭窗口
    window.deleteLater ()  # 删除窗口
except :
    pass
window = Tool_main.TemplateWindow ()  # 创建实例
window.show ()  # 显示窗口