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

    parenthesis = []
    parsed_list_of_tokens = []

    def item_parser(x):
        '''parses individual items from un_parsed list of tokens'''
        try:
            int(x)
            return (int(x))
        except ValueError:
            return (x)


    def is_parenthesis_valid(parenthesis_list_arg):
        '''finds the given list of parenthesis is valid set'''

        parenthesis_list_length = len(parenthesis_list_arg)

        if (parenthesis_list_length % 2 != 0):
            return False

        first_half_of_parenthesis = parenthesis_list_arg[:(parenthesis_list_length//2)]
        second_half_of_parenthesis = parenthesis_list_arg[parenthesis_list_length//2:parenthesis_list_length+1]
        print (first_half_of_parenthesis)
        print(second_half_of_parenthesis)
        for parenthesis in first_half_of_parenthesis:
            if(parenthesis != '('):
                return False

        for parenthesis in second_half_of_parenthesis:
            if(parenthesis != ')'):
                return False

        return True


    for x in range(0,len(un_parsed_list_of_tokens)):

        if(un_parsed_list_of_tokens[x] == '('):
            parenthesis.append('(')
        elif(un_parsed_list_of_tokens[x] == ')'):
            parenthesis.append(')')

        parsed_list_of_tokens.append(item_parser(un_parsed_list_of_tokens[x]))

    print(parenthesis)
    if (is_parenthesis_valid(parenthesis) == False):
        raise SyntaxError("Syntax Error invalid parenthesis")


    return parsed_list_of_tokens



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


def arithmetic_operator(s_expression):

    if(s_expression[0] == '+'):       # for expression starting with '+'
        result = 0
        x = 1

        while (x < len(s_expression)):
            if (type(s_expression[x]) == type([])):
                s_expression[x]  = evaluator(s_expression[x])
            if (type(s_expression[x])  == type('')):
                try:
                    s_expression[x] = ENV[s_expression[x]]
                except KeyError:
                    print("Variable not Declared")

            result += s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '-'):      # for expression starting with '-'

        result = s_expression[1]

        if(len(s_expression) == 2):   # Special case like (- 3) to return -3
           return (-1 * result)

        x = 2

        while (x < len(s_expression)):

            if (type(s_expression[x]) == type([])):
                s_expression[x]  = evaluator(s_expression[x])
            result -= s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '*'):       # for expression starting with '*'
        result = 1
        x = 1

        while (x < len(s_expression)):
            if (type(s_expression[x]) == type([])):
                s_expression[x]  = evaluator(s_expression[x])
            result *= s_expression[x]
            x += 1

        return result

    if(s_expression[0] == '/'):       # for expression starting with '/'
        result = s_expression[1]
        x = 2


        if(len(s_expression) == 2):     # special case to return (/ 5) as (1/5)
            return str(Fraction(1/s_expression[1]))

        while (x < len(s_expression)):
            if (type(s_expression[x]) == type([])):
                s_expression[x]  = evaluator(s_expression[x])
            result /= s_expression[x]
            x += 1

        return str(Fraction(result).limit_denominator())


def bind_variable(s_expression):

    if(type(s_expression[2]) == type(1)):         # if the 3rd element of the define statment is int create the variable and store the int
        ENV[s_expression[1]] = s_expression[2]
    elif(type(s_expression[2]) == type([])):       # if the 3rd element is of list instance send it to evaluator for evaluation
        ENV[s_expression[1]] = evaluator(s_expression[2])
    elif(type(s_expression[2]) == type('')):       # if the 3rd element is of string search the ENV for available value
        try:
            ENV[s_expression[1]] = ENV[s_expression[2]]
        except KeyError:
            raise SyntaxError ("Variable not found")

    return ENV    # review needed to decide the return type


def evaluator(s_expression):
    if (s_expression[0] == '+' or s_expression[0] ==  '-' or s_expression[0] ==  '*' or s_expression[0] ==  '/'):
        result = arithmetic_operator(s_expression)
        return result
    elif (s_expression[0] == 'define'):
        bind_variable(s_expression) # review needed to decide what return to put
        return
    elif(s_expression[0] == 'begin'):
        for x in s_expression:
            if(type(x) == type([])):
                print(evaluator(x))

ENV = {}


if __name__ == '__main__':

    input_string_main = input()
    print ('parser output : ', parser(scanner(input_string_main)))

