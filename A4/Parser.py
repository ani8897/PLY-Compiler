#!/usr/bin/python3

from __future__ import print_function
import sys
import ply.lex as lex
import ply.yacc as yacc

from ast import Node
from cfg import *
from symtable import *
from errors import *
import glob

tokens = (
		'ID', 'NUMBER','FLOATNUM',
		'COMMENT',
		'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
		'SEMICOLON', 'AMPERSAND', 'COMMA',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 
		'INT', 'VOID', 'FLOAT', 'MAIN', 
		'IF', 'ELSE', 'WHILE', 'RETURN',
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
	'float'	: 'FLOAT',
	'void' 	: 'VOID',
	'main' 	: 'MAIN',
	'if'	: 'IF',
	'else'	: 'ELSE',
	'while'	: 'WHILE',
	'return' : 'RETURN'
}

def t_COMMENT(t):
	r'//.*'
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
	glob.ast = Node('PROGRAM',p[2])
	

def p_declarations(p):
	'''
	declarations : declarations declaration
				| declarations funcproto
				|
	'''
	pass

def p_funcdefs(p):
	'''
	funcdefs : function funcdefs
			| function
	'''
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[2].insert(0,p[1])
		p[0] = p[2]


def p_funcproto(p):
	'''
	funcproto : ftypename LPAREN args RPAREN SEMICOLON
	ftypename : type fname
	'''
	if len(p) == 3:
		if glob.curr_sym_table.proto and (glob.curr_sym_table.ftype != p[1] or glob.curr_sym_table.findirection != p[2].syminfo.indirection):
			raiseFunctionTypeMismatch(glob.curr_sym_table.fname,glob.curr_sym_table.ftype,p[1],glob.curr_sym_table.findirection,p[2].syminfo.indirection,glob.line_number)
			glob.curr_sym_table = SymbolTable(glob.curr_sym_table.parent)
		else:
			glob.curr_sym_table.ftype = p[1]
	else:
		if not glob.curr_sym_table.proto:
			glob.curr_sym_table.proto = True
			glob.curr_sym_table.add_protoarglist(p[3])
			glob.curr_sym_table = glob.curr_sym_table.parent
		else:
			raiseProtoPreviouslyDeclared(glob.curr_sym_table.fname, glob.line_number)
			glob.curr_sym_table = glob.curr_sym_table.parent


def p_function(p):
	'''
	function : ftypename LPAREN dargs statements RBRACE
	dargs : args RPAREN LBRACE
	'''
	if len(p) == 4:
		glob.curr_sym_table.add_arglist(p[1])
	else:
		glob.curr_sym_table.definition = True
		st = glob.curr_sym_table
		p[0] = Node('FUNCTION',[st.fname,st.args,st.findirection,st.ftype,p[4].node])
		glob.curr_sym_table = glob.curr_sym_table.parent


def p_type(p):
	'''
	type : INT
		| VOID
		| FLOAT
	'''
	p[0] = p[1]

def p_main(p):
	'''
	main : MAIN
	'''
	p[0] = SDTS(None,Attributes('main',indirection=0))

def p_fname(p):
	'''
	fname : var
		| pointer
		| main
	'''
	func_name = p[1].syminfo.var_name
	(glob.curr_sym_table,status) = glob.root_table.add_function(func_name,p[1].syminfo.indirection)
	if not status: 
		raisePreviouslyDeclared(p[1],glob.line_number)
	# if glob.curr_sym_table.proto:
	# 	raiseProtoPreviouslyDeclared(func_name,glob.line_number)
	# 	glob.curr_sym_table = SymbolTable(glob.curr_sym_table.parent)
	glob.curr_sym_table.fname = func_name
	p[0] = p[1]


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

def p_arg(p):
	'''
	argcomp : COMMA arg argcomp
		|
	arg : type param
	'''
	if len(p) == 3:
		p[2].syminfo.type = p[1]
		p[0] = (p[2].syminfo,glob.line_number)
	elif len(p) == 4:
		p[3].insert(0,p[2])
		p[0] = p[3]
	else:
		p[0] = []

def p_param(p):
	'''
	param : var 
		| pointer 
		| address
	'''
	p[0] = p[1] # node + syminfo

def p_var(p):
	'''
	var : ID
	'''
	attribute = Attributes(p[1],indirection=0)
	p[0] = SDTS(Node('VAR('+p[1]+')',[],False),attribute)

def p_const(p):
	'''
	const : NUMBER
		| FLOATNUM
	'''
	attribute = Attributes(p[1],indirection=0)
	if str(p[1]).find('.') < 0: 
		attribute.is_int, attribute.type = True, 'int'
	else: 
		attribute.is_float, attribute.type = True, 'float'
	p[0] = SDTS(Node('CONST('+str(p[1])+')',[],True),attribute)


