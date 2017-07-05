from collections import namedtuple

def _paren(f):
    if not isinstance(f, Atom):
        return '({})'.format(f)
    else:
        return str(f)


class Formula:
    def __rshift__(self, other):
        return Implication(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    def __xor__(self, other):
        return Conjunction(self, other)

class Atom(Formula, namedtuple('Atom', 'formula')):
    def __str__(self):
        return str(self.formula)

class Implication(Formula, namedtuple('Implication', 'prem conc')):
    def __str__(self):
        return '{} → {}'.format(*map(_paren, (self.prem, self.conc)))

class Conjunction(Formula, namedtuple('Conjunction', 'left right')):
    def __str__(self):
        return '{} ∧ {}'.format(*map(_paren, (self.left, self.right)))

class Disjunction(Formula, namedtuple('Disjunction', 'left right')):
    def __str__(self):
        return '{} ∨ {}'.format(*map(_paren, (self.left, self.right)))

