# runs language from https://esolangs.org/wiki/New
# textfile indicates whether the string is a textfile
def run_newlang(rawcode: str, textfile=False) -> None:
    pointer = 0  # for instructions
    location = 0  # for tape
    tape = [0]

    if textfile:
        code = [char for char in open(f'{rawcode}', 'r').readlines() if char in set('I~O!*%()')]
    else:
        code = [char for char in rawcode if char in set('I~O!*%()')]

    corresponding_bracket = {}  # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []  # acts as a stack for the last bracket

    for num, char in enumerate(code):
        if char == '(':
            bracket_stack.append(num)
        elif char == ')':
            if len(bracket_stack) <= 0:
                raise ValueError('unmatched ]')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if len(bracket_stack) != 0:
        raise ValueError('unmatched [')

    while pointer < len(code):
        if code[pointer] == 'I':
            tape[location] += 1
        elif code[pointer] == '~':
            tape[location] -= 1
        elif code[pointer] == 'O':
            print(chr(tape[location] % 1114112), end='')
        elif code[pointer] == '!':
            if location == len(tape):
                raise KeyError("There is no next cell for ! to add from.")
            tape[location] += tape[location+1]
        elif code[pointer] == '*':
            location += 1
            if location == len(tape):
                tape.append(0)
        elif code[pointer] == '%':
            if location == 0:
                tape = [0] + tape
            else:
                location -= 1
        elif code[pointer] == '(':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == ')':
            if tape[location] != 0:
                pointer = corresponding_bracket[pointer]
        pointer += 1
