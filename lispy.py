from fractions import Fraction

def scanner(input_str):
    '''Scans the input string from standard input and replaces '(' with ' [ '
        and ')' with ' ] ' '''
    split_tokens = []
    input_str = input_str.replace('(', ' ( ')
    input_str = input_str.replace(')', ' ) ')

    split_tokens = input_str.split()

    return split_tokens


def parser(un_parsed_list_of_tokens):
    '''sends each un parsed element from un parsed
        list of tokens and uses item_parser funtion to
        parse those items'''

    parsed_list_of_tokens = []

    def item_parser(x):
        '''parses individual items from un_parsed list of tokens'''
        try:
            int(x)
            return (int(x))
        except ValueError:
            return (x)


    def build_list(un_parsed_tokens):
        new_list = []
        x = 0

        if(un_parsed_tokens[x] == '('):
            x += 1

            while(x < len(un_parsed_tokens)):
                if(un_parsed_tokens[x] == ')'):
                    return new_list           # base Return
                elif(un_parsed_tokens[x] == '('):
                    respective_close_int = find_respective_close(un_parsed_tokens,x)
                    sub_list = build_list(un_parsed_tokens[x:respective_close_int + 1])
                    x  = respective_close_int + 1
                    new_list.append(sub_list)
                elif(un_parsed_tokens[x] != ')' or '('):
                    new_list.append(un_parsed_tokens[x])
                    x += 1
        return new_list



    for x in range(0,len(un_parsed_list_of_tokens)):

        parsed_list_of_tokens.append(item_parser(un_parsed_list_of_tokens[x]))

    return build_list(parsed_list_of_tokens)


def find_respective_close(token_list,open_index):
    open_p = 0
    close_p = 0
    for x in range(open_index,len(token_list)+1):
        if(token_list[x] == '('):
            open_p += 1
        elif(token_list[x] == ')'):
            close_p += 1
        if (open_p == close_p):
            return x


def eval_and_return(token):
    if(type(token) is list):
        return evaluator(token)
    elif(type(token) is  str):
        try:
            return ENV[token]
        except KeyError:
            print ("Variable not found")
    elif(type(token) is int):
         return token


def arithmetic_operator(s_expression):

    if(s_expression[0] == '+'):       # for expression starting with '+'
        result = 0
        x = 1

        while (x < len(s_expression)):

            s_expression[x] = eval_and_return(s_expression[x])
            result += s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '-'):      # for expression starting with '-'

        result = s_expression[1]

        if(len(s_expression) == 2):   # Special case like (- 3) to return -3
           return (-1 * result)

        x = 2

        while (x < len(s_expression)):

            s_expression[x]  = eval_and_return(s_expression[x])
            result -= s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '*'):       # for expression starting with '*'
        result = 1
        x = 1

        while (x < len(s_expression)):
            s_expression[x]  = eval_and_return(s_expression[x])
            result *= s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '/'):       # for expression starting with '/'
        result = s_expression[1]
        x = 2


        if(len(s_expression) == 2):     # special case to return (/ 5) as (1/5)
            return 1/s_expression[1]

        while (x < len(s_expression)):
            s_expression[x]  = eval_and_return(s_expression[x])
            result /= s_expression[x]
            x += 1

        return result


def relational_operator(s_expression):
    ''' expects a list with first element with either '>' or '<' returns #t or
    #f based on the operands'''
    if(len(s_expression) == 2):
        return '#t'

    x = 2
    for y in range(0,len(s_expression)):
        if(type(s_expression[y]) == type([])):
            s_expression[y] = evaluator(s_expression[y])

    if(s_expression[0] == '<'):
        while x < len(s_expression):
            if ( s_expression[x-1] >= s_expression[x]):
                return '#f'
            x += 1
        return '#t'

    if(s_expression[0] == '>'):
        while x < len(s_expression):
            if (s_expression[x-1] <= s_expression[x]):
                return '#f'
            x += 1
        return '#t'

    if(s_expression[0] == '<='):
            while x < len(s_expression):
                if ( s_expression[x-1] > s_expression[x]):
                    return '#f'
                x += 1
            return '#t'

    if(s_expression[0] == '>='):
        while x < len(s_expression):
            if (s_expression[x-1] < s_expression[x]):
                return '#f'
            x += 1
        return '#t'


