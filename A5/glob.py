from symtable import RootTable
from pyparsing import Word, nums, OneOrMore, Regex, Optional

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
	add $sp, $sp, %d\n\
	lw $fp, -4($sp)\n\
	lw $ra, 0($sp)\n\
	jr $ra	# Jump back to the called procedure\n\
# Epilogue ends\n"

label = "label%d:"
jump_epilogue = "\tj epilogue_%s"


label_parser = '<bb' + ' ' + Word(nums)("block_num") +'>'
if_parser = 'if(t'+Word(nums)("temp_num")+') goto <bb '+Word(nums)("block_num")+'>'
else_parser = 'else goto <bb '+Word(nums)("block_num")+'>'
goto_parser = 'goto <bb '+Word(nums)("block_num")+'>'
return_parser = 'return '+Regex(r'\**[a-zA-Z_]*[a-zA-Z0-9_]*')("ret_token")
temp_assign_bin_parser = 't'+Word(nums)("temp_res")+' = '+Regex(r'[\*\&\-]*')("pre_op1")+'t'Word(nums)("temp_op1")+Regex(r'')("op")+Regex(r'[\*\&\-]*')("pre_op2")+'t'Word(nums)("temp_op2")
temp_assign_un_parser = 't'+Word(nums)("temp_res")+' = '+Regex(r'[\*\&\-]*')("pre_op1")+'t'Word(nums)("temp_op1")
# funcall_assign_parser =
# funcall_parser =  
