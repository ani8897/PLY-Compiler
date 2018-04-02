from __future__ import print_function
import glob
from collections import OrderedDict

class Block():

	def __init__(self,index,btype,contents,end,goto,cond=""):
		self.index = index
		self.btype = btype
		self.contents = contents
		self.end = end
		self.goto = goto
		self.cond = cond

	def block_print(self,rfile):
		print("<bb %d>"%self.index, file = rfile)
		for c in self.contents:
			print(c,file=rfile)
		if len(self.goto) == 0: 
			print("",file=rfile)
			return
		if len(self.goto) == 1:
			print("goto <bb %d>"%self.goto[0], file = rfile)
		else:
			print("if("+self.cond+") goto <bb %d>"%self.goto[0],file = rfile)
			print("else goto <bb %d>"%self.goto[1],file = rfile)
		print("",file=rfile)

class CFG():

	def __init__(self):
		self.blocks = {}

	def cfg_print(self,rfile=1):
		for b in OrderedDict(sorted(self.blocks.items(), key=lambda t: t[0])):
			self.blocks[b].block_print(rfile)

class FCFG():

	def __init__(self,fname):
		self.fname = fname
		self.cfg = None

	def print_fcfg(self,rfile):
		print("function %s"%self.fname,file=rfile)
		self.cfg.cfg_print(rfile)



def construct_cfg_prog(ast,rfile):

	fcfg_objects = []
	for func in ast.children:
		func_children = func.children
		fcfg = FCFG(func_children[0])

		temp_index = glob.block_index
		construct_cfg(func_children[4])
		glob.block_index = temp_index
		update_cfg(func_children[4])

		fcfg.cfg = glob.cfg
		fcfg_objects.append(fcfg)
		
		glob.cfg = CFG()

	for fcfg in fcfg_objects:
		fcfg.print_fcfg(rfile)


def construct_cfg(ast,parent_index=-1):

	stmts,num_stmts = ast.children,len(ast.children)
	
	if num_stmts == 0: return
	block = Block(glob.block_index,'',[],-1,[])
	glob.block_index += 1
	glob.block_bool = True

	for i in range(num_stmts):

		if stmts[i].token == 'ASGN':
			
			if not(glob.block_bool):
				block = Block(glob.block_index,'AS',[],-1,[])
				glob.block_index += 1
				glob.block_bool = True

			curr_index = glob.block_index
			node = stmts[i].reconstruct_node()
			block.contents.extend(node[0])
			
			if stmts[i].children[1].token[0:4] == 'CALL':
				glob.cfg.blocks[block.index] = block
				glob.block_bool = False

			if i+1<num_stmts and stmts[i+1].token != 'ASGN':
				block.goto.append(curr_index)
				glob.cfg.blocks[block.index] = block
				glob.block_bool = False
			
			if i+1 == num_stmts:
				if parent_index == -1:
					block.goto.append(curr_index)
				else:
					block.goto.append(parent_index)
				
				glob.cfg.blocks[block.index] = block
				glob.block_bool = False

		elif stmts[i].token == 'WHILE':
			if not(glob.block_bool):
				block = Block(glob.block_index,'WH',[],-1,[])
				glob.block_index += 1
				glob.block_bool = True
			curr_index = glob.block_index

			while_children = stmts[i].children
			node = while_children[0].reconstruct_node()
			block.cond = node[1]
			block.contents.extend(node[0])
			block.goto.append(curr_index)
			
			construct_cfg(while_children[1],curr_index-1)
			
			if i+1 == num_stmts and parent_index != -1:
				block.goto.append(parent_index)
			else:
				block.goto.append(glob.block_index)
			
			glob.cfg.blocks[block.index] = block
			glob.block_bool = False

		elif stmts[i].token == 'IF':
			if not(glob.block_bool):
				block = Block(glob.block_index,'IF',[],-1,[])
				glob.block_index += 1
				glob.block_bool = True
			curr_index = glob.block_index

			if_children = stmts[i].children
			node = if_children[0].reconstruct_node()
			block.cond = node[1]
			block.contents.extend(node[0])
			block.goto.append(curr_index)

			if i+1 == num_stmts:
				construct_cfg(if_children[1],parent_index)
			else:
				construct_cfg(if_children[1],-1)
			block.goto.append(glob.block_index)
			
			if len(if_children)==3:
				if i+1 == num_stmts:
					construct_cfg(if_children[2],parent_index)
				else:
					construct_cfg(if_children[2],-1)

			block.end = glob.block_index
			glob.cfg.blocks[block.index] = block
			glob.block_bool = False

		elif stmts[i].token == 'RET':
			if not(glob.block_bool):
				block = Block(glob.block_index,'RET',[],-1,[])
				glob.block_index += 1
				glob.block_bool = True

			ret_children = stmts[i].children
			if len(ret_children) != 0:
				node = ret_children[0].reconstruct_node()
				block.contents.extend(node[0])
				block.contents.append("return %s"%node[1])
			else:
				block.contents.append("return")

			glob.cfg.blocks[block.index] = block
			glob.block_bool = False

		elif stmts[i].token[0:4] == 'CALL':
			if not(glob.block_bool):
				block = Block(glob.block_index,'CALL',[],-1,[])
				glob.block_index += 1
				glob.block_bool = True

			node = stmts[i].reconstruct_node()
			block.contents.extend(node[0])
			block.contents.append(node[1])

			glob.cfg.blocks[block.index] = block
			glob.block_bool = False

