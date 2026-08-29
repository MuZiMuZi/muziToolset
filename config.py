# coding=utf-8
u"""
Muzi Rigging 全局路径配置。

这里只维护包路径和静态资源路径，不在这里放具体工具业务配置。
"""

from __future__ import print_function

import os


package_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(package_dir)

app_dir = os.path.join(package_dir, "app")
ui_dir = os.path.join(package_dir, "ui")
core_dir = os.path.join(package_dir, "core")
tools_dir = os.path.join(package_dir, "tools")
systems_dir = os.path.join(package_dir, "systems")
resources_dir = os.path.join(package_dir, "resources")

icons_dir = os.path.join(resources_dir, "icons")
controller_shapes_dir = os.path.join(
    resources_dir,
    "controller_shapes"
)
templates_dir = os.path.join(resources_dir, "templates")

# 迁移期间保留旧工具中常见的小写变量名。
# 新代码优先使用上面语义更清楚的名称。
icon_dir = icons_dir
image_dir = controller_shapes_dir
data_dir = controller_shapes_dir

version = "0.3.0"
debug = False
