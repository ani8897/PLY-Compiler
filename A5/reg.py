class Register():
	def __init__(self):
		self.freelist = ['s0','s1','s2','s3','s4','s5','s6','s7','t0','t1','t2','t3','t4','t5','t6','t7','t8','t9']
		self.mapping = {}

	def fetch_register(self):
		return self.freelist.pop(0)

	def free_register(self,reg_name):
		self.freelist.append(reg_name)
		self.freelist.sort()

	def add_mapping(self,temp_name):
		new_reg = fetch_register(self)
		self.mapping[temp_name] = new_reg
		return new_reg

	def clear_mapping(self,temp_name):
		free_register(self,self.mapping.pop(temp_name))