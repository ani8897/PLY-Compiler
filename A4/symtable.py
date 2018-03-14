from __future__ import print_function
import glob

class RootTable():

	def __init__(self):
		self.globals = {}
		self.funclist = {}

class SymbolTable():

	def __init__(self,parent):
		self.parent = parent
		self.locals = {}
		self.scopelist = {}

class Attributes():

	def __init__(self,var_type,width,indirection,offset):
		self.type = var_type
		self.width = width
		self.indirection = indirection
		self.offset = offset
