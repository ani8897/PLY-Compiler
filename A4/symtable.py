from __future__ import print_function
import glob

class RootTable():

	def __init__(self):
		self.globals = {}
		self.funclist = {}

	def print_root(self):
		for g in self.globals:
			print(g)
			self.globals[g].print_attr()
			print("---------")
		for f in self.funclist:
			print(f)
			self.funclist[f].print_table()
			print("!!!!!!!!!")


class SymbolTable():

	def __init__(self,parent):
		self.parent = parent
		self.locals = {}
		self.scopelist = {}

	def print_table(self):
		for local in self.locals:
			print(local)
			self.locals[local].print_attr()
		for scope in self.scopelist:
			print(scope)
			self.scopelist[scope].print_table()

class Attributes():

	def __init__(self,var_name,var_type = None ,width = None ,indirection = None ,offset = None):
		self.var_name = var_name
		self.type = var_type
		self.width = width
		self.indirection = indirection
		self.offset = offset

	def print_attr(self):
		print("name: %s type: %s indirection: %d"%(self.var_name,self.type,self.indirection))

class SDTS():

	def __init__(self,node,syminfo = None):
		self.node = node
		self.syminfo = syminfo