# coding=utf-8
u"""
Muzi Toolset 全局路径配置。

仓库根目录本身就是正式 Python Package。
这里只维护包路径和静态资源路径，不放具体工具业务配置。
"""

from __future__ import print_function

import os


package_dir = os.path.dirname(os.path.abspath(__file__))
project_root = package_dir

app_dir = os.path.join(package_dir, "app")
ui_dir = os.path.join(package_dir, "ui")
core_dir = os.path.join(package_dir, "core")
tools_dir = os.path.join(package_dir, "tools")
systems_dir = os.path.join(package_dir, "systems")
resources_dir = os.path.join(package_dir, "resources")
legacy_reference_dir = os.path.join(
    package_dir,
    "legacy_reference"
)

icons_dir = os.path.join(resources_dir, "icons")
controller_shapes_dir = os.path.join(
    resources_dir,
    "controller_shapes"
)
templates_dir = os.path.join(resources_dir, "templates")

# 旧工具中仍可能使用这些小写路径别名。
# 新代码优先使用上面语义更清楚的正式变量。
icon_dir = icons_dir
image_dir = controller_shapes_dir
data_dir = controller_shapes_dir

version = "0.3.0"
debug = False
