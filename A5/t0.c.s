
	.data

	.text	# The .text assembler directive indicates
	.globl func1	# The following is the code
func1:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 12	# Make space for the locals
 # Prologue ends

label0:
	lw $s0, 4($sp)
	move $v1, $s0 # move return value to $v1
	j epilogue_func1
# Epilogue begins
epilogue_func1:
	addi $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

