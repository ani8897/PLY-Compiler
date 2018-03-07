#!/usr/bin/python3

from __future__ import print_function
import sys
import ply.lex as lex
import ply.yacc as yacc


tokens = (
		'ID', 'NUMBER',
		'COMMENT',
		'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
		'SEMICOLON', 'AMPERSAND', 'COMMA',
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 
		'INT', 'VOID', 'MAIN', 
		'IF', 'ELSE', 'WHILE',
		'LT','GT','LE','GE','EQ','NOT', 'AND', 'OR'
)

t_ignore = " \t"

def t_newline(t):
	r'\n|\r\n'
	globals()["line"] += len(t.value)

t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
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
	('left', 'EQ', 'NOT'),
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

def p_start(p):
	'''
	start : function
	'''
	p[1].print_node(0,rfile = globals()["ast_file"])
	construct_cfg(p[1])
	globals()["cfg"].blocks[globals()["block_index"]] = Block(globals()["block_index"],'',["End"],-1,[])
	globals()["block_index"] = 1
	update_cfg(p[1])
	globals()["cfg"].cfg_print(rfile = globals()["cfg_file"])
	print("Successfully Parsed")

def p_function(p):
	'''
	function : VOID MAIN LPAREN RPAREN LBRACE statements RBRACE
	type : INT
		| VOID		
	'''
	if len(p) != 2:
		p[0] = p[6]

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
	address : AMPERSAND pointer
			| AMPERSAND address
			| AMPERSAND var
	'''
	p[0] = Node('ADDR',[p[2]],False)

def p_statements(p):
	'''
	statements :  statement statements
				| COMMENT statements
				| declaration statements
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

class Node():
	def __init__(self,token,children,is_const=False):
		self.token = token
		self.children = children
		self.is_const = is_const

	def print_node(self,depth,rfile=1):
		if self.token == "ASGN" and self.is_const and self.children[0].token[0:3] == 'VAR':
			print("Syntax error at ",self.children[0].token[4:-1]," =")
			exit(0)

		if(self.token == 'STMTS'):
			if len(self.children) != 0:
				i = 0
				for child in self.children:
					i+=1
					child.print_node(depth,rfile)
		else:
			print('\t'*depth + self.token, file=rfile)
			if len(self.children) != 0:
				i = 0
				print('\t'*depth + '(', file=rfile)
				for child in self.children:
					i+=1
					child.print_node(depth+1,rfile)
					if(i < len(self.children)): print('\t'*(depth+1) + ',', file=rfile)
				print('\t'*depth + ')', file=rfile)

	def reconstruct_node(self):
		tokenMap = {
			'ASGN' 	: '=',
			'PLUS'	: '+',
			'MINUS'	: '-',
			'MUL'	: '*',
			'DIV'	: '/',
			'LT'	: '<',
			'LE'	: '<=',
			'GT'	: '>',
			'GE'	: '>=',
			'EQ'	: '==',
			'AND'	: '&&',
			'OR'	: '||'
		}
		if self.token[0:3] == 'VAR' : return self.token[4:-1]
		elif self.token[0:5] == 'CONST': return self.token[6:-1]
		elif self.token == 'DEREF': return '*' + self.children[0].reconstruct_node()
		elif self.token == 'ADDR': return '&' + self.children[0].reconstruct_node()
		elif self.token == 'NOT': return '!' + self.children[0].reconstruct_node()
		elif self.token in tokenMap : return self.children[0].reconstruct_node() + tokenMap[self.token] + self.children[1].reconstruct_node()


