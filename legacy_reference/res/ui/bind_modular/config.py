import os
from enum import Enum , unique



project_root = os.path.dirname(__file__)
ui_dir = os.path.join(project_root , 'ui')
icon_dir = os.path.join(project_root , 'icon')

bind_root = os.path.abspath(__file__ + "/../../../../bind")
base_dir = os.path.join(bind_root , 'base')
chain_dir = os.path.join(bind_root , 'chain')
limb_dir = os.path.join(bind_root , 'limb')
module_dir = os.path.join(bind_root , 'module')



@unique
class Side(Enum) :
	# 定义边
	left = 'l'
	right = 'r'
	middle = 'm'



@unique
class Direction(Enum) :
	# 定义轴向
	y_positive = [0 , 1 , 0]
	y_negative = [0 , -1 , 0]
	x_POSITIVE = [1 , 0 , 0]
	x_negative = [-1 , 0 , 0]
	z_POSITIVE = [0 , 0 , 1]
	z_negative = [0 , 0 , -1]
