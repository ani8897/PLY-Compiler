
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
	li $s0, 52
	j label3
label1:
	li $s1, 0
	j label3
label2:
	li $s2, 1
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
	lw $s3, 12($sp)
	move $s4, $s3
	li $s3, 3
	j label5
label5:
	li $s5, 52
	j label8
label6:
	li $s6, 0
	j label8
label7:
	li $s7, 1
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
	li $t0, 52
	j label12
label10:
	li $t1, 0
	j label12
label11:
	li $t2, 1
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

