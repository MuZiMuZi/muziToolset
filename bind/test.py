from muziToolset.bind.Bind_Tool_main import Bind_Tool_main
from importlib import reload
reload(Bind_Tool_main)

try :
    win.close ()  # 为了不让窗口出现多个，因为第一次运行还没初始化，所以要try，在这里尝试先关闭，再重新新建一个窗口
    win.deleteLater ()
except :
    pass
win = Bind_Tool_main.Bind_Widget ()
win.show ()
