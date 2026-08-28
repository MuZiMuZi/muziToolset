# coding=utf-8
from __future__ import unicode_literals
import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_DIR)
TOOLS_DIR = os.path.join(PACKAGE_DIR, 'tools')
IMAGE_DIR = os.path.join(PACKAGE_DIR, 'image')
ICON_DIR = os.path.join(PACKAGE_DIR, 'icon')
UI_DIR = os.path.join(PACKAGE_DIR, 'ui')
QSS_DIR = os.path.join(PACKAGE_DIR, 'qss')

# Backward-compatible names used by legacy modules.
project_root = PACKAGE_DIR
tools_dir = TOOLS_DIR
data_dir = IMAGE_DIR
image_dir = IMAGE_DIR
icon_dir = ICON_DIR
ui_dir = UI_DIR
qss_dir = QSS_DIR

DEBUG = True
VERSION = '0.2.0'
