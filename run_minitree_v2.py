def output_preorder(upper, start=1):
    output = [start - 1]
    if start * 2 <= upper:
        output += output_preorder(upper, start * 2)
    if start * 2 + 1 <= upper:
        output += output_preorder(upper, start * 2 + 1)
    return output


def run_minitree(code, input_mode='tree'):
    if input_mode not in ('tree', 'linear'):
        raise ValueError('The only valid input modes are tree and linear.')

    valid_instructions = ('<', '>', '^', '@', '.', ',', '[', ']')
    code_tree = [inst for inst in code if inst in valid_instructions]
    data_tree = [0]
    iteration_order = output_preorder(len(code_tree))
    cp = 0  # code pointer
    dp = 1  # tape pointer

    input_string = ''

    if input_mode == 'linear':
        new_tree = [''] * len(code_tree)
        for num, char in enumerate(code_tree):
            new_tree[iteration_order[num]] = char
        print('Warning: The format is intended to be tree-based.\n'
              'This is your code as intended (tree):\n'
              f'{"".join(new_tree)}')
        code_tree = new_tree

    bracket_stack = []  # checks if brackets are fine
    corresponding_bracket = {}  # makes looping quicker

    for num, position in enumerate(iteration_order):
        if code_tree[position] == '[':
            bracket_stack.append(num)
        elif code_tree[position] == ']':
            if len(bracket_stack) <= 0:
                raise ValueError('unmatched ]')
            corresponding_bracket[num] = bracket_stack[-1]
            corresponding_bracket[bracket_stack[-1]] = num
            bracket_stack.pop()
    if len(bracket_stack) != 0:
        raise ValueError('unmatched [')

    while cp < len(iteration_order):
        inst = code_tree[iteration_order[cp]]
        if inst == '>':
            dp = dp * 2 + 1
            if dp > len(data_tree):
                data_tree += [0] * (dp - len(data_tree))
        elif inst == '<':
            dp *= 2
            if dp > len(data_tree):
                data_tree += [0] * (dp - len(data_tree))
        elif inst == '^':
            if dp == 1:
                raise ValueError('Cannot move up from root')
            dp //= 2
        elif inst == '@':
            data_tree[dp - 1] = (data_tree[dp - 1] - 1) % 2
        elif inst == '.':
            output = 0
            if dp * 4 + 3 > len(data_tree):
                data_tree += [0] * (dp * 4 + 3 - len(data_tree))
            output_bits = [dp * 4 + 3, dp * 4 + 2, dp * 2 + 1, dp * 4 + 1, dp * 4, dp * 2, dp]

            for bit in output_bits:
                output += data_tree[bit - 1]
                if bit != dp:
                    output *= 2

            print(chr(output), end='')
        elif inst == ',':
            if input_string == '':
                input_string = input(">>")
            if len(input_string) > 0:

                input_char = ord(input_string[0])

                if dp * 4 + 3 > len(data_tree):
                    data_tree += [0] * (dp * 4 + 3 - len(data_tree))
                input_bits = [dp, dp * 2, dp * 4, dp * 4 + 1, dp * 2 + 1, dp * 4 + 2, dp * 4 + 3]

                for bit in input_bits:
                    data_tree[bit - 1] = input_char % 2
                    input_char //= 2

                input_string = input_string[1:]
        elif inst == '[':
            if data_tree[dp - 1] == 0:
                cp = corresponding_bracket[cp]
        elif inst == ']':
            if data_tree[dp - 1] != 0:
                cp = corresponding_bracket[cp]
        cp += 1
    # print(data_tree)
