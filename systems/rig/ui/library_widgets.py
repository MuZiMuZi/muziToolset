# coding=utf-8
u"""绑定库的轻量绘制组件。矢量装饰随窗口缩放，不依赖外部图片或字体文件。"""

try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance


Qt = QtCore.Qt


# -----------------------------------------------------------------------------
# Shared palette
# -----------------------------------------------------------------------------
INK = "#232a27"
MUTED = "#8a9089"
LINE = "#d9ddd5"
PAPER = "#fbfbf7"
LIME = "#d7ef49"
LIME_SOFT = "#edf6bd"
LIME_DARK = "#617126"


def module_icon(color, code=""):
    u"""
    绘制统一的线框模块图标。

    图标保持低饱和线框风格；模块列表的真正强调色由选中状态负责，避免
    每个模块同时使用高饱和颜色导致视觉层级混乱。

    Args:
        color (str):
            模块提供的基础颜色。仅作为轻微识别色使用。
        code (str):
            保留给后续模块类型图形区分使用。

    Returns:
        QIcon:
            40 x 40 的矢量风格图标。
    """
    pixmap = QtGui.QPixmap(40, 40)
    pixmap.fill(Qt.transparent)

    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)

    base_color = QtGui.QColor(color)
    if not base_color.isValid():
        base_color = QtGui.QColor("#7d897b")

    # 降低模块原始颜色饱和度，让图标更接近工业线稿。
    muted_color = QtGui.QColor(base_color)
    h, s, v, a = muted_color.getHsv()
    if h >= 0:
        muted_color.setHsv(h, min(s, 85), max(v, 125), a)

    painter.setPen(QtGui.QPen(muted_color, 1.55))
    painter.setBrush(QtGui.QColor("#f7f8f3"))

    polygon = QtGui.QPolygonF()
    points = (
        (20, 4),
        (33, 12),
        (33, 28),
        (20, 36),
        (7, 28),
        (7, 12),
        (20, 4),
    )
    for x, y in points:
        polygon.append(QtCore.QPointF(x, y))

    painter.drawPolygon(polygon)
    painter.drawLine(7, 12, 20, 20)
    painter.drawLine(33, 12, 20, 20)
    painter.drawLine(20, 20, 20, 36)

    # 极小的酸橙色识别点用于统一整个模块库的视觉语言。
    painter.setPen(Qt.NoPen)
    painter.setBrush(QtGui.QColor(LIME))
    painter.drawEllipse(QtCore.QPointF(20, 20), 2.6, 2.6)

    painter.end()
    return QtGui.QIcon(pixmap)


class ArtHeader(QtWidgets.QFrame):
    u"""页眉中的工业线条、斜切面与酸橙色装饰。"""

    def paintEvent(self, event):
        u"""绘制不参与交互的轻量背景装饰。"""
        super(ArtHeader, self).paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # ------------------------------------------------------------------
        # 右侧低对比工业线条
        # ------------------------------------------------------------------
        painter.setPen(QtGui.QPen(QtGui.QColor("#dde0da"), 1))
        for index in range(10):
            x = width - 475 + index * 43
            painter.drawLine(x, height, x + 118, 0)

        # ------------------------------------------------------------------
        # 当前品牌强调的酸橙斜切带
        # ------------------------------------------------------------------
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor("#e3f58a"))
        lime_shape = QtGui.QPolygonF()
        lime_points = (
            (width - 350, height),
            (width - 255, 0),
            (width - 170, 0),
            (width - 265, height),
        )
        for x, y in lime_points:
            lime_shape.append(QtCore.QPointF(x, y))
        painter.drawPolygon(lime_shape)

        # ------------------------------------------------------------------
        # 一条深色工业切片，避免整块酸橙过于轻飘
        # ------------------------------------------------------------------
        painter.setBrush(QtGui.QColor("#39413b"))
        dark_shape = QtGui.QPolygonF()
        dark_points = (
            (width - 235, height),
            (width - 192, 0),
            (width - 166, 0),
            (width - 209, height),
        )
        for x, y in dark_points:
            dark_shape.append(QtCore.QPointF(x, y))
        painter.drawPolygon(dark_shape)

        # ------------------------------------------------------------------
        # 微型十字标记，模拟工程制图和活动 UI 的边角注记
        # ------------------------------------------------------------------
        painter.setPen(QtGui.QPen(QtGui.QColor("#a2ad8d"), 1))
        for index in range(4):
            x = width - 415 + index * 66
            painter.drawLine(x - 5, 18, x + 5, 18)
            painter.drawLine(x, 13, x, 23)

        painter.end()


