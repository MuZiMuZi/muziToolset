import muziToolset.bind.Bind_Tool_main as Bind_Tool_main
from importlib import reload
reload(Bind_Tool_main)

try :
    win.close ()
    win.deleteLater ()
except :
    pass
win = Bind_Tool_main.Bind_Widget ()
win.show ()
