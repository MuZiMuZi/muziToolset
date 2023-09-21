import os
from enum import Enum , unique



project_root = os.path.dirname(__file__)
data_dir = os.path.abspath (__file__ + "/../image")
ui_dir = os.path.abspath (__file__ + "/../ui")
icon_dir = os.path.abspath (__file__ + "/../icon")


print(icon_dir)