def update_cfg(ast,parent_index=-1,parent_if = False,parent_while = False):

	stmts,num_stmts = ast.children,len(ast.children)
	
	if num_stmts == 0: return
	block = glob.cfg.blocks[glob.block_index]
	glob.block_index += 1
	glob.block_bool = True

	for i in range(num_stmts):

		if stmts[i].token == 'ASGN':

			if not(glob.block_bool):
				block = glob.cfg.blocks[glob.block_index]
				glob.block_index += 1
				glob.block_bool = True
			curr_index = glob.block_index
			
			if stmts[i].children[1].token[0:4] == 'CALL':
				glob.block_bool = False

			if i+1<num_stmts and stmts[i+1].token != 'ASGN':
				glob.block_bool = False
			
			if i+1 == num_stmts:
				if parent_if and not(parent_while):
					block.goto[0] = parent_index
					glob.cfg.blocks[block.index] = block
				glob.block_bool = False


		elif stmts[i].token == 'WHILE':
			if not(glob.block_bool):
				block = glob.cfg.blocks[glob.block_index]
				glob.block_index += 1
				glob.block_bool = True
			curr_index = glob.block_index

			while_children = stmts[i].children
			update_cfg(while_children[1],parent_index,False,True)
			
			if i+1 == num_stmts and parent_if:
				block.goto[1] = parent_index

			glob.cfg.blocks[block.index] = block
			glob.block_bool = False



		elif stmts[i].token == 'IF':
			if not(glob.block_bool):
				block = glob.cfg.blocks[glob.block_index]
				glob.block_index += 1
				glob.block_bool = True
			curr_index = glob.block_index

			if_children = stmts[i].children

			if parent_if and i+1 == num_stmts:
				update_cfg(if_children[1],parent_index,True,parent_while)
			
				if len(if_children)==3:
					update_cfg(if_children[2],parent_index,True,parent_while)
				else:
					block.goto[1] = parent_index
				glob.cfg.blocks[block.index] = block
			elif not(parent_if) and i+1 == num_stmts:
				update_cfg(if_children[1],block.end,True,parent_while)
			
				if len(if_children)==3:
					update_cfg(if_children[2],block.end,True,parent_while)
			else:
				update_cfg(if_children[1],block.end,True,False)
			
				if len(if_children)==3:
					update_cfg(if_children[2],block.end,True,False)
			glob.block_bool = False

		elif stmts[i].token == 'RET':
			if not(glob.block_bool):
				glob.block_index += 1
			glob.block_bool = False

		elif stmts[i].token[0:4] == 'CALL':
			if not(glob.block_bool):
				glob.block_index += 1
				glob.block_bool = True
			glob.block_bool = False