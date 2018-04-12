import glob
from pyparsing import ParseException
type_sizes = {
	'int': '.word	0',
	'float' : '.space	8'
}

def generate_global(rfile):
	print(glob.data,file=rfile)

	for g in glob.root_table.globals:
		if glob.root_table.globals[g].type == 'int' or glob.root_table.globals[g].indirection != 0:
			print(glob.global_var%(glob.root_table.globals[g].var_name,type_sizes['int']),file=rfile)
		else:
			print(glob.global_var%(glob.root_table.globals[g].var_name,type_sizes['float']),file=rfile)
	print("",file=rfile)
	print(glob.text,file=rfile)

	if 'main' in glob.root_table.funclist:
		print(glob.globl%('main'),file=rfile)
	else:
		funclist = list(glob.root_table.funclist)
		print(glob.globl%(funclist[0]),file=rfile)

#### Parsing cfg ###

def parse_label(row,rfile):

	try:
		res = glob.label_parser.parseString(row)
		print(glob.label%int(res.block_num),file=rfile)
		return True
	except ParseException:
		return False

def parse_if(row,rfile):
	return False

def parse_else(row,rfile):
	return False

def parse_goto(row,rfile):
	return False

def parse_return(row,fname,rfile):

	tokens = row.split()
	if tokens[0] == 'return' and len(tokens) == 1:
		print(glob.jump_epilogue%fname,file=rfile)
		return True
	try:
		res = glob.return_parser.parseString(row)
		print(glob.jump_epilogue%fname,file=rfile)
		return True
	except ParseException:
		return False

####################
def generate_body(fname,rfile):

	while True:
		row = glob.cfg_file.readline()
		tokens = row.split()
		if len(tokens) != 0:
			# if tokens[0] == 'return':
			# 	print(glob.jump_epilogue%fname,file=rfile)
			# 	return
			if parse_label(row,rfile): continue
			if parse_if(row,rfile): continue
			if parse_else(row,rfile): continue
			if parse_goto(row,rfile): continue
			if parse_return(row,fname,rfile): return
		else:
			if row == 'return':
				print(glob.jump_epilogue%fname,file=rfile)
				return

def translate_cfg(rfile):

	while True:
		row = glob.cfg_file.readline()
		tokens = row.split()
		try:
			if tokens[0] == "function":
				fname = tokens[1].split('(')[0]
				print("%s:"%fname,file=rfile)
				num_locals = glob.root_table.get_size(fname)
				print(glob.prologue%num_locals,file=rfile)
				generate_body(fname,rfile)
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