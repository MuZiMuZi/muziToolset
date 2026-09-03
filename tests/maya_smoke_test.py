# coding=utf-8
u"""
Maya 2023 Smoke Test
====================

对 muziToolset 0.4 正式运行架构做一次非破坏性的启动检查。

验证：
    1. Maya / PySide 环境；
    2. Tool Registry；
    3. 当前 snake_case Core 模块；
    4. RigBase / ModuleBase / CtrlBase / Face Modules；
    5. Resources 和 Controller Shape JSON；
    6. UI Tool main() 是否能创建 QWidget；
    7. Command Tool 是否存在可调用 main()。

不会执行任何 Rig Build / Skin / Clean 场景修改。
"""

from __future__ import print_function

import importlib
import json
import os
import traceback

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWidgets import QWidget


package_name = __name__.split(".")[0]


ui_tool_modules = [
    "app.toolbox",
    "tools.basic.attr_tool",
    "tools.basic.connections_tool",
    "tools.basic.constraint_tool",
    "tools.basic.rename_tool",
    "tools.joint.joint_tool",
    "tools.joint.joint_resamp_tool",
    "tools.controller.control_shape_tool",
    "tools.controller.create_ctrl_tool",
    "tools.rig.rig_tool",
    "tools.rig.skirt_ctrl_tool",
    "tools.face.face_rig_tool",
    "tools.face.face_select_key_tool",
    "tools.skin.skin_tool",
    "tools.blendshape.add_blendshape_tool",
    "tools.blendshape.invert_shape_tool",
    "tools.clean.hierarchy_cleaner",
    "tools.clean.model_checker",
]


command_tool_modules = [
    "tools.basic.snap_tool",
    "tools.controller.create_fk_ctrl_tool",
]


core_modules = [
    "core.attr_utils",
    "core.blendshape_utils",
    "core.config_utils",
    "core.connection_utils",
    "core.constraint_utils",
    "core.control_shape_utils",
    "core.curve_utils",
    "core.hierarchy_utils",
    "core.joint_utils",
    "core.matrix_utils",
    "core.mesh_utils",
    "core.model_check_utils",
    "core.rename_utils",
    "core.scene_utils",
    "core.scene_utils",
    "core.skin_utils",
    "core.snap_utils",
    "core.transform_utils",
]


system_modules = [
    "systems",
    "systems.rig_base",
    "systems.module_base",
    "systems.ctrl_base",
    "systems.face",
    "systems.face.config",
    "systems.face.face_base",
    "systems.face.setup",
    "systems.face.setup.face_setup",
    "systems.face.guide",
    "systems.face.guide.face_guide",
    "systems.face.build",
    "systems.face.modules",
    "systems.face.modules.teeth",
    "systems.face.ui",
    "systems.face.ui.workflow_controller",
    "systems.face.ui.build_controller",
    "systems.body.skirt",
    "systems.body.skirt.builder",
]


expected_registry = {
    u"基础工具": [
        "attr_tool",
        "connections_tool",
        "constraint_tool",
        "rename_tool",
        "snap_tool",
    ],
    u"骨骼工具": [
        "joint_resamp_tool",
        "joint_tool",
    ],
    u"控制器工具": [
        "control_shape_tool",
        "create_ctrl_tool",
        "create_fk_ctrl_tool",
    ],
    u"绑定工具": [
        "rig_tool",
        "skirt_ctrl_tool",
    ],
    u"面部工具": [
        "face_rig_tool",
        "face_select_key_tool",
    ],
    u"蒙皮工具": [
        "skin_tool",
    ],
    u"BlendShape 工具": [
        "add_blendshape_tool",
        "invert_shape_tool",
    ],
    u"检查与清理": [
        "hierarchy_cleaner",
        "model_checker",
    ],
}


def _full_module_name(relative_name):
    u"""返回 muziToolset 根包下的完整模块名称。"""
    return "{}.{}".format(
        package_name,
        relative_name
    )


def _new_result(name, category):
    u"""创建单项测试结果。"""
    return {
        "name": name,
        "category": category,
        "passed": False,
        "message": "",
        "traceback": "",
    }


def _record_pass(results, name, category, message=u"通过"):
    u"""记录通过项。"""
    result = _new_result(
        name,
        category
    )
    result["passed"] = True
    result["message"] = message
    results.append(
        result
    )
    return result


def _record_fail(results, name, category, error):
    u"""记录失败项和 traceback。"""
    result = _new_result(
        name,
        category
    )
    result["message"] = str(error)
    result["traceback"] = traceback.format_exc()
    results.append(
        result
    )
    return result


