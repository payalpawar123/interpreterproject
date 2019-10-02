#Main structure.
queue = []
stack = []
missing_vars = set()



def IT_Tail():
    skip_spaces()
    token = lex_get()
    if token == "-":
        dequeue()
        token = lex_get()

        if token == ">":
            dequeue()
            return ("IT_Tail", CT(), IT_Tail())

        else:
            raise Exception("Expecting ->, but got -: " + str(token))
    else:
        return ("IT_END",)

def CT_Tail():
    skip_spaces()
    token = lex_get()
    if token == "^" or token == "V":
        dequeue()
        op = token
        return ("CT_Tail", op, L(), CT_Tail())

    else:
        return ("CT_END",)

def A():
    skip_spaces()
    token = lex_get()

    if token == "T":
        dequeue()
        return ("T",)
    elif token == "F":
        dequeue()
        return ("F",)
    elif token in ["a", "b", "c"]:
        dequeue()
        return ("VAR", token)
    elif token == "(":
        dequeue()
        it = IT()
        skip_spaces()
        token = lex_get()
        if token == ")":
            dequeue()
            return it
        else:
            raise Exception("Expecting ), but got: " + str(token))
def L():
    skip_spaces()
    token = lex_get()
    if token == "~":
        dequeue()
        return ("NOT", L())
    else:
        return A()


def CT():
    return ("CT", L(), CT_Tail())


#Imply term.
def IT():
    return ("IT", CT(), IT_Tail())

def VA():
        skip_spaces()
        token = lex_get()

        if token == "#":
            dequeue()
            skip_spaces()
            token = lex_get()

            if token in "abcdefghijklmnopqrstuvwxyz":
                var = token
                dequeue()
                skip_spaces()
                token = lex_get()

                if token == ":":
                    dequeue()
                    token = lex_get()

                    if token == "=":
                        dequeue()
                        it = IT()
                        skip_spaces()
                        token = lex_get()
                        if token == ";":
                            dequeue()
                            va = VA()
                            return ("VA", var, it, va)


                        else:
                            raise Exception("Expecting ;, but got: " + str(token))



                    else:
                        raise Exception("Expecting =, but got: " + str(token))

                else:
                    raise Exception("Expecting :, but got: " + str(token))
            else:
                raise Exception("Expecting a var, but got: " + str(token))

        else:

            return ("VA_END",)


# Boolean statement.
def B():
    va = VA()

    it = IT()
    skip_spaces()
    token = lex_get()
    if token == ".":
        return ("B", va, it)

    else:
        raise Exception("Expecting '.' got: " + str(token))


def lex_get():
    global queue
    return queue[0]


def dequeue():

    global queue

    if len(queue) == 0:
        print("Queue is empty!")
        return queue

    else:
        return queue.pop(0)

def skip_spaces():
    while lex_get() == ' ':
        dequeue()
def do_it(env, b, it):
    if it[0] == "IT_END":
        return b
    else:
        (_, ct, it_tail) = it
        beep = evaluate(env, ct)
        return do_it(env, (not b) or beep, it_tail)
def do_ct(env, b, ct):
    if ct[0] == "CT_END":
        return b
    else:
        (_, op, l, ct_tail) = ct
        beep = evaluate(env, l)
        if op == "^":
            return do_ct(env, b and beep, ct_tail)
        else:
            return do_ct(env, b or beep, ct_tail)

def evaluate(env, expr):
    global missing_vars
    if expr[0] == "IT":
        (_, ct, it_tail) = expr
        foo = evaluate(env, ct)
        return do_it(env, foo, it_tail)
    elif expr[0] == "CT":
        (_, l, ct_tail) = expr
        foo = evaluate(env, l)
        return do_ct(env, foo, ct_tail)
    elif expr[0] == "Not":
        (_, l) = expr
        return not evaluate(env, l)
    elif expr[0] == "VAR":
        (_, var) = expr
        if var not in env:
            missing_vars.add(var)
            return False
        else:
            return env[var]
    elif expr[0] == "T":
        return True
    elif expr[0] == "F":
        return False
    else:
        print(expr)
        raise Exception("wtf is this")

def do_vars(env, thing):
    if thing[0] == "VA_END":
        return env
    else:
        (_, var, it, more_thing) = thing
        foo = evaluate(env, it)
        env[var] = foo
        return do_vars(env, more_thing)
def do_b(b):
    (_, vars, it) = b
    env = do_vars({}, vars)
    return evaluate(env, it)
def main():

    global queue
    global stack

    #Get file
   # beep = input("gimme filename")
    FILE = open("Input.txt", "r")

    #Put the file into an array.
    lines = []
    for line in FILE:
        lines.append(line)


    #Stack
    expression = []
    str_ = ""
    #Assuming each line is an expression and each char a token.
    for line in lines:
        for i in range(len(line)):
            queue.append(line[i])
            stack.append(line[i])

    #Delete the null characters at the end
    stack = stack[:len(stack)-2]
    #Call to check bool statement
    try:
        value = do_b(B())
        if len(missing_vars) == 0:
            print("Expression is valid")
            print(value)
        else:
            print("Missing variables:")
            for x in missing_vars:
                print(x)
    except Exception as e:
        print("Expression is invalid.")
        #raise e



    FILE.close()

#Call main.
main()






