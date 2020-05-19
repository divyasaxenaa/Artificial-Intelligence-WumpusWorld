import sys
from logical_expression import *

def main(argv):    
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'r')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)   
    symlist = {}
    # Create the knowledge base with wumpus rules
    print('\nLoading wumpus rules...')
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        if subexpression.connective[0] == '':
            symlist[subexpression.symbol[0]] = True 
        if subexpression.connective[0].lower() == 'not':
            if subexpression.subexpressions[0].symbol \
            and subexpression.subexpressions[0].connective[0] == '':
               symlist[subexpression.subexpressions[0].symbol[0]] = False 
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'r')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print('Loading additional knowledge...')
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        if subexpression.connective[0] == '':
            symlist[subexpression.symbol[0]] = True   
        if subexpression.connective[0].lower() == 'not':
            if subexpression.subexpressions[0].connective[0] == '':
               symlist[subexpression.subexpressions[0].symbol[0]] = False 
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.
    print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'r')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print('Loading statement...')
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    negation = '(not '+ statement + ')'

    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    counter = [0]
    negation = read_expression(negation, counter)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print('\nChecking statement:',)
    print_expression(statement, '')
    print    

    # Run the statement through the inference engine
    tt_entails(knowledge_base, statement, negation, symlist)#divya

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)
