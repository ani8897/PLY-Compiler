from symtable import RootTable
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