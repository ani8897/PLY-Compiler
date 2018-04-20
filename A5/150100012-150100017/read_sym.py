import glob
from pyparsing import ParseException
from collections import OrderedDict
from cfg_parser import generate_body


def generate_global(rfile):
	print(glob.data,file=rfile)
	sorted_globals = OrderedDict(sorted(glob.root_table.globals.items()))
	for g in sorted_globals:
		if sorted_globals[g].type == 'int' or sorted_globals[g].indirection != 0:
			print(glob.global_var%(sorted_globals[g].var_name,glob.type_sizes['int']),file=rfile)
		else:
			print(glob.global_var%(sorted_globals[g].var_name,glob.type_sizes['float']),file=rfile)
	print("",file=rfile)
	# print(glob.text,file=rfile)

	# if 'main' in glob.root_table.funclist:
	# 	print(glob.globl%('main'),file=rfile)
	# else:
	# 	funclist = list(glob.root_table.funclist)
	# 	print(glob.globl%(funclist[0]),file=rfile)

#### Parsing cfg ###

def parse_blocks(fname,rfile):

	glob.stmtreturn = False
	while not glob.stmtreturn:
		row = glob.cfg_file.readline()
		generate_body(row,fname,rfile)

def translate_cfg(rfile):

	while True:
		row = glob.cfg_file.readline()
		tokens = row.split()
		try:
			if tokens[0] == "function":
				fname = tokens[1].split('(')[0]
				##Errors.txt changes
				print(glob.text,file=rfile)
				print(glob.globl%(fname),file=rfile)
				##
				print("%s:"%fname,file=rfile)
				num_locals = glob.root_table.get_size(fname)
				print(glob.prologue%num_locals,file=rfile)

				parse_blocks(fname,rfile)
				
				print(glob.epilogue%(fname,num_locals),file=rfile)
		except IndexError:
			if row == '\n': 
				continue
			else: 
				break			




def generate_assembly(rfile):
	generate_global(rfile)
	glob.cfg_file.seek(0,0)
	translate_cfg(rfile)