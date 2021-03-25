
from MGU import *
from utils import *
def xor(p1,p2):
    return (p1.negation and not p2.negation) or (not p1.negation and p2.negation)

def resolve2sentences(sentence, kb_sentence):
    sentence = sentence.copy()
    kb_sentence = kb_sentence.copy()
    for sen_index in range(len(sentence)):
        for kbsen_index in range(len(kb_sentence)):
            if xor(sentence[sen_index], kb_sentence[kbsen_index]):
                if sentence[sen_index].equals(kb_sentence[kbsen_index]) :
                    sentence.remove(sentence[sen_index])
                    kb_sentence.remove(kb_sentence[kbsen_index])
                    sentence.extend(kb_sentence)
                    return(sentence)
                else:
                    pre, dic = MGU(sentence[sen_index],kb_sentence[kbsen_index],{})
                    if pre!=None:
                        sentence = iterate_unify_sentence(sentence, dic)
                        kb_sentence = iterate_unify_sentence(kb_sentence, dic)
                        sentence.remove(sentence[sen_index])
                        kb_sentence.remove(kb_sentence[kbsen_index])
                        sentence.extend(kb_sentence)
                        return (sentence)

    return None

def resolve(sentence, KB):
    resolve_set = []
    for kb_sentence in KB:
        #print(sentence[0], kb_sentence[0])
        result = resolve2sentences(sentence, kb_sentence)
        #listPrinter(result)

        if result!=None:
            resolve_set.append(result)
    return resolve_set

#query is 2d array, should be negation in advanced
def resolution(KB, querys, max_loops):
    querys_set =[]
    querys_set.extend(querys)
    KB.extend(querys)
    for _ in range(max_loops):
        if len(querys_set)==0:
            break
        sentence = querys_set[0]
        print('sentence', end=' ')
        listPrinter(sentence)
        print( 'before')
        for i in KB:
            listPrinter(i)
        querys_set.remove(querys_set[0])
        resolve_set =resolve(sentence, KB)
        if [] in resolve_set:
            return True
        else:
            querys_set.extend(resolve_set)
            KB.extend(resolve_set)
        print('after')
        for i in KB:
            listPrinter(i)

    return False


if __name__ =='__main__':
    KB = []
    querys=[]
    x = Variable('x')
    y = Variable('y')
    a = Constant('a')
    b = Constant('b')
    p1 = Predicate('p1')
    p1.negation=True
    p1.arguments.append(a)

    p2 = Predicate('p2')
    p2.negation = True
    p2.arguments.append(x)

    p3 = Predicate('p1')
    p3.negation = False
    p3.arguments.append(x)

    p4 = Predicate('p2')
    p4.negation = True
    p4.arguments.append(x)

    p5 = Predicate('p2')
    p5.negation = False
    p5.arguments.append(b)



    KB.append([p1,p2])
    KB.append([p3, p4])
    querys.append([p5])

    print(resolution(KB,querys,10000))

