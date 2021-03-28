from random import random
from CNF import *
from utils import *

def removeImplies(sentence):
    while ('implies' in sentence):

        for i in range(len(sentence)):
            if sentence[i] == 'implies':
                sentence[i] = 'or'
                sentence.insert(i + 2, 'not')

    return sentence


def pushNegation(sentence, fol_engine):
    allNegationForward = False
    while (not allNegationForward):

        allNegationForward = True
        not_index = 0
        new_sentence = []
        for i in range(len(sentence)):
            if sentence[i] == 'not' and sentence[i + 1] not in fol_engine.predicates:
                allNegationForward = False
                not_index = i
                break
            new_sentence.append(sentence[i])

        old_sentence_index = not_index + 1
        if (not allNegationForward):

            while old_sentence_index < len(sentence):

                if sentence[old_sentence_index] == 'exist':
                    new_sentence.append('forAll')
                    new_sentence.append(sentence[old_sentence_index + 1])
                    new_sentence.append('not')
                    old_sentence_index += 2
                elif sentence[old_sentence_index] == 'forAll':
                    new_sentence.append('exist')
                    new_sentence.append(sentence[old_sentence_index + 1])
                    new_sentence.append('not')
                    old_sentence_index += 2
                elif sentence[old_sentence_index] == '(':
                    new_sentence.append('(')
                    new_sentence.append('not')
                    old_sentence_index += 1

                elif sentence[old_sentence_index] == 'not':
                    old_sentence_index += 1
                elif sentence[old_sentence_index] == 'and':
                    new_sentence.append('or')
                    new_sentence.append('(')
                    old_sentence_index += 2
                    new_sentence.append('not')
                    while sentence[old_sentence_index] != '(':
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(sentence[old_sentence_index])
                    old_sentence_index += 1

                    countOperation = 1
                    while countOperation != 0:
                        if sentence[old_sentence_index] == '(':
                            countOperation += 1
                        if sentence[old_sentence_index] == ')':
                            countOperation -= 1
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(',')
                    old_sentence_index += 1
                    new_sentence.append('not')

                elif sentence[old_sentence_index] == 'or':
                    new_sentence.append('and')
                    new_sentence.append('(')
                    old_sentence_index += 2
                    new_sentence.append('not')
                    while sentence[old_sentence_index] != '(':
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(sentence[old_sentence_index])
                    old_sentence_index += 1

                    countOperation = 1
                    while countOperation != 0:
                        if sentence[old_sentence_index] == '(':
                            countOperation += 1
                        if sentence[old_sentence_index] == ')':
                            countOperation -= 1
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(',')
                    old_sentence_index += 1
                    new_sentence.append('not')

                while old_sentence_index < len(sentence):
                    new_sentence.append(sentence[old_sentence_index])
                    old_sentence_index += 1

            sentence = new_sentence

    return sentence


def defineScope(sentence, fol_engine):
    while ' ' in sentence:
        sentence.remove(' ')
    # define the scope of all variable
    for quantify_index in range(len(sentence)):
        if sentence[quantify_index] in fol_engine.quantifies:

            # find the first '('
            index = 0
            leftbracket = 0
            for i in range(quantify_index + 2, len(sentence)):

                if sentence[i] == '(':
                    leftbracket = 1
                    index = i
                    break

            left_range = index + 1
            for index in range(left_range, len(sentence)):
                if leftbracket > 0:

                    if type(sentence[index]) == Variable:
                        quantify = Quantity(sentence[quantify_index + 1], quantify_index + 1)
                        if sentence[quantify_index] == 'exist':
                            quantify.forAll = False
                        sentence[index].scope.append(quantify)
                        if sentence[index].name == quantify.variable:
                            sentence[index].name = quantify.name
                    elif sentence[index] == '(':
                        leftbracket += 1
                    elif sentence[index] == ')':
                        leftbracket -= 1

                else:
                    break

    # remove quntity
    for i in range(len(sentence)):
        if sentence[i] in fol_engine.quantifies:
            sentence[i] = ' '
            sentence[i + 1] = ' '
    while ' ' in sentence:
        sentence.remove(' ')
    return sentence


