'''Provide a stacking interface for Eden.'''

from collections import namedtuple

from eden import *

class Argstore:
    opts = None
    def __init__(self, *args):
        assert(len(args) >= self.__class__.opts)
        self.args = args

class implelim(Argstore):
    order = 2
    opts = 0
    constructor = ImplicationElim

class implintr(Argstore):
    order = 1
    opts = 0 # Option is optional
    constructor = ImplicationIntro

class conjelim(Argstore):
    order = 2
    opts = 0
    constructor = ConjunctionElim

class conjintr(Argstore):
    order = 2
    opts = 0
    constructor = ConjunctionIntro

class disjelim(Argstore):
    order = 3
    opts = 0
    constructor = DisjunctionElim

class disjintr(Argstore):
    order = 1
    opts = 1
    constructor = DisjunctionIntro


def parse(*seq):
    stack = []
    for val in seq:
        if isinstance(val, Argstore):
            if isinstance(val, implintr) and not val.args:
                val.args = (next(iter(stack[-1].open)), )
            branches = reversed(tuple(stack.pop() for _ in range(val.order)))
            stack.append(val.constructor(*branches, *val.args))
        elif isinstance(val, Formula):
            stack.append(Assumption(val))
        else:
            stack.append(val)
    assert(len(stack) == 1)
    return stack.pop()

# Examples

A, B, C = Atom('A'), Atom('B'), Atom('C')

print(parse(
    A >> (B >> C),      A,
           implelim(),                  B,
                          implelim(),
                          implintr(A),
                          implintr(B),
                          implintr(),
))
