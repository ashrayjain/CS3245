class Operator(object):
    def __init__(self, val='Default', precedence=-1, associativity='left', nargs=0):
        self.val = val
        self.precedence = precedence
        self.associativity = associativity
        self.nargs = nargs

    def execute(self, args):
        pass

    def __eq__(self, other):
        return isinstance(other, Operator) and self.val == other.val

    def __str__(self):
        return self.val

class OROperator(Operator):
    def __init__(self):
        super(OROperator, self).__init__('OR', 1, 'left', 2)

    def execute(self, args):
        first = args[-2]
        second = args[-1]

        if first == None:
            return second
        elif second == None:
            return first

        #TODO
        return first

class ANDOperator(Operator):
    def __init__(self):
        super(ANDOperator, self).__init__('AND', 2, 'left', 2)

    def execute(self, args):
        first = args[-2]
        second = args[-1]

        if first == None or second == None:
            return None

        #TODO
        return first

class NOTOperator(Operator):
    def __init__(self):
        super(NOTOperator, self).__init__('NOT', 3, 'right', 1)

    def execute(self, args):
        first = args[-1]

        #TODO
        return None

class OpenBracketOperator(Operator):
    def __init__(self):
        super(OpenBracketOperator, self).__init__('(', -1, 'left', 0)

class DefaultOperator(Operator):
    def __init__(self):
        super(DefaultOperator, self).__init__('Default', -1, 'left', 0)

def to_op(token):
    if token == 'OR':
        return OROperator()
    elif token == 'AND':
        return ANDOperator()
    elif token == 'NOT':
        return NOTOperator()
    elif token == '(':
        return OpenBracketOperator()
 
    return DefaultOperator()

VALID_OPERATORS = [ ANDOperator(), OROperator(), NOTOperator() ]


