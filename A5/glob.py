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


li = "\tli $%s, %d"
la = "\tla $%s, global_%s"
lw = "\tlw $%s, %d($%s)"
sw_glob = "\tsw $%s, %s"
sw = "\tsw $%s, %d($%s)"
move = "\tmove $%s, $%s"

seq = "\tseq $%s, $%s, $%s"
sne = "\tsne $%s, $%s, $%s"
slt = "\tslt $%s, $%s, $%s"
bne = "\tbne $%s, $0, label%d"

addi = "\taddi $%s, $%s, %d"
subi = "\tsub $%s, $%s, %d"


add = "\tadd $%s, $%s, $%s"
sub = "\tsub $%s, $%s, $%s"
mul = "\tmul $%s, $%s, $%s"
div = "\tdiv $%s, $%s"
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

conditional = {
	'==' : seq,
	'!=' : sne,
	'&&' : _and,
	'||' : _or
}
