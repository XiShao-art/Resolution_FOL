from FOL import *

def iterate_unify(p, key,dic):
    #print(p)
    for i in range(len(p.arguments)):
        if p.arguments[i].name ==key:
            p.arguments[i] = dic[key].copy()

        elif type(p.arguments[i]) == Function:
            iterate_unify(p.arguments[i], key, dic)

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
                #print('fun  fun', unify)
                if check_fun_fun(p1.arguments[i],p2.arguments[i]):
                    #print('in fun')
                    stack1 = p1.arguments[i].arguments.copy()
                    stack2 = p2.arguments[i].arguments.copy()
                    while(True):
                        #print(len(stack1))
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
                           # print(32)
                            stack1.extend(stack1.pop().arguments.copy())
                            stack2.extend(stack2.pop().arguments.copy())
                        else:
                            stack1.pop()
                            stack2.pop()






    if len(unify.keys())!=0:
        #print(1)
        p1 = p1.copy()
        p2 = p2.copy()
        key = list(unify.keys())[-1]
        print('before',p1, p2, unify.keys(), unify[list(unify.keys())[0]])
        iterate_unify(p1,key,unify)
        iterate_unify(p2, key, unify)
        print('after',p1, p2, unify.keys(), unify[list(unify.keys())[0]])

        allUni.update(unify)
        return MGU(p1,p2, allUni)
    elif not p1.equals(p2):
        #print(p1.equals(p2))
        #return None, {}
        p1 = None
        allUni = {}
        return p1, allUni
    else:
        return p1, allUni











def check_var_fun(v1:Variable, f1:Function):
    flag = True
    for para in f1.arguments:
        if type(para) ==Variable and v1.name ==para.name:
            return False
        elif type(para) ==Function:
            flag = flag and check_var_fun(v1, para)
    return flag

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
          #  elif (type(f2.arguments[i])==Constant and type(f1.arguments[i])==Function) or :
    return flag

p1 =    Predicate('p')
p2 =    Predicate('p')
x =     Variable('x')
y =     Variable('y')
z =     Variable('z')
a = Constant('a')
b = Constant('b')
g_x= Function('g_x')
g_y= Function('g_y')
g_z= Function('g_z')
h_x= Function('h_x')

g_x.arguments.append(x)
g_x.arguments.append(y)

g_z.arguments.append(z)


g_y.arguments.append(a)
g_y.arguments.append(y)

g_y.name ='g_x'

p1.arguments.append(y)
p1.arguments.append(g_x)
p2.arguments.append(b)
p2.arguments.append(g_y)



pre,dic = MGU(p1, p2, {})
print(pre, dic)





