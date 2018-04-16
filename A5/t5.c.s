
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
 	sub $sp, $sp, 8	# Make space for the locals
 # Prologue ends

label2:
	addi $s1, $sp, 8
	sw $s1, 4($sp)
	li $s2, 9
	lw $s3, 4($sp)
	sw $s2, 0($s3)
	j label3
label3:
	li $s2, 5
	j label5
label4:
	lw $s3, 8($sp)
	move $s4, $s3
	li $s3, 3
	j label5
label5:
	j epilogue_main
# Epilogue begins
epilogue_main:
	add $sp, $sp, 8
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

