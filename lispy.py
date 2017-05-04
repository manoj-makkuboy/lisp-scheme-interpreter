def scanner(input_str):
    '''Scans the input string from standard input and replaces '(' with '['
        and ')' with ']' '''
    split_tokens = []
    input_str = input_str.replace('(', ' [ ')
    input_str = input_str.replace(')', ' ] ')

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

        if(un_parsed_list_of_tokens[x] == '['):
            parenthesis.append('(')
        elif(un_parsed_list_of_tokens[x] == ']'):
            parenthesis.append(')')

        parsed_list_of_tokens.append(item_parser(un_parsed_list_of_tokens[x]))

    print(parenthesis)
    if (is_parenthesis_valid(parenthesis) == False):
        raise SyntaxError("Syntax Error invalid parenthesis")

    return parsed_list_of_tokens



input_string_main = input()
print ('parser output : ', parser(scanner(input_string_main)))



