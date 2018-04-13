
	.data

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
main:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 20	# Make space for the locals
# Prologue ends
label0:
	addi $s0, $sp, 4
	sw $s0, 8($sp)
	li $s0, 5
	lw $s1, 8($sp)
	sw $s0, 0($s1)
	j label1
label1:
	lw $s0, 8($sp)
	lw $s1, 0($s0)
	li $s0, 4
	slt $s2, $s0, $s1
	move $s0, $s2
	not $s1, $s0
	move $s0, $s1
	bne $s0, $0, label2
	j label3
label2:
	li $s0, 4
	lw $s1, 12($sp)
	sw $s0, 0($s1)
	j label1
label3:
	j epilogue_main

# Epilogue begins
epilogue_main:
	add $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
