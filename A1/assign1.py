#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc


tokens = (
		'ID', 'NUMBER','FLOAT_NUMBER',
		'COMMENT',
		'EQUALS',
		'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
		'SEMICOLON','STAR', 'AMPERSAND', 'COMMA', 
		'INT', 'FLOAT', 'CHAR', 'VOID', 'MAIN',
)

t_ignore = " \t"

def t_newline(t):
	r'\n+'
	globals()["line"] += len(t.value)

t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_STAR = r'\*'
t_AMPERSAND = r'\&'
t_COMMA = r','

reserved = {
	'int' : 'INT',
	'float' : 'FLOAT',
	'char' : 'CHAR',
	'void' : 'VOID',
	'main' : 'MAIN',
}

def t_COMMENT(t):
	r'//.*'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'ID')
	return t

def t_FLOAT_NUMBER(t):
	r'\d+\.\d+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too large %d", t.value)
		t.value = 0
	return t

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print("Integer value too large %d", t.value)
		t.value = 0
	return t

def t_error(t): 
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
precedence = (
	('left', 'COMMA'),
	('right', 'EQUALS'),
	('right', 'AMPERSAND','STAR'),

)

def yaccprint(p):
	for x in p: print(x)
	print("\n")
####################### RULES ###################

def p_start(p):
	'''
	start : function
	'''
	g = globals()
	print("%d\n%d\n%d"%(g["idec"],g["pdec"],g["ass"]))

def p_function(p):
	'''
	function : type MAIN LPAREN args RPAREN LBRACE statements RBRACE
	type : INT
		| FLOAT
		| CHAR
		| VOID		
	'''
	pass

def p_args(p):
	'''
		args : arg COMMA args
			| arg
			| 
		arg : type ID
	'''
	pass

def p_pointer(p):
	'''
	pointer : STAR pointer
			| STAR ID
	'''
	p[0] = '*'
	pass

def p_address(p):
	'''
	address : AMPERSAND ID
	'''
	pass

def p_statements(p):
	'''
	statements :  statement statements
				| 
	statement : declaration
			| xassignment
			| COMMENT
	'''
	pass

def p_declaration(p):
	'''
	declaration : type idlist SEMICOLON
	'''
	pass

def p_idlist(p):
	'''
	idlist : pointer COMMA idlist 
			| ID COMMA idlist 
			| assignment COMMA idlist
			| assignment
			| ID
			| pointer
	'''
	if p[1] == '*':
		globals()['pdec']+=1
	elif p[1] != '*':
		globals()['idec']+=1 
	pass

def p_xassignment(p):
	'''
	xassignment : assignmentlist SEMICOLON
	'''
	pass

def p_assignmentlist(p):
	'''
	assignmentlist : assignment COMMA assignmentlist 
					| assignment
	'''
	pass

def p_assignment(p):
	'''
	assignment : ID EQUALS idassign
				| pointer EQUALS pointerassign
	'''
	p[0] = p[3]
	pass

def p_idassign(p):
	'''
	idassign : ID EQUALS idassign
			| address EQUALS idassign
			| address
			| ID
			| NUMBER
			| FLOAT_NUMBER
	'''
	globals()["ass"]+=1

def p_pointerassign(p):
	'''
	pointerassign : ID EQUALS pointerassign
			| address EQUALS pointerassign
			| pointer EQUALS pointerassign
			| pointer
			| address
			| ID
			| NUMBER
	'''
	p[0] = '*'
	globals()["ass"]+=1

def p_error(p):
	if p:
		print("syntax error at {0}, line number = {1}".format(p.value,globals()["line"]))
	else:
		print("syntax error at EOF")

####################### END ####################
def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Format: python assign1.py <filename>")
		exit(0)
	with open(sys.argv[1], 'r') as f:
		data = f.read()

	g = globals()
	g["idec"],g["pdec"],g["ass"],g["line"] = 0,0,0,0
	process(data)
