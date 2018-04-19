from symtable import RootTable
from reg import Register

# For maintaining new lines
line_number = 1

# printing ast
ast_file = ""

# printing cfg
cfg_file = ""
block_index = 0
temp_index = 0
block_bool = False
cfg = None
ast = []

#Type error dummy
type_error = "type_error"

# Root global
root_table = RootTable()

#Current function
sym_file = ""
curr_sym_table = root_table

#Assembly file
assembly_file = ""
stmtreturn = False

registers = Register()

#Constant strings
data = "\n\t.data"
global_var = "\tglobal_%s:\t%s"
text = "\t.text	# The .text assembler directive indicates"
globl = "\t.globl %s\t# The following is the code"

prologue = "\
# Prologue begins\n \
	sw $ra, 0($sp)	# Save the return address\n \
	sw $fp, -4($sp)	# Save the frame pointer\n \
	sub $fp, $sp, 8	# Update the frame pointer\n \
	sub $sp, $sp, %d	# Make space for the locals\n \
# Prologue ends\n"
epilogue = "\
# Epilogue begins\n\
epilogue_%s:\n\
	addi $sp, $sp, %d\n\
	lw $fp, -4($sp)\n\
	lw $ra, 0($sp)\n\
	jr $ra	# Jump back to the called procedure\n\
# Epilogue ends\n"

label = "label%d:"
jump_statement = "\tj label%d"
jump_epilogue = "\tj epilogue_%s"
j_cond_end = "\tj L_CondEnd_%d"
label_cond_end = "L_CondEnd_%d"
label_cond_false = "L_CondFalse_%d"
label_cond_true = "L_CondTrue_%d"


####### Float instructions #############
float_cond_num = 0
li_s = "\tli.s $%s, %s"
l_s = "\tl.s $%s, %d($%s)"
s_s = "\ts.s $%s, %d($%s)"
s_s_glob = "\ts.s $%s, %s"
mov_s = "\tmov.s $%s, $%s"
add_s = "\tadd.s $%s, $%s, $%s"
sub_s = "\tsub.s $%s, $%s, $%s"
mul_s = "\tmul.s $%s, $%s, $%s"
div_s = "\tdiv.s $%s, $%s, $%s"
c_lt_s = "\tc.lt.s $%s, $%s\n \
\tbc1f L_CondFalse_%d\n \
\tli $%s, 1\n \
\tj L_CondEnd_%d\n \
L_CondFalse_%d:\n\
\tli $%s 0\n\
L_CondEnd_%d:"

c_le_s = "\tc.le.s $%s, $%s\n \
\tbc1f L_CondFalse_%d\n \
\tli $%s, 1\n \
\tj L_CondEnd_%d\n \
L_CondFalse_%d:\n\
\tli $%s 0\n\
L_CondEnd_%d:"

c_eq_s = "\tc.eq.s $%s, $%s\n \
\tbc1f L_CondFalse_%d\n \
\tli $%s, 1\n \
\tj L_CondEnd_%d\n \
L_CondFalse_%d:\n\
\tli $%s 0\n\
L_CondEnd_%d:"

c_ne_s = "\tc.eq.s $%s, $%s\n \
\tbc1f L_CondTrue_%d\n \
\tli $%s, 0\n \
\tj L_CondEnd_%d\n \
L_CondTrue_%d:\n\
\tli $%s 1\n\
L_CondEnd_%d:"

neg_s = "\tneg.s $%s, $%s"


bc1t = "\tbc1f L_CondTrue_%d\n"
bc1f = "\tbc1f L_CondFalse_%d\n"


########################################


li = "\tli $%s, %d"
la = "\tla $%s, global_%s"
lw = "\tlw $%s, %d($%s)"
sw_glob = "\tsw $%s, %s"
sw = "\tsw $%s, %d($%s)"
move = "\tmove $%s, $%s"

seq = "\tseq $%s, $%s, $%s"
sne = "\tsne $%s, $%s, $%s"
slt = "\tslt $%s, $%s, $%s"
sle = "\tsle $%s, $%s, $%s"
bne = "\tbne $%s, $0, label%d"

addi = "\taddi $%s, $%s, %d"
subi = "\tsub $%s, $%s, %d"


add = "\tadd $%s, $%s, $%s"
sub = "\tsub $%s, $%s, $%s"
mul = "\tmul $%s, $%s, $%s"
div = "\tdiv $%s, $%s"
mflo = "\tmflo $%s"

negu = "\tnegu $%s, $%s"

_not = "\tnot $%s, $%s"
_and = "\tand $%s, $%s, $%s" 
_or = "\tor $%s, $%s, $%s"

jal = "\tjal %s"


arithmetic = {
	'+' : add,
	'-' : sub,
	'*' : mul
}

float_arithmetic = {
	'+' : add_s,
	'-' : sub_s,
	'*' : mul_s,
	'/' : div_s	
}

conditional = {
	'==' : seq,
	'!=' : sne,
	'<=' : sle,
	'<'  : slt,
	'&&' : _and,
	'||' : _or
}

float_conditional = {
	'==' : c_eq_s,
	'!=' : c_ne_s,
	'<=' : c_le_s,
	'<'  : c_lt_s
}

move_map = {
	True : mov_s,
	False : move
}

sw_map = {
	True : s_s,
	False : sw
}

sw_glob_map = {
	True : s_s_glob,
	False : sw_glob
}

negu_map = {
	True : neg_s,
	False : negu
}

lw_map = {
	True : l_s,
	False : lw
}
