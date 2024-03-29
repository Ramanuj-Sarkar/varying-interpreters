# runs language from https://esolangs.org/wiki/Brainfuck
# textfile indicates whether the string is a textfile
# starting_input indicates what the starting input should be, in case it shouldn't be taken from the text
def run_bf(code: str, textfile=False, starting_input='') -> None:
    pointer = 0  # for instructions
    location = 0  # for tape
    tape = [0]
    input_string = starting_input  # allows multiple inputs to happen easily

    if textfile:
        code = ''.join(open(f'{code}', 'r').readlines())
    corresponding_bracket = {}  # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []  # acts as a stack for the last bracket

    for num, char in enumerate(code):
        if char == '[':
            bracket_stack.append(num)
        elif char == ']':
            assert len(bracket_stack) > 0, 'unmatched ]'
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    assert len(bracket_stack) == 0, 'unmatched ['

    while pointer < len(code):
        if code[pointer] == '>':
            location += 1
            if location == len(tape):
                tape.append(0)
        elif code[pointer] == '<':
            assert location > 0, 'Cannot move left from position 0'
            location -= 1
        elif code[pointer] == '+':
            tape[location] = (tape[location] + 1) % 256
        elif code[pointer] == '-':
            tape[location] = (tape[location] - 1) % 256
        elif code[pointer] == '.':
            print(chr(tape[location]), end='')
        elif code[pointer] == ',':
            if input_string == '':
                input_string = input(">>")
            if len(input_string) > 0:
                tape[location] = ord(input_string[0])
                input_string = input_string[1:]
        elif code[pointer] == '[':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == ']':
            if tape[location] != 0:
                pointer = corresponding_bracket[pointer]
        pointer += 1
