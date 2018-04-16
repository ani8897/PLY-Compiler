
	.data
	global_g:	.word	0

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
main:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 24	# Make space for the locals
 # Prologue ends

label0:
	lw $s0, 16($sp)
	lw $s1, 0($s0)
	lw $s0, 12($sp)
	sw $s1, 0($s0)
	li $s0, 9
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label1
label1:
	j epilogue_main
# Epilogue begins
epilogue_main:
	add $sp, $sp, 24
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

f:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 12	# Make space for the locals
 # Prologue ends

label2:
	j epilogue_f
# Epilogue begins
epilogue_f:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

