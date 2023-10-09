from importlib import reload

from muziToolset.pyside import  open_Importdialog



reload (open_Importdialog)

try :
    test_dialog.close ()
    test_dialog.deleteLater ()
except :
    pass

test_dialog = open_Importdialog.OpenImportDialog ()
test_dialog.show ()