def _safe_delete_widget(widget):
    u"""关闭并释放 Smoke Test 创建的 QWidget。"""
    if widget is None:
        return

    if not isinstance(widget, QWidget):
        return

    try:
        widget.close()
    except Exception:
        pass

    try:
        widget.deleteLater()
    except Exception:
        pass

    application = QApplication.instance()

    if application is not None:
        try:
            application.processEvents()
        except Exception:
            pass


def _test_environment(results):
    u"""检查 Maya 与 Qt 基础环境。"""
    try:
        maya_version = cmds.about(
            version=True
        )
        api_version = cmds.about(
            apiVersion=True
        )
        _record_pass(
            results,
            "Maya Environment",
            "environment",
            u"Maya {} | API {}".format(
                maya_version,
                api_version
            )
        )
    except Exception as error:
        _record_fail(
            results,
            "Maya Environment",
            "environment",
            error
        )

    try:
        application = QApplication.instance()

        if application is None:
            raise RuntimeError(
                u"当前没有 QApplication，测试必须在 Maya GUI 中运行。"
            )

        _record_pass(
            results,
            "Qt Application",
            "environment",
            application.__class__.__name__
        )
    except Exception as error:
        _record_fail(
            results,
            "Qt Application",
            "environment",
            error
        )


def _test_registry(results):
    u"""检查主工具注册表是否包含全部正式工具。"""
    try:
        tools_module = importlib.import_module(
            _full_module_name("tools")
        )
        registered = tools_module.refresh_tools()
    except Exception as error:
        _record_fail(
            results,
            "Tool Registry Import",
            "registry",
            error
        )
        return

    _record_pass(
        results,
        "Tool Registry Import",
        "registry",
        u"已发现 {} 个分类".format(
            len(registered)
        )
    )

    for category_name in expected_registry:
        expected_tools = expected_registry[category_name]
        category_tools = registered.get(
            category_name,
            {}
        )
        missing_tools = []

        for tool_name in expected_tools:
            if tool_name not in category_tools:
                missing_tools.append(
                    tool_name
                )

        if missing_tools:
            _record_fail(
                results,
                category_name,
                "registry",
                RuntimeError(
                    u"缺少工具：{}".format(
                        ", ".join(missing_tools)
                    )
                )
            )
            continue

        _record_pass(
            results,
            category_name,
            "registry",
            u"{} 个工具".format(
                len(expected_tools)
            )
        )


def _test_import_list(results, relative_names, category):
    u"""批量测试普通 Python 模块 Import。"""
    for relative_name in relative_names:
        try:
            importlib.import_module(
                _full_module_name(relative_name)
            )
            _record_pass(
                results,
                relative_name,
                category,
                u"import 成功"
            )
        except Exception as error:
            _record_fail(
                results,
                relative_name,
                category,
                error
            )


def _test_resources(results):
    u"""检查正式资源路径和 Controller Shape JSON。"""
    try:
        config_module = importlib.import_module(
            _full_module_name("config")
        )
        resource_paths = [
            ("resources_dir", config_module.resources_dir),
            ("icons_dir", config_module.icons_dir),
            ("controller_shapes_dir", config_module.controller_shapes_dir),
        ]

        for path_name, path_value in resource_paths:
            if not os.path.isdir(path_value):
                raise RuntimeError(
                    u"资源目录不存在：{} = {}".format(
                        path_name,
                        path_value
                    )
                )

        _record_pass(
            results,
            "Resource Directories",
            "resources",
            u"资源目录存在"
        )
    except Exception as error:
        _record_fail(
            results,
            "Resource Directories",
            "resources",
            error
        )
        return

    try:
        shape_files = []
        file_names = os.listdir(
            config_module.controller_shapes_dir
        )

        for file_name in file_names:
            if file_name.lower().endswith(".json"):
                shape_files.append(
                    file_name
                )

        shape_files.sort()

        if not shape_files:
            raise RuntimeError(
                u"Controller Shape 目录中没有 JSON。"
            )

        first_shape_path = os.path.join(
            config_module.controller_shapes_dir,
            shape_files[0]
        )

        with open(first_shape_path, "r") as file_object:
            json.load(
                file_object
            )

        _record_pass(
            results,
            "Controller Shape Library",
            "resources",
            u"{} 个 JSON，首个文件解析成功".format(
                len(shape_files)
            )
        )
    except Exception as error:
        _record_fail(
            results,
            "Controller Shape Library",
            "resources",
            error
        )


