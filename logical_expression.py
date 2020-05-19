
import sys
from copy import copy
from datetime import datetime


class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []



def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print('\nINVALID\n')

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print('\nUnexpected end of input.\n')
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

#Divya Start


def __extend(format, symbol, value):
    format[symbol] = value
    return format


#Functions assists in forming Regular expression
def __get_exp(exp, symbols):
    if exp.symbol[0]:
        symbols.append(exp.symbol[0])
    for subexpression in exp.subexpressions:
        __get_exp(subexpression, symbols)


def __get_symbols(knowledge_base,statement,symlist):
    read_kb = []
    read_symbol = []
    __get_exp(knowledge_base, read_kb)
    __get_exp(statement, read_symbol)
    read_kb = list(set(read_kb))
    read_symbol = list(set(read_symbol))
    read_kb.extend(read_symbol)
    symbols = list(set(read_kb))
    return symbols


#Function to perform check of tt_entails for each statement
def __check_entails(knowledgeBase, alpha, symbols, format):
    if not symbols:
        if __pl_exp_state(knowledgeBase, format):
            return __pl_exp_state(alpha, format)
        else:
            return True
    pvalue = symbols[0]
    restvalue = symbols[1:]
    return __check_entails( knowledgeBase, alpha, restvalue, __extend(format, pvalue, True) ) \
           and __check_entails( knowledgeBase, alpha, restvalue, __extend(format, pvalue, False) )


#Function to check if the PL statement is true for collectives and each symbol
def __pl_exp_state(expression, format):
    if expression.connective[0].lower() == 'and':
        state = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                state = __pl_exp_state(subexpression, format)
                continue;
            state = state and __pl_exp_state(subexpression, format)
        return state
    elif expression.connective[0].lower() == 'or':
        state = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                state = __pl_exp_state(subexpression, format)
                continue;
            state = state or __pl_exp_state(subexpression, format)
        return state
    elif expression.connective[0].lower() == 'not':
        state = not __pl_exp_state(expression.subexpressions[0], format)
        return state
    elif expression.connective[0].lower() == 'xor':
        state = True
        for i, subexpression in enumerate(expression.subexpressions):
            if(i == 0):
                state = __pl_exp_state(subexpression, format)
                continue;
            state = state ^ __pl_exp_state(subexpression, format)
        return state
    elif expression.connective[0].lower() == 'if':
        exp1 = __pl_exp_state(expression.subexpressions[0], format)
        exp2 = __pl_exp_state(expression.subexpressions[1], format)
        return ( (not exp1) or exp2 )
    elif expression.connective[0].lower() == 'iff':
        exp1 = __pl_exp_state(expression.subexpressions[0], format)
        exp2 = __pl_exp_state(expression.subexpressions[1], format)
        return ( (not exp1) or exp2 ) and ( (not exp2) or exp1 )
    return format[expression.symbol[0]]


def __write_result(True_Statement,False_Statement):
    if True_Statement == True and False_Statement == False:
        result = ('Definitely True')
        print(': Definitely True')
    elif True_Statement == False and False_Statement == True:
        result = ('Definitely False')
        print(': Definitely False')
    elif True_Statement == False and False_Statement == False:
        result = ('Possibly True or Possibly False')
        print(': Possibly True or Possibly False')
    elif True_Statement == True and False_Statement == True:
        result = ('Both True & False')
        print(': Both True & False')
    else:
        result = ('Invalid Statement or Knowledge Base, Please try with different files')
    return  result


#Function performs task of tt_entails to check synbols and statements with my Knowledge Base
def tt_entails(knowledge_base, statement, false, symlist):
    try:
        Result = open('result.txt', 'w')
    except:
        print('Problem with output file')
    symbols= __get_symbols(knowledge_base, statement,symlist)
    format = symlist.copy();
    for symbol in format.keys():
        try:
            symbols.remove(symbol)
        except Exception:
            pass
    True_Statement = __check_entails(knowledge_base, statement, symbols, format)
    False_Statement = __check_entails(knowledge_base, false, symbols, format)
    result_value = __write_result(True_Statement,False_Statement)
    Result.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + result_value)
    Result.close()


    # Divya Stop
