import muziToolset.tools.Names_Tool_main as Names_Tool_main
from importlib import reload
reload(Names_Tool_main)
try:
    name_tool.close()
    name_tool.deleteLater ()
except :
    pass
name_tool = Names_Tool_main.Names_Tool_main()

name_tool.show()

