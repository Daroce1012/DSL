from .Terminal import*
from .Epsilon import Epsilon
from .NonTerminal import NonTerminal
from .Production import AttributeProduction

class Grammar:
    def __init__(self):
        self.Productions = []
        self.pType = None
        self.Non_terminals = []
        self.Terminals = []
        self.Start_symbol = None
        self.Epsilon = Epsilon(self)
        self.Eof = EOF(self)
        self.SymbolDict = {'eof': self.Eof}

    def non_terminal(self, name, start_symbol=False):
        if not name:
            raise Exception("Empty")
        term = NonTerminal(name, self)
        if start_symbol:
            if self.Start_symbol is None:
                self.Start_symbol = term
            else:
                raise Exception('Cannot define more than one start symbol')
        self.Non_terminals.append(term)
        self.SymbolDict[name] = term
        return term

    def non_terminals(self, names):
        aux = tuple(self.non_terminal(i) for i in names.strip().split())
        return aux

    def add_production(self, production):
        if len(self.Productions) == 0:
            self.pType = type(production)
        production.Left.Productions.append(production)
        self.Productions.append(production)

    def terminal(self, name):
        if not name:
            raise Exception('Empty')
        term = Terminal(name, self)
        self.Terminals.append(term)
        self.SymbolDict[name] = term
        return term

    def terminals(self, names):
        aux = tuple(self.terminal(i) for i in names.strip().split())
        return aux

    def __getitem__(self, item):
        try:
            return self.SymbolDict[item]
        except KeyError:
            return None

    def copy(self):
        g = Grammar()
        g.Productions = self.Productions.copy()
        g.Non_terminals = self.Non_terminals.copy()
        g.Terminals = self.Terminals.copy()
        g.pType = self.pType
        g.Start_symbol = self.Start_symbol
        g.Epsilon = self.Epsilon
        g.Eof = self.Eof
        g.SymbolDict = self.SymbolDict.copy()
        return g

    @property
    def is_augmented_grammar(self):
        augmented = 0
        for left, right in self.Productions:
            if self.Start_symbol == left:
                augmented += 1
        if augmented <= 1:
            return True
        else:
            return False

    def augmented_grammar(self, force=False):
        if not self.is_augmented_grammar or force:
            g = self.copy()
            s = g.Start_symbol
            g.Start_symbol = None
            ss = g.non_terminal('S\'', True)
            if g.pType is AttributeProduction:
                ss %= s + g.Epsilon, lambda x: x
            else:
                ss %= s + g.Epsilon
            return g
        else:
            return self.copy()