class StepButton(QtWidgets.QPushButton):
    u"""顶部四步导航，以大数字、切角和酸橙强调显示工作流状态。"""

    def __init__(self, number, title, subtitle, parent=None):
        u"""初始化步骤按钮。"""
        super(StepButton, self).__init__(parent)

        self.number = number
        self.title = title
        self.subtitle = subtitle
        self.stage_state = "available"

        self.setObjectName("WorkflowStep")
        self.setCheckable(True)
        self.setMinimumWidth(155)
        self.setFixedHeight(78)
        self.setAccessibleName("{} {} {}".format(number, title, subtitle))
        self.setCursor(Qt.PointingHandCursor)

    def set_stage_state(self, state):
        u"""设置 available / current / completed / locked 视觉状态。"""
        self.stage_state = state
        self.setEnabled(state != "locked")
        self.setChecked(state == "current")
        self.update()

    def paintEvent(self, event):
        u"""绘制步骤卡片，并保持 QPushButton 的交互状态。"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()

        # ------------------------------------------------------------------
        # Background
        # ------------------------------------------------------------------
        background = PAPER
        if self.stage_state == "current":
            background = "#f3f8dd"
        elif self.stage_state == "completed":
            background = "#f6f9e9"
        elif self.stage_state == "locked":
            background = "#f2f3ef"

        painter.fillRect(rect, QtGui.QColor(background))

        # 当前步骤增加左侧酸橙色切片，而不是整块高饱和填充。
        if self.stage_state == "current":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QtGui.QColor(LIME))
            accent = QtGui.QPolygonF()
            accent_points = (
                (0, 0),
                (52, 0),
                (33, rect.bottom()),
                (0, rect.bottom()),
            )
            for x, y in accent_points:
                accent.append(QtCore.QPointF(x, y))
            painter.drawPolygon(accent)

        # 卡片右侧斜切分隔线。
        painter.setPen(QtGui.QPen(QtGui.QColor(LINE), 1))
        painter.drawLine(rect.right(), 0, rect.right() - 34, rect.bottom())

        # ------------------------------------------------------------------
        # Number
        # ------------------------------------------------------------------
        text_color = INK if self.isEnabled() else "#a7aca6"
        number_color = text_color
        if self.stage_state == "current":
            number_color = "#20251f"

        painter.setPen(QtGui.QColor(number_color))
        number_font = QtGui.QFont("Georgia", 28)
        number_font.setItalic(True)
        painter.setFont(number_font)
        painter.drawText(
            QtCore.QRect(10, 10, 59, 49),
            Qt.AlignCenter,
            "{:02d}".format(self.number),
        )

        # ------------------------------------------------------------------
        # Title + subtitle
        # ------------------------------------------------------------------
        painter.setPen(QtGui.QColor(text_color))
        title_font = QtGui.QFont("Georgia", 12)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(
            QtCore.QRect(74, 16, rect.width() - 82, 23),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.title,
        )

        subtitle_color = MUTED if self.isEnabled() else "#afb3ae"
        painter.setPen(QtGui.QColor(subtitle_color))
        painter.setFont(QtGui.QFont("Microsoft YaHei UI", 9))
        painter.drawText(
            QtCore.QRect(74, 42, rect.width() - 86, 18),
            Qt.AlignLeft | Qt.AlignVCenter,
            self.subtitle,
        )

        # ------------------------------------------------------------------
        # State marker
        # ------------------------------------------------------------------
        if self.stage_state == "current":
            painter.setPen(QtGui.QPen(QtGui.QColor(LIME_DARK), 1.2))
            painter.drawLine(74, 66, rect.width() - 29, 66)

        elif self.stage_state == "completed":
            painter.setPen(Qt.NoPen)
            painter.setBrush(QtGui.QColor("#a9c935"))
            painter.drawEllipse(rect.width() - 29, 14, 16, 16)
            painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff"), 1.7))
            painter.drawLine(rect.width() - 25, 22, rect.width() - 22, 25)
            painter.drawLine(rect.width() - 22, 25, rect.width() - 17, 19)

        elif self.stage_state == "locked":
            painter.setPen(QtGui.QColor("#a4aaa4"))
            painter.setFont(QtGui.QFont("Segoe UI", 8))
            painter.drawText(
                QtCore.QRect(rect.width() - 49, 12, 38, 18),
                Qt.AlignCenter,
                "LOCK",
            )

        if self.hasFocus():
            painter.setPen(QtGui.QPen(QtGui.QColor("#7f952c"), 1.5))
            painter.drawRect(rect.adjusted(2, 2, -3, -3))

        painter.end()


class TickBox(QtWidgets.QCheckBox):
    u"""为酸橙色选中框补充明确勾号，同时保留 Qt 键盘与辅助功能。"""

    def paintEvent(self, event):
        u"""在 Qt 默认 CheckBox 之上绘制更清晰的勾号。"""
        super(TickBox, self).paintEvent(event)

        if not self.isChecked():
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        color = "#35451f" if self.isEnabled() else "#82906d"
        painter.setPen(QtGui.QPen(QtGui.QColor(color), 1.7))

        middle = self.height() // 2
        painter.drawLine(4, middle, 7, middle + 3)
        painter.drawLine(7, middle + 3, 13, middle - 4)
        painter.end()


class Section(QtWidgets.QWidget):
    u"""可折叠属性抽屉，折叠时释放垂直空间。"""

    def __init__(self, title, parent=None):
        u"""初始化 Section 标题按钮与 Form Body。"""
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
        self.button.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed,
        )

        self.body = QtWidgets.QWidget()
        self.form = QtWidgets.QFormLayout(self.body)
        self.form.setContentsMargins(12, 12, 12, 14)
        self.form.setSpacing(9)
        self.form.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow
        )
        self.form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(self.button)
        layout.addWidget(self.body)

        self.button.toggled.connect(self.set_expanded)

    def set_expanded(self, expanded):
        u"""同步标题箭头和属性区可见性。"""
        self.body.setVisible(expanded)
        self.button.setArrowType(
            Qt.DownArrow if expanded else Qt.RightArrow
        )
