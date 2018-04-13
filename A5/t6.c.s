
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
	li.s $f10, 9.8
	lw $s0, 4($sp)
	s.s $f10, 0($s0)
	# setting up activation record for called function
	li $s0, 3
	sw $s0, -4($sp)
	lw $s0, global_g
	sw $s0, 0($sp)
	sub $sp, $sp, 8
	jal f # function call
	add $sp, $sp, 8 # destroying activation record of called function
	move $s0, $v1 # using the return value of called function
	sw $s0, global_g
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
	.text	# The .text assembler directive indicates
	.globl f	# The following is the code
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
	move $s0, $s1
	move $v1, $s0 # move return value to $v1
	j epilogue_f

# Epilogue begins
epilogue_f:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
