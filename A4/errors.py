def raiseError(var_name,line_number):
	print("SDTS error: '%s' at line %d"%(var_name,line_number))

def raiseNotDeclared(var_name,line_number):
	print("variable '%s' at line %d not declared but used"%(var_name,line_number)) 

def raiseFunctionNotDefined(fname,line_number):
	print("function '%s' at line %d not defined"%(fname,line_number)) 

def raiseParamTypeMismatch(param,expected_param,fname,line_number):
	print("type of parameter '%s' does not match with expected type of '%s' in function '%s' at line %d"%(param,expected_param,fname,line_number)) 

def raiseNumParamMismatch(paramcount, eparamcount, fname,line_number):
	print("Expected number of parameters: %d, Number of parameters given: %d, in function '%s' at line %d"%(eparamcount, paramcount, fname,line_number))