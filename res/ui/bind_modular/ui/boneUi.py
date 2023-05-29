from functools import wraps



def update_base_name(func) :
	"""
	更新组件模块中的名称属性和结构
	"""
	
	
	
	@wraps(func)
	def wrap(self) :
		self.base = '{}_{}_{}'.format(
				self._rtype , self._side.value , self._name)
		func(self)
	
	
	
	return wrap
