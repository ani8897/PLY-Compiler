
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
	lw $s0, 20($sp)
	lw $s1, 0($s0)
	lw $s0, 16($sp)
	sw $s1, 0($s0)
	li.s $f10, 9.8
	lw $s0, 8($sp)
	s.s $f10, 0($s0)
	li $s0, 3
	sw $s0, -4($sp)
	la $s0, global_g
	lw $s1, 0($s0)
	sw $s1, 0($sp)
	sub $sp, $sp, 8
	jal f
	addi $sp, $sp, 8
	move $s0, $v1
	sw $s0, global_g
	j label1
label1:
	j epilogue_main
# Epilogue begins
epilogue_main:
	addi $sp, $sp, 24
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
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	move $v1, $s1 # move return value to $v1
	j epilogue_f
# Epilogue begins
epilogue_f:
	addi $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

