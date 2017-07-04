'''Humans can obtain Knowledge from trees in Eden, by way of Python.'''

from collections import namedtuple

compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

# Kind of useless, should check the type of the TREE ROOT INSTEAD
def roots(*types):
    def dec(f):
        def g(*args):
            for arg, t in zip(args[1:], types):
#                if isinstance(arg, Tree):
                    assert(isinstance(arg.root, t))
#                else:
#                    assert(isinstance(arg, t))
            return f(*args)
        return g
    return dec

def paren(f):
    if not isinstance(f, Atom):
        return '({})'.format(f)
    else:
        return str(f)




class Formula:
    pass

class Atom(Formula, namedtuple('Atom', 'formula')):
    def __str__(self):
        return str(self.formula)

class Implication(Formula, namedtuple('Implication', 'prem conc')):
    def __str__(self):
        return '{} → {}'.format(*map(paren, (self.prem, self.conc)))


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


class Eden:
    pass

class Forest(Eden, list):
    pass

class Tree(Eden):
    def discharge(self, formula):
        self.open = self.open - {formula}
        for b in self.branches:
            b.discharge(formula)

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

a, b, c = Atom('A'), Atom('B'), Atom('C')
pf = Assumption(Implication(a, Implication(b, c)))
pf = ImplicationElim(pf, Assumption(a))
pf = ImplicationElim(pf, Assumption(b))
pf = ImplicationIntro(pf, a)
pf = ImplicationIntro(pf, b)
print(pf)



"""
A → (B → C)        [A]                 
---------------------- →-              
        B → C                    [B]   
        ---------------------------- →-
                 C                     
                 ----- →+              
                 A → C                 
              ----------- →+
              B → (A → C)
              """
