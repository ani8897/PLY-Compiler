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
		elif fname in self.funclist and self.funclist[fname].proto:
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
			return (self.funclist[fname].ftype,self.funclist[fname].findirection,self.funclist[fname].protoargs,True)
		else:
			return (None,None,None,False)

	def print_symbol_table(self,rfile):
		print("Procedure table :-",file=rfile)
		print("-----------------------------------------------------------------",file=rfile)
		print("Name\t\t|\tReturn Type\t|\tParameter List",file=rfile)
		for function in self.funclist:
			if function == 'main':	continue
			print("%s\t\t|\t %s%s\t|\t"%(self.funclist[function].fname,self.funclist[function].ftype,'*'*self.funclist[function].findirection),end='',file=rfile)
			if not self.funclist[function].proto:
				funcargs = list(self.funclist[function].args.items())
				for i in range(len(funcargs)):
					if i == len(funcargs) - 1:
						print("%s "%funcargs[i][1].type+"*"*funcargs[i][1].indirection+" %s"%funcargs[i][0],end='',file=rfile)
					else:	
						print("%s "%funcargs[i][1].type+"*"*funcargs[i][1].indirection+" %s"%funcargs[i][0],end=', ',file=rfile)
				print("",file=rfile)
			else:
				funcargs = self.funclist[function].protoargs
				for i in range(len(funcargs)):
					if i == len(funcargs) - 1:
						print("%s "%funcargs[i][0]+"*"*funcargs[i][1]+" %s"%funcargs[i][2],end='',file=rfile)
					else:	
						print("%s "%funcargs[i][0]+"*"*funcargs[i][1]+" %s"%funcargs[i][2],end=', ',file=rfile)
				print("",file=rfile)
		print("-----------------------------------------------------------------",file=rfile)
		print("Variable table :-",file=rfile)
		print("-----------------------------------------------------------------",file=rfile)
		print("Name\t\t|\tScope\t\t|\tBase Type\t|\tDerived Type",file=rfile)
		print("-----------------------------------------------------------------",file=rfile)
		globe_list = self.globals
		for gvar in globe_list:
			print("%s\t\t|\tglobal\t|\t%s\t|\t%s"%(gvar,globe_list[gvar].type,"*"*globe_list[gvar].indirection),file=rfile)
		for function in self.funclist:
			symtable = self.funclist[function]
			for arg in symtable.args:
				print("%s\t\t|\tprocedure %s\t|\t%s\t|\t%s"%(symtable.args[arg].var_name,function,symtable.args[arg].type,"*"*symtable.args[arg].indirection),file=rfile)
			for local in symtable.locals:
				print("%s\t\t|\tprocedure %s\t|\t%s\t|\t%s"%(symtable.locals[local].var_name,function,symtable.locals[local].type,"*"*symtable.locals[local].indirection),file=rfile)
		print("-----------------------------------------------------------------",file=rfile)
		print("-----------------------------------------------------------------",file=rfile)



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
		self.protoargs.append((arg.type,arg.indirection,arg.var_name))

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
		return ('int',0,True)
	if attr.is_float:
		return ('float',0,True)

	if symtable == None:
		return (None,None,False)
	else:
		(symtype,indirection,status) = symtable.lookup_table(attr)
		if status:
			return (symtype,indirection,True)
		else:
			return lookup(symtable.parent,attr) 

def function_lookup(symtable,fname,paramlist):

	(ftype,findirection,protoargs,status) = glob.root_table.check_function(fname)
	
	if not status:
		raiseFunctionNotDefined(p[1].syminfo.var_name,glob.line_number)
		return (None,None,False)

	# arglist = args.items()
	if len(protoargs) != len(paramlist):
		raiseNumParamMismatch(len(paramlist),len(protoargs),fname,glob.line_number)
		return (ftype,findirection,True)

	for p in range(len(paramlist)):
		(symtype,symindirection) = paramlist[p]
		if protoargs[p][0] != symtype or (protoargs[p][1] != symindirection):
			raiseParamTypeMismatch('expression','arglist_var_name',fname,glob.line_number) 
	return (ftype,findirection,True)	


