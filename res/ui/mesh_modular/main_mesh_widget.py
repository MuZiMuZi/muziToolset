import muziToolset.res.ui.mesh_modular.mesh_widget as mesh_widget

from importlib import reload

reload(mesh_widget)
print(10)

Tool = mesh_widget.Selector_tool()
Tool.init_ui()