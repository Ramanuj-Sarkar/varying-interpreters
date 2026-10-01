# This runs the second version of this esolang: https://esolangs.org/wiki/2DFIM
def run_2dfim_v2(code_string, file_name=False, input_string=''):
    # This is the code itself.
    code = []

    # This is the memory
    memory = [False] * 11

    # You can use text files.
    if file_name:
        for line in open(code_string, 'r'):
            code.append(line.rstrip('\n'))
    else:
        code = code_string.split('\n')

    # This makes sure you can still go down
    # when one line is shorter than all the rest
    max_columns = max([len(line) for line in code])
    max_rows = len(code)

    # This indicates the next instruction in the code.
    pointer = (0, 0)

    # This indicates the current memory location.
    cell = 2

    while True:
        row, column = pointer[0], pointer[1]
        instruction = 'x'

        if column < len(code[row]) and code[row][column] in '<(':
            instruction = code[row][column]

            if instruction == '<':
                if cell != 0:
                    cell -= 1
            elif instruction == '(':
                cell += 1
                if cell == len(memory):
                    memory += [False]
                memory[cell] = not memory[cell]
                if not memory[cell]:
                    pointer = ((pointer[0] + 1) % max_rows, pointer[1] - 1)

            if memory[1]:
                # print("Input or output here.")
                out = memory[3:11]

                out_num = sum(2 ** (7 - power) for power, bit in enumerate(out) if bit == True)
                if out_num == 0:
                    in_str = ''
                    if input_string:
                        in_str = input_string[0]
                        input_string = input_string[1:]
                    else:
                        in_str += input("Input ASCII value between 1 and 255, inclusive:")

                    if in_str == '':
                        in_num = 0
                    else:
                        in_num = ord(in_str[0])
                        input_string += in_str[1:]

                    while not 1 <= in_num <= 255:
                        in_str = input("Input ASCII value between 1 and 255, inclusive:")
                        if in_str == '':
                            in_num = 0
                        else:
                            in_num = ord(in_str[0])

                        if 1 <= in_num <= 255:
                            input_string += in_str[1:]

                    for power in range(7, -1, -1):
                        memory[10 - power] = True if in_num // 2 ** power == 1 else False
                        in_num %= 2 ** power
                else:
                    print(chr(out_num),end='')
                memory[1] = False

        # print(pointer)
        pointer = (pointer[0], pointer[1] + 1)
        # print(pointer, cell, instruction)

        if pointer[1] == max_columns:
            if pointer[0] == max_rows - 1:
                if memory[cell]:
                    pointer = (pointer[0], 0)
                else:
                    break
            else:
                pointer = (pointer[0] + 1, 0)

    return memory, cell, pointer
