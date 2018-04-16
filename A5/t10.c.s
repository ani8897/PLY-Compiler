
	.data
	global_g3:	.word	0
	global_l3:	.word	0
	global_g:	.word	0
	global_var1:	.word	0
	global_var2:	.space	8

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
func1:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 4	# Make space for the locals
 # Prologue ends

label0:
	j label3
label1:
	j label3
label2:
	la $s0, global_g3
	lw $s1, 0($s0)
	li $s0, 1
	div $s1, $s0
	mflo $s2
	move $s0, $s2
	lw $s1, 4($sp)
	lw $s2, 0($s1)
	sw $s0, 0($s2)
	j label1
label3:
	j epilogue_func1
# Epilogue begins
epilogue_func1:
	add $sp, $sp, 4
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

main:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 12	# Make space for the locals
 # Prologue ends

label4:
	lw $s0, 4($sp)
	lw $s1, 0($s0)
	move $s0, $s1
	j label5
label5:
	j label8
label6:
	j label8
label7:
	la $s1, global_g3
	lw $s2, 0($s1)
	li $s1, 1
	add $s3, $s2, $s1
	move $s1, $s3
	la $s2, global_g3
	sw $s1, 0($s2)
	j label6
label8:
	j epilogue_main
# Epilogue begins
epilogue_main:
	add $sp, $sp, 12
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

func2:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 4	# Make space for the locals
 # Prologue ends

label9:
	j label12
label10:
	j label12
label11:
	la $s1, global_g3
	lw $s2, 0($s1)
	li $s1, 1
	add $s3, $s2, $s1
	move $s1, $s3
	la $s2, global_g3
	sw $s1, 0($s2)
	j label10
label12:
	j epilogue_func2
# Epilogue begins
epilogue_func2:
	add $sp, $sp, 4
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

