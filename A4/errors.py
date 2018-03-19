def raiseError(var_name,line_number):
	print("SDTS error: '%s' at line %d"%(var_name,line_number))

def raiseNotDeclared(var_name,line_number):
	print("variable '%s' at line %d not declared but used"%(var_name,line_number)) 