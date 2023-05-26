from importlib import reload

from muziToolset.pyside import dialog



reload(dialog)

try :
	test_dialog.close()
	test_dialog.deleteLater()
except :
	pass

test_dialog = dialog.TestDialog()
test_dialog.show()
