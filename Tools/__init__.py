from importlib import reload
from . import Joint_Tool_main , Names_Tool_main, config


reload (config)
# 导入所有需要的模块
if config.DEBUG :
    # 在DEBUG下reload所有模块
    reload (Joint_Tool_main)
    reload(Names_Tool_main)
    pass
