
	.data
global_g:	.word	0
global_g3:	.word	0
global_l3:	.word	0
global_var1:	.word	0
global_var2:	.space	8

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
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 52
	seq $s2, $s1, $s0
	move $s0, $s2
	bne $s0, $0, label1
	j label3
label1:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	lw $s0, 0($s1)
	li $s1, 0
	sne $s2, $s0, $s1
	move $s0, $s2
	bne $s0, $0, label2
	j label3
label2:
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 1
	add $s2, $s1, $s0
	move $s0, $s2
	lw $s1, 4($sp)
	lw $s2, 0($s1)
	sw $s0, 0($s2)
	j label1
label3:
	j epilogue_func1

# Epilogue begins
epilogue_func1:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
main:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 20	# Make space for the locals
# Prologue ends
label4:
	# setting up activation record for called function
	li $s0, 3
	sw $s0, -4($sp)
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	sw $s1, 0($sp)
	sub $sp, $sp, 8
	jal func2 # function call
	add $sp, $sp, 8 # destroying activation record of called function
	move $s0, $v1 # using the return value of called function
	sw $s0, global_g3
	j label5
label5:
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 52
	seq $s2, $s1, $s0
	move $s0, $s2
	bne $s0, $0, label6
	j label8
label6:
	lw $s0, 12($sp)
	lw $s1, 0($s0)
	li $s0, 0
	sne $s2, $s1, $s0
	move $s0, $s2
	bne $s0, $0, label7
	j label8
label7:
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 1
	add $s2, $s1, $s0
	move $s0, $s2
	lw $s1, global_g3
	sw $s0, 0($s1)
	j label6
label8:
	j epilogue_main

# Epilogue begins
epilogue_main:
	add $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
	.text	# The .text assembler directive indicates
	.globl func2	# The following is the code
func2:
# Prologue begins
	sw $ra, 0($sp)	# Save the return address
	sw $fp, -4($sp)	# Save the frame pointer
	sub $fp, $sp, 8	# Update the frame pointer
	sub $sp, $sp, 12	# Make space for the locals
# Prologue ends
label9:
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 52
	seq $s2, $s1, $s0
	move $s0, $s2
	bne $s0, $0, label10
	j label12
label10:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	li $s0, 0
	sne $s2, $s1, $s0
	move $s0, $s2
	bne $s0, $0, label11
	j label12
label11:
	lw $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 1
	add $s2, $s1, $s0
	move $s0, $s2
	lw $s1, global_g3
	sw $s0, 0($s1)
	j label10
label12:
	lw $s0, 4($sp)
	move $v1, $s0 # move return value to $v1
	j epilogue_func2

# Epilogue begins
epilogue_func2:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