def p_pointer(p):
	'''
	pointer : TIMES pointer %prec STAR
			| TIMES address %prec STAR
			| TIMES var %prec STAR
	'''
	p[2].syminfo.indirection += 1
	p[0] = SDTS(Node('DEREF',[p[2].node],False),p[2].syminfo)

def p_address(p):
	'''
	address : AMPERSAND var
	'''
	p[2].syminfo.indirection -= 1
	p[0] = SDTS(Node('ADDR',[p[2].node],False),p[2].syminfo)

def p_voidfuncall(p):
	'''
	voidfuncall : funcall SEMICOLON
	'''
	if p[1].syminfo.type != 'void':
		raiseReturnValueIgnored(p[1].syminfo.var_name,glob.line_number-1)
	p[0] = p[1]

def p_funcall(p):
	'''
	funcall : var LPAREN params RPAREN
	params : callparam paramcomp
			|
	'''
	if len(p) == 5:
		#check for params
		(ftype,findirection,status) = function_lookup(glob.curr_sym_table,p[1].syminfo.var_name,p[3].syminfo)
		attribute = Attributes(p[1].syminfo.var_name,var_type=ftype,indirection=findirection)
		if not status: 
			attribute.type = glob.type_error
		p[0] = SDTS(Node('FUNCALL',p[3].node),attribute)		
	elif len(p) == 3:
		p[2].node.insert(0,p[1].node)
		p[2].syminfo.insert(0,p[1].syminfo)
		p[0] = p[2]
	else:
		p[0] = SDTS([],[])

def p_paramcomp(p):
	'''
	paramcomp : COMMA callparam paramcomp
			| 
	callparam : expression
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[3].node.insert(0,p[2].node)
		p[3].syminfo.insert(0,p[2].syminfo)
		p[0] = p[3]
	else:
		p[0] = SDTS([],[])

def p_statements(p):
	'''
	statements :  statement statements
				| COMMENT statements
				| declaration statements
				| voidfuncall statements
				| retstatement statements
				| 
	statement : assignment
			| ifstatement
			| whilestatement
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif (len(p) == 3):
		try:
			if p[1].node.token != 'DECL':
				p[0] = SDTS(Node('STMTS',[p[1].node] + p[2].node.children))
			else:
				p[0] = p[2]
		except:
			p[0] = p[2]
	else:
		p[0] = SDTS(Node('STMTS',[]))

def p_retstatement(p):
	'''
	retstatement : RETURN expression SEMICOLON
				| RETURN SEMICOLON
	'''
	## Check the return type and the function return type
	if len(p) == 3 and glob.curr_sym_table.ftype != 'void':
		raiseExpectedReturn(glob.curr_sym_table.fname,glob.curr_sym_table.ftype,'void',0,0,glob.line_number)
	else:
		# p[2] is a tuple of type, indirection
		if glob.curr_sym_table.ftype != p[2].syminfo[0] or glob.curr_sym_table.findirection != p[2].syminfo[1]:
			raiseExpectedReturn(glob.curr_sym_table.fname,glob.curr_sym_table.ftype,p[2].syminfo[0],glob.curr_sym_table.findirection,p[2].syminfo[1],glob.line_number)

	if len(p) == 3:
		p[0] = SDTS(Node('RET',[]))
	else:
		p[0] = SDTS(Node('RET',[p[2].node]))	

def p_declaration(p):
	'''
	declaration : type idlist SEMICOLON
	'''
	for i in range(len(p[2])):
		if glob.curr_sym_table == glob.root_table:
			glob.curr_sym_table.globals[p[2][i].var_name].type = p[1]
		else:
			glob.curr_sym_table.locals[p[2][i].var_name].type = p[1]

	p[0] = SDTS(Node('DECL',[]),p[2])

def p_idlist(p):
	'''
	idlist : decl_var COMMA idlist 
			| decl_var
	'''
	if len(p) == 2:
		p[0] = [p[1].syminfo]
	else:
		p[3].insert(0,p[1].syminfo)
		p[0] = p[3]

def p_decl_var(p):
	'''
	decl_var : var
			| pointer
	'''
	(var_name,status) = glob.curr_sym_table.add_symbol(p[1].syminfo)
	if not status: 
		raisePreviouslyDeclared(var_name,glob.line_number)
	p[0] = p[1]