def VarConst2Node(sentence, fol_engine):
    for i in range(len(sentence)):
        if sentence[i] in fol_engine.constants:
            sentence[i] = Constant(sentence[i])
        elif sentence[i] in fol_engine.variables and sentence[i - 1] not in fol_engine.quantifies:
            sentence[i] = Variable(sentence[i])
        elif sentence[i] in fol_engine.predicates:
            sentence[i] = Predicate(sentence[i])
            if i > 0 and sentence[i - 1] == 'not':
                sentence[i].negation = True
                sentence[i - 1] = ' '
    return sentence


def All2Node(sentence, fol_engine):
    for i in range(len(sentence)):
        if sentence[i] in fol_engine.operations:
            sentence[i] = Operation(sentence[i])
        elif sentence[i] in fol_engine.predicates:
            sentence[i] = Predicate(sentence[i])
        elif sentence[i] in fol_engine.functions:
            sentence[i] = Function(sentence[i])
        elif type(sentence[i]) == str:

            assert sentence[i] == '(' or sentence[i] == ')' or sentence[i] == ',', 'undefined symbol'
    # convert all predicet to node
    stack = []
    for ele in sentence:

        if ele != ')':
            stack.append(ele)
        elif ele == ')':
            tempStack = []
            while stack[-1] != '(':
                if stack[-1] != ',':
                    tempStack.append(stack.pop())
                else:
                    stack.pop()
            stack.pop()
            if len(stack) != 0:
                if type(stack[-1]) == Function or type(stack[-1]) == Predicate:
                    tempStack.reverse()
                    stack[-1].arguments = tempStack
                    for arg in stack[-1].arguments:
                        arg.parent = stack[-1]

                elif type(stack[-1]) == Operation:
                    tempStack.reverse()
                    stack[-1].left = tempStack[0]
                    stack[-1].right = tempStack[1]
                    stack[-1].left.parent = stack[-1]
                    stack[-1].right.parent = stack[-1]

                else:
                    while len(tempStack) != 0:
                        stack.append(tempStack.pop())
            else:
                while len(tempStack) != 0:
                    stack.append(tempStack.pop())
    return stack[0]


def skolemization(root, fol_engine):
    stack = []
    stack.append(root)
    while len(stack) != 0:
        temp = stack.pop()
        if type(temp) != Variable and type(temp) != Constant:
            if temp.left != None:
                stack.append(temp.left)
            if temp.right != None:
                stack.append(temp.right)
            elif len(temp.arguments) != 0:

                for arg in temp.arguments:
                    stack.append(arg)
        elif type(temp) == Variable:
            exist = 0
            const_index = 0
            forAllList = []
            for quantity in temp.scope:

                if quantity.name != temp.name and quantity.forAll:
                    var = Variable(quantity.name)
                    forAllList.append(var)
                elif quantity.name == temp.name and quantity.forAll:
                    exist = 2
                    break
                elif quantity.name == temp.name and not quantity.forAll:
                    exist = 1
                    const_index = quantity.index
                    break

            if exist == 0:
                pass
            elif exist == 2:  # no exist, no need to change
                pass
            elif exist == 1:
                if len(forAllList) == 0:
                    const = Constant(fol_engine.constants[int(const_index) % len(fol_engine.constants)])

                    parent = temp.parent
                    if type(parent) == Operation:
                        if parent.left.name == temp.name:
                            parent.left = const
                        else:
                            parent.right = const
                    else:
                        for arg_index in range(len(parent.arguments)):
                            if parent.arguments[arg_index].name == temp.name:
                                parent.arguments[arg_index] = const
                else:

                    func = Function('F_' + str(int(random()*10000)%20))
                    for var in forAllList:
                        var.parent = func
                        func.arguments.append(var)
                    parent = temp.parent
                    if type(parent) == Operation:
                        if parent.left.name == temp.name:
                            parent.left = func
                        else:
                            parent.right = func
                    else:
                        for arg_index in range(len(parent.arguments)):
                            if parent.arguments[arg_index].name == temp.name:
                                parent.arguments[arg_index] = func
    return root


def sentence_parse(fol_engine: FOL_Engine, sentence: str):
    sentence = sentence.split()

    sentence = removeImplies(sentence)

    sentence = pushNegation(sentence, fol_engine)

    sentence = VarConst2Node(sentence, fol_engine)  # change constant and varaiable to node

    sentence = defineScope(sentence, fol_engine)

    rootNode = All2Node(sentence, fol_engine)

    skolemization(rootNode, fol_engine)

    convert2CNF(rootNode)

    return rootNode
