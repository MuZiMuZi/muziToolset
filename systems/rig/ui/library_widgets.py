# coding=utf-8
u"""绑定库的轻量绘制组件。矢量装饰随窗口缩放，不依赖外部图片或字体文件。"""

try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance


Qt = QtCore.Qt


def module_icon(color, code=""):
    u"""绘制统一的线框模块图标，替代依赖系统字体的特殊字符图标。"""
    pixmap = QtGui.QPixmap(40, 40)
    pixmap.fill(Qt.transparent)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.setPen(QtGui.QPen(QtGui.QColor(color), 1.7))
    painter.setBrush(QtGui.QColor("#f3f6ee"))
    points = [(20, 4), (33, 12), (33, 28), (20, 36), (7, 28), (7, 12), (20, 4)]
    polygon = QtGui.QPolygonF()
    for x, y in points:
        polygon.append(QtCore.QPointF(x, y))
    painter.drawPolygon(polygon)
    painter.drawLine(7, 12, 20, 20)
    painter.drawLine(33, 12, 20, 20)
    painter.drawLine(20, 20, 20, 36)
    painter.end()
    return QtGui.QIcon(pixmap)


class ArtHeader(QtWidgets.QFrame):
    u"""页眉中的工业线条与酸橙色装饰，文字由普通 Qt 控件负责。"""

    def paintEvent(self, event):
        super(ArtHeader, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor("#e1f385"))
        polygon = QtGui.QPolygonF()
        for x, y in [(width - 345, height), (width - 225, 0), (width - 135, 0), (width - 255, height)]:
            polygon.append(QtCore.QPointF(x, y))
        painter.drawPolygon(polygon)
        painter.setPen(QtGui.QPen(QtGui.QColor("#d4d9cc"), 1))
        for index in range(8):
            x = width - 440 + index * 47
            painter.drawLine(x, height, x + 130, 0)
        painter.setPen(QtGui.QPen(QtGui.QColor("#9bab79"), 1))
        for index in range(4):
            x = width - 385 + index * 65
            painter.drawLine(x - 5, 18, x + 5, 18)
            painter.drawLine(x, 13, x, 23)
        painter.end()


class StepButton(QtWidgets.QPushButton):
    u"""顶部五步导航，以清晰数字和切角高亮呈现当前操作阶段。"""

    def __init__(self, number, title, subtitle, parent=None):
        super(StepButton, self).__init__(parent)
        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.setObjectName("WorkflowStep")
        self.setCheckable(True)
        self.setMinimumWidth(155)
        self.setFixedHeight(78)
        self.setAccessibleName("{} {} {}".format(number, title, subtitle))
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        color = "#e1f680" if self.isChecked() else "#fbfcf8"
        painter.fillRect(rect, QtGui.QColor(color))
        painter.setPen(QtGui.QPen(QtGui.QColor("#dce0d4"), 1))
        painter.drawLine(rect.right(), 0, rect.right() - 38, rect.bottom())
        text_color = "#26312b" if self.isEnabled() else "#a9afa8"
        painter.setPen(QtGui.QColor(text_color))
        number_font = QtGui.QFont("Georgia", 29)
        number_font.setItalic(True)
        painter.setFont(number_font)
        painter.drawText(QtCore.QRect(13, 12, 59, 49), Qt.AlignCenter, "{:02d}".format(self.number))
        title_font = QtGui.QFont("Georgia", 12)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(QtCore.QRect(77, 17, rect.width() - 78, 23), Qt.AlignLeft | Qt.AlignVCenter, self.title)
        painter.setFont(QtGui.QFont("Microsoft YaHei UI", 9))
        painter.drawText(QtCore.QRect(77, 42, rect.width() - 80, 18), Qt.AlignLeft | Qt.AlignVCenter, self.subtitle)
        if self.isChecked():
            painter.setPen(QtGui.QPen(QtGui.QColor("#4f6034"), 1))
            painter.drawLine(78, 66, rect.width() - 31, 66)
        if self.hasFocus():
            painter.setPen(QtGui.QPen(QtGui.QColor("#769523"), 2))
            painter.drawRect(rect.adjusted(2, 2, -3, -3))
        painter.end()


class TickBox(QtWidgets.QCheckBox):
    u"""为酸橙色选中框补充明确勾号，同时保留 Qt 的键盘和辅助功能。"""

    def paintEvent(self, event):
        super(TickBox, self).paintEvent(event)
        if not self.isChecked():
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        color = "#374c23" if self.isEnabled() else "#82906d"
        painter.setPen(QtGui.QPen(QtGui.QColor(color), 1.7))
        middle = self.height() // 2
        painter.drawLine(4, middle, 7, middle + 3)
        painter.drawLine(7, middle + 3, 13, middle - 4)
        painter.end()


class Section(QtWidgets.QWidget):
    u"""可折叠属性抽屉，折叠时释放空间。"""

    def __init__(self, title, parent=None):
        super(Section, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.button = QtWidgets.QToolButton()
        self.button.setText(title)
        self.button.setProperty("role", "section")
        self.button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.button.setArrowType(Qt.DownArrow)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.body = QtWidgets.QWidget()
        self.form = QtWidgets.QFormLayout(self.body)
        self.form.setContentsMargins(12, 12, 12, 14)
        self.form.setSpacing(9)
        self.form.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        layout.addWidget(self.button)
        layout.addWidget(self.body)
        self.button.toggled.connect(self.set_expanded)

    def set_expanded(self, expanded):
        u"""同步标题箭头和属性区可见性。"""
        self.body.setVisible(expanded)
        self.button.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
