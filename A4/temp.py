def p_args(p):
	'''
	args : arg argcomp
		|
	  
	'''
	if len(p) == 1:
		p[0] = []
	else:
		p[2].insert(0,p[1])
		p[0] = p[2]
