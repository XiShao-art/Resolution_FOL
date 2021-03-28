from  FOL import  *
def remove_or_redundance(sentence):
    for i in range(len(sentence)-1):
        for j in range(i+1, len(sentence)):
            if sentence[i]!=None and sentence[i].equals(sentence[j]) :
                if sentence[i].negation == sentence[j].negation:
                    sentence[j] =None

    while None in sentence:
        sentence.remove(None)

def print_unify(p1,dic):
    if p1 == None:
        print("no unifiable")
        return
    print(p1, end = ' , ')
    keys = list(dic.keys())
    for key in keys:
        print(key,'=>',dic[key], end = "; ")
    print()

def listPrinter(sentence):
    for  i in sentence:
        print(i, end =  ' ')
    print()

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

def iterate_unify_pre(p, key, dic):
    for i in range(len(p.arguments)):
        if p.arguments[i].name ==key:
            p.arguments[i] = dic[key].copy()

        elif type(p.arguments[i]) == Function:
            iterate_unify_pre(p.arguments[i], key, dic)

def iterate_unify_sentence(sentence, dic):
    sentence = sentence.copy()
    for sen in range(len(sentence)):
        sentence[sen] = sentence[sen].copy()
    keys = list(dic.keys())
    for p in sentence:
        for key in keys:
            iterate_unify_pre(p, key, dic)
    return sentence

def or2sentence(root):
    sentence = []
    stack = []
    stack.append(root)
    while len(stack) != 0:
        temp = stack.pop()
        if temp.name == 'or':
            if type(temp.left) != Operation:
                sentence.append(temp.left)
            else:
                stack.append(temp.left)

            if type(temp.right) != Operation:
                sentence.append(temp.right)
            else:
                stack.append(temp.right)
    return sentence

def getKey(p):
    return p.name

def tree2KB(root):
    KB = []
    stack = []
    stack.append(root)
    while len(stack) != 0:
        temp = stack.pop()
        if temp.name=='and':
            if type(temp.left)!= Operation and not ifContains(KB, [temp.left]):
                KB.append([temp.left])
            else:
                stack.append(temp.left)

            if type(temp.right) != Operation and not ifContains(KB, [temp.right]):
                KB.append([temp.right])
            else:
                stack.append(temp.right)
        elif temp.name=='or':
            sentence = or2sentence(temp)
            sentence.sort(key=getKey)
            remove_or_redundance(sentence)
            if not  ifContains(KB, sentence):

                KB.append(sentence)
        else:
            if not ifContains(KB, [temp]):
                KB.append([temp])

    for i in KB:
        remove_or_redundance(i)
    return KB

def ifContains(KB, sentence):
    for kbsen in KB:
        flag = True
        if len(kbsen)==len(sentence):
            for i in range(len(kbsen)):
                flag = flag and kbsen[i].equals(sentence[i]) and kbsen[i].negation ==sentence[i].negation
            if flag:
                return True
    return False


