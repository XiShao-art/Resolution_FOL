from preprocess import sentence_parse
from utils import *

'''
find if it have one avaliable unify and update the predicate
run until no avaliable unfiy can be find
'''
def MGU(p1:Predicate, p2:Predicate, allUni):
    unify = {}
    if len(p1.arguments) != len(p2.arguments):
        return None, unify
    else:

        for i in range(len(p1.arguments)):
            if type(p1.arguments[i])==Variable and type(p2.arguments[i])==Variable and p2.arguments[i].name !=p1.arguments[i].name:
                unify[p1.arguments[i].name] = p2.arguments[i].copy()
                break
            elif  type(p1.arguments[i])==Variable and type(p2.arguments[i])==Constant:
                unify[p1.arguments[i].name] = p2.arguments[i].copy()
                break
            elif  type(p1.arguments[i])==Constant and type(p2.arguments[i])==Variable:
                unify[p2.arguments[i].name] = p1.arguments[i].copy()
                break
            elif type(p1.arguments[i])==Variable and type(p2.arguments[i])==Function:
                if check_var_fun(p1.arguments[i],p2.arguments[i]):
                    unify[p1.arguments[i].name] = p2.arguments[i].copy()
                    break
            elif type(p1.arguments[i])==Function and type(p2.arguments[i])==Variable:
                if check_var_fun(p2.arguments[i], p1.arguments[i]):
                    unify[p2.arguments[i].name] = p1.arguments[i].copy()
                    break
            elif type(p1.arguments[i])==Function and type(p2.arguments[i])==Function:
                if check_fun_fun(p1.arguments[i],p2.arguments[i]):

                    stack1 = p1.arguments[i].arguments.copy()
                    stack2 = p2.arguments[i].arguments.copy()
                    while(True):

                        if(len(stack1)==0):
                            break
                        if type(stack1[-1])==Variable:
                            if stack1[-1].name != stack2[-1].name:
                                unify[stack1[-1].name] = stack2[-1].copy()
                                break
                            else:
                                stack1.pop()
                                stack2.pop()
                        elif type(stack2[-1]) == Variable:
                            if stack1[-1].name != stack2[-1].name:
                                unify[stack2[-1].name] = stack1[-1].copy()
                                break
                            else:
                                stack1.pop()
                                stack2.pop()
                        elif type(stack2[-1]) == Function and type(stack1[-1]) == Function:

                            stack1.extend(stack1.pop().arguments.copy())
                            stack2.extend(stack2.pop().arguments.copy())
                        else:
                            stack1.pop()
                            stack2.pop()






    if len(unify.keys())!=0:
        p1 = p1.copy()
        p2 = p2.copy()
        key = list(unify.keys())[-1]
        iterate_unify_pre(p1,key,unify)
        iterate_unify_pre(p2, key, unify)
        allUni.update(unify)
        return MGU(p1,p2, allUni)
    elif not p1.equals(p2):
        p1 = None
        allUni = {}
        return p1, allUni
    else:
        return p1, allUni


'''
if f1 contains v1, it can never unify,
check wether it have 
'''
def check_var_fun(v1:Variable, f1:Function):
    flag = True
    for para in f1.arguments:
        if type(para) ==Variable and v1.name ==para.name:
            return False
        elif type(para) ==Function:
            flag = flag and check_var_fun(v1, para)
    return flag

'''
first f1 and f2 should have same name
the arg crrospond func should not have the arg
like: f(g(x), y), f(x,y). It can never unify
'''
def check_fun_fun(f1:Function, f2:Function):
    flag = True
    if f1.name != f2.name:
        return False
    else:
        for i in range(len(f1.arguments)):
            if type(f1.arguments[i])==Function and type(f2.arguments[i])==Function:
                flag = flag and check_fun_fun(f1.arguments[i], f2.arguments[i])
            elif type(f1.arguments[i])==Variable and type(f2.arguments[i])==Function:
                flag = flag and check_var_fun(f1.arguments[i], f2.arguments[i])
            elif type(f2.arguments[i])==Variable and type(f1.arguments[i])==Function:
                flag = flag and check_var_fun(f2.arguments[i], f1.arguments[i])
    return flag

'''
some test cases
'''
if __name__ == '__main__':
    fol_engine = FOL_Engine()
    fol_engine.constants = ['a','b']#change if you want more constant
    fol_engine.functions = ['f','h','g']#change if you want more function
    print('input one predicate')
    p1 = input()
    p1 = sentence_parse(fol_engine, p1)
    p1 = tree2KB(p1)

    print('input another predicate')
    p2 = input()
    p2 = sentence_parse(fol_engine, p2)
    p2 = tree2KB(p2)

    pre,dic = MGU(p1[0][0], p2[0][0], {})
    print_unify(pre,dic)






