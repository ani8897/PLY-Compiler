
	.data
	global_x:	.word	0
	global_y:	.space	8

	.text	# The .text assembler directive indicates
	.globl func1	# The following is the code
func1:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 24	# Make space for the locals
 # Prologue ends

label0:
	la $s0, global_y
	sw $s0, globals_x
	la $s0, global_x
	l.s $f10, 0($s0)
	la $s0, global_x
	l.s $f12, 0($s0)
	mul.s $f14, $f10, $f12
	mov.s $f10, $f14
	la $s0, global_x
	l.s $f12, 0($s0)
	add.s $f14, $f12, $f10
	mov.s $f10, $f14
	la $s0, global_x
	l.s $f12, 0($s0)
	la $s0, global_x
	l.s $f14, 0($s0)
	div.s $f16, $f12, $f14
	mov.s $f12, $f16
	sub.s $f14, $f10, $f12
	mov.s $f10, $f14
	la $s0, global_x
	s.s $f10, 0($s0)
	j label1
label1:
	li.s $f10, 7.0
	li.s $f12, 3.0
	c.eq.s $f10, $f12
 	bc1f L_CondFalse_0
 	li $s0, 1
 	j L_CondEnd_0
 L_CondFalse_0:
	li $s0 0
L_CondEnd_0:
	move $s1, $s0
	bne $s1, $0, label2
	j label2
label2:
	li.s $f10, 7.2
	li.s $f12, 3.1
	c.eq.s $f10, $f12
 	bc1f L_CondTrue_1
 	li $s0, 0
 	j L_CondEnd_1
 L_CondTrue_1:
	li $s0 1
L_CondEnd_1:
	move $s1, $s0
	bne $s1, $0, label3
	j label3
label3:
	li.s $f10, 6.0
	li.s $f12, 3.0
	c.lt.s $f12, $f10
 	bc1f L_CondFalse_2
 	li $s0, 1
 	j L_CondEnd_2
 L_CondFalse_2:
	li $s0 0
L_CondEnd_2:
	move $s1, $s0
	bne $s1, $0, label4
	j label4
label4:
	li.s $f10, 6.2
	li.s $f12, 3.1
	c.le.s $f12, $f10
 	bc1f L_CondFalse_3
 	li $s0, 1
 	j L_CondEnd_3
 L_CondFalse_3:
	li $s0 0
L_CondEnd_3:
	move $s1, $s0
	bne $s1, $0, label5
	j label5
label5:
	li.s $f10, 5.0
	li.s $f12, 3.0
	c.lt.s $f10, $f12
 	bc1f L_CondFalse_4
 	li $s0, 1
 	j L_CondEnd_4
 L_CondFalse_4:
	li $s0 0
L_CondEnd_4:
	move $s1, $s0
	bne $s1, $0, label6
	j label6
label6:
	li.s $f10, 5.2
	li.s $f12, 3.1
	c.le.s $f10, $f12
 	bc1f L_CondFalse_5
 	li $s0, 1
 	j L_CondEnd_5
 L_CondFalse_5:
	li $s0 0
L_CondEnd_5:
	move $s1, $s0
	bne $s1, $0, label7
	j label7
label7:
	lw $s0, 4($sp)
	move $v1, $s0
	j epilogue_func1
# Epilogue begins
epilogue_func1:
	addi $sp, $sp, 24
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

