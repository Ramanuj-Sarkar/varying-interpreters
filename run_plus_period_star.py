# runs language from https://esolangs.org/wiki/%2B.*
# starting_input indicates what the starting input should be, in case it shouldn't be taken from the text
def run_plus_period_star(code: str, starting_input=''):
    pointer = 0  # for instructions
    location = 0  # for tape
    tape = [0]
    input_string = starting_input  # allows multiple inputs to happen easily

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
        elif code[pointer] == '*':
            if tape[location] == 0:
                pointer = -1
        pointer += 1
    return tape

if __name__ == '__main__':
    run_plus_period_star('>+.>+.*<*')  # prints out chr(1) twice, looks like AA
    # run_plus_period_star('>+.<*')  # does the thing the language's name is supposed to do
