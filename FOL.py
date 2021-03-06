OPERATIONS = ['and', 'or', 'implies']
QUANTIFIES = ['exist', 'forAll']
VARIABLES = []
PREDICATES = []
FUNCTIONS = []
CONSTANTS = []

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

    def __str__(self):
        return self.name

class Operation(Node,object):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = True
    def copy(self):
        v1 = Operation(self.name)

        return v1

    def equals(self,v):
        return v.name ==self.name

class Predicate(Node,object):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.arguments = []
        self.isOperation = False
    def copy(self):
        v1 = Predicate(self.name)
        v1.arguments = []
        v1.negation = self.negation
        for arg in self.arguments:
            v1.arguments.append(arg.copy())
        return v1

    def equals(self,v):
        flag = v.name == self.name
        for arg_index in range(len(self.arguments)):
            flag = flag and self.arguments[arg_index].equals(v.arguments[arg_index])
        return flag

    def __str__(self):
        s='( '
        for i in self.arguments:

            s+=str(i)+' '
        if self.negation:
            return '-'+self.name+' '+s+')'
        else:
            return self.name + ' ' + s + ')'

class Function(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.arguments = []
        self.isOperation = False
    def __str__(self):
        s='( '
        for i in self.arguments:
            s+=str(i)+' '
        return self.name+' '+s+')'

    def copy(self):
        v1 = Function(self.name)
        v1.arguments = []
        for arg in self.arguments:
            v1.arguments.append(arg.copy())
        return v1

    def equals(self,v):
        flag = v.name == self.name
        for arg_index in range(len(self.arguments)):
            flag = flag and self.arguments[arg_index].equals(v.arguments[arg_index])
        return flag

class Constant(Node):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False
    def copy(self):
        v1 = Constant(self.name)
        return v1
    def equals(self,v):
        return v.name ==self.name

class Variable(Node,object):
    def __init__(self, Name:str):
        Node.__init__(self, Name)
        self.isOperation = False
        self.scope = []
    def copy(self):
        v1 = Variable(self.name)
        return v1
    def equals(self,v):
        return v.name ==self.name

class FOL_Engine:
    def __init__(self):
        self.operations = OPERATIONS
        self.quantifies = QUANTIFIES
        self.variables = VARIABLES
        self.predicates = PREDICATES
        self.constants = CONSTANTS
        self.functions = FUNCTIONS




