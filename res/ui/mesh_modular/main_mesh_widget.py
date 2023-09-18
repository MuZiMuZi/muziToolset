import muziToolset.res.ui.mesh_modular.mesh_widget as mesh_widget
from pymel.core import workspaceControl
from importlib import reload

reload(mesh_widget)
print(10)


Tool = mesh_widget.Selector_tool()

if workspaceControl(Tool.winTitle ,exists=True):
    workspaceControl(Tool.winTitle, edit=True,close = True)
workspaceControl(Tool.winTitle,retain = False,floating = True, uiScript = 'Tool.init_ui()')