def p_assignment(p):
	'''
	assignment : pointer EQUALS expression SEMICOLON
				| var EQUALS expression SEMICOLON
	'''
	(symtype,symindirection,status) = lookup(glob.curr_sym_table, p[1].syminfo)
	if not status: 
		raiseNotDeclared(p[1].syminfo.var_name,glob.line_number-1)
		symtype,symindirection = glob.type_error,float("inf")
	actual_indirection = symindirection - p[1].syminfo.indirection
	if actual_indirection < 0:
		raiseTooMuchIndirection(p[1].syminfo.var_name,glob.line_number-1)
		symtype = glob.type_error
	(rtype,rindirection) = p[3].syminfo
	if (symtype != rtype) or actual_indirection != rindirection:
		raiseTypeMismatch(symtype,rtype,actual_indirection,rindirection,glob.line_number-1)

	p[0] = SDTS(Node('ASGN',[p[1].node,p[3].node],p[3].node.is_const))

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
	comp_map = {
		'<':'LT',
		'>':'GT',
		'<=':'LE',
		'>=':'GE',
		'==':'EQ',
		'!=':'NE',
		'&&':'AND',
		'||':'OR'
	}
	if len(p) == 3:
		p[0] = SDTS(Node('NOT',[p[2].node],p[2].node.is_const),p[2].syminfo)
	if p[2] in comp_map:
		ast_node = Node(comp_map[p[2]],[p[1].node,p[3].node],p[1].node.is_const and p[3].node.is_const)
		(ltype,lindirection),(rtype,rindirection) = p[1].syminfo,p[3].syminfo
		if ltype == glob.type_error or rtype == glob.type_error:
			p[0] = SDTS(ast_node,('BOOL',0))
		elif ltype != rtype  or lindirection != rindirection:
			raiseTypeMismatch(ltype,rtype,lindirection,rindirection,glob.line_number)
			p[0] = SDTS(ast_node,('BOOL',0)) 
		else:
			p[0] = SDTS(ast_node,('BOOL',0))

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
		p[0] = SDTS(Node('STMTS',[]))
	else:
		p[0] = SDTS(Node('STMTS',[p[1].node]))

def p_ifstatement(p):
	'''
	ifstatement : IF LPAREN condition RPAREN controlbody %prec IFX
				| IF LPAREN condition RPAREN controlbody ELSE controlbody
	'''
	if len(p) == 6:
		p[0] = SDTS(Node('IF',[p[3].node,p[5].node]))
	else:
		p[0] = SDTS(Node('IF',[p[3].node,p[5].node,p[7].node]))

def p_whilestatement(p):
	'''
	whilestatement : WHILE LPAREN condition RPAREN controlbody
	'''
	p[0] = SDTS(Node('WHILE',[p[3].node,p[5].node]))


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
	op_map = {
		'+':'PLUS',
		'-':'MINUS',
		'*':'MUL',
		'/':'DIV'
	}
	if len(p) == 2:
		#lookup and return (type,indirection)
		if p[1].syminfo.type == None:
			(symtype,symindirection,status) = lookup(glob.curr_sym_table, p[1].syminfo)
			if not status: 
				raiseNotDeclared(p[1].syminfo.var_name,glob.line_number)
				symtype,symindirection = glob.type_error,float("inf") 
			actual_indirection = symindirection - p[1].syminfo.indirection
			if actual_indirection < 0:
				raiseTooMuchIndirection(p[1].syminfo.var_name,glob.line_number)
				symtype = glob.type_error
			p[0] = SDTS(p[1].node,(symtype,actual_indirection))
		else:
			p[0] = SDTS(p[1].node,(p[1].syminfo.type,p[1].syminfo.indirection))

	elif p[2] in op_map:
		ast_node = Node(op_map[p[2]],[p[1].node,p[3].node],p[1].node.is_const and p[3].node.is_const)
		(ltype,lindirection),(rtype,rindirection) = p[1].syminfo,p[3].syminfo
		if ltype == glob.type_error or rtype == glob.type_error :
			p[0] = SDTS(ast_node,(glob.type_error,0))
		elif (ltype != rtype) or lindirection != rindirection:
			raiseTypeMismatch(ltype,rtype,lindirection,rindirection,glob.line_number)
			p[0] = SDTS(ast_node,(glob.type_error,0))
		else:
			p[0] = SDTS(ast_node,(ltype,lindirection))
		
	else :
		p[0] = p[2]

def p_expression_uminus(p):
	'''
	expression : MINUS expression %prec UMINUS
	'''
	p[0] = SDTS(Node('UMINUS',[p[2].node],p[2].node.is_const),p[2].syminfo)
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
	glob.sym_file = open(sys.argv[1] + '.sym','w')
	glob.cfg = CFG()
	
	process(data)

	glob.ast.print_node(0,rfile = glob.ast_file)
	# construct_cfg(glob.ast)
	# glob.cfg.blocks[glob.block_index] = Block(glob.block_index,'',["End"],-1,[])
	# glob.block_index = 1
	# update_cfg(glob.ast)
	# glob.cfg.cfg_print(rfile = glob.cfg_file)

	glob.root_table.print_symbol_table(rfile=glob.sym_file)

	print("Successfully Parsed")