def construct_cfg(ast,parent_index=-1):

	stmts,num_stmts = ast.children,len(ast.children)
	
	if num_stmts == 0: return
	block = Block(globals()["block_index"],'',[],-1,[])
	globals()["block_index"] += 1
	globals()["block_bool"] = True

	for i in range(num_stmts):

		if stmts[i].token == 'ASGN':
			if not(globals()["block_bool"]):
				block = Block(globals()["block_index"],'AS',[],-1,[])
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]
			block.contents.append(stmts[i].reconstruct_node())
			if i+1<num_stmts and stmts[i+1].token != 'ASGN':
				block.goto.append(curr_index)
				globals()["cfg"].blocks[block.index] = block
				globals()["block_bool"] = False
			if i+1 == num_stmts:
				if parent_index == -1:
					block.goto.append(curr_index)
				else:
					block.goto.append(parent_index)
				globals()["cfg"].blocks[block.index] = block
				globals()["block_bool"] = False

		elif stmts[i].token == 'WHILE':
			if not(globals()["block_bool"]):
				block = Block(globals()["block_index"],'WH',[],-1,[])
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]

			while_children = stmts[i].children
			block.contents.append(while_children[0].reconstruct_node())
			block.goto.append(curr_index)
			
			construct_cfg(while_children[1],curr_index-1)
			
			if i+1 == num_stmts and parent_index != -1:
				block.goto.append(parent_index)
			else:
				block.goto.append(globals()["block_index"])
			
			globals()["cfg"].blocks[block.index] = block
			globals()["block_bool"] = False


		elif stmts[i].token == 'IF':
			if not(globals()["block_bool"]):
				block = Block(globals()["block_index"],'IF',[],-1,[])
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]

			if_children = stmts[i].children
			block.contents.append(if_children[0].reconstruct_node())
			block.goto.append(curr_index)

			construct_cfg(if_children[1],parent_index)
			block.goto.append(globals()["block_index"])
			
			if len(if_children)==3:
				construct_cfg(if_children[2],parent_index)

			block.end = globals()["block_index"]
			globals()["cfg"].blocks[block.index] = block
			globals()["block_bool"] = False

def update_cfg(ast,parent_index=-1,parent_if = False,parent_while = False):

	stmts,num_stmts = ast.children,len(ast.children)
	
	if num_stmts == 0: return
	block = globals()["cfg"].blocks[globals()["block_index"]]
	globals()["block_index"] += 1
	globals()["block_bool"] = True

	for i in range(num_stmts):

		if stmts[i].token == 'ASGN':
			if not(globals()["block_bool"]):
				block = globals()["cfg"].blocks[globals()["block_index"]]
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]
			if i+1<num_stmts and stmts[i+1].token != 'ASGN':
				globals()["block_bool"] = False
			if i+1 == num_stmts:
				if parent_if and not(parent_while):
					block.goto[0] = parent_index
					globals()["cfg"].blocks[block.index] = block
				globals()["block_bool"] = False


		elif stmts[i].token == 'WHILE':
			if not(globals()["block_bool"]):
				block = globals()["cfg"].blocks[globals()["block_index"]]
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]

			while_children = stmts[i].children
			update_cfg(while_children[1],parent_index,False,True)
			
			if i+1 == num_stmts and parent_if:
				block.goto[1] = parent_index

			globals()["cfg"].blocks[block.index] = block
			globals()["block_bool"] = False



		elif stmts[i].token == 'IF':
			if not(globals()["block_bool"]):
				block = globals()["cfg"].blocks[globals()["block_index"]]
				globals()["block_index"] += 1
				globals()["block_bool"] = True
			curr_index = globals()["block_index"]

			if_children = stmts[i].children

			if parent_if and i+1 == num_stmts:
				update_cfg(if_children[1],parent_index,True,parent_while)
			
				if len(if_children)==3:
					update_cfg(if_children[2],parent_index,True,parent_while)
				else:
					block.goto[1] = parent_index
				globals()["cfg"].blocks[block.index] = block
			else:
				update_cfg(if_children[1],block.end,True,parent_while)
			
				if len(if_children)==3:
					update_cfg(if_children[2],block.end,True,parent_while)
			globals()["block_bool"] = False

class Block():

	def __init__(self,index,btype,contents,end,goto):
		self.index = index
		self.btype = btype
		self.contents = contents
		self.end = end
		self.goto = goto

	def block_print(self,rfile):
		print("<bb %d>"%self.index, file = rfile)
		for c in self.contents:
			print(c,file=rfile)
		if len(self.goto) == 0: return
		if len(self.goto) == 1:
			print("goto <bb %d>"%self.goto[0], file = rfile)
		else:
			print("if goto <bb %d>"%self.goto[0],file = rfile)
			print("else goto <bb %d>"%self.goto[1],file = rfile)
		print("",file=rfile)

class CFG():

	def __init__(self):
		self.blocks = {}

	def cfg_print(self,rfile=1):
		for b in self.blocks:
			self.blocks[b].block_print(rfile)


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

	globals()["line"] = 1
	globals()["trees"] = []
	globals()["ast_file"] = open(sys.argv[1] + '.ast','w')
	globals()["cfg_file"] = open(sys.argv[1] + '.cfg','w')
	globals()["block_index"] = 1
	globals()["block_bool"] = False
	globals()["temp_index"] = 1
	globals()["cfg"] = CFG()
	globals()["contents"] = []
	
	process(data)