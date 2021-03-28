from FOL import *
from preprocess import *
def convert2CNF(root):
    if type(root)!= Operation or root ==None:
        return

    if root.name == 'or':
        if root.left.name == 'and':
            andTerm = root.left
            temp = root.right
            newLeft = Operation('or')
            newRight = Operation('or')

            newLeft.left = andTerm.left
            newLeft.right = temp

            newRight.left = andTerm.right
            newRight.right = temp

            root.left = newLeft
            root.right = newRight
            root.name = 'and'

        elif root.right.name == 'and':
            andTerm = root.right
            temp = root.left

            newLeft = Operation('or')
            newRight = Operation('or')

            newLeft.left = andTerm.left
            newLeft.right =temp

            newRight.left = andTerm.right
            newRight.right = temp

            root.left = newLeft
            root.right = newRight
            root.name = 'and'
    convert2CNF(root.left)
    convert2CNF(root.right)

if __name__ == '__main__' :
    sentence = input()
    fol_engine = FOL_Engine()
    root = sentence_parse(fol_engine, sentence)
    KB=tree2KB(root)
    for i in KB:
        listPrinter(i)

