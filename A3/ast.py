from __future__ import print_function
import glob

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
			'PLUS'	: '+',
			'MINUS'	: '-',
			'MUL'	: '*',
			'DIV'	: '/',
			'LT'	: '<',
			'LE'	: '<=',
			'GT'	: '>',
			'GE'	: '>=',
			'EQ'	: '==',
			'NE'	: '!=',
			'AND'	: '&&',
			'OR'	: '||'
		}
		
		if self.token[0:3] == 'VAR' : 
			return ([],self.token[4:-1])
		
		elif self.token[0:5] == 'CONST': 
			return ([],self.token[6:-1])
		
		elif self.token == 'DEREF': 
			child = self.children[0].reconstruct_node()
			return ([],'*' + child[1])
		
		elif self.token == 'ADDR': 
			child = self.children[0].reconstruct_node()
			return ([],'&' + child[1])

		elif self.token == 'UMINUS': 
			child = self.children[0].reconstruct_node()
			if child[1][0] == '-':

				new_temp1 = glob.temp_index
				new_temp_variable1 = "t"+str(new_temp1)
				glob.temp_index +=1
				
				code = new_temp_variable1 + " = " + child[1]
				child[0].append(code)

				new_temp2 = glob.temp_index
				new_temp_variable2 = "t"+str(new_temp2)
				glob.temp_index +=1

				code = new_temp_variable2 + " = -" + new_temp_variable1
				child[0].append(code)

				return (child[0],new_temp_variable2)
			else:
				return (child[0],'-' + child[1])
		
		elif self.token == 'NOT': 
			child = self.children[0].reconstruct_node()
			
			new_temp = glob.temp_index
			new_temp_variable = "t"+str(new_temp)
			glob.temp_index +=1
			
			code = new_temp_variable + " = !" + child[1]
			child[0].append(code)
			return (child[0],new_temp_variable)

		elif self.token == 'ASGN':
			left_child = self.children[0].reconstruct_node() 
			right_child = self.children[1].reconstruct_node()

			code = left_child[1] + " = " + right_child[1]
			right_child[0].append(code)
			return (right_child[0],left_child[1])

		elif self.token in tokenMap : 
			left_child = self.children[0].reconstruct_node() 
			right_child = self.children[1].reconstruct_node()

			new_temp = glob.temp_index
			new_temp_variable = "t"+str(new_temp)
			glob.temp_index +=1

			code = new_temp_variable + " = " + left_child[1] + " " + tokenMap[self.token] + " " + right_child[1]
			left_child[0].extend(right_child[0])
			left_child[0].append(code)
			return (left_child[0],new_temp_variable)