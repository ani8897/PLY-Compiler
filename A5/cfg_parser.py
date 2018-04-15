#!/usr/bin/python3

from __future__ import print_function
import sys
import ply.lex as lex
import ply.yacc as yacc

import glob

tokens = (
		'ID','TEMPVAR','NUMBER','FLOATNUM',
		'LPAREN', 'RPAREN', 'BLOCK',
		'AMPERSAND', 'COMMA',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 
		'IF', 'ELSE', 'RETURN','GOTO',
		'LT','GT','LE','GE','EQ','NE','NOT','AND', 'OR'
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
t_AND = r'\&\&'
t_OR = r'\|\|'
t_AMPERSAND = r'\&'
t_COMMA = r','

reserved = {
	'if'	: 'IF',
	'else'	: 'ELSE',
	'goto' : 'GOTO',
	'return' : 'RETURN',
	'bb' : 'BLOCK'
}

def t_TEMPVAR(t):
	r't[0-9]+'
	return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'ID')
	return t


def t_FLOATNUM(t):
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
	('right', 'AMPERSAND','STAR'),
)

def yaccprint(p):
	for x in p: print(x)
	print("\n")

####################### RULES ###################

def p_statement(p):
	'''
	statement : label 
			| assignment
			| ifstmt
			| elsestmt
			| gotostmt
			| returnstmt
			| funcall
			|
	'''
	pass

def p_pointer(p):
	'''
	pointer : TIMES pointer %prec STAR
			| TIMES address %prec STAR
			| TIMES ID %prec STAR
	'''
	if p[2][0] == 'A':
		p[0] = ('P',p[2][1],p[2][2]+1)
	elif p[2][0] == 'P':
		p[0] = ('P',p[2][1],p[2][2]+1)
	else:
		p[0] = ('P',p[2],1)
		

def p_address(p):
	'''
	address : AMPERSAND ID
	'''
	p[0] = ('A',p[2],-1)


def p_var_id(p):
	'''
	var : ID
	'''
	p[0] = ('I',p[1],0)

def p_var_tempvar(p):
	'''
	var : TEMPVAR
	'''
	p[0] = ('T',p[1],0)

def p_var_const(p):
	'''
	var : const
	'''
	p[0] = ('C',p[1],0)

def p_var_pointer(p):
	'''
	var : pointer
	'''
	p[0] = p[1]

def p_const(p):
	'''
	const : NUMBER
		| FLOATNUM
	'''
	reg = glob.registers.fetch_register()
	print(glob.li%(reg,p[1]),file=globals()['rfile'])
	p[0] = reg

def p_label(p):
	'''
	label : LT BLOCK NUMBER GT
	'''
	print(glob.label%int(p[3]),file=globals()['rfile'])

def p_assignment(p):
	'''
	assignment : unassign
			| binassign
			| funassign
	'''
	pass

def p_funassign(p):
	'''
	funassign : var EQUALS funcall
	'''
	pass

def p_funcall(p):
	'''
	funcall : var LPAREN params RPAREN
	params : var paramcomp
			|
	'''
	pass

def p_paramcomp(p):
	'''
	paramcomp : COMMA var paramcomp
			|
	'''
	pass

def p_unassign(p):
	'''
	unassign : var EQUALS var
			| var EQUALS MINUS var
			| var EQUALS NOT var
			| var EQUALS address
	'''
	try:
		rt,ft = glob.root_table, glob.root_table.funclist[globals()['fname']]
		if len(p) == 4:
			if p[3][0] == 'A':

				r_reg = glob.registers.fetch_register()
				if p[3][1] in rt.globals:
					print(glob.la%(r_reg,p[3][1]),file=globals()['rfile'])
				else:
					offset = ft.var_offset(p[3][1])
					print(glob.addi%(r_reg,'sp',offset),file=globals()['rfile'])
				
				l_reg = glob.registers.fetch_register()
				if p[1][0] == 'P':
					if p[1][1] in rt.globals:
						print(glob.la%(l_reg,p[1][1]),file=globals()['rfile'])
					else:
						offset = ft.var_offset(p[1][1])
						print(glob.lw%(l_reg,offset,'sp'),file=globals()['rfile'])
					
					for indirection in  range(p[1][2] - 1):
						t_reg = glob.registers.fetch_register()
						print(glob.lw%(t_reg,0,l_reg),file=globals()['rfile'])
						glob.registers.free_register(l_reg)
						l_reg = t_reg

					print(glob.sw%(r_reg,0,l_reg),file=globals()['rfile'])
					glob.registers.free_register(l_reg)
					glob.registers.free_register(r_reg)
	except:
		pass




def p_binassign(p):
	'''
	binassign : var EQUALS var binop var
	'''
	pass

def p_binop(p):
	'''
	binop : condop 
		| arithop
	'''
	pass

def p_condop(p):
	'''
	condop : LT
			| GT
			| GE
			| LE
			| EQ
			| NE
			| AND
			| OR
	'''
	pass

def p_arithop(p):
	'''
	arithop : PLUS
			| MINUS
			| TIMES
			| DIVIDE
	'''
	pass

def p_ifstmt(p):
	'''
	ifstmt : IF LPAREN TEMPVAR RPAREN GOTO LT BLOCK NUMBER GT
	'''
	pass

def p_elsestmt(p):
	'''
	elsestmt : ELSE gotostmt
	'''
	pass

def p_gotostmt(p):
	'''
	gotostmt : GOTO LT BLOCK NUMBER GT
	'''
	print(glob.jump_statement%int(p[4]),file=globals()['rfile'])

def p_returnstmt(p):
	'''
	returnstmt : RETURN
			| RETURN var
			| RETURN address
	'''
	glob.stmtreturn = True
	print(glob.jump_epilogue%globals()['fname'],file=globals()['rfile'])

def p_error(p):
	if p:
		print("Syntax error at '{0}' line no  '{1}'".format(p.value,glob.line_number))
	else:
		print("Syntax error at EOF")

def generate_body(data,fname,rfile):
	# print(data)
	globals()['fname'] = fname
	globals()['rfile'] = rfile
	lex.lex()
	yacc.yacc(debug = False, write_tables = False)
	yacc.parse(data)
