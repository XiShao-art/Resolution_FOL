from  FOL import  Variable, Constant

def listPrinter(sentence):
    for  i in sentence:
        print(i, end =  ' ')

def tree_print(root):
    stack = []
    stack.append(root)
    while len(stack) != 0:
        temp = stack.pop()
        if type(temp) !=Variable and type(temp) !=Constant:
            if temp.left != None:
                stack.append(temp.left)

            if temp.right != None:
                stack.append(temp.right)
                print(temp.name+' '+str(temp.left)+' '+str(temp.right))
            elif len(temp.arguments) != 0:
                for arg in temp.arguments:
                    stack.append(arg)
                print(temp.name, end=' ')
                listPrinter(temp.arguments)
                print()
