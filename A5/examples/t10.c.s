
	.data
global_g:	.word	0
global_l3:	.word	0
global_var2:	.space	8
global_var1:	.word	0
global_g3:	.word	0

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
	lw $s1, 4($sp)
	lw $s2, 0($s1)
	lw $s1, 0($s2)
	li $s2, 0
	sne $s3, $s1, $s2
	move $s1, $s3
	bne $s1, $0, label2
	j label3
label2:
	lw $s2, global_g3
	lw $s3, 0($s2)
	li $s2, 1
	add $s4, $s3, $s2
	move $s2, $s4
	lw $s3, 4($sp)
	lw $s4, 0($s3)
	sw $s2, 0($s4)
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
	lw $s2, 4($sp)
	lw $s3, 0($s2)
	move $s2, $s3
	# setting up activation record for called function
	li $s3, 3
	sw $s3, -4($sp)
	sw $s2, 0($sp)
	sub $sp, $sp, 8
	jal func2 # function call
	add $sp, $sp, 8 # destroying activation record of called function
	move $s2, $v1 # using the return value of called function
	sw $s2, global_g3
	j label5
label5:
	lw $s2, global_g3
	lw $s3, 0($s2)
	li $s2, 52
	seq $s4, $s3, $s2
	move $s2, $s4
	bne $s2, $0, label6
	j label8
label6:
	lw $s3, 12($sp)
	lw $s4, 0($s3)
	li $s3, 0
	sne $s5, $s4, $s3
	move $s3, $s5
	bne $s3, $0, label7
	j label8
label7:
	lw $s4, global_g3
	lw $s5, 0($s4)
	li $s4, 1
	add $s6, $s5, $s4
	move $s4, $s6
	lw $s5, global_g3
	sw $s4, 0($s5)
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
	lw $s4, global_g3
	lw $s5, 0($s4)
	li $s4, 52
	seq $s6, $s5, $s4
	move $s4, $s6
	bne $s4, $0, label10
	j label12
label10:
	lw $s5, 4($sp)
	lw $s6, 0($s5)
	li $s5, 0
	sne $s7, $s6, $s5
	move $s5, $s7
	bne $s5, $0, label11
	j label12
label11:
	lw $s6, global_g3
	lw $s7, 0($s6)
	li $s6, 1
	add $t0, $s7, $s6
	move $s6, $t0
	lw $s7, global_g3
	sw $s6, 0($s7)
	j label10
label12:
	lw $s6, 4($sp)
	move $v1, $s6 # move return value to $v1
	j epilogue_func2

# Epilogue begins
epilogue_func2:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends
