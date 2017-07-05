'''Humans can obtain Knowledge from trees in Eden, by way of Python.'''

from collections import namedtuple

compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def roots(*types):
    def dec(f):
        def g(*args):
            for arg, t in zip(args[1:], types):
                assert(isinstance(arg.root, t))
            return f(*args)
        return g
    return dec

def paren(f):
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

    def implintr(self, *args, **kwargs):
        return Assumption(self).implintr(*args, **kwargs)

    def disjintr(self, *args, **kwargs):
        return Assumption(self).disjintr(*args, **kwargs)

class Atom(Formula, namedtuple('Atom', 'formula')):
    def __str__(self):
        return str(self.formula)

class Implication(Formula, namedtuple('Implication', 'prem conc')):
    def __str__(self):
        return '{} → {}'.format(*map(paren, (self.prem, self.conc)))

class Conjunction(Formula, namedtuple('Conjunction', 'left right')):
    def __str__(self):
        return '{} ∧ {}'.format(*map(paren, (self.left, self.right)))

class Disjunction(Formula, namedtuple('Disjunction', 'left right')):
    def __str__(self):
        return '{} ∨ {}'.format(*map(paren, (self.left, self.right)))


def make_str_tree(tree, name):
    lines = []
    sep = ' ' * 8
    width = lambda s: max(len(line) for line in str(s).split('\n'))
    height = lambda s: len(str(s).split('\n'))
    total_height = max((height(t) for t in tree.branches), default=0)
    padded = [('\n' * (total_height - height(b)) + str(b)).split('\n')
              for b in tree.branches]
    branch_widths = [width(b) for b in tree.branches]
    for elems in zip(*padded):
        padded_elems = [e + ' ' * (branch_widths[i] - len(e))
                        for i, e in enumerate(elems)]
        lines.append(sep.join(padded_elems))
    prev_width = (len(lines[-1].strip()) if lines else 0)
    total_width = (sum(branch_widths) + len(sep) * (len(tree.branches) - 1))
    curr_pad_len = (total_width - len(str(tree.root))) // 2
    if prev_width < len(str(tree.root)):
        hline = ' ' * curr_pad_len + '-' * len(str(tree.root))
    else:
        prev_pad = len(lines[-1]) - len(lines[-1].lstrip())
        hline = ' ' * prev_pad + '-' * prev_width
    lines.append(hline + ' ' + name)
    lines.append(' ' * curr_pad_len + str(tree.root))
    return '\n'.join(lines)


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

class Tree:
    def implintr(self, prem_formula=None):
        if not prem_formula:
            prem_formula = next(iter(self.open))
        return ImplicationIntro(self, prem_formula)

    def disjintr(self, weak_formula):
        return DisjunctionIntro(self, weak_formula)

    def discharge(self, formula):
        self.open = self.open - {formula}
        for b in self.branches:
            b.discharge(formula)

    def is_closed(self):
        return not self.open

class Assumption(Tree):
    def __init__(self, formula):
        self.root = formula
        self.branches = ()
        self.open = frozenset({formula})

    def __str__(self):
        if self.open:
            return str(self.root)
        else:
            return '[{}]'.format(self.root)

class ImplicationElim(Tree):
    @roots(Implication, Formula)
    def __init__(self, impl, prem):
        assert(impl.root.prem == prem.root)
        self.root = impl.root.conc
        self.branches = (impl, prem)
        self.open = impl.open | prem.open

    def __str__(self):
        return make_str_tree(self, '→-')

class ImplicationIntro(Tree):
    @roots(Formula)
    def __init__(self, conc, prem_formula):
        self.root = Implication(prem_formula, conc.root)
        self.branches = (conc, )
        self.open = conc.open
        self.discharge(prem_formula)

    def __str__(self):
        return make_str_tree(self, '→+')

class ConjunctionElim(Tree):
    @roots(Conjunction, Formula)
    def __init__(self, conj, result):
        self.root = result.root
        self.branches = (conj, result)
        result.discharge(conj.root.left)
        result.discharge(conj.root.right)
        self.open = conj.open | result.open

    def __str__(self):
        return make_str_tree(self, '∧-')

class ConjunctionIntro(Tree):
    @roots(Formula, Formula)
    def __init__(self, left, right):
        self.root = Conjunction(left.root, right.root)
        self.branches = (left, right)
        self.open = left.open | right.open

    def __str__(self):
        return make_str_tree(self, '∧+')

class DisjunctionElim(Tree):
    @roots(Disjunction, Formula, Formula)
    def __init__(self, disj, left, right):
        assert(left.root == right.root)
        self.root = left.root
        self.branches = (disj, left, right)
        left.discharge(disj.root.left)
        right.discharge(disj.root.right)
        self.open = disj.open | left.open | right.open

    def __str__(self):
        return make_str_tree(self, '∨-')

class DisjunctionIntro(Tree):
    @roots(Formula)
    def __init__(self, parent, weak_formula):
        self.root = Disjunction(parent.root, weak_formula)
        self.branches = (parent,)
        self.open = parent.open

    def __str__(self):
        return make_str_tree(self, '∨+')

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