def bind_variable(s_expression):

    try:

        if(s_expression[2][0] == 'lambda'):

            ENV[s_expression[1]] = s_expression[2]
            return ENV
    except TypeError:
        pass

    ENV[s_expression[1]] = eval_and_return(s_expression[2])

    return ENV    # review needed to decide the return type


def if_statement(s_expression):
    if (evaluator(s_expression[1]) == '#t'):
        if(type(s_expression[2]) == type([])):
            return evaluator(s_expression[2])
        elif(type(s_expression[2]) == type(0)):
            return s_expression[2]
        elif(type(s_expression[2] == type(''))):
            try:
                return (ENV[s_expression[2]])
            except KeyError:
                print("variable not found")

    else:
        if(type(s_expression[3]) == type([])):
            return evaluator(s_expression[3])
        elif(type(s_expression[3]) == type(0)):
            return s_expression[3]
        elif(type(s_expression[3] == type(''))):
            try:
                return (ENV[s_expression[3]])
            except KeyError:
                print("variable not found")


def function_call(s_expression, lambda_expression):
    function_env = {}
    if(len(s_expression[1:])  != len(lambda_expression[1])):
           raise SyntaxError ("number of actual args and formal args not matching")

    for x in range(0,len(lambda_expression[1])):  # building function_env
        function_env[lambda_expression[1][x]] =  eval_and_return(s_expression [x+1])  # assigning s_expression's args to saved lambda's variables in function_env dict
#    return function_env   # return for testing purpose
    global ENV
    ENV = {**ENV , **function_env}              # workaround and needs to be changed

    return evaluator(lambda_expression[2])

def evaluator(s_expression, function_env = None):
    ''' gets a list as input and dispatches the list to various functions based on the first element of the list '''
    if (s_expression[0] == '+' or s_expression[0] ==  '-' or s_expression[0] ==  '*' or s_expression[0] ==  '/'):
        result = arithmetic_operator(s_expression)
        return result
    elif(s_expression[0] == '>' or s_expression[0] == '<'  or s_expression[0] == '>=' or s_expression[0] == '<='):
        result = relational_operator(s_expression)
        return result

    elif (s_expression[0] == 'define'):
        bind_variable(s_expression) # review needed to decide what return to put
        return ENV
    elif (s_expression[0] == 'if'):
        return if_statement(s_expression)

    elif(s_expression[0] == 'begin'):

        for x in range(0,len(s_expression)):

            if(type(s_expression[x]) == type([])):
                result = evaluator(s_expression[x])
                if(x == (len(s_expression) - 1)):
                    return result

    elif(s_expression[0] == 'max'):
        result = max_fn(s_expression)
        return result

    elif(s_expression[0] == 'min'):
        result = min_fn(s_expression)
        return result

    elif(s_expression[0] == 'quote'):
        result = quote_fn(s_expression)
        return result

    elif(s_expression[0] in ENV):                   # user defined function call
        if type(ENV[s_expression[0]]) == list:
            if (ENV[s_expression[0]][0] == 'lambda'):
                lambda_expression =  ENV[s_expression[0]]
                return function_call(s_expression,lambda_expression)


ENV = {}


def max_fn(s_expression):
    for x in range(1,len(s_expression)):
        if type(s_expression[x]) == type([]):
            s_expression[x] =  evaluator(s_expression[x])
    return max(s_expression[1:])


def min_fn(s_expression):
    for x in range(1,len(s_expression)):
        if type(s_expression[x]) == type([]):
            s_expression[x] =  evaluator(s_expression[x])
    return min(s_expression[1:])


def quote_fn(s_expression):
    s_expression[1] = str(s_expression[1]).replace("[","(").replace("]",")").replace("'",'').replace(",",'')
    return s_expression[1]

def make_float_fraction(float_value):

    return str(Fraction(float_value).limit_denominator())


if __name__ == '__main__':

    while True:                  # REPL
        input_value = input("manoj's lispy >>> ")
        result = evaluator((parser(scanner(input_value))))   #str(Fraction(result).limit_denominator())
        if(isinstance(result,float)):
           result =  make_float_fraction(result)
        print ("LISPY output : ",result)


#    input_string_main = input()
#    parsed_output = parser(scanner(input_string_main))
#    print ('parser output : ', parsed_output)
#    built_list_output = build_list(parsed_output)
#    print ('built output : ',(built_list_output))
#    print ('evaluator output : ', evaluator(built_list_output))
