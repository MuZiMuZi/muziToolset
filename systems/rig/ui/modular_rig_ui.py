# coding=utf-8
u"""Muzi 绑定库：四步导航、模块与模板目录、场景结构和可折叠属性。"""

from functools import partial

from .library_widgets import QtCore, QtGui, QtWidgets, Qt, wrapInstance
from .library_widgets import ArtHeader, StepButton, Section, TickBox, module_icon
from .library_style import stylesheet
from .. import library_catalog as catalog
from ..library_service import RigLibraryService


def label(text, role=None):
    u"""创建具有局部主题角色的文本。"""
    widget = QtWidgets.QLabel(text)
    if role:
        widget.setProperty("role", role)
    return widget


def button(text, callback, tooltip=""):
    u"""创建带明确操作文字的按钮。"""
    widget = QtWidgets.QPushButton(text)
    widget.setCursor(Qt.PointingHandCursor)
    widget.setToolTip(tooltip)
    widget.clicked.connect(callback)
    return widget


class ModularRigWindow(QtWidgets.QWidget):
    u"""正式绑定库窗口；注入服务时可在普通 Qt 环境检查完整布局。"""

    build_requested = QtCore.Signal(str)

    def __init__(self, parent=None, service=None):
        if parent is None and service is None:
            import maya.OpenMayaUI as omui
            pointer = omui.MQtUtil.mainWindow()
            if pointer:
                parent = wrapInstance(int(pointer), QtWidgets.QWidget)
        super(ModularRigWindow, self).__init__(parent)
        self.service = service if service is not None else RigLibraryService()
        self.current_id = None
        self.current_module = None
        self.current_step = 1
        self.loading = False
        self.jobs = []

        self.setup_window()
        self._create_layout()
        self.apply_style()
        self.load_data()
        self.refresh_ui()
        self._start_scene_jobs()

    # =========================================================
    # Window
    # =========================================================

    def setup_window(self):
        u"""设置窗口自身属性，不创建内部控件。"""
        self.setObjectName("ModularRigWindow")
        self.setWindowTitle(u"Muzi · 绑定库 / Rig Library")
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setMinimumSize(1120, 740)
        self.resize(1440, 980)
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            available = screen.availableGeometry()
            self.resize(min(1440, max(1120, available.width() - 60)),
                        min(980, max(740, available.height() - 80)))
        # 沿用窗口管理器已有的标志，保留绑定库自己的主题。
        self.setProperty("muzi_window_theme_applied", True)

    def apply_style(self):
        u"""从独立主题模块应用绑定库样式。"""
        self.setStyleSheet(stylesheet)

    def load_data(self):
        u"""将绑定目录载入 UI；实际业务数据始终由 Service 持有。"""
        self.refresh_module_list()

    def refresh_ui(self):
        u"""数据发生变化后的统一 UI 刷新入口。"""
        self.refresh_rig_structure()

    def refresh_step_ui(self):
        u"""刷新顶部步骤和当前属性区域。"""
        self._sync_workflow_steps()

    def refresh_module_list(self):
        u"""刷新模块与模板目录。"""
        self._populate_library()

    def refresh_rig_structure(self):
        u"""刷新中间模块结构及其关联区域。"""
        self._render_tree()

    def refresh_properties(self):
        u"""刷新当前模块属性。"""
        self._load_properties()

    def refresh_status(self):
        u"""刷新当前步骤提示和主操作按钮。"""
        self._update_action()

    def _create_layout(self):
        u"""建立可调整宽度的三栏结构；右侧属性独立滚动。"""
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(20, 15, 20, 15)
        main.setSpacing(10)
        header = ArtHeader()
        header.setObjectName("HeaderFrame")
        header.setFixedHeight(89)
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(16, 8, 16, 8)
        brand = label("M", "title")
        brand.setStyleSheet("font-family: Georgia; font-size: 51px; color: #42553b;")
        brand.setFixedWidth(58)
        header_layout.addWidget(brand)
        titles = QtWidgets.QVBoxLayout()
        titles.setSpacing(2)
        titles.addWidget(label("Muzi Rig Library", "title"))
        titles.addWidget(label(u"MODULAR SYSTEM   /   木子绑定库   /   CREATE WITH CLARITY", "subtitle"))
        header_layout.addLayout(titles)
        header_layout.addStretch(1)
        self.import_button = button(u"导入配置", self.import_recipe, u"追加 JSON 模块配置")
        self.export_button = button(u"导出配置", self.export_recipe, u"保存模块参数；不包含 Maya 场景或 Guide 位置")
        self.help_button = button("?", self.show_help, u"查看四步操作说明")
        self.help_button.setFixedWidth(34)
        header_layout.addWidget(self.import_button)
        header_layout.addWidget(self.export_button)
        header_layout.addWidget(self.help_button)
        main.addWidget(header)

        steps = QtWidgets.QHBoxLayout()
        steps.setSpacing(1)
        self.step_buttons = []
        entries = (("Setup", u"配置与层级"), ("Guide", u"导入与定位"),
                   ("Ctrl", u"创建与调整"), ("Final", u"检查与完成"))
        for index, (title, subtitle) in enumerate(entries, 1):
            widget = StepButton(index, title, subtitle)
            widget.clicked.connect(partial(self.set_current_step, index))
            self.step_buttons.append(widget)
            steps.addWidget(widget, 1)
        main.addLayout(steps)

        self.splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setHandleWidth(7)
        self.left_panel, left = self._panel(u"MODULE LIBRARY", "03 / 03")
        self.left_panel.setMinimumWidth(225)

        self.library_tabs = QtWidgets.QTabWidget()
        self.library_tabs.setObjectName("LibraryTabs")
        self.library_tabs.setDocumentMode(True)

        self.module_page = QtWidgets.QWidget()
        module_layout = QtWidgets.QVBoxLayout(self.module_page)
        module_layout.setContentsMargins(0, 10, 0, 0)
        module_layout.setSpacing(10)
        self.module_search = QtWidgets.QLineEdit()
        self.module_search.setPlaceholderText(u"搜索模块 / Search modules...")
        self.module_search.textChanged.connect(self.filter_modules)
        module_layout.addWidget(self.module_search)
        self.module_list = QtWidgets.QListWidget()
        self.module_list.setIconSize(QtCore.QSize(32, 32))
        self.module_list.itemDoubleClicked.connect(self.add_selected_module)
        module_layout.addWidget(self.module_list, 1)
        self.add_button = button(u"+  添加模块", self.add_selected_module)
        module_layout.addWidget(self.add_button)
        module_note = label(u"只显示仓库中已经具有正式构建入口的模块。", "muted")
        module_note.setWordWrap(True)
        module_layout.addWidget(module_note)

        self.template_page = QtWidgets.QWidget()
        template_layout = QtWidgets.QVBoxLayout(self.template_page)
        template_layout.setContentsMargins(0, 10, 0, 0)
        template_layout.setSpacing(10)
        self.template_search = QtWidgets.QLineEdit()
        self.template_search.setPlaceholderText(u"搜索模板 / Search templates...")
        self.template_search.textChanged.connect(self.filter_templates)
        template_layout.addWidget(self.template_search)
        self.template_list = QtWidgets.QListWidget()
        self.template_list.setIconSize(QtCore.QSize(32, 32))
        self.template_list.itemDoubleClicked.connect(self.add_selected_template)
        template_layout.addWidget(self.template_list, 1)
        template_layout.addWidget(button(u"+  添加模板组合", self.add_selected_template))
        template_note = label(u"模板仅组合当前可用模块，不包含 Maya 场景数据。", "muted")
        template_note.setWordWrap(True)
        template_layout.addWidget(template_note)

        self.library_tabs.addTab(self.module_page, u"MODULES  03")
        self.library_tabs.addTab(self.template_page, u"TEMPLATES  03")
        left.addWidget(self.library_tabs, 1)
        self.splitter.addWidget(self.left_panel)

        self.center_panel, center = self._panel("RIG STRUCTURE", "SCENE")
        self.center_panel.setMinimumWidth(315)
        self.tree_search = QtWidgets.QLineEdit()
        self.tree_search.setPlaceholderText(u"搜索结构 / Search hierarchy...")
        self.tree_search.textChanged.connect(self.filter_tree)
        center.addWidget(self.tree_search)
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.addWidget(button(u"+ 添加", self.open_module_library, u"切换到左侧模块库"))
        self.remove_button = button(u"移除", self.remove_current, u"仅移除尚未构建的模块配置")
        toolbar.addWidget(self.remove_button)
        toolbar.addStretch(1)
        toolbar.addWidget(button(u"刷新", self.refresh_scene))
        center.addLayout(toolbar)
        self.module_tree = QtWidgets.QTreeWidget()
        self.module_tree.setColumnCount(3)
        self.module_tree.setHeaderLabels([u"模块", u"侧", u"状态"])
        self.module_tree.setIndentation(17)
        self.module_tree.setUniformRowHeights(True)
        self.module_tree.setAnimated(False)
        self.module_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.module_tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.module_tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.module_tree.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.module_tree.currentItemChanged.connect(self.tree_selected)
        self.module_tree.itemDoubleClicked.connect(self.select_tree_nodes)
        self.module_tree.customContextMenuRequested.connect(self.show_structure_context_menu)
        center.addWidget(self.module_tree, 1)
        self.empty_label = label(u"从左侧添加模块，\n或选择 Face Starter 模板开始。", "muted")
        self.empty_label.setAlignment(Qt.AlignCenter)
        center.addWidget(self.empty_label)
        self.structure_note = label(u"双击模块可在 Maya 中选中其现有节点。", "muted")
        self.structure_note.setWordWrap(True)
        center.addWidget(self.structure_note)
        self.splitter.addWidget(self.center_panel)

        self.right_panel, right = self._panel("PROPERTIES", "MODULE")
        self.right_panel.setMinimumWidth(410)
        banner = QtWidgets.QFrame()
        banner.setObjectName("ModuleBanner")
        banner_layout = QtWidgets.QVBoxLayout(banner)
        banner_layout.setContentsMargins(16, 12, 16, 12)
        self.property_title = label(u"选择一个模块", "moduleTitle")
        self.property_subtitle = label(u"在结构中选择模块以编辑参数", "muted")
        self.property_subtitle.setWordWrap(True)
        banner_layout.addWidget(self.property_title)
        banner_layout.addWidget(self.property_subtitle)
        right.addWidget(banner)
        self.property_scroll = QtWidgets.QScrollArea()
        self.property_scroll.setWidgetResizable(True)
        self.property_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.property_body = QtWidgets.QWidget()
        properties = QtWidgets.QVBoxLayout(self.property_body)
        properties.setContentsMargins(0, 0, 3, 0)
        properties.setSpacing(8)
        self._create_properties(properties)
        properties.addStretch(1)
        self.property_scroll.setWidget(self.property_body)
        right.addWidget(self.property_scroll, 1)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([285, 450, 605])
        main.addWidget(self.splitter, 1)

        footer = QtWidgets.QFrame()
        footer.setProperty("role", "panel")
        bottom = QtWidgets.QHBoxLayout(footer)
        bottom.setContentsMargins(18, 12, 14, 12)
        self.status_dot = label("●")
        self.status_dot.setStyleSheet("color: #a6c643; font-size: 25px;")
        bottom.addWidget(self.status_dot)
        status_layout = QtWidgets.QVBoxLayout()
        self.status_label = label(u"准备开始。", "status")
        self.status_label.setWordWrap(True)
        self.status_hint = label(u"添加模块后，创建基础层级。", "muted")
        self.status_hint.setWordWrap(True)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.status_hint)
        bottom.addLayout(status_layout, 1)
        self.validate_button = button(u"检查 / Validate", self.validate_current_step)
        self.validate_button.setMinimumHeight(36)
        bottom.addWidget(self.validate_button)
        self.build_button = button(u"创建基础层级", self.build_current_step)
        self.build_button.setProperty("role", "primary")
        self.build_button.setMinimumWidth(250)
        bottom.addWidget(self.build_button)
        main.addWidget(footer)

    def _panel(self, title, badge):
        u"""创建分栏面板和统一标题行。"""
        panel = QtWidgets.QFrame()
        panel.setProperty("role", "panel")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 14)
        layout.setSpacing(11)
        heading = QtWidgets.QHBoxLayout()
        heading.addWidget(label(title, "panelTitle"))
        heading.addStretch(1)
        heading.addWidget(label(badge, "muted"))
        layout.addLayout(heading)
        return panel, layout

    def _create_properties(self, layout):
        u"""属性只展示当前后端能够保存或生效的参数。"""
        basic = Section("Setup / 基本设置")
        self.basic_section = basic
        self.enabled_check = TickBox(u"参与构建")
        basic.form.addRow(u"Enable Module", self.enabled_check)
        self.name_edit = QtWidgets.QLineEdit()
        basic.form.addRow(u"Module Name", self.name_edit)
        self.side_combo = QtWidgets.QComboBox()
        for title, value in ((u"Left / 左", "lf"), (u"Right / 右", "rt"), (u"Center / 中", "md")):
            self.side_combo.addItem(title, value)
        basic.form.addRow("Side", self.side_combo)
        self.parent_label = label(u"Rig Library / 默认根组", "muted")
        basic.form.addRow("Parent", self.parent_label)
        layout.addWidget(basic)

        guides = Section("Guide / 定位设置")
        self.guide_section = guides
        guides.button.setChecked(False)
        self.guide_hint = label("", "muted")
        self.guide_hint.setWordWrap(True)
        guides.form.addRow(self.guide_hint)
        self.guide_edit = QtWidgets.QPlainTextEdit()
        self.guide_edit.setFixedHeight(92)
        self.guide_edit.setPlaceholderText(u"每行一个 Guide，按 FK 链顺序排列。\n耳朵 / 舌头留空时自动读取模板。")
        guides.form.addRow(self.guide_edit)
        guide_actions = QtWidgets.QHBoxLayout()
        self.pick_button = button(u"读取 Maya 选择", self.pick_guides)
        self.save_guides_button = button(u"保存 Guide 列表", self.save_guides)
        guide_actions.addWidget(self.pick_button)
        guide_actions.addWidget(self.save_guides_button)
        guides.form.addRow(guide_actions)
        layout.addWidget(guides)

        controls = Section("Controller / 控制器设置")
        self.control_section = controls
        self.axis_combo = QtWidgets.QComboBox()
        self.axis_combo.addItems(catalog.axes)
        controls.form.addRow(u"Shape Axis / 朝向", self.axis_combo)
        self.size_spin = self._spin()
        controls.form.addRow(u"Size / 大小", self.size_spin)
        self.color_spin = QtWidgets.QSpinBox()
        self.color_spin.setRange(0, 31)
        self.color_spin.setKeyboardTracking(False)
        controls.form.addRow(u"Color / 索引颜色", self.color_spin)
        self.control_check = TickBox(u"显示当前模块控制器")
        controls.form.addRow(self.control_check)
        controls.form.addRow(label(u"构建后修改外观立即生效。", "muted"))
        layout.addWidget(controls)

        joints = Section("Joint / 骨骼设置")
        self.joint_section = joints
        self.radius_spin = self._spin()
        joints.form.addRow(u"Joint Radius / 半径", self.radius_spin)
        self.axis_check = TickBox(u"显示关节局部轴")
        self.joint_check = TickBox(u"显示当前模块骨骼")
        joints.form.addRow(self.axis_check)
        joints.form.addRow(self.joint_check)
        layout.addWidget(joints)
        self.enabled_check.toggled.connect(lambda value: self.change_property("enabled", value))
        self.name_edit.editingFinished.connect(lambda: self.change_property("name", self.name_edit.text().strip()))
        self.side_combo.currentIndexChanged.connect(lambda index: self.change_property("side", self.side_combo.currentData()))
        self.axis_combo.currentTextChanged.connect(lambda value: self.change_property("ctrl_axis", value))
        self.size_spin.valueChanged.connect(lambda value: self.change_property("ctrl_size", value))
        self.color_spin.valueChanged.connect(lambda value: self.change_property("ctrl_color", value))
        self.radius_spin.valueChanged.connect(lambda value: self.change_property("jnt_radius", value))
        self.axis_check.toggled.connect(lambda value: self.change_property("show_axis", value))
        self.joint_check.toggled.connect(lambda value: self.change_property("show_joints", value))
        self.control_check.toggled.connect(lambda value: self.change_property("show_controls", value))

    def _spin(self):
        u"""统一浮点范围，结束输入后才更新场景。"""
        spin = QtWidgets.QDoubleSpinBox()
        spin.setRange(0.01, 100.0)
        spin.setDecimals(2)
        spin.setSingleStep(0.1)
        spin.setKeyboardTracking(False)
        return spin

    def _populate_library(self):
        u"""目录完全来自已登记模块，不展示旧界面的演示数据。"""
        for entry in catalog.modules:
            item_text = u"{}\n{}".format(entry["title"], entry["description"])
            item = QtWidgets.QListWidgetItem(module_icon(entry["color"]), item_text)
            item.setSizeHint(QtCore.QSize(0, 62))
            item.setData(Qt.UserRole, entry["key"])
            item.setToolTip(entry["description"])
            self.module_list.addItem(item)
        for entry in catalog.templates:
            item_text = u"{}\n{}".format(entry["title"], entry["description"])
            item = QtWidgets.QListWidgetItem(module_icon("#8fac35"), item_text)
            item.setSizeHint(QtCore.QSize(0, 62))
            item.setData(Qt.UserRole, entry["key"])
            item.setToolTip(entry["description"])
            self.template_list.addItem(item)
        self.module_list.setCurrentRow(0)
        self.template_list.setCurrentRow(0)
        self._update_library_counts()

    def _filter_list(self, widget, text):
        for index in range(widget.count()):
            item = widget.item(index)
            item.setHidden(text.lower() not in (item.text() + " " + item.toolTip()).lower())

    def filter_modules(self, text):
        u"""按名称和说明过滤模块。"""
        self._filter_list(self.module_list, text)
        self._update_library_counts()

    def filter_templates(self, text):
        u"""按名称和组成过滤模板。"""
        self._filter_list(self.template_list, text)
        self._update_library_counts()

    def _visible_item_count(self, widget):
        u"""统计搜索后仍可见的目录项目。"""
        count = 0
        for index in range(widget.count()):
            if not widget.item(index).isHidden():
                count += 1
        return count

    def _update_library_counts(self):
        u"""在 Tab 标题中显示可见数和总数。"""
        self.library_tabs.setTabText(
            0,
            u"MODULES  {} / {}".format(self._visible_item_count(self.module_list), self.module_list.count())
        )
        self.library_tabs.setTabText(
            1,
            u"TEMPLATES  {} / {}".format(self._visible_item_count(self.template_list), self.template_list.count())
        )

    def open_module_library(self):
        u"""从结构工具栏回到模块目录，准备添加新模块。"""
        self.library_tabs.setCurrentIndex(0)
        self.module_search.setFocus()
        self._status(u"请从左侧选择模块，双击或点击“添加模块”。")

    def filter_tree(self, text):
        u"""搜索名称、侧别和状态，并保留命中子节点的完整父路径。"""
        query = text.strip().lower()

        def visit(item):
            values = []
            for column in range(self.module_tree.columnCount()):
                values.append(item.text(column))
            values.append(item.toolTip(0))
            own_match = query in u" ".join(values).lower()
            child_match = False
            for index in range(item.childCount()):
                child_match = visit(item.child(index)) or child_match
            item.setHidden(not (own_match or child_match))
            if query and child_match:
                item.setExpanded(True)
            return own_match or child_match
        for index in range(self.module_tree.topLevelItemCount()):
            visit(self.module_tree.topLevelItem(index))

    def current_record(self):
        u"""取得当前选择对应的真实配置。"""
        for record in self.service.document["modules"]:
            if record["id"] == self.current_id:
                return record
        return None

    def _render_tree(self):
        u"""重建精简模块树；场景节点不再作为子层级显示。"""
        self.module_tree.blockSignals(True)
        self.module_tree.clear()
        records = self.service.document["modules"]
        root = QtWidgets.QTreeWidgetItem(["rig_library", "", u"{} 模块".format(len(records))])
        root.setIcon(0, module_icon("#759539"))
        root.setData(0, Qt.UserRole + 2, "root")
        self.module_tree.addTopLevelItem(root)
        root.setExpanded(True)
        selected_item = None
        built_count = 0
        for record in records:
            entry = catalog.get_module(record["kind"])
            state = u"已构建" if record["built"] else u"待构建"
            if not record["enabled"]:
                state = u"已停用"
            if record["built"]:
                built_count += 1
            item = QtWidgets.QTreeWidgetItem([record["name"], record["side"].upper(), state])
            item.setIcon(0, module_icon(entry["color"]))
            item.setData(0, Qt.UserRole, record["id"])
            item.setData(0, Qt.UserRole + 2, "module:" + record["id"])
            item.setToolTip(0, entry["description"])
            selectable_nodes = []
            candidate_nodes = catalog.guide_names(record)
            if record["built"]:
                outputs = catalog.output_names(record)
                candidate_nodes = candidate_nodes + outputs["joints"] + outputs["controls"]
            for name in candidate_nodes:
                if self.service.node_exists(name):
                    selectable_nodes.append(name)
            item.setData(0, Qt.UserRole + 1, selectable_nodes)
            state_color = "#4f762a" if record["built"] else "#967428"
            if not record["enabled"]:
                state_color = "#8b9488"
            item.setForeground(2, QtGui.QBrush(QtGui.QColor(state_color)))
            root.addChild(item)
            if selected_item is None or record["id"] == self.current_id:
                selected_item = item
        if selected_item:
            self.current_id = selected_item.data(0, Qt.UserRole)
            self.current_module = self.current_id
            self.module_tree.setCurrentItem(selected_item)
        else:
            self.current_id = None
            self.current_module = None
        self.module_tree.blockSignals(False)
        count = len(records)
        self.empty_label.setVisible(count == 0)
        self.structure_note.setText(
            u"{} 个模块 · {} 个已构建\n双击模块可在 Maya 中选中其现有节点。".format(count, built_count))
        self.filter_tree(self.tree_search.text())
        self._load_properties()
        self._sync_workflow_steps()
        self._update_action()

    def tree_selected(self, current, previous=None):
        u"""节点选择与所属模块的属性区保持同步。"""
        identity = current.data(0, Qt.UserRole) if current else None
        self.set_current_module(identity)

    def set_current_module(self, module_identity):
        u"""设置当前模块，再刷新与模块相关的区域。"""
        self.current_module = module_identity
        self.current_id = module_identity
        self.refresh_properties()
        self.refresh_status()

    def _load_properties(self):
        record = self.current_record()
        self.property_body.setEnabled(record is not None)
        self.remove_button.setEnabled(record is not None and not record["built"])
        if record is None:
            self.property_title.setText(u"选择一个模块")
            self.property_subtitle.setText(u"从左侧添加模块，开始配置绑定。")
            return
        self.loading = True
        try:
            entry = catalog.get_module(record["kind"])
            self.property_title.setText(entry["title"])
            self.property_subtitle.setText(entry["description"])
            self.enabled_check.setChecked(record["enabled"])
            self.enabled_check.setEnabled(not record["built"])
            self.name_edit.setText(record["name"])
            self.name_edit.setEnabled(not record["built"] and record["kind"] == "fk_chain")
            self.side_combo.setCurrentIndex(self.side_combo.findData(record["side"]))
            self.side_combo.setEnabled(not record["built"] and record["kind"] != "tongue")
            self.axis_combo.setCurrentText(record["ctrl_axis"])
            self.size_spin.setValue(record["ctrl_size"])
            self.color_spin.setValue(record["ctrl_color"])
            self.radius_spin.setValue(record["jnt_radius"])
            self.axis_check.setChecked(record["show_axis"])
            self.joint_check.setChecked(record["show_joints"])
            self.control_check.setChecked(record["show_controls"])
            self.guide_edit.setPlainText("\n".join(record["guides"]))
            self.guide_edit.setEnabled(not record["built"])
            self.pick_button.setEnabled(not record["built"])
            self.save_guides_button.setEnabled(not record["built"])
            self.guide_hint.setText(u"{} 个 Guide · {}".format(len(catalog.guide_names(record)),
                                   u"手动指定顺序" if record["guides"] else u"按模板标准名称读取"))
        finally:
            self.loading = False

    def _run(self, operation, success):
        u"""统一处理错误并恢复界面，不把异常吞掉或显示虚假的成功状态。"""
        try:
            result = operation()
        except Exception as error:
            self._status(str(error), error=True)
            self._load_properties()
            return False
        self.refresh_ui()
        self._status(success(result) if callable(success) else success)
        return True

    def _status(self, text, error=False):
        first = text.splitlines()[0] if text else ""
        self.status_label.setText(first[:100])
        self.status_label.setToolTip(text)
        self.status_dot.setStyleSheet("color: {}; font-size: 25px;".format("#bf7056" if error else "#a6c643"))
        if error:
            self.status_hint.setText(u"请修正后重试；悬停状态文字可查看全部问题。")

    def add_selected_module(self, *args):
        u"""将当前目录项加入结构。"""
        item = self.module_list.currentItem()
        if item is None or item.isHidden():
            return
        def add():
            self.current_id = self.service.add_module(item.data(Qt.UserRole))
        self._run(add, u"模块已加入绑定结构。")

    def add_selected_template(self, *args):
        u"""添加预设组合并保留已有模块。"""
        item = self.template_list.currentItem()
        if item is None or item.isHidden():
            return
        self._run(lambda: self.service.add_template(item.data(Qt.UserRole)), u"模板组合已添加，已有模块保留原设置。")

    def remove_current(self):
        u"""移除当前尚未构建的模块。"""
        if self.current_id:
            self._run(lambda: self.service.remove_module(self.current_id), u"待建模块已移除。")

    def change_property(self, key, value):
        u"""按当前模块状态保存参数或更新外观。"""
        if self.loading or self.current_id is None:
            return
        record = self.current_record()
        if record[key] == value:
            return
        self._run(lambda: self.service.update_module(self.current_id, {key: value}),
                  u"外观已更新。" if record["built"] else u"模块参数已保存。")

    def pick_guides(self):
        u"""读取当前选择；最终顺序由编辑区中的文本行明确决定。"""
        names = self.service.selected_guides()
        if not names:
            self._status(u"请先在 Maya 中按链条顺序选择 Guide。", error=True)
            return
        self.guide_edit.setPlainText("\n".join(names))
        self._status(u"已读取选择，请核对顺序并点击“保存 Guide 列表”。")

    def save_guides(self):
        u"""校验并保存当前 Guide 列表。"""
        if self.current_id is None:
            return
        names = []
        for line in self.guide_edit.toPlainText().splitlines():
            if line.strip():
                names.append(line.strip())
        self._run(lambda: self.service.update_module(self.current_id, {"guides": names}), u"Guide 列表已保存。")

    def mirror_current_module(self):
        u"""将当前左右模块的参数与 Guide 定位镜像到配对侧。"""
        if self.current_id is None:
            return
        self._run(
            lambda: self.service.mirror_module(self.current_id),
            lambda result: u"已镜像到{}：{} 个 Guide 定位。".format(
                result["side"].upper(), result["guide_count"]))

    def create_structure_context_menu(self, item):
        u"""为模块行创建右键菜单；根节点不提供模块操作。"""
        if item is None:
            return None
        identity = item.data(0, Qt.UserRole)
        if identity is None:
            return None
        record = None
        for candidate in self.service.document["modules"]:
            if candidate["id"] == identity:
                record = candidate
                break
        if record is None:
            return None

        menu = QtWidgets.QMenu(self.module_tree)
        if record["built"]:
            text = u"已构建模块不可镜像"
            enabled = False
        elif record["side"] not in ("lf", "rt"):
            text = u"中央模块不需要镜像"
            enabled = False
        else:
            destination = u"右侧" if record["side"] == "lf" else u"左侧"
            text = u"镜像设置与定位到{}".format(destination)
            enabled = True
        action = menu.addAction(text)
        action.setEnabled(enabled)
        action.setToolTip(u"沿世界 X=0 镜像到配对模块")
        action.triggered.connect(lambda checked=False: self.mirror_current_module())
        return menu

    def show_structure_context_menu(self, position):
        u"""在鼠标所在模块行显示镜像操作。"""
        item = self.module_tree.itemAt(position)
        menu = self.create_structure_context_menu(item)
        if menu is None:
            return
        self.module_tree.setCurrentItem(item)
        global_position = self.module_tree.viewport().mapToGlobal(position)
        execute = getattr(menu, "exec_", None)
        if execute is None:
            execute = menu.exec
        execute(global_position)
        menu.deleteLater()

    def set_step(self, number, *args):
        u"""四段导航对应真实能力，Ctrl 阶段一次完成骨骼和控制器。"""
        workflow = self.service.workflow_state()
        if not workflow["unlocked"].get(number, False):
            self._status(u"当前阶段尚未解锁，请先完成前一步。", error=True)
            return
        self.current_step = number
        self._sync_workflow_steps()
        self._update_action()

    def set_current_step(self, step, *args):
        u"""公开的步骤状态入口。"""
        return self.set_step(step)

    def _sync_workflow_steps(self):
        u"""根据场景实际进度刷新步骤的完成、当前和锁定状态。"""
        workflow = self.service.workflow_state()
        if not workflow["unlocked"].get(self.current_step, False):
            self.current_step = workflow["suggested"]
        self._sync_property_sections()
        for index, widget in enumerate(self.step_buttons, 1):
            if index == self.current_step:
                state = "current"
            elif workflow["completed"].get(index, False):
                state = "completed"
            elif workflow["unlocked"].get(index, False):
                state = "available"
            else:
                state = "locked"
            widget.set_stage_state(state)

    def _sync_property_sections(self):
        u"""右侧属性区只显示当前步骤对应的设置，并保持该区域展开。"""
        sections = {
            1: self.basic_section,
            2: self.guide_section,
            3: self.control_section,
            4: self.joint_section,
        }
        for step, section in sections.items():
            active = step == self.current_step
            section.setVisible(active)
            if active:
                section.button.setChecked(True)

    def _update_action(self):
        if not hasattr(self, "build_button"):
            return
        texts = {1: u"创建基础层级", 2: u"导入 Face Guide", 3: u"创建控制系统", 4: u"完成并选择控制器"}
        hints = {1: u"添加模块与组合模板，然后创建基础层级。",
                 2: u"耳朵与舌头使用 Face Guide；通用 FK 请指定有序 Guide。",
                 3: u"创建骨骼、控制器与驱动连接；右侧参数可实时调整外观。",
                 4: u"最终检查全部已构建模块，并选择所有主控制器。"}
        self.build_button.setText(texts[self.current_step])
        self.status_hint.setText(hints[self.current_step])
        workflow = self.service.workflow_state()
        enabled = bool(self.service.document["modules"]) and workflow["unlocked"].get(self.current_step, False)
        self.build_button.setEnabled(enabled)

    def run_step(self):
        u"""底部主按钮执行当前阶段操作。"""
        if self.current_step == 1:
            if self._run(self.service.setup, u"基础层级已准备好，下一步导入并调整 Guide。"):
                self.set_step(2)
        elif self.current_step == 2:
            if self._run(self.service.import_guide, u"Face Guide 已就绪，请在 Maya 中检查并调整位置。"):
                self.set_step(3)
        elif self.current_step == 3:
            if self._run(self.service.build, lambda count: u"Ctrl 完成：{} 个新模块。".format(count)):
                self.build_requested.emit("all")
                self.set_step(4)
        elif self.current_step == 4:
            self._run(self.service.finalize,
                      lambda count: u"Final 完成：已检查并选择 {} 个主控制器。".format(count))

    def build_current_step(self):
        u"""公开的当前步骤构建入口。"""
        return self.run_step()

    def validate_scene(self):
        u"""显示只读预检查结果。"""
        def check():
            errors = self.service.validate()
            if errors:
                raise RuntimeError("\n".join(errors))
        self._run(check, u"检查通过，可以构建待建模块。")

    def validate_current_step(self):
        u"""公开的当前步骤检查入口。"""
        return self.validate_scene()

    def select_tree_nodes(self, item, column=0):
        u"""双击模块，在 Maya 中选中其现有 Guide、Joint 和 Control。"""
        names = item.data(0, Qt.UserRole + 1)
        if names:
            self.service.select_nodes(names)

    def refresh_scene(self, *args):
        u"""从场景恢复最新配置。"""
        self._run(self.service.reload, u"已从当前场景刷新绑定库。")

    def import_recipe(self):
        u"""通过文件对话框追加 JSON 配置。"""
        path, selected = QtWidgets.QFileDialog.getOpenFileName(self, u"导入绑定库配置", "", "Rig recipe (*.json)")
        if path:
            self._run(lambda: self.service.import_recipe(path), u"配置已添加，请检查 Guide。")

    def export_recipe(self):
        u"""导出可复用的模块参数。"""
        path, selected = QtWidgets.QFileDialog.getSaveFileName(self, u"导出模块参数", "muzi_rig_recipe.json", "Rig recipe (*.json)")
        if path:
            if not path.lower().endswith(".json"):
                path += ".json"
            self._run(lambda: self.service.export_recipe(path), u"模块参数已导出；Maya 场景请单独保存。")

    def show_help(self):
        u"""说明真实支持范围以及各阶段操作。"""
        QtWidgets.QMessageBox.information(self, u"绑定库使用说明", u"1. 添加 Ear、Tongue、FK Chain，或添加模板组合。\n"
            u"2. Setup 创建根组；Guide 导入仓库现有 Face Guide。\n"
            u"3. 在 Maya 中调整 Guide，再点击 Validate；Ctrl 创建骨骼和控制器并调整外观。\n"
            u"4. Final 检查全部模块并选择主控制器。\n\n"
            u"配置随 Maya 场景保存；JSON 只保存模块参数，不包含绑定或 Guide 位置。\n"
            u"通用 FK 按文本行顺序读取 Guide。已构建模块锁定身份与定位输入。\n"
            u"当前版本支持根命名空间中的一套绑定库。")

    def _start_scene_jobs(self):
        u"""撤销、重做和切换场景后刷新；窗口销毁时清理所有回调。"""
        commands = getattr(self.service, "cmds", None)
        if commands is None or not hasattr(commands, "scriptJob"):
            return
        for event in ("Undo", "Redo", "SceneOpened", "NewSceneOpened"):
            callback = partial(self.refresh_timer.start, 0)
            self.jobs.append(commands.scriptJob(event=[event, callback], protected=True))
        jobs = self.jobs
        def cleanup(*args):
            for job in list(jobs):
                if commands.scriptJob(exists=job):
                    commands.scriptJob(kill=job, force=True)
            jobs[:] = []
        self.destroyed.connect(cleanup)


__all__ = ["ModularRigWindow"]
