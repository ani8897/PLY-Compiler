
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
	addi $s1, $sp, 12
	sw $s1, 4($sp)
	addi $s2, $sp, 16
	sw $s2, 8($sp)
	li $s3, 2
	lw $s4, 4($sp)
	sw $s3, 0($s4)
	li $s3, 3
	lw $s4, 8($sp)
	sw $s3, 0($s4)
	lw $s3, 16($sp)
	move $s4, $s3
	lw $s3, 16($sp)
	move $s5, $s3
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

