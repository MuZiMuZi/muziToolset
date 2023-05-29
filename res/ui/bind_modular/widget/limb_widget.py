import os

from PySide2.QtUiTools import QUiLoader
from ..widget import base_widget
from ..config import Side , ui_dir , Direction
from ..ui import bind , base , chain,limb
from . import base_widget
from importlib import reload



reload(base_widget)
reload(chain)