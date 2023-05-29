import os



project_root = os.path.dirname(__file__)
ui_dir = os.path.join(project_root , 'ui')
icon_dir = os.path.join(project_root , 'icon')

bind_root = os.path.abspath(__file__ + "/../../../../bind")
base_dir = os.path.join(bind_root , 'base')
chain_dir = os.path.join(bind_root , 'chain')
module_dir = os.path.join(bind_root , 'module')
