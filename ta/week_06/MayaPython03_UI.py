# coding=utf-8
import maya.mel as mel
import pymel.core as pm


def setIsolateView(onOff):
    mel.eval('enableIsolateSelect modelPanel4 {}'.format(onOff))


class IsoViewer:
    '''
    :type win : pm.ui.Window
    :type form : pm.ui.FormLayout
    :type btn : pm.ui.iconTextButton
    '''

    def __init__(self):
        self.winName = 'IsolateSelectTool'
        self.title = 'Isolate Tool'
        self.icon = 'nodeGrapherSoloed.svg'
        self.width = 200
        self.height = 200
        self.create_Ui()

    def lockWindow(self, *args):
        self.width = self.win.getWidth()
        self.height = self.win.getHeight()
        self.win.setSizeable(False)
        self.win.setTitleBarMenu(False)
        self.win.setTitleBar(False)
        self.win.setWidthHeight([self.width, self.height])

    def unlockWindow(self, *args):
        self.win.setSizeable(True)
        self.win.setTitleBarMenu(True)
        self.win.setTitleBar(True)

    def close(self, *args):
        self.win.delete()

    def setImg(self, *args):
        if mel.eval('isolateSelect -q -state modelPanel4'):
            self.icon = 'nodeGrapherSoloed.svg'
        else:
            self.icon = 'nodeGrapherUnsoloed.svg'
        self.btn.setImage1(self.icon)

    def setIsolate(self, *args):
        seled = [s for s in pm.selected(type = 'transform')if s.getShape()]
        if not seled:
            pm.warning('No shape object detected.Please select an object with shapes.')
        setIsolateView(1 if seled else 0)
        self.setImg()

    def create_Ui(self):
        if pm.window(self.winName, exists = True):
            pm.deleteUI(self.winName, window = True)
        self.win = pm.window(self.winName, title = self.title, width = self.width, height = self.height)
        with pm.formLayout() as self.form:
            self.btn = pm.iconTextButton(style = 'iconOnly', command = self.setIsolate)
            self.setImg()
            with pm.popupMenu():
                pm.menuItem(label = 'lock', image = 'lockGeneric.png', command = self.lockWindow)
                pm.menuItem(label = 'unLock', image = 'unlockGeneric.png', command = self.unlockWindow)
                pm.menuItem(label = 'close', image = 'closeTabButton.png', command = self.close)
        # pm.formLayout(
        #     self.form,edit = True,
        #     attachForm = [
        #         (self.btn,'top',5),
        #         (self.btn, 'bottom', 5),
        #         (self.btn, 'left', 5),
        #         (self.btn, 'right', 5)
        #     ]
        # )
        self.form.attachForm(self.btn.name(), 'top', 5)
        self.form.attachForm(self.btn.name(), 'bottom', 5)
        self.form.attachForm(self.btn.name(), 'left', 5)
        self.form.attachForm(self.btn.name(), 'right', 5)
        self.win.show()

        self.win.setSizeable(True)
        self.win.setTitleBarMenu(True)
        self.win.setTitleBar(True)


ik = IsoViewer()
