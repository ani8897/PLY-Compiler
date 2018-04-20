
	.data
	global_d:	.word	0

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
f:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 16	# Make space for the locals
 # Prologue ends

label0:
	addi $s0, $sp, 8
	sw $s0, 4($sp)
	j label1
label1:
	lw $s0, 4($sp)
	move $v1, $s0 # move return value to $v1
	j epilogue_f
# Epilogue begins
epilogue_f:
	addi $sp, $sp, 16
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
	addi $s0, $sp, 8
	sw $s0, 4($sp)
	li $s0, 9
	lw $s1, 4($sp)
	sw $s0, 0($s1)
	j label3
label3:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	li $s0, 5
	slt $s2, $s0, $s1
	move $s0, $s2
	bne $s0, $0, label4
	j label5
label4:
	li $s0, 3
	sw $s0, -4($sp)
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	sw $s1, 0($sp)
	sub $sp, $sp, 8
	jal f
	addi $sp, $sp, 8
	move $s0, $v1
	sw $s0, global_d
	j label5
label5:
	j epilogue_main
# Epilogue begins
epilogue_main:
	addi $sp, $sp, 16
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

