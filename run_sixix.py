# runs language which can be found here:
# https://esolangs.org/wiki/6ix
def run_sixix(method="input"):
    # puts input into code
    code = []
    if method == "input":
        print("Enter your code here:")
        line = input()
        while line != "end":
            code.append(line.strip(' '))
            line = input()
    else:
        for line in open(method, 'r'):
            code.append(line.strip('\n').strip(' '))

    # instantiates pointer, variable name holder,
    # and loop checking variables
    pointer = 0
    variable_names = {}
    in_loop = 0
    loop_top = 0

    # this function analyses the strings
    # to tell if they are variables or not
    def analyse_string(unanalysed: str) -> str:
        unanalysed = unanalysed.strip(' ')
        # strings which start with var
        # might be variables
        if "var" == unanalysed[:3]:
            further = unanalysed[3:].strip(' ')
            if further in variable_names:
                return variable_names[further]
        return unanalysed

    # the main code loop
    while pointer < len(code):
        if "goto" == code[pointer][:4]:
            # I decided goto could also use variables
            # as long as they passed goto requirements
            goto_num = analyse_string(code[pointer][4:])

            # goto_num must consist of digits to become an int
            # this also rules out all negative numbers
            if not goto_num.isdigit():
                raise ValueError(f"Goto Error at line {pointer+1}: goto does not have a corresponding number.")
            goto_num = int(goto_num)

            # goto_num must be within these bounds to work
            if not 1 <= goto_num <= len(code)+1:
                raise ValueError(f"Goto Error at Line {pointer}: The goto points to a line which doesn't exist.")
            pointer = int(goto_num) - 2
        elif "print" == code[pointer][:5]:
            # the string must be analysed
            # in case it's a variable
            print_string = analyse_string(code[pointer][5:])
            print(print_string)
        elif "input" == code[pointer][:5]:
            # this is a variable by default
            # so it cannot be analysed using the function
            input_var = code[pointer][5:].strip(" ")
            # the variable cannot be blank
            if len(input_var) <= 0:
                raise SyntaxError(f"Input Error at line {pointer+1}: variable is not being assigned.")
            variable_names[input_var] = input("Input a variable:")
        elif "var" == code[pointer][:3]:
            # this strips the code of spaces at the end
            # then splits it on the first equals and no later ones
            equals = code[pointer][3:].strip(" ").split("=", 1)

            # this is in case there is no equals sign
            if len(equals) != 2:
                raise SyntaxError(f"Var Error at line {pointer+1}: var is not being assigned.")
            equals = [x.strip(" ") for x in equals]

            # the first argument is already a variable by default
            # the second argument might be a variable
            variable_names[equals[0]] = analyse_string(equals[1])
        elif "loop" == code[pointer]:
            if in_loop == 0:
                # this is the beginning loop
                loop_top = pointer
            elif in_loop == 1:
                # this is the ending loop the first time
                pointer = loop_top
            else:
                # this is the ending loop the second time
                in_loop = -1
            in_loop += 1
        elif "end" == code[pointer]:
            break
        # putting the pointer increment here
        # forces the goto to not make sense
        # but saves on space a bit
        pointer += 1
