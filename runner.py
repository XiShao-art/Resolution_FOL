from Resolution import resolution
from preprocess import  sentence_parse
from utils import *
if __name__ == '__main__':

    fol_engine = FOL_Engine()
    KB=[]
    KB_size = int(input())
    for i in range(KB_size):
        root = sentence_parse(fol_engine, input())
        KB.extend(tree2KB(root))
    query = 'not '+input()
    query = sentence_parse(fol_engine, query)
    query = tree2KB(query)

    print(resolution(KB,query, 1000))

