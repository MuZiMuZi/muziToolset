import muziToolset.bind.module.face_module.eye as eye
# from importlib import reload

print(25)

reload(eye)



def build_setup() :
	eye_l = eye.Eye(side = 'l' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
	                control_parent = None)
	eye_l.build_setup()
	
	eye_r = eye.Eye(side = 'r' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
	                control_parent = None)
	eye_r.build_setup()



def build_rig() :
	eye_l = eye.Eye(side = 'l' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
	                control_parent = None)
	eye_l.build_rig()
	
	eye_r = eye.Eye(side = 'r' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
	                control_parent = None)
	eye_r.build_rig()



#
build_setup()
# build_rig()
