
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
	lw $s0, 12($sp)
	l.s $f10, 0($s0)
	sw $f10, -4($sp)
	lw $s0, 16($sp)
	lw $s1, 0($s0)
	sw $s1, 0($sp)
	sub $sp, $sp, 8
	jal f
	addi $sp, $sp, 8
	move $s0, $v1
	sw $s0, 4($sp)
	j label1
label1:
	j epilogue_main
# Epilogue begins
epilogue_main:
	addi $sp, $sp, 20
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

f:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 16	# Make space for the locals
 # Prologue ends

label2:
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

