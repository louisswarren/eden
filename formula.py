from collections import namedtuple

def _paren(f):
    if not isinstance(f, (Atom, Predicate, Universal, Existential)):
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


class Atom(Formula, namedtuple('Atom', 'name')):
    def __str__(self):
        return str(self.name)

    def free_terms(self):
        return frozenset()

    def term_sub(self, old, new):
        return self


class Predicate(Formula, namedtuple('Predicate', 'name term')):
    def __str__(self):
        return str(self.name) + str(self.term)

    def free_terms(self):
        return frozenset((self.term, ))

    def term_sub(self, old, new):
        if self.term == old:
            return Predicate(self.name, new)
        else:
            return self

class Implication(Formula, namedtuple('Implication', 'prem conc')):
    def __str__(self):
        return '{} → {}'.format(*map(_paren, (self.prem, self.conc)))

    def free_terms(self):
        return self.prem.free_terms() | self.conc.free_terms()

    def term_sub(self, old, new):
        return Implication(self.prem.term_sub(old, new),
                           self.conc.term_sub(old, new))


class Conjunction(Formula, namedtuple('Conjunction', 'left right')):
    def __str__(self):
        return '{} ∧ {}'.format(*map(_paren, (self.left, self.right)))

    def free_terms(self):
        return self.left.free_terms() | self.right.free_terms()

    def term_sub(self, old, new):
        return Conjunction(self.left.term_sub(old, new),
                           self.right.term_sub(old, new))


class Disjunction(Formula, namedtuple('Disjunction', 'left right')):
    def __str__(self):
        return '{} ∨ {}'.format(*map(_paren, (self.left, self.right)))

    def free_terms(self):
        return self.left.free_terms() | self.right.free_terms()

    def term_sub(self, old, new):
        return Disjunction(self.left.term_sub(old, new),
                           self.right.term_sub(old, new))


class Universal(Formula, namedtuple('Universal', 'term formula')):
    def __str__(self):
        return '∀{} {}'.format(self.term, _paren(self.formula))

    def free_terms(self):
        return self.formula.free_terms() - {self.term}

    def term_sub(self, old, new):
        if self.term != old:
            return Universal(self.term, self.formula.term_sub(old, new))
        else:
            return self


class Existential(Formula, namedtuple('Existential', 'term formula')):
    def __str__(self):
        return '∃{} {}'.format(self.term, _paren(self.formula))

    def free_terms(self):
        return self.formula.free_terms - {self.term}

    def term_sub(self, old, new):
        if self.term != old:
            return Universal(self.term, self.formula.term_sub(old, new))
        else:
            return self
