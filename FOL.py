
OPERATIONS = ['and', 'or', 'implies']
QUANTIFIES = ['exist', 'forAll']
VARIABLES = []
PREDICATES = []
FUNCTIONS = []
CONSTANTS = []

# VARIABLES_obj = []
# CONSTANTS_obj = []

for i in range(97, 109):
    CONSTANTS.append(str(chr(i)))# lowercase letters m to z

for i in range(109, 123):
    VARIABLES.append(str(chr(i)))  # lowercase letters a to l

for i in range(65, 77):
    FUNCTIONS.append(str(chr(i)))# uppercase letters

for i in range(77, 91):
    PREDICATES.append(str(chr(i)))# uppercase letters






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
        self.parent = None


    # def negated(self):
    #     if self.isOperation:
    #         if self.name == 'and':
    #             self.name = 'or'
    #             self.right.negated()
    #             self.left.negated()
    #         elif self.name == 'or':
    #             self.name = 'and'
    #             self.right.negated()
    #             self.left.negated()
    #         elif self.name == 'implies':
    #             self.name = 'and'
    #             self.right.negated()
    #
    #     else :
    #         self.negation = not self.negation

    def __str__(self):
        return self.name

class Operation(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = True


class Predicate(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.arguments = []
        self.isOperation = False
    def __str__(self):
        s='[ '
        for i in self.arguments:
            s+=str(i)+' '
        if self.negation:
            return '-'+self.name+' '+s+']'
        else:
            return self.name + ' ' + s + ']'

class Function(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.arguments = []
        self.isOperation = False
    def __str__(self):
        s='[ '
        for i in self.arguments:
            s+=str(i)+' '
        return self.name+' '+s+']'

class Constant(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False

class Variable(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False
        self.scope = []

    # def __str__(self):
    #     s=''
    #     for i in self.scope:
    #         s+=i.name+','
    #     return self.name+  '('+s+') '

class FOL_Engine:
    def __init__(self):
        self.operations = OPERATIONS
        self.variables =  VARIABLES
        self.predicates = PREDICATES
        self.quantifies = QUANTIFIES
        self.constants = CONSTANTS
        self.functions = FUNCTIONS






   #  a = ['a','b','a']
   #
   #  print(a)
   #  fol_engine = FOL_Engine()
   # # for i in sentence_parse(fol_engine,input()):




