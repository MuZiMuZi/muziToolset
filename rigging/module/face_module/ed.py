driven_list = [1,2,3,4,5,6,7]


[0,3,6]
[0,2,3]
[0,1,2]
[3,4,6]
[4,5,6]


for index in range(len(driven_list)) :
	front_driver = index - 1
	after_driver = index + 1
	driven = index
	# 判断为首部或者是尾部的情况下
	if index == 0 or index == len(driven_list) :
		pass
	# 判断为中间的数值的时候
	if index == len(driven_list) / 2 :
		print(index)
	else :
		pass