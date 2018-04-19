class Register():
	def __init__(self):
		self.freelist = ['s0','s1','s2','s3','s4','s5','s6','s7','t0','t1','t2','t3','t4','t5','t6','t7','t8','t9']
		self.fpfreelist = ['f10','f12','f14','f16','f18','f20','f22','f24','f26','f28','f30']
		self.mapping = {}

	def fetch_register(self,is_float=False):
		if is_float:
			return self.fpfreelist.pop(0)
		return self.freelist.pop(0)

	def free_register(self,reg_name):
		if reg_name[0] == 'f':
			self.fpfreelist.append(reg_name)
			self.fpfreelist.sort()
		else:
			self.freelist.append(reg_name)
			self.freelist.sort()

	def add_mapping(self,temp_name, is_float=False):
		new_reg = self.fetch_register(is_float)
		self.mapping[temp_name] = new_reg
		return new_reg

	def clear_mapping(self,temp_name):	
		self.free_register(self.mapping.pop(temp_name))

	def get_mapping(self,temp_name):
		return self.mapping[temp_name]

	def is_float(self, temp_name):
		return self.mapping[temp_name][0] == 'f'

	def is_float_reg(self, reg_name):
		return reg_name[0] == 'f'