# runs language from https://esolangs.org/wiki/(_%CD%A1%C2%B0_%CD%9C%CA%96_%CD%A1%C2%B0)fuck
def run_lenny(code: str, actually_run = False) -> None:
    pointer = 0  # for instructions
    row = 0     # for up and down tape
    column = 0  # for left and right tape
    tape = [[0]]
    input_string = ''  # allows multiple inputs easily

    corresponding_bracket = {}       # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []     # acts as a stack for the last bracket
    for num in range(len(code)):
        if code[num:num+5] == '( ͡°(':
            bracket_stack.append(num)
        elif code[num:num+5] == ') ͡°)':
            if len(bracket_stack) <= 0:
                raise ValueError('unmatched ) ͡°)')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if balance != 0:
        raise ValueError('unmatched ( ͡°(')

    while pointer < len(code):
        skip = 1
        if code[pointer:pointer+11] == 'ᕦ( ͡°ヮ ͡°)ᕥ':
            column += 1
            if column == len(tape[row]):
                for row_number in range(len(tape)):
                    tape[row_number].append(0)
            skip = 11
        elif code[pointer:pointer+18] == '(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ.*':
            column -= 1
            if column < 0:  # I've decided you CAN do this, actually
                for row_number in range(len(tape)):
                    tape[row_number] = [0] + tape[row_number]
                column += 1
            skip = 18
        elif code[pointer:pointer+12] == '( ͡°╭͜ʖ╮ ͡°)':
            row += 1
            if row == len(tape):
                tape.append([0]*(column+1))
            skip = 12
        elif code[pointer:pointer+13] == 'ᕦ( ͡° ͜ʖ ͡°)ᕥ':
            row -= 1
            if row < 0:
                tape = [[0]*(column+1)] + tape
                row += 1
            skip = 13
        elif code[pointer:pointer+11] == '( ͡° ͜ʖ ͡°)':
            tape[row][column] = (tape[row][column] + 1) % 256
            skip = 11
        elif code[pointer:pointer+7] == '(> ͜ʖ<)':
            tape[row][column] = (tape[row][column] - 1) % 256
            skip = 7
        elif code[pointer:pointer+7] == '(♥ ͜ʖ♥)':
            print(chr(tape[row][column]),end='')
            skip = 7
        elif code[pointer:pointer+13] == 'ᕙ( ͡° ͜ʖ ͡°)ᕗ':
            if input_string == '':
                input_string = input(">>")
            if len(input_string) > 0:
                tape[row][column] = ord(input_string[0])
                input_string = input_string[1:]
            skip = 13
        elif code[pointer:pointer+5] == '( ͡°(':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
            skip = 5
        elif code[pointer:pointer+5] == ') ͡°)':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer:pointer+3] == 'ಠ_ಠ':
            break
        pointer += skip
