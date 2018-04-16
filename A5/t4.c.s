
	.data
	global_d:	.word	0

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
f:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 8	# Make space for the locals
 # Prologue ends

label0:
	addi $s0, $sp, 8
	sw $s0, 4($sp)
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

main:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 16	# Make space for the locals
 # Prologue ends

label2:
	addi $s0, $sp, 12
	sw $s0, 4($sp)
	addi $s0, $sp, 16
	sw $s0, 8($sp)
	li $s0, 2
	lw $s1, 4($sp)
	sw $px, 0($s1)
	li $px, 3
	lw $s1, 8($sp)
	sw $py, 0($s1)
	lw $py, 16($sp)
	move $s1, $py
	lw $py, 16($sp)
	move $s2, $py
	j label3
label3:
	j epilogue_main
# Epilogue begins
epilogue_main:
	add $sp, $sp, 16
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

