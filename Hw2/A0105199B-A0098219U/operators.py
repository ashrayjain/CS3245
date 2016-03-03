class Operator:
    def __init__(self, ival):
        self.val = ival
        self.associativity = 'left'
 
        if ival == 'OR':
            self.precedence = 1
        elif ival == 'AND':
            self.precedence = 2
        elif ival == 'NOT':
            self.precedence = 3
            self.associativity = 'right'
        else:
            self.precedence = -1

    def __eq__(self, other):
        return isinstance(other, Operator) and self.val == other.val

    def __str__(self):
        return self.val

VALID_OPERATORS = [ Operator('AND'), Operator('OR'), Operator('NOT') ]


