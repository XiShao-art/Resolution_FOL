# class Predicate:
#     def __init__(self, name: str, arguments: [], positive: bool):
#         self.name = name
#         self.arguments = arguments
#         self.positive = positive
#
#     def get(self,z ):
#         s = self.name+ str(self.arguments)
#         if not self.positive:
#             s='~' + s
#
#         return s

'''
This is class for the quantity:
for all, exists
'''
OPERATIONS = ['and', 'or', 'implies']
QUANTIFIES = ['exist', 'forAll']
VARIABLES = []
PREDICATES = []
CONSTANTS = []

for i in range(97, 109):
    CONSTANTS.append(str(chr(i)))# lowercase letters m to z

for i in range(109, 123):
    VARIABLES.append(str(chr(i)))  # lowercase letters a to l

for i in range(65, 91):
    PREDICATES.append(str(chr(i)))# uppercase letters

def listPrinter(sentence):
    for  i in sentence:
        print(i, end =  ' ')
class Quantity:
    def __init__(self, variable: str, index):
        self.forAll = True
        self.variable = variable
        self.index = str(index) # the variable and qunaity may be the same, but not the same scope: exists x(x=1) & exists x(x=2)
        self.name = variable+'_'+self.index
class Node:
    def __init__(self, Name: str):
        self.isOperation = True  #the flag to judge if it is operation (implies: =>, and:& ...)
        self.name = Name
        self.negation = False
        self.left = None  # if it is operation Node
        self.right = None


    def negated(self):
        if self.isOperation:
            if self.name == 'and':
                self.name = 'or'
                self.right.negated()
                self.left.negated()
            elif self.name == 'or':
                self.name = 'and'
                self.right.negated()
                self.left.negated()
            elif self.name == 'implies':
                self.name = 'and'
                self.right.negated()

        else :
            self.negation = not self.negation

    def __str__(self):
        return self.name

class operation(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = True


class Predicate(Node):
    def __init__(self, Name:str, arguments):
        Node.__init__(self, Name)
        self.arguments = arguments
        self.isOperation = False

class Constant(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False

class Variable(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False
        self.scope = []

    def __str__(self):
        return 'var'+' '+self.name+  ' '+str(self.scope)

class FOL_Engine:
    def __init__(self):
        self.operations = OPERATIONS
        self.variables =  VARIABLES
        self.predicates = PREDICATES
        self.quantifies = QUANTIFIES
        self.constants = CONSTANTS

def removeImplies(sentence):
    while('implies' in sentence):

        for i in range(len(sentence)):
            if sentence[i]=='implies':
                sentence[i] = 'or'
                sentence.insert(i+2, 'not')
    return sentence

def pushNegation(sentence, fol_engine):
    allNegationForward = False
    while(not allNegationForward):

        allNegationForward = True
        not_index = 0
        new_sentence = []
        for i in range(len(sentence)):
            if sentence[i] == 'not' and sentence[i+1] not in fol_engine.predicates:

                allNegationForward = False
                not_index = i
                break
            new_sentence.append(sentence[i])

        old_sentence_index = not_index+1
        if (not allNegationForward ):
            while old_sentence_index<len(sentence):

                if sentence[old_sentence_index] == 'exist':
                    new_sentence.append('forAll')
                    new_sentence.append(sentence[old_sentence_index+1])
                    new_sentence.append('not')
                    old_sentence_index+=2
                elif sentence[old_sentence_index] == 'forAll':
                    new_sentence.append('exist')
                    new_sentence.append(sentence[old_sentence_index + 1])
                    new_sentence.append('not')
                    old_sentence_index += 2

                elif sentence[old_sentence_index] == 'not':
                    old_sentence_index+=1
                elif sentence[old_sentence_index] =='and':
                    new_sentence.append('or')
                    new_sentence.append('(')
                    old_sentence_index+=2
                    new_sentence.append('not')
                    countOperation = 1
                    while sentence[old_sentence_index]!=',' or countOperation!=1:
                        if sentence[old_sentence_index] in fol_engine.operations:
                            countOperation+=1
                        if sentence[old_sentence_index] == ',':
                            countOperation-=1
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(',')
                    old_sentence_index += 1
                    new_sentence.append('not')
                elif sentence[old_sentence_index] =='or':
                    new_sentence.append('and')
                    new_sentence.append('(')
                    old_sentence_index+= 2
                    new_sentence.append('not')
                    countOperation = 1
                    while sentence[old_sentence_index]!=',' or countOperation!=1:
                        if sentence[old_sentence_index] in fol_engine.operations:
                            countOperation+=1
                        if sentence[old_sentence_index] == ',':
                            countOperation-=1
                        new_sentence.append(sentence[old_sentence_index])
                        old_sentence_index += 1
                    new_sentence.append(',')
                    old_sentence_index += 1
                    new_sentence.append('not')
                while old_sentence_index < len(sentence):
                    new_sentence.append(sentence[old_sentence_index])
                    old_sentence_index += 1
            sentence = new_sentence
            listPrinter((sentence))
            print()




    return sentence


def defineScope(sentence):
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
            # Todo： the '(' may be not find
            for index in range(left_range, len(sentence)):
                if leftbracket > 0:

                    if type(sentence[index]) == Variable:
                        quantify = Quantity(sentence[quantify_index + 1], quantify_index + 1)
                        if sentence[index] == 'exist':
                            quantify.forAll = False
                        sentence[index].scope.append(quantify)
                    elif sentence[index] == '(':
                        leftbracket += 1
                    elif sentence[index] == ')':
                        leftbracket -= 1

                else:
                    break
    return sentence

def sentence_parse(fol_engine: FOL_Engine, sentence: str) :
    sentence = sentence.split()

    sentence = removeImplies(sentence)

    sentence = pushNegation(sentence, fol_engine)
    listPrinter(sentence)


    # change constant and varaiable to node
    for i in range(len(sentence)):
        if sentence[i] in fol_engine.constants:
            sentence[i] = Constant(sentence[i])
        elif sentence[i] in fol_engine.variables and sentence[i-1] not in fol_engine.quantifies:
            sentence[i] = Variable(sentence[i])


    sentence = defineScope(sentence)




    return sentence


if __name__ == '__main__':

    fol_engine = FOL_Engine()
    for i in sentence_parse(fol_engine,input()):
       # print(i)
        pass

   #  a = ['a','b','a']
   #
   #  print(a)
   #  fol_engine = FOL_Engine()
   # # for i in sentence_parse(fol_engine,input()):
   #  a = Variable(1)
   #  print(type(a) == Variable)



