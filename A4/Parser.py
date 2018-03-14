#!/usr/bin/python3

from __future__ import print_function
import sys
import ply.lex as lex
import ply.yacc as yacc

from ast import Node
from cfg import *
from symtable import *
import glob

tokens = (
		'ID', 'NUMBER',
		'COMMENT',
		'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
		'SEMICOLON', 'AMPERSAND', 'COMMA',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 
		'INT', 'VOID', 'FLOAT', 'MAIN', 
		'IF', 'ELSE', 'WHILE',
		'LT','GT','LE','GE','EQ','NE','NOT', 'AND', 'OR'
)

t_ignore = " \t"

def t_newline(t):
	r'\n|\r\n'
	glob.line_number += len(t.value)

t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'\!\='
t_NOT = r'\!'
t_LT = r'<'
t_GT = r'>'

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
t_AND = r'\&\&'
t_OR = r'\|\|'
t_AMPERSAND = r'\&'
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

def t_FLOAT(t):
	r'\d+\.\d+'
	try:
		t.value = float(t.value)
	except ValueError:
		print("Float value too precise %d", t.value)
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
	print("Illegal character %s" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
precedence = (
	('right', 'EQUALS'),
	('left', 'OR'),
	('left', 'AND'),
	('left', 'EQ', 'NE','NOT'),
	('left', 'LT', 'GT', 'LE', 'GE'),
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

def p_program(p):
	'''
	program : declarations funcdefs
	'''
	p[1].print_node(0,rfile = glob.ast_file)
	construct_cfg(p[1])
	glob.cfg.blocks[glob.block_index] = Block(glob.block_index,'',["End"],-1,[])
	glob.block_index = 1
	update_cfg(p[1])
	glob.cfg.cfg_print(rfile = glob.cfg_file)
	print("Successfully Parsed")


def p_funcdefs(p):
	'''
	funcdefs : function funcdefs
			| function
	'''
	pass

def p_declarations(p):
	'''
	declarations : declarations declaration
				|
	'''
	pass


def p_function(p):
	'''
	function : type fname LPAREN args RPAREN LBRACE statements RBRACE
	fname : ID
		  | MAIN
	type : INT
		| VOID
		| FLOAT
	'''
	if len(p) != 2:
		p[0] = p[6]

def p_args(p):
	'''
	args : arg argcomp
		|
	argcomp : COMMA arg argcomp
		|  
	arg : type param
	param : var 
		| pointer 
		| address
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
		| FLOAT
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
	address : AMPERSAND pointer
			| AMPERSAND address
			| AMPERSAND var
	'''
	p[0] = Node('ADDR',[p[2]],False)

def p_voidfuncall(p):
	'''
	voidfuncall : funcall SEMICOLON
	'''
	pass

def p_funcall(p):
	'''
	funcall : var LPAREN params RPAREN
	params : callparam paramcomp
			|
	paramcomp : COMMA callparam paramcomp
			| 
	callparam : param
			| const
	'''
	pass

def p_statements(p):
	'''
	statements :  statement statements
				| COMMENT statements
				| declaration statements
				| voidfuncall statements
				| 
	statement : assignment
			| ifstatement
			| whilestatement
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif (len(p) == 3):
		try:
			if p[1].token != 'DECL':
				p[0] = Node('STMTS',[p[1]] + p[2].children)
			else:
				p[0] = p[2]
		except:
			p[0] = p[2]
	else:
		p[0] = Node('STMTS',[])

def p_declaration(p):
	'''
	declaration : type idlist SEMICOLON
	'''
	p[0] = Node('DECL',[])

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

def p_condition(p):
	'''
	condition :	expression LT expression
				| expression GT expression
				| expression LE expression
				| expression GE expression
				| expression EQ expression
				| expression NE expression
				| condition AND condition
				| condition OR condition
				| NOT condition
				| LPAREN condition RPAREN
	'''
	if len(p) == 2:
		p[0] = Node('NOT',[p[2]],p[2].is_const)
	if p[2] == '<':
		p[0] = Node('LT',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '>':
		p[0] = Node('GT',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '<=':
		p[0] = Node('LE',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '>=':
		p[0] = Node('GE',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '==':
		p[0] = Node('EQ',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '!=':
		p[0] = Node('NE',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '&&':
		p[0] = Node('AND',[p[1],p[3]],p[1].is_const and p[3].is_const)
	elif p[2] == '||':
		p[0] = Node('OR',[p[1],p[3]],p[1].is_const and p[3].is_const)
	else :
		p[0] = p[2]

def p_controlbody(p):
	'''
	controlbody : LBRACE statements RBRACE
			| statement
			| SEMICOLON
	'''
	if len(p) == 4:
		p[0] = p[2]
	elif p[1] == ';':
		p[0] = Node('STMTS',[])
	else:
		p[0] = Node('STMTS',[p[1]])

def p_ifstatement(p):
	'''
	ifstatement : IF LPAREN condition RPAREN controlbody %prec IFX
				| IF LPAREN condition RPAREN controlbody ELSE controlbody
	'''
	if len(p) == 6:
		p[0] = Node('IF',[p[3],p[5]])
	else:
		p[0] = Node('IF',[p[3],p[5],p[7]])

def p_whilestatement(p):
	'''
	whilestatement : WHILE LPAREN condition RPAREN controlbody
	'''
	p[0] = Node('WHILE',[p[3],p[5]])


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
				| funcall
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
		print("Syntax error at '{0}' line no  '{1}'".format(p.value,glob.line_number))
	else:
		print("Syntax error at EOF")

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Format: python assign3.py <filename>")
		exit(0)
	with open(sys.argv[1], 'r') as f:
		data = f.read()

	glob.ast_file = open(sys.argv[1] + '.ast','w')
	glob.cfg_file = open(sys.argv[1] + '.cfg','w')
	glob.cfg = CFG()
	
	process(data)