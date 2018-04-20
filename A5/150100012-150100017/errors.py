def raisePreviouslyDeclared(var_name,line_number):
	print("variable '%s' at line %d has been declared before"%(var_name,line_number))

def raiseNotDeclared(var_name,line_number):
	print("variable '%s' at line %d not declared but used"%(var_name,line_number)) 

def raiseFunctionNotDefined(fname,line_number):
	print("function '%s' at line %d not defined"%(fname,line_number)) 

def raiseParamTypeMismatch(fname,line_number):
	print("Parameter type mismatch in function '%s' at line %d"%(fname,line_number)) 

def raiseNumParamMismatch(paramcount, eparamcount, fname,line_number):
	print("Expected number of parameters: %d, Number of parameters given: %d, in function '%s' at line %d"%(eparamcount, paramcount, fname,line_number))

def raiseReturnValueIgnored(fname,line_number):
	print("Return value of function '%s' at line %d is ignored"%(fname,line_number))

def raiseTooMuchIndirection(var_name,line_number):
	print("Too much indirection on '%s' at line %d"%(var_name,line_number))

def raiseTypeMismatch(ltype,rtype,lindirection,rindirection,line_number):
	if lindirection == rindirection:
		print("Incompatible types, %s and %s, at line %d"%(ltype,rtype,line_number))
	else:
		print("Incompatible dereferencing at line %d"%(line_number))

def raiseProtoPreviouslyDeclared(fname,line_number):
	print("prototype for function '%s' at line %d has been declared before"%(fname,line_number))

def	raiseProtoParamTypeMismatch(fname,var_name,argtype,prototype,line_number):
	print("type '%s' of argument '%s' does not match with expected type '%s' in prototype declaration of function '%s' at line %d"%(argtype, var_name, prototype,fname,line_number))

def	raiseProtoParamIndirectionMismatch(fname,var_name,argindirection,protoindirection,line_number):
	print("Indirection '%d' of argument '%s' does not match with expected indirection '%d' in prototype declaration of function '%s' at line %d"%(argindirection, var_name, protoindirection,fname,line_number))

def raiseFunctionTypeMismatch(fname,ltype,rtype,lindirection,rindirection,line_number):
	if lindirection == rindirection:
		print("Incompatible types for function %s, with types %s and %s, at line %d"%(fname, ltype,rtype,line_number))
	else:
		print("Incompatible dereferencing for function %s at line %d"%(fname, line_number))

def raiseExpectedReturn(fname,expected_type,actual_type,expected_indirection,actual_indirection,line_number):
	if actual_indirection == expected_indirection:
		print("Incompatible return types in function %s , expected: %s and actual :%s, at line %d"%(fname,expected_type,actual_type,line_number))
	else:
		print("Incompatible dereferencing of return statement in function %s at line %d"%(fname, line_number))

def raiseDirectUseOfNonPointer(var_name,line_number):
	print("direct use of non pointer variable %s at line number %d"%(var_name,line_number))