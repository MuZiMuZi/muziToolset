import muziToolset.MuziTools.rigging_toolbox as rigging_toolbox

from importlib import reload


reload (rigging_toolbox)

try :
    window.close ()  # 关闭窗口
    window.deleteLater ()  # 删除窗口
except :
    pass
window = rigging_toolbox.main ()  # 创建实例
