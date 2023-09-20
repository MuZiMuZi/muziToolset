import muziToolset.tools.Joint_Tool_main as Joint_Tool_main
from pymel.core import workspaceControl
from importlib import reload
reload(Joint_Tool_main)

Tool = Joint_Tool_main.Joint_Tool ()

if workspaceControl (Tool.win_title , exists = True) :
    workspaceControl (Tool.win_title , edit = True , close = True)

workspaceControl (Tool.win_title , retain = False , floating = True , uiScript = 'Tool.init_ui()')


