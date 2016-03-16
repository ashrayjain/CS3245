from math import log10

from collections import deque
from operators import to_op, VALID_OPERATORS

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

STEMMER = PorterStemmer()


def get_reverse_polish(expr):
    op_stack = []
    out_queue = deque([])

    expr = expr.replace('(', '( ')
    expr = expr.replace(')', ' )')

    for token in expr.strip().split():
        op = to_op(token)

        if op in VALID_OPERATORS:
            while op_stack and \
                ((op_stack[-1].associativity == 'left' and
                    op_stack[-1].precedence >= op.precedence) or
                    (op_stack[-1].associativity == 'right' and
                        op_stack[-1].precedence > op.precedence)):
                out_queue.append(op_stack.pop())
            op_stack.append(op)
        elif token == '(':
            op_stack.append(to_op(token))
        elif token == ')':
            while op_stack[-1].val != '(':
                out_queue.append(op_stack.pop())
            op_stack.pop()
        else:
            out_queue.append(preprocess_token(token))

    while op_stack:
        out_queue.append(op_stack.pop())

    return out_queue


def preprocess_token(token):
    return STEMMER.stem(token).lower()


def preprocess_text(text):
    v = {}
    for w in word_tokenize(text):
        word = STEMMER.stem(w).lower()
        v[word] = v.get(word, 0) + 1
    return v

def tf(val):
    if val > 0:
        return 1 + log10(val)
    return 0


def idf(val, n):
    if val == 0:
        return 0
    return log10(1.0 * n / val)


if __name__ == '__main__':
    q = 'bill OR Gates AND (vista OR XP) AND NOT mac'
    print str([str(x) for x in get_reverse_polish(q)])
