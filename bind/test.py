import muziToolset.bind.Bind_Tool_main as Bind_Tool_main
import reload
reload(Bind_Tool_main)

try :
    bind_Tool.close ()
    bind_Tool.deleteLater ()
except :
    pass
bind_Tool = Bind_Tool_main.Bind_Tool ()

bind_Tool.show ()