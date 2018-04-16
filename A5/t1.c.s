
	.data
	global_d:	.word	0

	.text	# The .text assembler directive indicates
	.globl f	# The following is the code
f:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 8	# Make space for the locals
 # Prologue ends

label0:
	la $s0, global_d
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	addi $s1, $sp, 8
	lw $s2, 4($sp)
	sw $s1, 0($s2)
	j label1
label1:
	j epilogue_f
# Epilogue begins
epilogue_f:
	add $sp, $sp, 8
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

