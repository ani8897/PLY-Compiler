#!/usr/bin/python3

from __future__ import print_function
import sys
import ply.lex as lex
import ply.yacc as yacc


tokens = (
		'ID', 'NUMBER',
		'COMMENT',
		'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
		'SEMICOLON','AND','OR', 'COMMA',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 
		'INT', 'VOID', 'MAIN', 
		'IF', 'ELSE', 'WHILE',
		'LESSER','GREATER','LESSEREQUAL','GREATEREQUAL','EQUALITY','UNEQUAL',
)

t_ignore = " \t"

def t_newline(t):
	r'\n|\r\n'
	globals()["line"] += len(t.value)

t_LESSEREQUAL = r'<='
t_GREATEREQUAL = r'>='
t_EQUALITY = r'=='
t_UNEQUAL = r'!='
t_LESSER = r'<'
t_GREATER = r'>'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_AND = r'\&'
t_OR = r'\|'
t_COMMA = r','

reserved = {
	'int' 	: 'INT',
	'void' 	: 'VOID',
	'main' 	: 'MAIN',
	'if'	: 'IF',
	'else'	: 'ELSE',
	'while'	: 'WHILE',
}

def t_COMMENT(t):
	r'//.*'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'ID')
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
	print("Illegal character %s" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
precedence = (
	('right', 'EQUALS'),
	('left', 'OR'),
	('left', 'AND'),
	('left', 'EQUALITY', 'UNEQUAL'),
	('left', 'LESSER', 'GREATER', 'LESSEREQUAL', 'GREATEREQUAL'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('right', 'UMINUS'),
	('right', 'AMPERSAND','STAR'),
	('left', 'IFX'),
	('left', 'ELSE')
)

def yaccprint(p):
	for x in p: print(x)
	print("\n")
####################### RULES ###################

def p_start(p):
	'''
	start : function
	'''
	for t in globals()["trees"]:
		if t.is_const and t.children[0].token[0:3] == 'VAR':
			print("Syntax error at ",t.children[0].token[4:-1]," =")
			exit(0)
		t.print_node(0,rfile = globals()["output_file"])
		print('',file = globals()["output_file"])
	print("Successfully Parsed")
	pass

def p_function(p):
	'''
	function : VOID MAIN LPAREN RPAREN LBRACE statements RBRACE
	type : INT
		| VOID		
	'''
	pass

def p_var(p):
	'''
	var : ID
	'''
	p[0] = Node('VAR('+p[1]+')',[],False)

def p_const(p):
	'''
	const : NUMBER
	'''
	p[0] = Node('CONST('+str(p[1])+')',[],True)


def p_pointer(p):
	'''
	pointer : TIMES pointer %prec STAR
			| TIMES address %prec STAR
			| TIMES var %prec STAR
	'''
	p[0] = Node('DEREF',[p[2]],False)

def p_address(p):
	'''
	address : AND pointer %prec AMPERSAND
			| AND address %prec AMPERSAND
			| AND var %prec AMPERSAND
	'''
	p[0] = Node('ADDR',[p[2]],False)

def p_statements(p):
	'''
	statements :  statement statements
				| 
	statement : declaration
			| assignment
			| ifstatement
			| whilestatement
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
			| ID
			| pointer
	'''
	pass

def p_assignment(p):
	'''
	assignment : pointer EQUALS expression SEMICOLON
				| var EQUALS expression SEMICOLON
	'''
	p[0] = Node('ASGN',[p[1],p[3]],p[3].is_const)
	globals()["trees"].append(p[0])



def p_condition(p):
	'''
	condition :	condition LESSER condition
				| condition GREATER condition
				| condition LESSEREQUAL condition
				| condition GREATEREQUAL condition
				| condition EQUALITY condition
				| condition UNEQUAL condition
				| condition AND condition
				| condition OR condition
				| expression
	'''
	pass

def p_controlbody(p):
	'''
	controlbody : LBRACE statements RBRACE
			| statement
			| SEMICOLON
	'''
	pass

def p_ifstatement(p):
	'''
	ifstatement : IF LPAREN condition RPAREN controlbody %prec IFX
				| IF LPAREN condition RPAREN controlbody ELSE controlbody
	'''
	pass

def p_whilestatement(p):
	'''
	whilestatement : WHILE LPAREN condition RPAREN controlbody
	'''
	pass



def p_expression(p):
	'''
	expression : expression PLUS expression
				| expression MINUS expression
				| expression TIMES expression
				| expression DIVIDE expression
				| pointer
				| address
				| const
				| var
				| LPAREN expression RPAREN
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif p[2] == '+':
		p[0] = Node('PLUS',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '-':
		p[0] = Node('MINUS',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '*':
		p[0] = Node('MUL',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '/':
		p[0] = Node('DIV',[p[1],p[3]],p[1].is_const and p[3].is_const)
	else :
		p[0] = p[2]

def p_expression_uminus(p):
	'''
	expression : MINUS expression %prec UMINUS
	'''
	p[0] = Node('UMINUS',[p[2]],p[2].is_const)
	pass

def p_error(p):
	if p:
		print("Syntax error at '{0}' line no  '{1}'".format(p.value,globals()["line"]))
	else:
		print("Syntax error at EOF")

####################### END ####################

class Node:
	def __init__(self,token,children,is_const):
		self.token = token
		self.children = children
		self.is_const = is_const

	def print_node(self,depth,rfile=1):
		print('\t'*depth + self.token, file=rfile)
		if len(self.children) != 0:
			i = 0
			print('\t'*depth + '(', file=rfile)
			for child in self.children:
				i+=1
				child.print_node(depth+1,rfile)
				if(i < len(self.children)): print('\t'*(depth+1) + ',', file=rfile)
			print('\t'*depth + ')', file=rfile)

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

	globals()["line"] = 1
	globals()["trees"] = []
	globals()["output_file"] = open('Parser_ast_' + sys.argv[1] + '.txt','w')
	process(data)
