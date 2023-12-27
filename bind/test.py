from importlib import reload

import muziToolset.bind.Bind_Tool_main as Bind_Tool_main


reload (Bind_Tool_main)

try :
    win.close ()
    win.deleteLater ()
except :
    pass
win = Bind_Tool_main.Bind_Widget ()
win.show ()