def _test_command_tools(results):
    u"""命令型工具只检查 Import 和 main()，不执行场景修改。"""
    for relative_name in command_tool_modules:
        try:
            module = importlib.import_module(
                _full_module_name(relative_name)
            )
            main_function = getattr(
                module,
                "main",
                None
            )

            if not callable(main_function):
                raise RuntimeError(
                    u"模块没有可调用的 main()。"
                )

            _record_pass(
                results,
                relative_name,
                "command_tool",
                u"main() 可调用，未执行场景操作"
            )
        except Exception as error:
            _record_fail(
                results,
                relative_name,
                "command_tool",
                error
            )


def _test_ui_tools(results, test_window_manager=False):
    u"""创建全部窗口型工具，验证 QWidget 和 Window Manager。"""
    window_manager = None

    if test_window_manager:
        try:
            window_manager = importlib.import_module(
                _full_module_name("app.window_manager")
            )
        except Exception as error:
            _record_fail(
                results,
                "Window Manager Import",
                "window_manager",
                error
            )
            test_window_manager = False

    for relative_name in ui_tool_modules:
        widget = None
        tool_key = "smoke/{}".format(
            relative_name
        )

        try:
            module = importlib.import_module(
                _full_module_name(relative_name)
            )
            main_function = getattr(
                module,
                "main",
                None
            )

            if not callable(main_function):
                raise RuntimeError(
                    u"模块没有可调用的 main()。"
                )

            if test_window_manager:
                widget = window_manager.show_tool(
                    tool_key,
                    main_function
                )
            else:
                widget = main_function()

            if not isinstance(widget, QWidget):
                raise TypeError(
                    u"窗口型工具 main() 没有返回 QWidget，实际类型：{}".format(
                        type(widget).__name__
                    )
                )

            application = QApplication.instance()

            if application is not None:
                application.processEvents()

            _record_pass(
                results,
                relative_name,
                "ui_tool",
                u"{} 创建成功".format(
                    widget.__class__.__name__
                )
            )
        except Exception as error:
            _record_fail(
                results,
                relative_name,
                "ui_tool",
                error
            )
        finally:
            if test_window_manager:
                if window_manager is not None:
                    try:
                        window_manager.close_tool(
                            tool_key
                        )
                    except Exception:
                        pass
            else:
                _safe_delete_widget(
                    widget
                )


def _restore_selection(selection):
    u"""恢复运行 Smoke Test 前的 Maya 选择。"""
    valid_selection = []

    for node in selection:
        if cmds.objExists(node):
            valid_selection.append(
                node
            )

    try:
        if valid_selection:
            cmds.select(
                valid_selection,
                replace=True
            )
        else:
            cmds.select(
                clear=True
            )
    except Exception:
        pass


def _print_report(report):
    u"""把 Smoke Test 结果输出到 Maya Script Editor。"""
    print("")
    print("=" * 78)
    print("Muzi Toolset - Maya Smoke Test")
    print("Architecture: RigBase / ModuleBase / CtrlBase")
    print("=" * 78)

    for result in report["results"]:
        status = "PASS"

        if not result["passed"]:
            status = "FAIL"

        print(
            u"[{0}] {1} | {2} | {3}".format(
                status,
                result["category"],
                result["name"],
                result["message"]
            )
        )

        if not result["passed"]:
            if result["traceback"]:
                print(
                    result["traceback"]
                )

    print("-" * 78)
    print(
        u"Total: {0} | Passed: {1} | Failed: {2}".format(
            report["total"],
            report["passed"],
            report["failed"]
        )
    )
    print("=" * 78)


def run(test_window_manager=False):
    u"""运行完整非破坏性 Maya Smoke Test。"""
    results = []
    original_selection = cmds.ls(
        selection=True,
        long=True
    )

    if original_selection is None:
        original_selection = []

    try:
        _test_environment(
            results
        )
        _test_registry(
            results
        )
        _test_import_list(
            results,
            core_modules,
            "core"
        )
        _test_import_list(
            results,
            system_modules,
            "systems"
        )
        _test_resources(
            results
        )
        _test_command_tools(
            results
        )
        _test_ui_tools(
            results,
            test_window_manager=test_window_manager
        )
    finally:
        _restore_selection(
            original_selection
        )

    passed_count = 0
    failed_count = 0

    for result in results:
        if result["passed"]:
            passed_count += 1
        else:
            failed_count += 1

    report = {
        "total": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "results": results,
    }

    _print_report(
        report
    )
    return report


__all__ = [
    "run",
]
