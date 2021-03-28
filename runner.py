from Resolution import resolution
from preprocess import  sentence_parse
from utils import *
if __name__ == '__main__':
    fol_engine = FOL_Engine()

    print('if you want to define sigma structure enter 1, otherwise enter any key')

    mode = input()

    if mode == '1':
        print('enter predicate, press \'end\' to end')
        PREDICATES_input = []
        while (True):
            temp = input()
            if temp == 'end':
                break
            PREDICATES_input.append(temp)

        print('enter function, press \'end\' to end')
        FUNCTIONS_input = []
        while (True):
            temp = input()
            if temp == 'end':
                break
            FUNCTIONS_input.append(temp)

        print('enter variable, press \'end\' to end')
        VARIABLES_input = []
        while (True):
            temp = input()
            if temp == 'end':
                break
            VARIABLES_input.append(temp)

        print('enter constant, press \'end\' to end')
        CONSTANTS_input = []
        while (True):
            temp = input()
            if temp == 'end':
                break
            CONSTANTS_input.append(temp)

        fol_engine.predicates = PREDICATES_input
        fol_engine.functions = FUNCTIONS_input
        fol_engine.variables = VARIABLES_input
        fol_engine.constants = CONSTANTS_input

    KB=[]
    print('input KB size:')
    KB_size = int(input())
    for i in range(KB_size):
        print('input sentence:')
        root = sentence_parse(fol_engine, input())
        KB.extend(tree2KB(root))
    print('input query:')
    query = 'not '+input()
    query = sentence_parse(fol_engine, query)
    query = tree2KB(query)

    print(resolution(KB,query, 100))

