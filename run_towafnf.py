# runs language from https://esolangs.org/wiki/There_Once_was_a_Fish_Named_Fred
# textfile indicates whether the string is a textfile
def run_towafnf(code_str: str, textfile=False):
    pointer = 0  # for instructions
    location = 0  # for tape
    tape = [0]

    if textfile:
        with open(f'{code_str}', 'r') as f:
            code_str = ''.join(f.readlines())

    code = code_str.split()
    corresponding_bracket = {}  # dictionary where the values are the corresponding bracket positions of the keys
    bracket_stack = []  # acts as a stack for the last bracket

    for num, word in enumerate(code):
        if word == 'named':
            bracket_stack.append(num)
        elif word == 'Fred':
            if len(bracket_stack) <= 0:
                raise ValueError('unmatched "Fred"')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if len(bracket_stack) != 0:
        raise ValueError('unmatched "named"')

    while pointer < len(code):
        if code[pointer] == 'once':
            location += 1
            if location == len(tape):
                tape.append(0)
        elif code[pointer] == 'there':
            if location <= 0:
                raise ValueError('Cannot move left from position 0')
            location -= 1
        elif code[pointer] == 'was':
            tape[location] = (tape[location] + 1) % 256
        elif code[pointer] == 'a':
            tape[location] = (tape[location] - 1) % 256
        elif code[pointer] == 'fish':
            print(chr(tape[location]), end='')
        elif code[pointer] == 'named':
            if tape[location] == 0:
                pointer = corresponding_bracket[pointer]
        elif code[pointer] == 'Fred':
            if tape[location] != 0:
                pointer = corresponding_bracket[pointer]
        pointer += 1


if __name__ == '__main__':
    run_towafnf('was was was was was was was was named once was was was was named once was was once was was was once was was was once was there there there there a Fred once was once was once a once once was named there Fred there a Fred once once fish once a a a fish was was was was was was was fish fish was was was fish once once fish there a fish there fish was was was fish a a a a a a fish a a a a a a a a fish once once was fish once was was fish')
