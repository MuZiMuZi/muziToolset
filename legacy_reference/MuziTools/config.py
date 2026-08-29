# coding=utf-8
u"""MuziTools 路径与版本配置。"""

from __future__ import unicode_literals

import os


PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)

TOOLS_DIR = os.path.join(PACKAGE_DIR, "tools")
IMAGE_DIR = os.path.join(PACKAGE_DIR, "image")
ICON_DIR = os.path.join(PACKAGE_DIR, "icon")

# 当前工具代码仍有少量地方使用小写路径变量，统一在这里提供。
tools_dir = TOOLS_DIR
data_dir = IMAGE_DIR
image_dir = IMAGE_DIR
icon_dir = ICON_DIR

DEBUG = True
VERSION = "0.2.0"
