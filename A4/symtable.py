from __future__ import print_function
import glob
from collections import OrderedDict

class RootTable():

	def __init__(self):
		self.parent = None
		self.globals = OrderedDict()
		self.funclist = OrderedDict()

	def print_root(self):
		for g in self.globals:
			print(g)
			self.globals[g].print_attr()
			print("---------")
		for f in self.funclist:
			print(f)
			self.funclist[f].print_table()
			print("!!!!!!!!!")

	def add_function(self,fname):
		new_symtable = SymbolTable(self)
		if fname in self.funclist:
			return (new_symtable,False)
		else: 
			self.funclist[fname] = new_symtable
			return (new_symtable,True)

	def add_symlist(self,symlist):
		status,errvarlist = True, []
		for i in range(len(symlist)):
			(var,tstatus) = self.add_global(symlist[i])
			status = tstatus and status
			if not tstatus: errvarlist.append(var)
		return (errvarlist,status)
			
	def add_symbol(self,symbol):
		if symbol.var_name in self.globals:
			return (symbol.var_name,False)
		else:
			self.globals[symbol.var_name] = symbol
			return (symbol.var_name,True)

	def lookup_table(self,attr):
		var_name = attr.var_name
		if var_name in self.globals:
			return (self.globals[var_name].type,self.globals[var_name].indirection,True)
		else:
			return (None,None,False)

class SymbolTable():

	def __init__(self,parent):
		self.parent = parent
		self.ftype = None
		self.args = OrderedDict()
		self.locals = OrderedDict()
		self.scopelist = OrderedDict()

	def print_table(self):
		for arg in self.args:
			print(arg)
			self.args[arg].print_attr()
		for local in self.locals:
			print(local)
			self.locals[local].print_attr()
		for scope in self.scopelist:
			print(scope)
			self.scopelist[scope].print_table()

	def add_symbol(self,symbol):
		if symbol.var_name in self.locals: #Check with self.args too (Ask Jabalpur)
			return (symbol.var_name,False)
		else:
			self.locals[symbol.var_name] = symbol
			return (symbol.var_name,True)

	def add_arg(self,arg):
		if arg.var_name in self.args: 
			return (arg.var_name,False)
		else:
			self.args[arg.var_name] = arg
			return (arg.var_name,True) 

	def lookup_table(self,attr):
		var_name = attr.var_name
		if var_name in self.locals:
			return (self.locals[var_name].type,self.locals[var_name].indirection,True)
		elif var_name in self.args:
			return (self.args[var_name].type,self.args[var_name].indirection,True)
		else:
			return (None,None,False)

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

def lookup(symtable,attr):

	if symtable.parent == None:
		return (None,None,False)
	else:
		(symtype,indirection,status) = symtable.lookup_table(attr)
		if status:
			return (symtype,indirection,True)
		else:
			return lookup(symtable.parent,attr) 
