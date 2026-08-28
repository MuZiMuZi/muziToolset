import sys
import os

def initialize():

    # ? 手动定义插件根目录（最稳定）
    root = "C:/Users/X/Documents/maya/scripts/muziToolset/MuziTools"

    # 加入 Python path
    if root not in sys.path:
        sys.path.append(root)

    tools_path = os.path.join(root, "tools")
    if tools_path not in sys.path:
        sys.path.append(tools_path)

    import rigging_toolbox
    rigging_toolbox.show()