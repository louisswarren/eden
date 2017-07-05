'''Provide a methodic interface for Eden.'''

from eden import *

def Formula_implintr(self, *args, **kwargs):
    return Assumption(self).implintr(*args, **kwargs)

def Formula_disjintr(self, *args, **kwargs):
    return Assumption(self).disjintr(*args, **kwargs)

def Tree_implintr(self, prem_formula=None):
    if not prem_formula:
        prem_formula = next(iter(self.open))
    return ImplicationIntro(self, prem_formula)

def Tree_disjintr(self, weak_formula):
    return DisjunctionIntro(self, weak_formula)

Formula.implintr = Formula_implintr
Formula.disjintr = Formula_disjintr
Tree.implintr = Tree_implintr
Tree.disjintr = Tree_disjintr


def assumise(*args):
    for arg in args:
        if isinstance(arg, Formula):
            yield Assumption(arg)
        else:
            yield arg

class Forest(list):
    def implelim(self):
        return ImplicationElim(*assumise(*self))

    def conjelim(self):
        return ConjunctionElim(*assumise(*self))

    def conjintr(self):
        return ConjunctionIntro(*assumise(*self))

    def disjelim(self):
        return DisjunctionElim(*assumise(*self))

def F(*b):
    return Forest(b)


# Examples

A, B, C = Atom('A'), Atom('B'), Atom('C')

pf = (
F(
F(       A >> (B >> C),      A                                                 )
                .implelim(),                      B                            )
                                .implelim()
                                .implintr(A)
                                .implintr(B)
                                .implintr()
)
print(pf)
assert(pf.is_closed())




print(
        A
    .disjintr(B)
)
print()

print(
F(    A | B,
F(                 A >> C,      A                                              )
                       .implelim(),
F(                                        B >> C,     B                        )
                                            .implelim()                        )
                       .disjelim()
)
print()


print(
F(    A,       B                                                               )
      .conjintr()
)
print()


print(
F(        A ^ B,
F(F(                             A >> (B >> C),         A                      )
                                           .implelim()                         ,
                                                               B               )
                                                  .implelim()                  )
                   .conjelim()
)
print()
