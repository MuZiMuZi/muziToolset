# coding=utf-8
u"""
Muzi Toolset 全局路径配置。

仓库根目录本身就是正式 Python Package。
这里只维护包路径、静态资源路径和统一资源命名规则，不放具体工具业务逻辑。
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
module_guide_dir = os.path.join(
    resources_dir,
    "module_guide"
)
templates_dir = os.path.join(resources_dir, "templates")

# Module Guide 统一命名规则。
# 模板文件：<module>_guide.ma
# Guide Root：grp_md_<module>_guide_001
# Guide Display Curve：crv_md_<module>_guide_001
#
# 例如：
# face -> face_guide.ma -> grp_md_face_guide_001
# ear  -> grp_md_ear_guide_001 -> crv_md_ear_guide_001
# arm  -> arm_guide.ma -> grp_md_arm_guide_001
module_guide_template_file_format = "{}_guide.ma"
module_guide_root_name_format = "grp_md_{}_guide_001"
module_guide_curve_name_format = "crv_md_{}_guide_001"

# 旧工具中仍可能使用这些小写路径别名。
# 新代码优先使用上面语义更清楚的正式变量。
icon_dir = icons_dir
image_dir = controller_shapes_dir
data_dir = controller_shapes_dir

version = "0.3.0"
debug = False
