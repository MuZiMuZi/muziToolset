from importlib import reload

from muziToolset.pyside import dialog



reload(dialog)

t = dialog.TestDialog()
t.show()
