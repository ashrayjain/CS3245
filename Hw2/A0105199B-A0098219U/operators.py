class Operator(object):
    def __init__(self, val='Default', precedence=-1, associativity='left'):
        self.val = val
        self.precedence = precedence
        self.associativity = associativity

    def execute(self, args):
        pass

    def __eq__(self, other):
        return isinstance(other, Operator) and self.val == other.val

    def __str__(self):
        return self.val

class OROperator(Operator):
    def __init__(self):
        super(OROperator, self).__init__('OR', 1, 'left')

    def execute(self, args):
        first = args[-2]
        second = args[-1]

        args = args[:-2] + ['resultOr']

        return args

class ANDOperator(Operator):
    def __init__(self):
        super(ANDOperator, self).__init__('AND', 2, 'left')

    def execute(self, args):
        first = args[-2]
        second = args[-1]

        args = args[:-2] + ['resultAnd']

        return args

class NOTOperator(Operator):
    def __init__(self):
        super(NOTOperator, self).__init__('NOT', 3, 'right')

    def execute(self, args):
        first = args[-2]

        args = args[:-1] + ['resultNot']

        return args

class OpenBracketOperator(Operator):
    def __init__(self):
        super(OpenBracketOperator, self).__init__('(', -1, 'left')

class DefaultOperator(Operator):
    def __init__(self):
        super(DefaultOperator, self).__init__('Default', -1, 'left')

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


