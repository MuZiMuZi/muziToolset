from muziToolset.res.ui.bind_modular import bind_widget
from importlib import reload
reload(bind_widget)

window = bind_widget.BindSystemWindow()
window.show()