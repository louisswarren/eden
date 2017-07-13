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

class univelim(Argstore):
    order = 1
    opts = 0 # Option is optional
    constructor = UniversalElim

class univintr(Argstore):
    order = 1
    opts = 0 # Options are optional
    constructor = UniversalIntro

class exiselim(Argstore):
    order = 2
    opts = 0 # Options are optional
    constructor = ExistentialElim

class exisintr(Argstore):
    order = 1
    opts = 0 # Options are optional
    constructor = ExistentialIntro

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
print()

Px = Predicate('P', 'x')
print(parse(
    Universal('x', Px),
    univelim('y'),
    univintr(),
))
print()

Pt = Predicate('P', 't')
print(parse(
    Existential('x', Px),
                Universal('x', Px >> A),
                univelim('t'),
                                Pt,
                    implelim(),
            exiselim('t'),
))
print()

print(parse(
    Pt,
    exisintr('t', 'x'),
))
