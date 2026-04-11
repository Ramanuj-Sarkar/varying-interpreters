# runs language from https://esolangs.org/wiki/Linear_bounded_brainfuck
def run_lbf(code: str, textfile=False, starting_input='') -> None:
    pointer = 0  # for instructions
    location = 0  # for tape
    counter = 0

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

    tape = [ord(x) for x in starting_input] + ([0] * len(code))

    while pointer < len(code):
        if code[pointer] == '>':
            location += 1
            assert location < len(tape), f'Cannot move right from position {len(tape)}'
        elif code[pointer] == '<':
            if location == 0:
                raise ValueError('Cannot move left from position 0')
            location -= 1
        elif code[pointer] == '+':
            tape[location] = (tape[location] + 1) % 256
        elif code[pointer] == '-':
            tape[location] = (tape[location] - 1) % 256
        elif code[pointer] == '.':
            print(chr(tape[location]), end='')
        elif code[pointer] == '[':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == ']':
            if tape[location] != 0:
                pointer = corresponding_bracket[pointer]
        pointer += 1


if __name__ == '__main__':
    run_lbf('[.>]', False, 'Hello World.')
