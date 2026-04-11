# runs language from https://esolangs.org/wiki/BFFB
# textfile indicates whether the string is a textfile
# starting_input indicates what the starting input should be, in case it shouldn't be taken from the text
def run_bffb(rawcode: str, textfile=False, starting_input='') -> None:
    pointer = 0  # for instructions
    location = 0  # for tape
    tape = [0]
    input_string = starting_input  # allows multiple inputs to happen easily

    if textfile:
        with open(rawcode, 'r') as s:
            code = [char for char in ''.join(s.readlines()) if char in set('+-><,.[]')]
    else:
        code = [char for char in rawcode if char in set('+-><,.[]')]

    print(code)

    mirror = {'+': '+',
              '-': '-',
              '>': '<',
              '<': '>',
              ',': ',',
              '.': '.',
              '[': ']',
              ']': '['}

    for x in range(len(code)):
        first, last = code[x], code[len(code) - 1 - x]
        if mirror[first] != last:
            raise SyntaxError(f'{first} is not the mirror image of {last}')

    corresponding_bracket = {}  # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []  # acts as a stack for the last bracket

    for num, char in enumerate(code):
        if char == '[':
            bracket_stack.append(num)
        elif char == ']':
            if len(bracket_stack) <= 0:
                raise ValueError('unmatched ]')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if len(bracket_stack) != 0:
        raise ValueError('unmatched [')

    while pointer < len(code):
        if code[pointer] == '>':
            location += 1
            if location == len(tape):
                tape.append(0)
        elif code[pointer] == '<':
            if location <= 0:
                raise ValueError('Cannot move left from position 0')
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

if __name__ == '__main__':
    run_bffb(",[.,][,.],")
