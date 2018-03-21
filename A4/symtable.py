from __future__ import print_function
import glob
from errors import *
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

	def add_function(self,fname,findirection):
		new_symtable = SymbolTable(self)
		if fname in self.funclist and self.funclist[fname].definition:
			return (new_symtable,False)
		elif fname in self.funclist and self.proto:
			return (self.funclist[fname],True)
		else: 
			self.funclist[fname] = new_symtable
			self.funclist[fname].findirection = findirection
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

	def check_function(self,fname):
		if fname in self.funclist:
			return (self.funclist[fname].ftype,self.funclist[fname].args,True)
		else:
			return (None,False)

class SymbolTable():

	def __init__(self,parent):
		self.parent = parent
		self.fname = None
		self.ftype = None
		self.findirection = None
		self.protoargs = []
		self.args = OrderedDict()
		self.locals = OrderedDict()
		self.scopelist = OrderedDict()
		self.proto = False
		self.definition = False


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

	def add_protoarglist(self,protoarglist):
		for protoarg in protoarglist:
			self.add_protoarg(protoarg[0])

	def add_protoarg(self,arg):
		self.protoargs.append((arg.type,arg.indirection))

	def add_arglist(self,arglist):
		for arg in arglist:
			(arg_name,status) = self.add_arg(arg[0],arg[1])
			if not status: 
				raisePreviouslyDeclared(arg_name,arg[1])

	def add_arg(self,arg,line_number):
		args_added = len(self.args.items())
		if self.proto:
			if arg.var_name in self.args: 
				return (arg.var_name,False)
			else:
				protoarg = self.protoargs[args_added]
				if protoarg[0] != arg.type:
					raiseProtoParamTypeMismatch(self.fname,arg.var_name,arg.type,protoarg[0],line_number)
				elif protoarg[1] != arg.indirection:
					raiseProtoParamIndirectionMismatch(self.fname,arg.var_name,arg.indirection,protoarg[1],line_number)
				self.args[arg.var_name] = arg
				return (arg.var_name,True) 
		else:
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

	def __init__(self,var_name,var_type = None ,width = None ,indirection = None ,offset = None,is_int = False,is_float = False):
		self.var_name = var_name
		self.type = var_type
		self.width = width
		self.indirection = indirection
		self.offset = offset
		self.is_int = is_int
		self.is_float = is_float

	def print_attr(self):
		print("name: %s type: %s indirection: %d"%(self.var_name,self.type,self.indirection))

class SDTS():

	def __init__(self,node,syminfo = None):
		self.node = node
		self.syminfo = syminfo

def lookup(symtable,attr):

	if attr.is_int:
		return ('INT',0,True)
	if attr.is_float:
		return ('FLOAT',0,True)

	if symtable.parent == None:
		return (None,None,False)
	else:
		(symtype,indirection,status) = symtable.lookup_table(attr)
		if status:
			return (symtype,indirection,True)
		else:
			return lookup(symtable.parent,attr) 

def function_lookup(symtable,fname,paramlist):

	(ftype,args,status) = glob.root_table.check_function(fname)
	
	if not status:
		raiseFunctionNotDefined(p[1].syminfo.var_name,glob.line_number)
		return (None,False)

	arglist = args.items()
	if len(arglist) != len(paramlist):
		raiseNumParamMismatch(len(paramlist),len(arglist),fname,glob.line_number)
		return (ftype,True)

	for p in range(len(paramlist)):
		(symtype,symindirection,status) = lookup(symtable,paramlist[p])
		if arglist[p][1].type != symtype or (arglist[p][1].indirection != symindirection - paramlist[p].indirection):
			raiseParamTypeMismatch(paramlist[p].var_name,arglist[p][1].var_name,fname,glob.line_number) 
	return (ftype,True)	


