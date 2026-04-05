import random


def run_befunge(code_string: str, file_name: True):
    stack = []
    y = 0
    x = 0

    # This is the code itself.
    running = []

    # You can use text files
    if file_name:
        for line in open(code_string, 'r'):
            goodline = line.strip('\n')
            running.append(goodline)
    else:
        running = code_string.split('\n')

    if len(running) > 25:
        raise ValueError("The height of the playfield cannot exceed 25 characters.")

    for line in running:
        if len(line) > 80:
            raise ValueError("The width of the playfield cannot exceed 80 characters.")

    direction = '>'
    direction_string = 'v<^>'
    string_mode = False

    char = running[y][x]
    while char != '@':
        if char == '"':
            string_mode = not string_mode

        elif string_mode:
            stack.append(ord(char))

        elif ord('0') <= ord(char) <= ord('9'):
            stack.append(int(char))

        elif char in {'v', '<', '^', '>', '?', ':', '&', '~'}:  # don't pop any values
            if char in direction_string:
                direction = char
            elif char == '?':
                direction = direction_string[random.randint(0, 3)]
            elif char == ':':
                if len(stack) == 0:
                    stack.append(0)
                stack.append(stack[-1])
            elif char in {'&', '~'}:
                result = input() # does not support multiple character inputs
                if char == '&':
                    if not result.isdigit():
                        raise ValueError("Input of & must be an integer.")
                    stack.append(int(result))
                else:
                    stack.append(ord(result[0]))

        elif char == '#':
            if direction == 'v':
                y = (y + 1) % len(running)
            elif direction == '<':
                x = (x - 1) % len(running[y])
            elif direction == '^':
                y = (y - 1) % len(running)
            else:
                x = (x + 1) % len(running[y])

        elif char in {'!', '_', '|', '$', '.', ','}:  # pop one value
            result = stack.pop()
            if char == '!':
                stack.append(1 if result == 0 else 0)
            elif char == '_':
                direction = ('>' if result == 0 else '<')
            elif char == '|':
                direction = ('v' if result == 0 else '^')
            if char == '.':
                print(str(result),end='')
            elif char == ',':
                print('' if result == 0 else chr(result),end='')

        elif char in {'+', '-', '*', '/', '%', '`', '\\', 'g'}:  # pop two values, push one value
            a = stack.pop()
            if len(stack) == 0:
                b = 0
            else:
                b = stack.pop()

            if char == '+':
                result = b + a
            elif char == '-':
                result = b - a
            elif char == '*':
                result = b * a
            elif char == '/':
                if a == 0:
                    result = int(input(f'What do you want {b}/0 to equal?'))
                else:
                    result = b // a
            elif char == '%':
                if a == 0:
                    result = 0
                else:
                    result = b % a
            elif char == '`':
                result = int(b > a)
            elif char == '\\':
                stack.append(a)
                result = b
            elif char == 'g':
                if a >= len(running) or b >= len(running[a]):
                    result = 0
                else:
                    result = ord(running[a][b])
            stack.append(result)

        elif char == 'p':
            py = stack.pop()
            assign_row = running[py]
            px = stack.pop()
            pv = chr(stack.pop())
            assign_row = assign_row[:px] + pv + assign_row[px + 1:]
            running[py] = assign_row

        if direction == 'v':
            y = (y + 1) % 25
        elif direction == '<':
            x = (x - 1) % 80
        elif direction == '^':
            y = (y - 1) % 25
        else:
            x = (x + 1) % 80

        char = running[y][x] if y < len(running) and x < len(running[y]) else ' '


if __name__ == '__main__':
    run_befunge('>1+:3%!#v_>:5%!#v_v\n'
                '^,*52.:_ `@#\\"d" :<\n'
                ' v"Fizz"<        >v\n'
                ' >,,,,:5%        | \n'
                '     v,,,,"Buzz"<< \n'
                '^,*52<            <', False)
