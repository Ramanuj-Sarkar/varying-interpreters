.data
header: .asciiz "Commands|Data"
zero_front_string: .asciiz "   0    |"
one_zero_string: .asciiz "   10   |"
one_one_string: .asciiz "   11   |"
new_line: .asciiz "\n"
error_message: .asciiz "You can only have 0 or 1 in the program and data."
data_space: .space 64

program: .asciiz "0"
data: .asciiz "1111111111111111111111"

.text

j main

# $a0 = program
# $a1 = data
bitwise_cyclic_tag:
subi $sp, $sp, 12
sw $s0, ($sp) # beginning of program
sw $s1, 4($sp) # end of number
sw $s2, 8($sp) # end of possible stretching
move $s0, $a0
la $s1, data_space
add $s2, $s1, 64
start_data_shift_loop:
lb $t0, ($a1)
beqz $t0, end_data_shift_loop
beq $t0, 48, correct_input
beq $t0, 49, correct_input
j error_command
correct_input:
sb $t0, ($s1)
addi $a1, $a1, 1
addi $s1, $s1, 1
j start_data_shift_loop
end_data_shift_loop:
la $a0, header
li $v0, 4
syscall
move $t0, $s0 # which numeral of the program?
sub $s1, $s1, 1
start_cyclic_loop:
la $t1, data_space # which numeral of the data?
la $a0, new_line
li $v0, 4
syscall
beq $s1, $s2, end_cyclic_loop
lb $t2, ($t0) # which value of the byte being checked?
bne $t2, $zero, not_at_end
move $t0, $s0
lb $t2, ($t0)
not_at_end: 
beq $t2, 48, zero_command
beq $t2, 49, one_command
j error_command
zero_command:
la $a0, zero_front_string
li $v0, 4
syscall
addi $t0, $t0, 1
li $v0, 11
start_space_printing:
lb $a0, ($t1)
bne $a0, 32, end_space_printing
syscall
addi $t1, $t1, 1
j start_space_printing
end_space_printing:
li $a0, 32
syscall
beq $t1, $s1, end_cyclic_loop
sb $a0, ($t1)
start_numeral_printing:
addi $t1, $t1, 1
lb $a0, ($t1)
syscall
beq $t1, $s1, start_cyclic_loop
j start_numeral_printing
one_command:
addi $t0, $t0, 1
lb $t2, ($t0)
bne $t2, $zero, one_not_at_end
move $t0, $s0
lb $t2, ($t0)
one_not_at_end: 
bne $t2, 48, did_not_print_one_zero
la $a0, one_zero_string
li $v0, 4
syscall
j rest_of_one
did_not_print_one_zero:
bne $t2, 49, error_command
la $a0, one_one_string
li $v0, 4
syscall
rest_of_one:
addi $s1, $s1, 1
sb $t2, ($s1)
addi $t0, $t0, 1
li $v0, 11
start_one_printing:
lb $a0, ($t1)
syscall
beq $t1, $s1, start_cyclic_loop
addi $t1, $t1, 1
j start_one_printing
error_command:
la $a0, error_message
li $v0, 4
syscall
end_cyclic_loop:
lw $s0, ($sp)
lw $s1, 4($sp)
lw $s2, 8($sp)
addi $sp, $sp, 12
jr $ra

main:
la $a0, program
la $a1, data
jal bitwise_cyclic_tag
li $v0, 10
syscall
