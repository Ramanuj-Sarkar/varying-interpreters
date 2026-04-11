# runs language from https://esolangs.org/wiki/Brainfuck+3
def run_bfp3(code: str, textfile=False) -> None:
    pointer=0   # for instructions
    row = 0   # for up and down tape
    column=0  # for left and right tape
    tape=[[0]]
    input_string = ''   # multiple inputs are possible

    if textfile:
        code = ''.join(open(f'{code}', 'r').readlines())

    corresponding_bracket = {}  # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []  # acts as a stack for the last bracket

    for num, char in enumerate(code):
        if char == '[':
            bracket_stack.append(num)
        elif char == ']':
            if len(bracket_stack) <= 0:
                return ValueError('unmatched ]')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if len(bracket_stack) != 0:
        raise ValueError('unmatched [')

    while pointer < len(code):
        if code[pointer] == '>':
            column += 1
            if column >= len(tape[row]):
                tape[row] += [0]
        elif code[pointer] == '<':
            column -= 1
            if column < 0:
                for row_number in range(len(tape)):
                    tape[row_number] = [0] + tape[row_number]
                column += 1
        elif code[pointer] == 'v':
            row += 1
            if row == len(tape):
                tape.append([0]*(column+1))
            if column >= len(tape[row]):
                tape[row] += [0] * (1 + column - len(tape[row]))  # this saves tape space
        elif code[pointer] == '^':
            row -= 1
            if row < 0:
                tape = [[0]*(column+1)] + tape
                row += 1
            if column >= len(tape[row]):
                tape[row] += [0] * (1 + column - len(tape[row]))  # this saves tape space
        elif code[pointer] == '+':
            tape[row][column] = (tape[row][column] + 1) % 256
        elif code[pointer] == '-':
            tape[row][column] = (tape[row][column] - 1) % 256
        elif code[pointer] == '.':
            print(chr(tape[row][column]),end='')
        elif code[pointer] == ',':
            if input_string == '':
                input_string = input(">>")
            if len(input_string) > 0:
                tape[row][column] = ord(input_string[0])
            input_string = input_string[1:]
        elif code[pointer] == '[':
            if tape[row][column] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == ']':
            if tape[row][column] != 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == 'x':
            break
        pointer += 1
    print(tape)
