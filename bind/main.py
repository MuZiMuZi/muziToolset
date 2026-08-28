# 导入模块
from importlib import reload

# 导入绑定工具主模块
import muziToolset.bind.Bind_Tool_main as Bind_Tool_main


# 重新加载主模块，以便应用最新修改
reload (Bind_Tool_main)

# 尝试关闭和删除现有窗口
try :
    win.close ()
    win.deleteLater ()
except :
    # 如果关闭或删除失败，忽略异常
    pass

# 创建并显示绑定工具主窗口
win = Bind_Tool_main.Bind_Widget ()
win.show ()
