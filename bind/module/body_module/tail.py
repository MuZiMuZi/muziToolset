from bind.chain import chainIKFK



class Tail(chainIKFK.ChainIKFK) :
	
	
	
	def __init__(self , side , name , joint_number , direction , is_stretch = 1 , length = 10 , joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , is_stretch , length , joint_parent , control_parent)
		self._rtype = 'Tail'



if __name__ == '__main__' :
	def x() :
		finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
		                     joint_parent = None , control_parent = None)
		finger_l.build_setup()
	
	
	
	def y() :
		finger_l = tail.Tail(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
		                     joint_parent = None , control_parent = None)
		finger_l.build_rig()
	
	
	
	x()
	y()
