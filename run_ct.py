# runs language under CT from https://esolangs.org/wiki/Bitwise_Cyclic_Tag
# the idea is that the program uses 0, 1, and ;
# while the data itself is the same as BCT
def run_ct(program: str, data: str) -> None:
    # Will not operate on strings which contain non-bits
    if not set(program).issubset({'0', '1', ';'}):
        raise ValueError("The input strings must contain only 0, 1, and ;. The program string contains at least one illegal character.")
    if not set(data).issubset({'0', '1'}):
        raise ValueError("The data string must contain only 0 and 1. The data string contains at least one illegal character.")
    # padding for print statements
    padding = ""
    # allows you to step through the program
    # and quickly stop infinite loops
    stop = ""
    # if data is empty, it stops
    # if input is not empty, it stops
    print('Commands|Data')
    while data != "" and stop == "":
        if program[0] == ";":
            # prints output similar to esolangs page
            print(f"    {program[0]}   |{padding}{data}", end="")
            program = program[1:] + program[:1]
            padding += " "
            data = data[1:]
        else:
            print(f"    {program[0]}   |{padding}{data}", end="")
            if data[0] == "1":
                data += program[0]
            program = program[1:] + program[:1]
        stop = input()


if __name__ == '__main__':
    run_ct('1', '1')
