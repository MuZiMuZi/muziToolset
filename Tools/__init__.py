from importlib import reload
import config


reload (config)
# 导入所有需要的模块
import Names_Tool_main
import Joint_Tool_main
import Rig_Tool_main
import Tool_main

if config.DEBUG :
    # 在DEBUG下reload所有模块
    reload (Joint_Tool_main)
    reload(Names_Tool_main)
    reload (Rig_Tool_main)
    reload (Tool_main)
