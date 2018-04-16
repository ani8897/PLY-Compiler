
	.data

	.text	# The .text assembler directive indicates
	.globl main	# The following is the code
main:
# Prologue begins
 	sw $ra, 0($sp)	# Save the return address
 	sw $fp, -4($sp)	# Save the frame pointer
 	sub $fp, $sp, 8	# Update the frame pointer
 	sub $sp, $sp, 8	# Make space for the locals
 # Prologue ends

label0:
	addi $s0, $sp, 4
	sw $s0, 8($sp)
	li $s1, 2
	lw $s2, 8($sp)
	sw $s1, 0($s2)
	j label1
label1:
	j epilogue_main
# Epilogue begins
epilogue_main:
	add $sp, $sp, 8
	lw $fp, -4($sp)
	lw $ra, 0($sp)
	jr $ra	# Jump back to the called procedure
# Epilogue ends

